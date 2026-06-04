#!/usr/bin/env python3
"""Pre-flight check for RS-AgentBench: verify everything is ready to launch a sweep.

Run from anywhere — script auto-resolves paths from its own location.

Usage:
    uv run python preflight_check.py

Exit code:
    0 — all checks passed (ready to launch `./sweep_model.sh <model> 5`)
    1 — one or more BLOCKING issues found
    2 — only WARNINGS (sweep can run, but some optional features unavailable)
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BENCHMARK = Path(__file__).resolve().parent
ROOT = BENCHMARK.parent

# ---------------------------------------------------------------------------
# Pretty output
# ---------------------------------------------------------------------------

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

if not sys.stdout.isatty():
    GREEN = YELLOW = RED = BOLD = DIM = RESET = ""

OK_MARK = f"{GREEN}✓{RESET}"
WARN_MARK = f"{YELLOW}⚠{RESET}"
FAIL_MARK = f"{RED}✗{RESET}"


class Status:
    blockers: list[str] = []
    warnings: list[str] = []

    @classmethod
    def ok(cls, msg: str) -> None:
        print(f"  {OK_MARK} {msg}")

    @classmethod
    def warn(cls, msg: str, fix: str | None = None) -> None:
        print(f"  {WARN_MARK} {msg}")
        if fix:
            print(f"     {DIM}→ fix: {fix}{RESET}")
        cls.warnings.append(msg)

    @classmethod
    def fail(cls, msg: str, fix: str | None = None) -> None:
        print(f"  {FAIL_MARK} {msg}")
        if fix:
            print(f"     {DIM}→ fix: {fix}{RESET}")
        cls.blockers.append(msg)


def section(title: str) -> None:
    print(f"\n{BOLD}── {title} ──{RESET}")


# ---------------------------------------------------------------------------
# 1. Code / config files
# ---------------------------------------------------------------------------

REQUIRED_CODE = {
    "runner.py":             "agent runner (entry point)",
    "agent.py":              "pydantic-ai agent + tools",
    "aggregate.py":          "results aggregator",
    "kb_index.py":           "KB index builder (offline)",
    "kb_search.py":          "KB hybrid search (runtime)",
    "kb_common.py":          "shared KB utilities",
    "sweep_model.sh":        "full-sweep launcher",
    "preflight_check.py":    "this script",
    "PROTOCOL.md":           "experimental protocol",
    "PROTOCOL_CHANGELOG.md": "protocol changelog",
    "evaluation/metrics.py": "binary + multiclass metric impls",
    "evaluation/__init__.py":"evaluation package marker",
    "prepare_tif/prepare_all.sh": "one-command dataset prep",
    "prepare_tif/fetch.py":           "Sentinel-2 + WorldCover fetcher",
    "prepare_tif/derive_gt.py":       "T1/T3 GT derivation",
    "prepare_tif/fetch_oscd_to_tif.py": "T2 OSCD → TIF converter",
    "prepare_tif/fetch_burn_to_tif.py":  "T4 CaBuAr → TIF converter",
}

REQUIRED_TASKS = ["water", "change", "landcover", "burn"]
REQUIRED_SKILLS = {
    "water_extraction":     "water-extraction",
    "change_detection":     "change-detection",
    "land_classification":  "land-cover",
    "burn_scar_detection":  "burn-scar-detection",
}


def check_code_files() -> None:
    section("1. Code & protocol files")
    for rel, desc in REQUIRED_CODE.items():
        path = BENCHMARK / rel
        if path.exists():
            Status.ok(f"{rel:42s} ({desc})")
        else:
            Status.fail(f"{rel:42s} MISSING ({desc})",
                        fix="re-clone the repo (this file is tracked)")


# ---------------------------------------------------------------------------
# 2. Task configs + skill files
# ---------------------------------------------------------------------------

def check_tasks_and_skills() -> None:
    section("2. Task configs & SKILL.md files")
    for task in REQUIRED_TASKS:
        tjson = BENCHMARK / "tasks" / f"{task}.json"
        if not tjson.exists():
            Status.fail(f"tasks/{task}.json MISSING",
                        fix="re-clone (tracked file)")
            continue
        cfg = json.loads(tjson.read_text())
        # Verify required keys
        required_keys = {"task_type", "dataset", "input_format", "prompt_template",
                         "samples_file", "evaluation"}
        missing = required_keys - set(cfg.keys())
        if missing:
            Status.fail(f"tasks/{task}.json missing keys: {missing}")
            continue
        # Verify prompt placeholders match what runner provides
        provided = {"image_path", "output_path", "width", "height",
                    "image_a_path", "image_b_path"}
        placeholders = set(re.findall(r"\{(\w+)\}", cfg["prompt_template"]))
        unknown = placeholders - provided
        if unknown:
            Status.fail(f"tasks/{task}.json prompt has unknown placeholders: {unknown}")
            continue
        # Verify skill name matches
        task_type = cfg["task_type"]
        skill_name = REQUIRED_SKILLS.get(task_type)
        if skill_name is None:
            Status.fail(f"tasks/{task}.json: unknown task_type {task_type}")
            continue
        skill_path = BENCHMARK / "skills" / skill_name / "SKILL.md"
        if not skill_path.exists():
            Status.fail(f"skills/{skill_name}/SKILL.md MISSING",
                        fix="re-clone (tracked file)")
            continue
        Status.ok(f"tasks/{task}.json + skills/{skill_name}/SKILL.md  (eval={cfg['evaluation']})")


# ---------------------------------------------------------------------------
# 3. KB index + content
# ---------------------------------------------------------------------------

def check_kb() -> None:
    section("3. KB index (for C1 SearchDocs tool)")
    required_files = {
        "kb/embeddings.npz":   "dense embeddings (Qwen3-Embedding-0.6B)",
        "kb/chunks.json":      "chunk metadata",
        "kb/bm25_index.pkl":   "BM25 sparse index",
        "kb/_meta.json":       "build manifest",
    }
    all_present = True
    for rel, desc in required_files.items():
        path = BENCHMARK / rel
        if path.exists():
            sz = path.stat().st_size
            Status.ok(f"{rel:32s}  {sz/1024:>7.1f} KB  ({desc})")
        else:
            Status.fail(f"{rel:32s} MISSING ({desc})",
                        fix=f"cd benchmark && uv run python kb_index.py")
            all_present = False
    # Verify md source dirs exist
    for sub in ["01_domain", "02_techniques", "03_libraries"]:
        d = BENCHMARK / "kb" / sub
        if d.exists() and any(d.iterdir()):
            n = sum(1 for _ in d.rglob("*.md"))
            Status.ok(f"kb/{sub}/  ({n} markdown files)")
        else:
            Status.warn(f"kb/{sub}/ missing or empty",
                        fix="re-clone (tracked dir; required to rebuild kb_index.py)")
    if all_present:
        # Sanity: chunks count matches embeddings rows
        try:
            import numpy as np
            embs = np.load(BENCHMARK / "kb/embeddings.npz")["embeddings"]
            chunks = json.loads((BENCHMARK / "kb/chunks.json").read_text())
            if embs.shape[0] != len(chunks):
                Status.fail(f"KB index corruption: {len(chunks)} chunks vs {embs.shape[0]} embeddings",
                            fix="cd benchmark && uv run python kb_index.py")
            else:
                Status.ok(f"KB index integrity: {len(chunks)} chunks × {embs.shape[1]}-dim embeddings")
        except Exception as e:
            Status.warn(f"KB integrity check skipped: {e}")


# ---------------------------------------------------------------------------
# 4. Dataset / sample manifests + actual files
# ---------------------------------------------------------------------------

EXPECTED_DATA = {
    "water":     {"binary": True,  "fixed": (1024, 1024), "bands": 10, "dual": False},
    "landcover": {"binary": False, "fixed": (1024, 1024), "bands": 10, "dual": False},
    "change":    {"binary": True,  "fixed": None,         "bands": 10, "dual": True},
    "burn":      {"binary": True,  "fixed": (512, 512),   "bands": 10, "dual": True},
}


def check_datasets() -> None:
    section("4. datasets_tif/ — sample manifests & actual files")
    try:
        import rasterio
        import numpy as np
        from PIL import Image
    except ImportError as e:
        Status.fail(f"required python lib missing: {e}",
                    fix="cd benchmark && uv sync")
        return

    for task, spec in EXPECTED_DATA.items():
        manifest = BENCHMARK / "datasets_tif" / task / "samples_v1.json"
        if not manifest.exists():
            Status.fail(f"datasets_tif/{task}/samples_v1.json MISSING",
                        fix="cd benchmark && ./prepare_tif/prepare_all.sh")
            continue
        samples = json.loads(manifest.read_text())
        if len(samples) != 10:
            Status.fail(f"{task}: manifest has {len(samples)} samples (expected 10)")
            continue

        # Spot-check first sample's files exist + have right shape
        s = samples[0]
        base = BENCHMARK / "datasets_tif" / task
        broken = []
        files_to_check = []
        if spec["dual"]:
            files_to_check += [(base / s["image_a"], "tif"),
                               (base / s["image_b"], "tif")]
        else:
            files_to_check += [(base / s["image"], "tif")]
        files_to_check += [(base / s["label"], "label")]

        for path, kind in files_to_check:
            if not path.exists():
                broken.append(f"{path.relative_to(BENCHMARK)} missing")
                continue
            try:
                if kind == "tif":
                    with rasterio.open(path) as src:
                        if src.count != spec["bands"]:
                            broken.append(f"{path.name}: bands={src.count} (want {spec['bands']})")
                        if src.dtypes[0] != "uint16":
                            broken.append(f"{path.name}: dtype={src.dtypes[0]} (want uint16)")
                else:  # label
                    img = Image.open(path)
                    arr = np.asarray(img)
                    uniq = sorted(np.unique(arr).tolist())
                    if spec["binary"]:
                        if not (set(uniq) <= {0, 255}):
                            broken.append(f"{path.name}: non-binary uniques={uniq}")
                    else:
                        if not (set(uniq) <= {0, 1, 2, 3, 255}):
                            broken.append(f"{path.name}: non-class uniques={uniq}")
            except Exception as e:
                broken.append(f"{path.name}: {type(e).__name__}: {e}")

        # Full file existence check (not just first sample)
        n_missing = 0
        for s in samples:
            if spec["dual"]:
                paths = [base / s["image_a"], base / s["image_b"], base / s["label"]]
            else:
                paths = [base / s["image"], base / s["label"]]
            n_missing += sum(1 for p in paths if not p.exists())

        if broken or n_missing:
            issues = []
            if broken:
                issues.append(f"first-sample broken: {broken[:2]}")
            if n_missing:
                issues.append(f"{n_missing} files missing across all samples")
            Status.fail(f"{task}: " + "; ".join(issues),
                        fix="cd benchmark && rm -rf datasets_tif/{task}/data datasets_tif/{task}/samples_v1.json && ./prepare_tif/prepare_all.sh")
        else:
            Status.ok(f"datasets_tif/{task}/  10 samples  ({spec['bands']}-band, binary={spec['binary']}, dual={spec['dual']})")


# ---------------------------------------------------------------------------
# 5. Python environments
# ---------------------------------------------------------------------------

def check_envs() -> None:
    section("5. Python environments")
    bench_venv = BENCHMARK / ".venv"
    ws_venv = ROOT / "workspace" / ".venv"
    if bench_venv.exists():
        Status.ok(f"benchmark/.venv  (for runner / aggregate / kb_index)")
    else:
        Status.fail("benchmark/.venv MISSING",
                    fix="cd benchmark && uv sync")
    if ws_venv.exists():
        Status.ok(f"workspace/.venv  (for agent's RunPython subprocess)")
    else:
        Status.fail("workspace/.venv MISSING",
                    fix="cd workspace && uv sync   (or set up via workspace/setup.sh)")


# ---------------------------------------------------------------------------
# 6. .env keys
# ---------------------------------------------------------------------------

def check_env_keys() -> None:
    section("6. .env API keys")
    env_path = ROOT / ".env"
    if not env_path.exists():
        Status.fail(".env file MISSING at repo root",
                    fix=f"cp .env.example .env  (then fill in keys)")
        return
    # Read .env into a dict
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"\'')

    REQUIRED_KEYS = [
        ("OPENAI_API_KEY",       "API key for the OpenAI-compatible endpoint"),
        ("OPENAI_BASE_URL",      "base URL of the OpenAI-compatible endpoint"),
        ("TAVILY_API_KEY",       "Tavily web search (C2/C4/C6/C7 conditions)"),
    ]
    OPTIONAL_KEYS = [
        ("KB_SEARCH_BASE_URL",   "remote RAG service URL (optional; falls back to local hybrid search)"),
    ]
    for key, desc in REQUIRED_KEYS:
        val = env.get(key, "")
        if val:
            preview = val[:18] + "..." if len(val) > 22 else val
            Status.ok(f"{key:25s} = {preview}  ({desc})")
        else:
            Status.fail(f"{key} not set in .env",
                        fix=f"add `{key}=...` to .env  ({desc})")
    for key, desc in OPTIONAL_KEYS:
        val = env.get(key, "")
        if val:
            Status.ok(f"{key:25s}  set ({desc})")
        else:
            Status.warn(f"{key} not set ({desc})")


# ---------------------------------------------------------------------------
# 7. External services reachability (best-effort)
# ---------------------------------------------------------------------------

def check_external_services() -> None:
    section("7. External services (probe only; warnings non-fatal)")
    env_path = ROOT / ".env"
    if not env_path.exists():
        Status.warn("skipping service probe (no .env)")
        return
    # Re-read .env to get fresh values for probing
    env = {}
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"\'')

    # Probe RAG (HTTP GET /health, 5s timeout)
    rag_url = env.get("KB_SEARCH_BASE_URL", "")
    if rag_url:
        try:
            import urllib.request
            with urllib.request.urlopen(f"{rag_url.rstrip('/')}/health", timeout=5) as r:
                data = json.loads(r.read())
                if data.get("status") == "ok":
                    Status.ok(f"KB RAG service alive: {rag_url}  device={data.get('device')}, n_chunks={data.get('n_chunks')}")
                else:
                    Status.warn(f"KB RAG status={data.get('status')!r}",
                                fix="check rag service logs; agent will fall back to local search")
        except Exception as e:
            Status.warn(f"KB RAG unreachable ({rag_url}): {type(e).__name__}",
                        fix="agent will fall back to local hybrid search (slower, needs ~3 GB RAM)")

    # Probe the model endpoint (a tiny chat completion against the
    # configured OpenAI-compatible URL).
    for env_key, base_url_key, label in [
        ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OpenAI-compatible endpoint"),
    ]:
        key = env.get(env_key, "")
        base = env.get(base_url_key, "")
        if not key or not base:
            continue
        try:
            import urllib.request
            req = urllib.request.Request(
                base.rstrip("/") + "/chat/completions",
                data=b'{"model":"none","messages":[{"role":"user","content":"x"}],"max_tokens":1}',
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as r:
                    Status.ok(f"{label}: HTTPS reachable ({r.status})")
            except urllib.error.HTTPError as e:
                # 4xx = endpoint reachable but request rejected (model='none' is bogus on purpose)
                if 400 <= e.code < 500:
                    Status.ok(f"{label}: reachable (HTTP {e.code} — auth/payload accepted, only model rejected)")
                else:
                    Status.warn(f"{label}: HTTP {e.code}")
        except Exception as e:
            Status.warn(f"{label} unreachable: {type(e).__name__}",
                        fix="check network / proxy")

    # Tavily (POST /search with the configured key, expect 200)
    tav_key = env.get("TAVILY_API_KEY", "")
    if tav_key:
        try:
            import urllib.request
            req = urllib.request.Request(
                "https://api.tavily.com/search",
                data=json.dumps({"api_key": tav_key, "query": "ping",
                                 "search_depth": "basic", "max_results": 1}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                Status.ok(f"Tavily reachable + key valid (HTTP {r.status})")
        except urllib.error.HTTPError as e:
            if e.code == 432:
                Status.warn("Tavily quota exceeded (HTTP 432)",
                            fix="top up at tavily.com or rotate the key")
            else:
                Status.warn(f"Tavily HTTP {e.code}")
        except Exception as e:
            Status.warn(f"Tavily unreachable: {type(e).__name__}")


# ---------------------------------------------------------------------------
# 8. Imports + agent_log retry-instrumentation sanity
# ---------------------------------------------------------------------------

def check_imports() -> None:
    section("8. Module import sanity")
    # Run the imports inside a subprocess of the benchmark venv if available
    venv_python = BENCHMARK / ".venv" / "bin" / "python"
    if not venv_python.exists():
        Status.warn("skipping import sanity (benchmark/.venv missing)")
        return
    code = (
        "import sys; sys.path.insert(0, '.');"
        "from agent import BenchDeps, agent;"
        "from runner import CONFIG_MATRIX, _route_for_model, create_model_instance;"
        "assert len(CONFIG_MATRIX) == 8, f'wrong cfg count: {len(CONFIG_MATRIX)}';"
        "import kb_search; import kb_common;"
        "print('OK', list(CONFIG_MATRIX.keys()))"
    )
    try:
        r = subprocess.run([str(venv_python), "-c", code],
                           cwd=BENCHMARK, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            Status.ok(f"imports + CONFIG_MATRIX  →  {r.stdout.strip()}")
        else:
            Status.fail(f"import failed: {r.stderr.strip()[:200]}",
                        fix="cd benchmark && uv sync")
    except Exception as e:
        Status.fail(f"import sanity failed: {e}")


# ---------------------------------------------------------------------------
# 9. Final verdict
# ---------------------------------------------------------------------------

def main() -> int:
    print(f"{BOLD}RS-AgentBench preflight check{RESET}")
    print(f"{DIM}benchmark dir: {BENCHMARK}{RESET}")

    check_code_files()
    check_tasks_and_skills()
    check_kb()
    check_datasets()
    check_envs()
    check_env_keys()
    check_external_services()
    check_imports()

    print()
    if Status.blockers:
        print(f"{RED}{BOLD}✗ {len(Status.blockers)} BLOCKING issue(s) found{RESET} "
              f"({len(Status.warnings)} warnings).  "
              f"Fix the items marked above, then re-run.")
        return 1
    if Status.warnings:
        print(f"{YELLOW}{BOLD}⚠ ready to launch with {len(Status.warnings)} warning(s){RESET}.")
        print(f"{DIM}You can still run experiments; some optional features may be unavailable.{RESET}")
        return 2
    print(f"{GREEN}{BOLD}✓ all checks passed — ready to launch{RESET}")
    print(f"{DIM}Suggested next step:  ./sweep_model.sh <model_id> 5{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
