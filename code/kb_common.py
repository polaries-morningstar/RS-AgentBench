"""Shared utilities for kb_index.py and kb_search.py.

Centralized so the indexer and searcher can never drift on tokenization,
device selection, or version tagging.
"""
from __future__ import annotations

import re

# Bumped whenever bm25_tokenize semantics change. Stored in the BM25 pickle
# at index time and verified at runtime — a mismatch means the index was built
# with an incompatible tokenizer and retrieval would silently degrade.
BM25_TOKENIZE_VERSION = "v1"

_BM25_TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def bm25_tokenize(text: str) -> list[str]:
    """Lowercase + alphanumeric/underscore split, drop length-1 tokens.

    Examples:
        ``cv.HoughLinesP`` -> ``["cv", "houghlinesp"]``
        ``THRESH_OTSU``    -> ``["thresh_otsu"]``
        ``K-means``        -> ``["means"]`` ("k" is length-1, dropped)
    """
    return [t for t in _BM25_TOKEN_RE.findall(text.lower()) if len(t) > 1]


def select_device(requested: str = "auto") -> str:
    """Resolve "auto" -> cuda > mps > cpu. Pass-through for explicit values."""
    if requested != "auto":
        return requested
    import torch

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"
