"""
KB Indexer v2 — Engineering-grade RAG index builder.

Pipeline:
  1. Code-fence aware markdown chunker (header hierarchy + 50-token overlap)
  2. Dense embeddings via Qwen/Qwen3-Embedding-0.6B (1024d, multilingual)
  3. Sparse index via Okapi BM25 (rank_bm25)
  4. Persist: embeddings.npz, chunks.json, bm25_index.pkl, _meta.json

Usage:
    uv run python kb_index.py
    uv run python kb_index.py --kb-dir ./kb --device mps
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from kb_common import BM25_TOKENIZE_VERSION, bm25_tokenize, select_device

# ---------------------------------------------------------------------------
# Configuration (also written to _meta.json for reproducibility)
# ---------------------------------------------------------------------------

EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
EMBEDDING_DIM = 1024

CHUNKER_VERSION = "v2-code-aware"
CHUNK_MAX_TOKENS = 400
CHUNK_MIN_TOKENS = 50
CHUNK_OVERLAP_TOKENS = 50

ENCODE_BATCH_SIZE = 16

# ---------------------------------------------------------------------------
# Code-fence aware markdown chunker
# ---------------------------------------------------------------------------

_CODE_FENCE_RE = re.compile(r"^\s*```")
_HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def _count_tokens(text: str, tokenizer) -> int:
    """Accurate token count using the embedding model's tokenizer."""
    return len(tokenizer.encode(text, add_special_tokens=False))


def _split_long_text(
    text: str,
    max_tokens: int,
    overlap_tokens: int,
    tokenizer,
) -> list[str]:
    """Split overlong block into ≤max_tokens windows. Paragraph → sentence → char."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0

    def flush_with_overlap():
        nonlocal current, current_tokens
        if not current:
            return
        chunks.append("\n\n".join(current))
        # Keep tail paragraphs whose total tokens < overlap_tokens
        if overlap_tokens > 0:
            tail: list[str] = []
            tail_tok = 0
            for p in reversed(current):
                pt = _count_tokens(p, tokenizer)
                if tail_tok + pt > overlap_tokens:
                    break
                tail.insert(0, p)
                tail_tok += pt
            current = tail
            current_tokens = tail_tok
        else:
            current = []
            current_tokens = 0

    for para in paragraphs:
        ptok = _count_tokens(para, tokenizer)

        # Paragraph itself too long → split by sentence then by chars
        if ptok > max_tokens:
            flush_with_overlap()
            current = []
            current_tokens = 0
            chunks.extend(_split_paragraph(para, max_tokens, overlap_tokens, tokenizer))
            continue

        if current_tokens + ptok > max_tokens and current:
            flush_with_overlap()

        current.append(para)
        current_tokens += ptok

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _split_paragraph(
    para: str,
    max_tokens: int,
    overlap_tokens: int,
    tokenizer,
) -> list[str]:
    """Split a single overlong paragraph: sentence -> char fallback.

    Carries trailing sentences whose cumulative token count is <= overlap_tokens
    forward to the next chunk so adjacent chunks share semantic context.
    """
    sentences = re.split(r"(?<=[.!?。！？])\s+", para)
    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0

    def flush_with_overlap():
        nonlocal current, current_tokens
        if not current:
            return
        chunks.append(" ".join(current))
        if overlap_tokens <= 0:
            current = []
            current_tokens = 0
            return
        tail: list[str] = []
        tail_tok = 0
        for s in reversed(current):
            st = _count_tokens(s, tokenizer)
            if tail_tok + st > overlap_tokens:
                break
            tail.insert(0, s)
            tail_tok += st
        current = tail
        current_tokens = tail_tok

    for sent in sentences:
        if not sent.strip():
            continue
        stok = _count_tokens(sent, tokenizer)

        # Sentence too long -> char split (no overlap; this path is rare)
        if stok > max_tokens:
            flush_with_overlap()
            current = []
            current_tokens = 0
            cpt = max(1, len(sent) // stok)
            target_chars = max(200, max_tokens * cpt)
            step = max(100, target_chars - overlap_tokens * cpt)
            for i in range(0, len(sent), step):
                chunks.append(sent[i : i + target_chars])
            continue

        if current_tokens + stok > max_tokens and current:
            flush_with_overlap()

        current.append(sent)
        current_tokens += stok

    if current:
        chunks.append(" ".join(current))

    return chunks


def chunk_markdown(text: str, source: str, tokenizer) -> list[dict]:
    """Split markdown into chunks, respecting code fences and header hierarchy.

    Each chunk dict: {text, source, section, header_path}
    `text` is prefixed with a [source > section] breadcrumb so the embedding
    captures structural context.
    """
    lines = text.split("\n")
    in_code = False

    # Stage 1: split into blocks at headers (outside code)
    # block = (header_path: list[(level, title)], content_lines: list[str])
    blocks: list[tuple[list[tuple[int, str]], list[str]]] = []
    header_stack: list[tuple[int, str]] = []
    buffer: list[str] = []

    for line in lines:
        if _CODE_FENCE_RE.match(line):
            in_code = not in_code
            buffer.append(line)
            continue

        if not in_code:
            m = _HEADER_RE.match(line)
            if m:
                # Flush previous block
                if any(ln.strip() for ln in buffer):
                    blocks.append((list(header_stack), buffer))
                buffer = []
                # Update header stack: pop deeper-or-equal level
                level = len(m.group(1))
                title = m.group(2).strip()
                header_stack = [h for h in header_stack if h[0] < level]
                header_stack.append((level, title))
                # Also include the header line itself in the next block's content
                # so the chunk text retains the section title
                buffer.append(line)
                continue

        buffer.append(line)

    if any(ln.strip() for ln in buffer):
        blocks.append((list(header_stack), buffer))

    # Stage 2: blocks → chunks (split long, merge tiny)
    chunks: list[dict] = []
    for path, block_lines in blocks:
        block_text = "\n".join(block_lines).strip()
        if not block_text:
            continue

        section = " > ".join(t for _, t in path) if path else "(root)"
        n_tokens = _count_tokens(block_text, tokenizer)

        if n_tokens <= CHUNK_MAX_TOKENS:
            # Tiny -> merge into previous chunk only if same source AND section
            # (cross-section merges would dilute section-level retrieval precision)
            if (
                n_tokens < CHUNK_MIN_TOKENS
                and chunks
                and chunks[-1]["source"] == source
                and chunks[-1]["section"] == section
            ):
                chunks[-1]["text"] += "\n\n" + block_text
                continue
            chunks.append({"text": block_text, "source": source, "section": section})
        else:
            for sub in _split_long_text(
                block_text, CHUNK_MAX_TOKENS, CHUNK_OVERLAP_TOKENS, tokenizer
            ):
                chunks.append({"text": sub, "source": source, "section": section})

    # Stage 3: prepend breadcrumb (helps embedding & BM25 capture context)
    for c in chunks:
        breadcrumb = f"[{c['source']} > {c['section']}]"
        if not c["text"].startswith(breadcrumb):
            c["text"] = f"{breadcrumb}\n\n{c['text']}"

    return chunks


# ---------------------------------------------------------------------------
# Embedding (Qwen3-Embedding-0.6B)
# ---------------------------------------------------------------------------


def embed_chunks(chunks: list[dict], device: str) -> tuple[np.ndarray, str]:
    """Embed chunk texts. Documents do NOT need a query prompt.

    Returns (embeddings (N, D) float32, model commit hash if available else "").
    """
    from sentence_transformers import SentenceTransformer

    print(f"Loading embedding model: {EMBEDDING_MODEL} on device={device}")
    model = SentenceTransformer(EMBEDDING_MODEL, device=device)

    # Capture the resolved HF commit hash for reproducibility manifest.
    commit = ""
    try:
        # SentenceTransformer wraps the underlying transformer; it exposes
        # config via the first auto_model module on most versions.
        commit = getattr(model[0].auto_model.config, "_commit_hash", "") or ""
    except Exception:
        pass

    texts = [c["text"] for c in chunks]
    print(f"Encoding {len(texts)} chunks (batch_size={ENCODE_BATCH_SIZE})...")

    embeddings = model.encode(
        texts,
        batch_size=ENCODE_BATCH_SIZE,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return np.asarray(embeddings, dtype=np.float32), commit


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


def _file_sha256(path: Path) -> str:
    """Full 64-char SHA256 of file contents (used as a content fingerprint)."""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def build_index(kb_dir: Path, device: str = "auto"):
    kb_dir = kb_dir.resolve()
    md_files = sorted(kb_dir.rglob("*.md"))

    if not md_files:
        print(f"No .md files found in {kb_dir}")
        return

    print(f"Found {len(md_files)} markdown files in {kb_dir}")

    # Load tokenizer (used for accurate token counts during chunking)
    from transformers import AutoTokenizer

    print(f"Loading tokenizer: {EMBEDDING_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)

    # Stage A: chunk all files (strict UTF-8: silent corruption would poison
    # the index, so we abort instead of substituting U+FFFD)
    print("\n[1/4] Chunking...")
    all_chunks: list[dict] = []
    file_hashes: dict[str, str] = {}
    for f in md_files:
        rel = str(f.relative_to(kb_dir))
        try:
            text = f.read_text(encoding="utf-8", errors="strict")
        except UnicodeDecodeError as e:
            raise RuntimeError(
                f"KB file {rel} is not valid UTF-8 ({e}). "
                f"Fix the file before re-running kb_index.py."
            ) from e
        file_hashes[rel] = _file_sha256(f)
        file_chunks = chunk_markdown(text, rel, tokenizer)
        all_chunks.extend(file_chunks)
        print(f"  {rel}: {len(file_chunks)} chunks")

    n_chunks = len(all_chunks)
    print(f"\nTotal chunks: {n_chunks}")

    # Quick stats
    sizes = [len(c["text"]) for c in all_chunks]
    sizes.sort()
    print(
        f"  char size: min={sizes[0]}, p50={sizes[n_chunks // 2]}, "
        f"p90={sizes[int(n_chunks * 0.9)]}, max={sizes[-1]}"
    )
    tok_sizes = [_count_tokens(c["text"], tokenizer) for c in all_chunks]
    tok_sizes.sort()
    print(
        f"  token size: min={tok_sizes[0]}, p50={tok_sizes[n_chunks // 2]}, "
        f"p90={tok_sizes[int(n_chunks * 0.9)]}, max={tok_sizes[-1]}"
    )

    # Stage B: dense embeddings
    print("\n[2/4] Embedding (dense)...")
    t0 = time.time()
    selected_device = select_device(device)
    embeddings, embedding_commit = embed_chunks(all_chunks, selected_device)
    print(f"  shape: {embeddings.shape}, took {time.time() - t0:.1f}s")

    # Stage C: BM25 index
    print("\n[3/4] Building BM25 sparse index...")
    from rank_bm25 import BM25Okapi

    t0 = time.time()
    tokenized_corpus = [bm25_tokenize(c["text"]) for c in all_chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    print(f"  done in {time.time() - t0:.1f}s")

    # Stage D: persist
    print("\n[4/4] Saving...")
    emb_path = kb_dir / "embeddings.npz"
    chunks_path = kb_dir / "chunks.json"
    bm25_path = kb_dir / "bm25_index.pkl"
    meta_path = kb_dir / "_meta.json"

    np.savez_compressed(emb_path, embeddings=embeddings)
    chunks_path.write_text(
        json.dumps(all_chunks, ensure_ascii=False, indent=None),
        encoding="utf-8",
    )
    with open(bm25_path, "wb") as f:
        pickle.dump(
            {"bm25": bm25, "tokenize_fn": f"bm25_tokenize_{BM25_TOKENIZE_VERSION}"},
            f,
        )

    # Capture library versions for reproducibility
    import platform
    import sys
    import sentence_transformers as st_mod
    import transformers as tf_mod
    import torch as torch_mod
    import rank_bm25 as bm25_mod

    versions = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "torch": torch_mod.__version__,
        "transformers": tf_mod.__version__,
        "sentence_transformers": st_mod.__version__,
        "rank_bm25": getattr(bm25_mod, "__version__", "unknown"),
    }

    meta = {
        "embedding_model": EMBEDDING_MODEL,
        "embedding_model_revision": embedding_commit,
        "embedding_dim": EMBEDDING_DIM,
        "reranker_model": "Qwen/Qwen3-Reranker-0.6B",
        "retrieval_pipeline": "dense + bm25 -> RRF -> cross-encoder rerank",
        "rrf_k": 60,
        "dense_top_k": 30,
        "sparse_top_k": 30,
        "rerank_input_top_k": 20,
        "rerank_output_top_k": 5,
        "rerank_batch_size": 1,
        "score_threshold": 0.3,
        "chunker_version": CHUNKER_VERSION,
        "chunk_max_tokens": CHUNK_MAX_TOKENS,
        "chunk_min_tokens": CHUNK_MIN_TOKENS,
        "chunk_overlap_tokens": CHUNK_OVERLAP_TOKENS,
        "encode_batch_size": ENCODE_BATCH_SIZE,
        "bm25_tokenize_version": BM25_TOKENIZE_VERSION,
        "n_chunks": n_chunks,
        "n_files": len(md_files),
        "indexed_at": datetime.now(timezone.utc).isoformat(),
        "device": selected_device,
        "versions": versions,
        "kb_files_sha256": file_hashes,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"\n  {emb_path.name}      {emb_path.stat().st_size / 1024:.0f} KB\n"
        f"  {chunks_path.name}     {chunks_path.stat().st_size / 1024:.0f} KB\n"
        f"  {bm25_path.name}  {bm25_path.stat().st_size / 1024:.0f} KB\n"
        f"  {meta_path.name}      {meta_path.stat().st_size / 1024:.0f} KB"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build hybrid RAG index for RS-AgentBench")
    parser.add_argument(
        "--kb-dir",
        type=Path,
        default=Path(__file__).parent / "kb",
        help="Knowledge base directory (default: ./kb/)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "mps", "cuda"],
        help="Device for embedding model",
    )
    args = parser.parse_args()

    build_index(args.kb_dir, args.device)
