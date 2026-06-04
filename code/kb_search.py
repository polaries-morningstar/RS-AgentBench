"""KB Search v2: hybrid retrieval + cross-encoder rerank.

Pipeline:
  query
    -> dense top-30  (Qwen3-Embedding-0.6B, cosine over normalized embeddings)
    -> sparse top-30 (BM25 Okapi over alphanumeric tokens)
    -> RRF fusion (Cormack 2009, k=60, 1-indexed rank) -> top-N
    -> cross-encoder rerank (Qwen3-Reranker-0.6B; calibrated p(yes) via
       softmax over yes/no logits at the final position) -> top-5
    -> score threshold filter (drop p(yes) < 0.30)

Module-level singleton for runtime use:
    from kb_search import search
    text = search("Otsu thresholding", top_k=5)
"""
from __future__ import annotations

import json
import os
import pickle
import threading
from collections import OrderedDict, defaultdict
from pathlib import Path

import numpy as np

from kb_common import BM25_TOKENIZE_VERSION, bm25_tokenize, select_device

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
EMBEDDING_DIM = 1024  # Must match kb_index.EMBEDDING_DIM
RERANKER_MODEL = "Qwen/Qwen3-Reranker-0.6B"

DENSE_TOP_K = 30
SPARSE_TOP_K = 30
RRF_K = 60
RERANK_INPUT_TOP_K = int(os.getenv("KB_RERANK_INPUT_TOP_K", "10"))
RERANK_OUTPUT_TOP_K = 5
SCORE_THRESHOLD = 0.3
RESULT_CACHE_MAX_SIZE = 256

# Reranker mini-batch size — DEVICE-AWARE.
#
# MPS / CPU: batch=1 is FASTEST (verified May 2026, M4 Pro 48GB, Qwen3-Reranker-0.6B
# fp32, 20 candidate docs of 200-600 tokens each):
#   bs=1  → 5.11s/query (mean over 12)   RSS 4095M
#   bs=4  → 6.46s/query                   RSS 4096M  (-21%)
#   bs=8  → 7.18s/query                   RSS 4095M  (-29%)
#   bs=20 → 7.86s/query                   RSS 4095M  (-35%)
# Why batch=1 wins on MPS:
#   1. Padding waste: docs vary 200-600 tokens; batched padding wastes ~30-50%
#      attention compute.
#   2. MPS shader cache: each (batch, seq_len) shape compiles its own kernel —
#      bs=1 always re-uses one cached kernel; larger batches recompile per
#      length distribution.
#
# CUDA: batch=8 wins (verified May 2026, RTX 3090, fp16, 10 candidates):
#   - 3090 has 10 496 cores; bs=1 leaves them mostly idle (~44% util peak)
#   - Tensor Cores need larger matmuls to engage
#   - Kernel launch overhead amortizes over the batch
# Padding waste is real but small relative to the parallelism gain.
#
# Override via env var KB_RERANK_BATCH_SIZE (set to 0/empty for auto).
_RERANK_BATCH_SIZE_OVERRIDE = int(os.getenv("KB_RERANK_BATCH_SIZE", "0") or "0")

# Reranker prompt (per official model card)
_RERANK_TASK = (
    "Given a remote-sensing or image-processing question, "
    "retrieve passages that answer the question."
)
_EMBED_QUERY_TASK = (
    "Given a remote-sensing or image-processing question, "
    "retrieve relevant passages that answer the question."
)

# ---------------------------------------------------------------------------
# Hybrid searcher
# ---------------------------------------------------------------------------


class HybridKBSearcher:
    """Hybrid retriever: dense + sparse → RRF → cross-encoder rerank."""

    def __init__(self, kb_dir: str | Path, device: str = "auto"):
        kb_dir = Path(kb_dir).resolve()

        emb_path = kb_dir / "embeddings.npz"
        chunks_path = kb_dir / "chunks.json"
        bm25_path = kb_dir / "bm25_index.pkl"
        meta_path = kb_dir / "_meta.json"

        for p in (emb_path, chunks_path, bm25_path):
            if not p.exists():
                raise FileNotFoundError(
                    f"KB index file missing: {p}. "
                    f"Run `uv run python kb_index.py` first."
                )

        self.embeddings: np.ndarray = np.load(emb_path)["embeddings"]
        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks: list[dict] = json.load(f)
        # NOTE: pickle is trusted only because kb_dir is a local artifact built
        # by us. Never point this at user-supplied input.
        with open(bm25_path, "rb") as f:
            payload = pickle.load(f)
        self.bm25 = payload["bm25"]
        bm25_tag = payload.get("tokenize_fn", "")

        # Sanity checks: stale/corrupt indices silently produce garbage
        # retrieval, which would invalidate experimental results. Fail loudly.
        if len(self.chunks) != self.embeddings.shape[0]:
            raise RuntimeError(
                f"Index corrupted: {len(self.chunks)} chunks vs "
                f"{self.embeddings.shape[0]} embeddings. Rebuild with kb_index.py."
            )
        if self.embeddings.shape[1] != EMBEDDING_DIM:
            raise RuntimeError(
                f"Embedding dim mismatch: index has {self.embeddings.shape[1]}, "
                f"runtime expects {EMBEDDING_DIM}. Index was likely built with "
                f"a different embedding model — rebuild with kb_index.py."
            )
        expected_bm25_tag = f"bm25_tokenize_{BM25_TOKENIZE_VERSION}"
        if bm25_tag != expected_bm25_tag:
            raise RuntimeError(
                f"BM25 tokenizer version mismatch: index has {bm25_tag!r}, "
                f"runtime expects {expected_bm25_tag!r}. Rebuild with kb_index.py."
            )
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                if meta.get("embedding_model") and meta["embedding_model"] != EMBEDDING_MODEL:
                    raise RuntimeError(
                        f"Embedding model mismatch: index built with "
                        f"{meta['embedding_model']!r}, runtime expects "
                        f"{EMBEDDING_MODEL!r}. Rebuild with kb_index.py."
                    )
            except json.JSONDecodeError:
                pass  # _meta.json corruption is non-fatal at search time

        self._device = select_device(device)
        # Device-aware rerank batch size: CUDA prefers batch=8 (parallelism wins),
        # MPS/CPU prefer batch=1 (variable-length padding + shader-cache overhead).
        # Env var KB_RERANK_BATCH_SIZE overrides if non-zero.
        if _RERANK_BATCH_SIZE_OVERRIDE > 0:
            self._rerank_batch_size = _RERANK_BATCH_SIZE_OVERRIDE
        else:
            self._rerank_batch_size = 8 if self._device == "cuda" else 1
        self._embed_model = None
        self._rerank_tokenizer = None
        self._rerank_model = None
        self._rerank_prefix_ids: list[int] = []
        self._rerank_suffix_ids: list[int] = []
        self._rerank_yes_id: int = -1
        self._rerank_no_id: int = -1
        self._degraded_to_cpu = False  # set if rerank OOMed and stayed on CPU
        self._model_lock = threading.Lock()  # guards lazy model loading
        self._result_cache_lock = threading.Lock()
        # Benchmark runs repeat many exact KB queries across samples/repetitions.
        # Cache final search outputs so we can skip redundant dense+rereank work.
        self._result_cache: OrderedDict[
            tuple[str, int, float],
            tuple[tuple[tuple[str, float, str, str], ...], float],
        ] = OrderedDict()

    def _get_embed_model(self):
        with self._model_lock:
            if self._embed_model is None:
                from sentence_transformers import SentenceTransformer

                self._embed_model = SentenceTransformer(
                    EMBEDDING_MODEL, device=self._device
                )
        return self._embed_model

    def _get_rerank_model(self):
        with self._model_lock:
            if self._rerank_model is None:
                import torch
                from transformers import AutoModelForCausalLM, AutoTokenizer

                tokenizer = AutoTokenizer.from_pretrained(
                    RERANKER_MODEL, padding_side="left"
                )
                # fp16 on MPS triggers segfaults during batched inference for
                # the Qwen3 architecture. fp32 on MPS/CPU; fp16 only on CUDA.
                dtype = torch.float16 if self._device == "cuda" else torch.float32
                model = (
                    AutoModelForCausalLM.from_pretrained(
                        RERANKER_MODEL, torch_dtype=dtype
                    )
                    .to(self._device)
                    .eval()
                )

                prefix = (
                    "<|im_start|>system\nJudge whether the Document meets the "
                    "requirements based on the Query and the Instruct provided. "
                    'Note that the answer can only be "yes" or "no".'
                    "<|im_end|>\n<|im_start|>user\n"
                )
                suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

                yes_id = tokenizer.convert_tokens_to_ids("yes")
                no_id = tokenizer.convert_tokens_to_ids("no")
                if yes_id == tokenizer.unk_token_id or no_id == tokenizer.unk_token_id:
                    raise RuntimeError(
                        "Reranker tokenizer maps 'yes'/'no' to UNK — model is "
                        "incompatible with the prompt format used here."
                    )

                self._rerank_tokenizer = tokenizer
                self._rerank_model = model
                self._rerank_prefix_ids = tokenizer.encode(
                    prefix, add_special_tokens=False
                )
                self._rerank_suffix_ids = tokenizer.encode(
                    suffix, add_special_tokens=False
                )
                self._rerank_yes_id = yes_id
                self._rerank_no_id = no_id

        return self._rerank_model, self._rerank_tokenizer

    # ------------------------------ stages ---------------------------------

    def _dense_search(self, query: str, top_k: int) -> list[tuple[int, float]]:
        model = self._get_embed_model()
        # Qwen3-Embedding queries benefit from the 'query' prompt
        q_emb = model.encode(
            [query],
            prompt_name="query",
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        q_emb = np.asarray(q_emb, dtype=np.float32)
        scores = (self.embeddings @ q_emb.T).squeeze(-1)
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [(int(i), float(scores[i])) for i in top_idx]

    def _sparse_search(self, query: str, top_k: int) -> list[tuple[int, float]]:
        tokens = bm25_tokenize(query)
        if not tokens:
            return []
        scores = self.bm25.get_scores(tokens)
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [(int(i), float(scores[i])) for i in top_idx if scores[i] > 0]

    @staticmethod
    def _rrf_fuse(
        dense: list[tuple[int, float]],
        sparse: list[tuple[int, float]],
        k: int = RRF_K,
        top_n: int = RERANK_INPUT_TOP_K,
    ) -> list[int]:
        # Reciprocal Rank Fusion (Cormack, Clarke, Buettcher 2009).
        # Canonical formulation uses 1-indexed rank: score = 1 / (k + rank),
        # rank starting at 1. enumerate(..., start=1) matches the paper.
        rrf: dict[int, float] = defaultdict(float)
        for rank, (idx, _) in enumerate(dense, start=1):
            rrf[idx] += 1.0 / (k + rank)
        for rank, (idx, _) in enumerate(sparse, start=1):
            rrf[idx] += 1.0 / (k + rank)
        ordered = sorted(rrf.items(), key=lambda x: -x[1])
        return [idx for idx, _ in ordered[:top_n]]

    def _rerank(self, query: str, doc_indices: list[int]) -> list[float]:
        """Score (query, doc) pairs in mini-batches to bound peak memory.

        Falls back from MPS to CPU on OOM (transparent retry per mini-batch).
        """
        if not doc_indices:
            return []
        import torch

        model, tokenizer = self._get_rerank_model()

        max_len = 8192
        body_max = max_len - len(self._rerank_prefix_ids) - len(self._rerank_suffix_ids)

        all_scores: list[float] = []
        bs = self._rerank_batch_size
        for start in range(0, len(doc_indices), bs):
            mb_indices = doc_indices[start : start + bs]
            pairs_text = [
                f"<Instruct>: {_RERANK_TASK}\n<Query>: {query}\n"
                f"<Document>: {self.chunks[i]['text']}"
                for i in mb_indices
            ]

            # add_special_tokens=False: we manage prefix/suffix manually, so
            # any auto-prepended BOS/EOS would push the concatenated sequence
            # past max_len and silently corrupt the cross-encoder input.
            encoded = tokenizer(
                pairs_text,
                padding=False,
                truncation="longest_first",
                max_length=body_max,
                return_attention_mask=False,
                add_special_tokens=False,
            )
            for i, ids in enumerate(encoded["input_ids"]):
                full = self._rerank_prefix_ids + ids + self._rerank_suffix_ids
                if len(full) > max_len:
                    full = full[: max_len - len(self._rerank_suffix_ids)] + self._rerank_suffix_ids
                encoded["input_ids"][i] = full
            batch = tokenizer.pad(encoded, padding=True, return_tensors="pt")

            scores = self._rerank_forward(model, batch)
            all_scores.extend(scores)

            # Free per-batch activation memory (MPS/CUDA can accumulate)
            if self._device == "mps":
                torch.mps.empty_cache()
            elif self._device == "cuda":
                torch.cuda.empty_cache()

        return all_scores

    @staticmethod
    def _is_oom(err: Exception) -> bool:
        """Detect OOM across torch backends (CUDA, MPS) without relying on
        a single string format."""
        import torch

        if isinstance(err, getattr(torch.cuda, "OutOfMemoryError", ())):
            return True
        msg = str(err).lower()
        return "out of memory" in msg or "mps backend out of memory" in msg

    def _rerank_score_batch(self, model, batch) -> list[float]:
        """Forward pass + score extraction. Assumes batch is already on
        model.device. log_softmax operates per-row so scores from different
        mini-batches are comparable (calibrated probability of 'yes')."""
        import torch

        with torch.no_grad():
            logits = model(**batch).logits[:, -1, :]
            yes = logits[:, self._rerank_yes_id]
            no = logits[:, self._rerank_no_id]
            stacked = torch.stack([no, yes], dim=1)
            log_probs = torch.nn.functional.log_softmax(stacked, dim=1)
            return log_probs[:, 1].exp().tolist()

    def _rerank_forward(self, model, batch) -> list[float]:
        """Forward pass with OOM fallback to CPU. If we ever fall back, stay
        on CPU permanently for this searcher instance — bouncing the model
        between devices is brittle and can leave it half-migrated."""
        import torch

        if self._degraded_to_cpu:
            cpu_batch = {k: v.to("cpu") for k, v in batch.items()}
            return self._rerank_score_batch(model, cpu_batch)

        try:
            batch_on_dev = {k: v.to(model.device) for k, v in batch.items()}
            return self._rerank_score_batch(model, batch_on_dev)
        except RuntimeError as e:
            if not self._is_oom(e):
                raise
            # OOM: free the device cache, permanently move model to CPU,
            # rerun this batch on CPU. Subsequent batches will bypass MPS.
            if self._device == "mps":
                torch.mps.empty_cache()
            elif self._device == "cuda":
                torch.cuda.empty_cache()
            print(
                f"[kb_search] Reranker OOM on {self._device}, falling back "
                f"to CPU permanently for this session.",
                flush=True,
            )
            model.to("cpu")
            self._degraded_to_cpu = True
            cpu_batch = {k: v.to("cpu") for k, v in batch.items()}
            return self._rerank_score_batch(model, cpu_batch)

    # ------------------------------ public API -----------------------------

    def _get_cached_result(
        self, key: tuple[str, int, float]
    ) -> tuple[list[tuple[str, float, str, str]], float] | None:
        with self._result_cache_lock:
            cached = self._result_cache.get(key)
            if cached is None:
                return None
            self._result_cache.move_to_end(key)
            cached_results, top_raw = cached
        return list(cached_results), top_raw

    def _put_cached_result(
        self,
        key: tuple[str, int, float],
        results: list[tuple[str, float, str, str]],
        top_raw: float,
    ) -> None:
        with self._result_cache_lock:
            self._result_cache[key] = (tuple(results), top_raw)
            self._result_cache.move_to_end(key)
            while len(self._result_cache) > RESULT_CACHE_MAX_SIZE:
                self._result_cache.popitem(last=False)

    def search(
        self,
        query: str,
        top_k: int = RERANK_OUTPUT_TOP_K,
        score_threshold: float = SCORE_THRESHOLD,
    ) -> tuple[list[tuple[str, float, str, str]], float]:
        """Hybrid retrieve + rerank.

        Returns (results, top_raw_score) where:
          - results: list of (text, rerank_score, source, section) sorted desc;
            empty if all candidates score below `score_threshold`.
          - top_raw_score: the highest rerank score seen, useful for diagnosing
            empty-result cases (0.0 if no candidates were found at all).
        """
        query = query.strip()
        if not query:
            return [], 0.0
        cache_key = (query, top_k, score_threshold)
        cached = self._get_cached_result(cache_key)
        if cached is not None:
            return cached

        dense = self._dense_search(query, DENSE_TOP_K)
        sparse = self._sparse_search(query, SPARSE_TOP_K)
        candidates = self._rrf_fuse(dense, sparse)
        if not candidates:
            return [], 0.0

        scores = self._rerank(query, candidates)
        ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])
        top_raw = ranked[0][1] if ranked else 0.0

        results: list[tuple[str, float, str, str]] = []
        for idx, score in ranked:
            if score < score_threshold:
                continue
            chunk = self.chunks[idx]
            results.append((chunk["text"], score, chunk["source"], chunk["section"]))
            if len(results) >= top_k:
                break

        self._put_cached_result(cache_key, results, top_raw)
        return results, top_raw

    def search_formatted(self, query: str, top_k: int = RERANK_OUTPUT_TOP_K) -> str:
        """Search and return a formatted string for the agent."""
        if not query.strip():
            return "Empty query — please provide a non-empty search string."

        results, top_raw = self.search(query, top_k)
        if not results:
            return (
                f"No documents passed the relevance threshold "
                f"({SCORE_THRESHOLD:.2f}); top candidate scored {top_raw:.2f}. "
                f"Try rephrasing with more specific technical terms (e.g. "
                f"function names, library APIs, or precise concepts)."
            )
        parts = []
        for i, (text, score, source, section) in enumerate(results, 1):
            confidence = "low" if score < 0.5 else "medium" if score < 0.8 else "high"
            parts.append(
                f"--- Result {i} (from {source} :: {section}, "
                f"relevance: {score:.2f} [{confidence}]) ---\n{text}"
            )
        return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Module-level singleton (thread-safe; first-call args win)
# ---------------------------------------------------------------------------

_searcher: HybridKBSearcher | None = None
_searcher_lock = threading.Lock()
_searcher_init_args: tuple[str, str] | None = None


def get_searcher(
    kb_dir: str | Path = "", device: str = "auto"
) -> HybridKBSearcher:
    """Return the module-level singleton. Args are honoured on the FIRST call;
    subsequent calls that resolve to different (kb_dir, device) raise — silent
    rejection would make device/kb_dir mismatches invisible bugs.

    "auto" device is resolved before comparison so callers passing "auto" and
    callers passing the resolved name (e.g. "mps") are equivalent.
    """
    global _searcher, _searcher_init_args
    with _searcher_lock:
        resolved_kb = str(Path(kb_dir).resolve()) if kb_dir else str(
            (Path(__file__).parent / "kb").resolve()
        )
        resolved_device = select_device(device)
        if _searcher is None:
            _searcher = HybridKBSearcher(resolved_kb, device=resolved_device)
            _searcher_init_args = (resolved_kb, resolved_device)
        else:
            assert _searcher_init_args is not None
            if (resolved_kb, resolved_device) != _searcher_init_args:
                raise RuntimeError(
                    f"get_searcher() reinitialisation conflict: "
                    f"first call used {_searcher_init_args!r}, "
                    f"this call requested {(resolved_kb, resolved_device)!r}. "
                    f"Use the same args or restart the process."
                )
    return _searcher


def search(query: str, top_k: int = RERANK_OUTPUT_TOP_K, kb_dir: str | Path = "") -> str:
    """Convenience function for agent.SearchDocs tool."""
    return get_searcher(kb_dir).search_formatted(query, top_k)


# ---------------------------------------------------------------------------
# CLI for sanity-checking retrieval quality
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Query the KB index")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--kb-dir", type=Path, default=Path(__file__).parent / "kb")
    args = parser.parse_args()

    s = HybridKBSearcher(args.kb_dir)
    print(s.search_formatted(args.query, args.top_k))
