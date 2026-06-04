"""FastAPI service for KB retrieval on a remote host.

Designed for deployment on a Linux + CUDA machine so the benchmark can offload
hybrid retrieval + reranking over HTTP.

Example:
    cd benchmark
    ./.venv/bin/python kb/serve.py --host 0.0.0.0 --port 8009 --device cuda --prewarm

Endpoints:
    GET  /health
    GET  /config
    POST /search/raw
    POST /search/formatted
"""
from __future__ import annotations

import argparse
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BENCHMARK_DIR = Path(__file__).resolve().parent.parent
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from kb_search import (  # noqa: E402
    RERANK_INPUT_TOP_K,
    RERANK_OUTPUT_TOP_K,
    SCORE_THRESHOLD,
    HybridKBSearcher,
)


class SearchRawRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    top_k: int = Field(
        default=RERANK_OUTPUT_TOP_K, ge=1, le=20, description="Final result count"
    )
    score_threshold: float = Field(
        default=SCORE_THRESHOLD, ge=0.0, le=1.0, description="Rerank score cutoff"
    )


class SearchFormattedRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    top_k: int = Field(
        default=RERANK_OUTPUT_TOP_K, ge=1, le=20, description="Final result count"
    )


def create_app(
    kb_dir: Path,
    device: str = "auto",
    prewarm: bool = False,
) -> FastAPI:
    searcher = HybridKBSearcher(kb_dir=kb_dir, device=device)
    startup_error: str | None = None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nonlocal startup_error
        if prewarm:
            try:
                # Preload both models so the first real request does not pay the
                # full cold-start cost. On CUDA, this also materializes the
                # model weights onto GPU up front.
                searcher._get_embed_model()
                searcher._get_rerank_model()
            except Exception as exc:  # noqa: BLE001
                startup_error = f"{type(exc).__name__}: {exc}"
        app.state.searcher = searcher
        app.state.startup_error = startup_error
        yield

    app = FastAPI(
        title="AutoGIS KB Search API",
        description="Hybrid dense + BM25 + rerank KB retrieval service.",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health")
    def health() -> dict:
        return {
            "status": "ok" if startup_error is None else "degraded",
            "device": searcher._device,
            "kb_dir": str(kb_dir),
            "n_chunks": len(searcher.chunks),
            "rerank_input_top_k": RERANK_INPUT_TOP_K,
            "rerank_output_top_k": RERANK_OUTPUT_TOP_K,
            "score_threshold": SCORE_THRESHOLD,
            "prewarm": prewarm,
            "startup_error": startup_error,
        }

    @app.get("/config")
    def config() -> dict:
        return {
            "device": searcher._device,
            "kb_dir": str(kb_dir),
            "n_chunks": len(searcher.chunks),
            "rerank_input_top_k": RERANK_INPUT_TOP_K,
            "rerank_output_top_k": RERANK_OUTPUT_TOP_K,
            "score_threshold": SCORE_THRESHOLD,
        }

    @app.post("/search/raw")
    def search_raw(req: SearchRawRequest) -> dict:
        if startup_error is not None:
            raise HTTPException(status_code=503, detail=startup_error)
        t0 = time.perf_counter()
        results, top_raw = searcher.search(
            req.query,
            top_k=req.top_k,
            score_threshold=req.score_threshold,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "query": req.query,
            "elapsed_ms": round(elapsed_ms, 2),
            "top_raw_score": top_raw,
            "result_count": len(results),
            "results": [
                {
                    "text": text,
                    "score": score,
                    "source": source,
                    "section": section,
                }
                for text, score, source, section in results
            ],
        }

    @app.post("/search/formatted")
    def search_formatted(req: SearchFormattedRequest) -> dict:
        if startup_error is not None:
            raise HTTPException(status_code=503, detail=startup_error)
        t0 = time.perf_counter()
        text = searcher.search_formatted(req.query, top_k=req.top_k)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "query": req.query,
            "elapsed_ms": round(elapsed_ms, 2),
            "text": text,
        }

    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve benchmark KB over HTTP")
    parser.add_argument(
        "--kb-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="KB directory containing embeddings.npz / chunks.json / bm25_index.pkl",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "mps", "cuda"],
        help="Model device; auto resolves cuda > mps > cpu",
    )
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8009)
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Uvicorn worker count. Use 1 for a single shared GPU model instance.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
    )
    parser.add_argument(
        "--prewarm",
        action="store_true",
        help="Load embedding + rerank models during startup to avoid first-request cold start.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = create_app(
        kb_dir=args.kb_dir.resolve(),
        device=args.device,
        prewarm=args.prewarm,
    )
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_level=args.log_level,
    )


if __name__ == "__main__":
    main()
