"""
RS-AgentBench agent — narrowed tool surface for clean knowledge-effect comparison.

Tools (always):
    RunPython     — execute a Python snippet in an isolated subprocess
    SubmitAnswer  — explicit termination signal (raises UsageLimitExceeded)

Conditional:
    SearchDocs    — RAG over reference KB (C1, C5)
    Skill         — load a SKILL.md (C3, C5)

Removed (vs prior version): Bash, Read, Write, Edit. The benchmark deliverable
is one PNG; multi-file workflow is unnecessary and induces a "coding session"
behavior that pollutes the experiment.
"""
from __future__ import annotations

import asyncio
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

from pydantic_ai import Agent, RunContext
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.models.test import TestModel
from pydantic_ai.tools import ToolDefinition

KB_SEARCH_BASE_URL = os.getenv("KB_SEARCH_BASE_URL", "").rstrip("/")
KB_SEARCH_TIMEOUT_S = float(os.getenv("KB_SEARCH_TIMEOUT_S", "30"))


# ---------------------------------------------------------------------------
# Agent dependencies
# ---------------------------------------------------------------------------

@dataclass
class BenchDeps:
    """Shared state injected into every tool via RunContext[BenchDeps]."""
    session_id: str
    project_dir: Path          # Agent's working directory (temp, per-run)
    workspace_path: Path       # Holds .venv for python execution + skills/
    venv_path: Path | None = None
    tool_log: list = field(default_factory=list)
    # Budget tracking — set by runner before agent.run()
    start_time: float = 0.0
    tool_call_limit: int = 20
    show_skill: bool = False   # C3/C5/C6 expose Skill tool
    show_kb: bool = False      # C1/C5/C6 expose SearchDocs tool
    show_ws: bool = False      # C2/C6 expose WebSearch (Tavily) tool
    # Output validation: runner sets these so SubmitAnswer can verify
    # the agent actually produced a usable output before terminating.
    expected_output_path: str = "artifacts/output.png"
    expected_output_size: tuple[int, int] | None = None
    # SubmitAnswer state
    submitted: bool = False
    submission_notes: str = ""
    submit_attempts: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Budget helper — appended to every tool result
# ---------------------------------------------------------------------------

def _budget_exhausted(deps: BenchDeps) -> bool:
    """True when the agent has used its productive-tool budget. SubmitAnswer
    is unaffected (it doesn't consume budget)."""
    return len(deps.tool_log) >= deps.tool_call_limit


_BUDGET_EXHAUSTED_MSG = (
    "Tool budget exhausted. SubmitAnswer is the only remaining tool — "
    "call it now to end the run. (RunPython / SearchDocs / WebSearch / Skill "
    "are no longer available.)"
)


def _budget_info(deps: BenchDeps) -> str:
    # We deliberately don't expose a running counter — showing exact "X/20"
    # biases behaviour (over-iterate to fill quota, or submit early to save
    # quota). But we DO want a qualitative warning when the agent is about
    # to be force-terminated, so it has a chance to call SubmitAnswer first.
    if deps.submitted:
        return ""
    remaining = max(0, deps.tool_call_limit - len(deps.tool_log))
    base = "\n[When `artifacts/output.png` is ready, call SubmitAnswer to finish.]"
    # Thresholds scale with the budget: warn at the last ~17% of calls,
    # then again at the very last call. With limit=30 this fires at
    # ≤5 remaining ("low") and ≤1 remaining ("last call").
    low_threshold = max(3, deps.tool_call_limit // 6)   # 5 for limit=30, 3 for limit=20
    if remaining <= 1:
        base += "\n[Last call before forced termination — call SubmitAnswer now or your output will be evaluated as-is.]"
    elif remaining <= low_threshold:
        base += "\n[Running low on tool calls — submit soon.]"
    return base


# ---------------------------------------------------------------------------
# Agent singleton (model injected at runtime)
# ---------------------------------------------------------------------------

agent = Agent(TestModel(), deps_type=BenchDeps, output_type=str)


# ---------------------------------------------------------------------------
# System prompt — dynamic per condition
# ---------------------------------------------------------------------------

@agent.system_prompt
async def system_prompt(ctx: RunContext[BenchDeps]) -> str:
    return (
        "You are a remote-sensing image-analysis agent. Write Python "
        "(numpy, rasterio, cv2, sklearn, scipy, skimage, PIL) to analyze the imagery. "
        "You cannot see the image; inspect it via code and iterate as needed.\n\n"
        "Image-level metadata (CRS, bounds, transform, dtype) lives inside the GeoTIFF — "
        "query it with rasterio (`src.crs`, `src.bounds`, `src.transform`, `src.descriptions`).\n\n"
        "Save the final mask to `artifacts/output.png`, then call SubmitAnswer to end the run. "
        "SubmitAnswer validates the file (existence, readable, correct size) and rejects invalid "
        "submissions for free — fix and resubmit.\n\n"
        "No deep learning. No `pip install`."
    )


# ---------------------------------------------------------------------------
# Tool: RunPython — sandboxed Python execution
# ---------------------------------------------------------------------------

_OUTPUT_LIMIT = 10_000

# Auto-seeding prelude — injected before every RunPython invocation so
# stochastic CV ops (K-means init, RANSAC, MSER, etc.) are deterministic
# without forcing the agent to remember to seed everything.
_SEED_PRELUDE = (
    "import os as _os, random as _random\n"
    "_os.environ.setdefault('PYTHONHASHSEED', '0')\n"
    "_random.seed(0)\n"
    "try:\n"
    "    import numpy as _np; _np.random.seed(0)\n"
    "except Exception: pass\n"
    "try:\n"
    "    import cv2 as _cv2; _cv2.setRNGSeed(0)\n"
    "except Exception: pass\n"
)

# Path-level guards: block any code referencing GT or benchmark internals.
_BENCHMARK_DIR = str(Path(__file__).resolve().parent)
_BLOCKED_SUBSTRINGS = (
    f"{_BENCHMARK_DIR}/datasets",
    f"{_BENCHMARK_DIR}/results",
    f"{_BENCHMARK_DIR}/evaluation",
    "_gt_eval",
    "_perturbation",
    # Process escape hatches — block at source level (they wouldn't help anyway)
    "subprocess",
    "os.system",
    "os.popen",
    "os.execv",
    "os.execve",
    "os.execl",
    "os.execlp",
    "pty.spawn",
)


@agent.tool
async def RunPython(
    ctx: RunContext[BenchDeps],
    code: str,
    timeout: int = 60,
) -> str:
    """Run Python code; returns stdout+stderr. Each call is a fresh subprocess (state does not persist)."""
    if ctx.deps.submitted:
        return "RunPython rejected: SubmitAnswer was already called. The run is over."

    if _budget_exhausted(ctx.deps):
        return _BUDGET_EXHAUSTED_MSG

    timeout = max(5, min(timeout, 180))
    start = time.monotonic()

    # Source-level guard: refuse code that names GT/results paths or shell escape APIs.
    for needle in _BLOCKED_SUBSTRINGS:
        if needle in code:
            ctx.deps.tool_log.append({
                "tool": "RunPython", "status": "blocked", "needle": needle,
                "code_preview": code[:200],
            })
            return (
                f"Code rejected: references blocked identifier '{needle}'. "
                "Stay within the project_dir and avoid shell-escape APIs."
                + _budget_info(ctx.deps)
            )

    # Minimal environment — venv on PATH, project_dir as HOME/TMPDIR.
    venv = ctx.deps.venv_path or (ctx.deps.workspace_path / ".venv")
    venv_bin = str(venv / "bin") if venv.exists() else ""
    env = {
        "PATH": f"{venv_bin}:/usr/local/bin:/usr/bin:/bin" if venv_bin else os.environ.get("PATH", ""),
        "HOME": str(ctx.deps.project_dir),
        "TMPDIR": str(ctx.deps.project_dir),
        "VIRTUAL_ENV": str(venv) if venv.exists() else "",
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
        "TERM": os.environ.get("TERM", "xterm"),
        "DYLD_LIBRARY_PATH": os.environ.get("DYLD_LIBRARY_PATH", ""),
    }

    python_bin = str(venv / "bin" / "python") if venv.exists() else "python3"

    final_code = _SEED_PRELUDE + code
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            python_bin, "-c", final_code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(ctx.deps.project_dir),
            env=env,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = stdout.decode(errors="replace") + stderr.decode(errors="replace")
    except asyncio.TimeoutError:
        if proc and proc.returncode is None:
            try:
                proc.kill()
                await proc.wait()
            except Exception:
                pass
        output = f"RunPython timed out after {timeout}s. Tighten your code or split work across calls."
    except Exception as e:
        output = f"RunPython error: {e}"

    elapsed_ms = int((time.monotonic() - start) * 1000)
    ctx.deps.tool_log.append({
        "tool": "RunPython", "code_preview": code[:200],
        "elapsed_ms": elapsed_ms, "status": "ok",
    })

    if len(output) > _OUTPUT_LIMIT:
        output = output[:_OUTPUT_LIMIT] + f"\n... (truncated {len(output) - _OUTPUT_LIMIT} chars; print summaries, not raw arrays)"
    return output + _budget_info(ctx.deps)


# ---------------------------------------------------------------------------
# Tool: SubmitAnswer — explicit termination
# ---------------------------------------------------------------------------

# Cap on failed submissions to prevent the agent from looping on Submit
# instead of producing the file. Each rejected attempt is free, but after
# this many rejections the run is force-terminated regardless.
_MAX_SUBMIT_ATTEMPTS = 5


@agent.tool
async def SubmitAnswer(ctx: RunContext[BenchDeps], notes: str) -> str:
    """End the run. Validates artifacts/output.png (exists, readable, correct size). Rejected submissions are free; fix and retry."""
    if ctx.deps.submitted:
        return "Already submitted — the run is over."

    rel_path = ctx.deps.expected_output_path
    output_path = ctx.deps.project_dir / rel_path

    def _record(status: str, **extra) -> None:
        ctx.deps.submit_attempts.append({"status": status, "notes_preview": notes[:200], **extra})

    def _force_terminate(reason: str):
        ctx.deps.submitted = True
        ctx.deps.submission_notes = notes[:2000]
        raise UsageLimitExceeded(f"SubmitAnswer cap reached: {reason}")

    # Check 1: file must exist
    if not output_path.exists():
        _record("no_file")
        if len(ctx.deps.submit_attempts) >= _MAX_SUBMIT_ATTEMPTS:
            _force_terminate("no output file produced after repeated attempts")
        return (
            f"SubmitAnswer rejected: `{rel_path}` does not exist. "
            f"Save your output mask with RunPython first, then call SubmitAnswer again. "
            f"This call did NOT consume tool budget."
            + _budget_info(ctx.deps)
        )

    # Check 2: file must open as an image
    try:
        from PIL import Image
        img = Image.open(output_path)
        size = img.size  # (W, H)
        img.verify()  # detect truncated / corrupted PNG
    except Exception as e:
        _record("unreadable", error=f"{type(e).__name__}: {e}")
        if len(ctx.deps.submit_attempts) >= _MAX_SUBMIT_ATTEMPTS:
            _force_terminate("output file unreadable after repeated attempts")
        return (
            f"SubmitAnswer rejected: `{rel_path}` cannot be opened as an image "
            f"({type(e).__name__}: {e}). Re-save it as a valid PNG and submit again. "
            f"This call did NOT consume tool budget."
            + _budget_info(ctx.deps)
        )

    # Check 3: size must match (when the runner has set an expected size)
    if ctx.deps.expected_output_size is not None:
        ew, eh = ctx.deps.expected_output_size
        aw, ah = size
        if (aw, ah) != (ew, eh):
            _record("wrong_size", got=[aw, ah], expected=[ew, eh])
            if len(ctx.deps.submit_attempts) >= _MAX_SUBMIT_ATTEMPTS:
                _force_terminate("wrong-size output after repeated attempts")
            return (
                f"SubmitAnswer rejected: output is {aw}x{ah} but the task requires {ew}x{eh}. "
                f"Re-save with the correct size and submit again. "
                f"This call did NOT consume tool budget."
                + _budget_info(ctx.deps)
            )

    # All checks passed — voluntary termination
    _record("ok")
    ctx.deps.submitted = True
    ctx.deps.submission_notes = notes[:2000]
    raise UsageLimitExceeded("SubmitAnswer called — voluntary termination")


# ---------------------------------------------------------------------------
# Tool: Skill (C3, C5) — prepare= callback hides schema in C0/C1
# ---------------------------------------------------------------------------

async def _prepare_skill(ctx: RunContext[BenchDeps], tool_def: ToolDefinition) -> ToolDefinition | None:
    return tool_def if ctx.deps.show_skill else None


@agent.tool(prepare=_prepare_skill)
async def Skill(ctx: RunContext[BenchDeps], skill_name: str) -> str:
    """Load a curated SKILL.md procedure for this task."""
    if ctx.deps.submitted:
        return "Skill rejected: SubmitAnswer was already called."

    if _budget_exhausted(ctx.deps):
        return _BUDGET_EXHAUSTED_MSG

    if "/" in skill_name or "\\" in skill_name or ".." in skill_name:
        return f"Invalid skill name: '{skill_name}'"

    skills_dir = ctx.deps.workspace_path / ".agent" / "skills"
    skill_path = skills_dir / skill_name / "SKILL.md"

    if not skill_path.exists():
        ctx.deps.tool_log.append({"tool": "Skill", "skill_name": skill_name, "status": "not_found"})
        return f"Skill '{skill_name}' not found." + _budget_info(ctx.deps)

    content = skill_path.read_text(encoding="utf-8")
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    ctx.deps.tool_log.append({"tool": "Skill", "skill_name": skill_name, "status": "ok"})
    return content + _budget_info(ctx.deps)


# ---------------------------------------------------------------------------
# Tool: WebSearch (C2, C6) — Tavily-backed open-web search
# ---------------------------------------------------------------------------

async def _prepare_web_search(ctx: RunContext[BenchDeps], tool_def: ToolDefinition) -> ToolDefinition | None:
    return tool_def if ctx.deps.show_ws else None


@agent.tool(prepare=_prepare_web_search)
async def WebSearch(ctx: RunContext[BenchDeps], query: str) -> str:
    """Search the open web via Tavily; returns top-5 results (title, URL, snippet).

    Call multiple times with different targeted queries to gather different
    aspects of a problem (formula, empirical threshold, pitfall, library API,
    etc.). Short specific queries (3–8 words) outperform long ones. Follow up
    when initial results are partial.
    """
    if ctx.deps.submitted:
        return "WebSearch rejected: already submitted."

    if _budget_exhausted(ctx.deps):
        return _BUDGET_EXHAUSTED_MSG

    log_entry: dict = {"tool": "WebSearch", "query": query[:200]}
    ctx.deps.tool_log.append(log_entry)

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        log_entry["status"] = "setup_error"
        log_entry["error"] = "TAVILY_API_KEY missing"
        return "WebSearch unavailable: TAVILY_API_KEY not configured." + _budget_info(ctx.deps)

    try:
        import httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 5,
                    "include_answer": False,
                    "include_raw_content": False,
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:  # noqa: BLE001 — runtime failures isolated per-call
        log_entry["status"] = "error"
        log_entry["error"] = f"{type(e).__name__}: {e}"
        return f"WebSearch error ({type(e).__name__}): {e}" + _budget_info(ctx.deps)

    results = (data.get("results") or [])[:5]
    if not results:
        log_entry["status"] = "empty"
        return f"No web results for '{query}'." + _budget_info(ctx.deps)

    log_entry["status"] = "ok"
    log_entry["n_results"] = len(results)

    chunks = []
    for i, r in enumerate(results, 1):
        title = (r.get("title") or "(no title)").strip()
        url = (r.get("url") or "").strip()
        content = (r.get("content") or "").strip()[:500]
        chunks.append(f"[{i}] {title}\n{url}\n{content}")

    return "\n\n---\n\n".join(chunks) + _budget_info(ctx.deps)


# ---------------------------------------------------------------------------
# Tool: SearchDocs (C1, C5) — prepare= callback hides schema in C0/C3
# ---------------------------------------------------------------------------

async def _prepare_search_docs(ctx: RunContext[BenchDeps], tool_def: ToolDefinition) -> ToolDefinition | None:
    return tool_def if ctx.deps.show_kb else None


async def _search_docs_remote(query: str, top_k: int = 5) -> tuple[str, dict]:
    import httpx

    if not KB_SEARCH_BASE_URL:
        raise RuntimeError("KB_SEARCH_BASE_URL is not configured")

    url = f"{KB_SEARCH_BASE_URL}/search/formatted"
    async with httpx.AsyncClient(timeout=KB_SEARCH_TIMEOUT_S) as client:
        resp = await client.post(url, json={"query": query, "top_k": top_k})
        resp.raise_for_status()
        data = resp.json()

    text = data.get("text")
    if not isinstance(text, str):
        raise RuntimeError("Remote KB response missing 'text' field")
    return text, {
        "backend": "http",
        "url": url,
        "upstream_elapsed_ms": data.get("elapsed_ms"),
    }


def _search_docs_local(query: str, top_k: int = 5) -> tuple[str, dict]:
    from kb_search import search as kb_search_fn

    return kb_search_fn(query, top_k=top_k), {"backend": "local"}


@agent.tool(prepare=_prepare_search_docs)
async def SearchDocs(ctx: RunContext[BenchDeps], query: str) -> str:
    """Search the curated reference library (RS knowledge, spectral-index
    formulas, Sentinel-2 band specs, CV techniques, Python API docs).

    Call multiple times with different targeted queries — one query per
    concept (e.g., 'MNDWI water threshold', then 'Otsu scikit-image', then
    'rasterio multiband read'). Short specific queries (3–8 words) work
    better than long ones. Follow up when initial results don't cover what
    you need.
    """
    if ctx.deps.submitted:
        return "SearchDocs rejected: SubmitAnswer was already called."

    if _budget_exhausted(ctx.deps):
        return _BUDGET_EXHAUSTED_MSG

    if not ctx.deps.show_kb:
        return "Documentation search is not available in this configuration."

    start = time.monotonic()
    log_entry: dict = {"tool": "SearchDocs", "query": query[:200]}
    ctx.deps.tool_log.append(log_entry)

    try:
        if KB_SEARCH_BASE_URL:
            try:
                results, meta = await _search_docs_remote(query, top_k=5)
                log_entry.update(meta)
            except Exception as remote_err:  # noqa: BLE001
                log_entry["http_error"] = f"{type(remote_err).__name__}: {remote_err}"
                log_entry["fallback"] = "local"
                results, meta = _search_docs_local(query, top_k=5)
                log_entry.update(meta)
        else:
            results, meta = _search_docs_local(query, top_k=5)
            log_entry.update(meta)
    except (FileNotFoundError, ImportError):
        log_entry["status"] = "setup_error"
        log_entry["elapsed_ms"] = int((time.monotonic() - start) * 1000)
        raise
    except Exception as e:  # noqa: BLE001
        import traceback
        log_entry["status"] = "error"
        log_entry["error"] = f"{type(e).__name__}: {e}"
        log_entry["elapsed_ms"] = int((time.monotonic() - start) * 1000)
        traceback.print_exc()
        return f"Documentation search error ({type(e).__name__}): {e}"

    log_entry["status"] = "ok"
    log_entry["elapsed_ms"] = int((time.monotonic() - start) * 1000)
    return results + _budget_info(ctx.deps)
