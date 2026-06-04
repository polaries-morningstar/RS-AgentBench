"""
RS-AgentBench runner — standalone benchmark using a pydantic-ai agent over
any OpenAI-compatible Chat-Completions endpoint.

The runner reads two environment variables for the LLM endpoint:

    OPENAI_BASE_URL   e.g. https://api.openai.com/v1
    OPENAI_API_KEY    your API key

and uses them for every backbone. To target a different provider (DashScope,
DeepSeek's first-party endpoint, Moonshot, OpenRouter, a self-hosted vLLM,
etc.) point ``OPENAI_BASE_URL`` at that provider's OpenAI-compat endpoint and
swap ``OPENAI_API_KEY`` accordingly; no code change is needed.

Usage:
    uv run python runner.py --task water --config C0 --model qwen3-8b --sample 2571
    uv run python runner.py --task burn  --config C3 --model deepseek-v4-pro --all
    uv run python runner.py --task water --config C0 --model kimi-k2.6 --all --repeat 3
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import shutil
import sys
import tempfile
import time
import traceback
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from pydantic_ai import UsageLimits
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.settings import ModelSettings

# ---------------------------------------------------------------------------
# Paths & env
# ---------------------------------------------------------------------------

BENCHMARK_DIR = Path(__file__).resolve().parent
ROOT_DIR = BENCHMARK_DIR.parent
load_dotenv(ROOT_DIR / ".env")

# Real venv for Bash tool (has numpy, cv2, sklearn, etc.)
REAL_VENV = ROOT_DIR / "workspace" / ".venv"


def create_model_instance(model_str: str):
    """Create a pydantic-ai model against any OpenAI-compatible endpoint.

    Reads ``OPENAI_BASE_URL`` and ``OPENAI_API_KEY`` from the environment and
    talks to that endpoint via the standard ``openai.AsyncOpenAI`` client. The
    same endpoint shape (Chat Completions over HTTPS, JSON-schema tool calls)
    is exposed by every backbone used in this study; only the ``base_url`` and
    ``api_key`` differ between providers.

    Reasoning models (those that emit ``reasoning_content`` alongside the
    visible reply) must echo that field back to the API on subsequent
    assistant messages, or the conversation breaks mid-trial. We enable the
    pass-back when the model name indicates a reasoning SKU.
    """
    base_url = os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    if not (base_url and api_key):
        raise RuntimeError(
            "Set OPENAI_BASE_URL and OPENAI_API_KEY in the environment "
            "(e.g. in a project-root .env file). This runner uses a single "
            "OpenAI-compatible endpoint for every backbone."
        )

    from openai import AsyncOpenAI
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    from pydantic_ai.profiles.openai import OpenAIModelProfile
    import httpx

    timeout = httpx.Timeout(180, connect=30)  # extended-thinking responses are slower
    client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
    provider = OpenAIProvider(openai_client=client)

    ml = model_str.lower()
    is_nothinking_variant = "nothinking" in ml
    needs_thinking_passback = (not is_nothinking_variant) and (
        ml.startswith("qwen")
        or "v4-flash" in ml or "v4-pro" in ml
        or "thinking" in ml
        or "-r1" in ml or "/r1" in ml
        or ml.startswith("kimi-") or ml.startswith("moonshot-")
    )
    profile = None
    if needs_thinking_passback:
        profile = OpenAIModelProfile(
            supports_thinking=True,
            thinking_always_enabled=True,
            openai_chat_thinking_field="reasoning_content",
            openai_chat_send_back_thinking_parts="field",
        )
    return OpenAIChatModel(model_str, provider=provider, profile=profile)

# ---------------------------------------------------------------------------
# Config matrix
# ---------------------------------------------------------------------------

CONFIG_MATRIX = {
    # Full 2^3 factorial over {KB, WS, SK} — see PROTOCOL §1.
    # Numbering follows the isolation conditions (C0-C3) plus the four
    # combination cells (C4-C7) added in v1.3 to support the RQ2 RANOVA / main-
    # effect & interaction analysis. C4 was intentionally undefined in v1.2 on
    # the design-rationale assumption that KB and WS are redundant; v1.3 tests
    # that assumption empirically.
    "C0": {"kb": False, "ws": False, "sk": False},  # bare LLM
    "C1": {"kb": True,  "ws": False, "sk": False},  # KB only (RAG)
    "C2": {"kb": False, "ws": True,  "sk": False},  # WS only (Tavily)
    "C3": {"kb": False, "ws": False, "sk": True},   # SK only (curated SOP)
    "C4": {"kb": True,  "ws": True,  "sk": False},  # KB + WS  (v1.3)
    "C5": {"kb": True,  "ws": False, "sk": True},   # KB + SK  (v1.3)
    "C6": {"kb": False, "ws": True,  "sk": True},   # WS + SK  (v1.3)
    "C7": {"kb": True,  "ws": True,  "sk": True},   # KB + WS + SK (full stack) (v1.3)
}

TASK_SKILL_MAP = {
    "water_extraction": "water-extraction",
    "change_detection": "change-detection",
    "land_classification": "land-cover",
    "burn_scar_detection": "burn-scar-detection",
    "compositional_spatial_query": "compositional-spatial-query",  # T5 (was T7) — multi-step compositional spatial query
}


# ---------------------------------------------------------------------------
# Perturbation (data contamination defense)
# ---------------------------------------------------------------------------

def apply_perturbation(project_dir: Path, task_type: str, gt_path: Path, seed: int | None = None) -> str:
    from PIL import Image, ImageEnhance

    if seed is not None:
        random.seed(seed)
    choice = random.choice(["none", "rotate_90", "rotate_180", "rotate_270", "flip_h", "flip_v", "brightness"])

    def transform(path: Path, skip_brightness: bool = False):
        img = Image.open(path)
        if "rotate" in choice:
            angle = int(choice.split("_")[1])
            img = img.rotate(angle, expand=False)
        elif choice == "flip_h":
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif choice == "flip_v":
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif choice == "brightness" and not skip_brightness:
            img = ImageEnhance.Brightness(img).enhance(random.uniform(0.8, 1.2))
        img.save(path)

    if choice != "none":
        if task_type == "change_detection":
            state = random.getstate()
            transform(project_dir / "image_A.png")
            random.setstate(state)
            transform(project_dir / "image_B.png")
        else:
            transform(project_dir / "input.png")

        if "rotate" in choice or "flip" in choice:
            if gt_path.exists():
                transform(gt_path, skip_brightness=True)

    # Write perturbation info to a temp location (NOT in project_dir, agent shouldn't see it)
    # Caller is responsible for saving this info
    return choice


# ---------------------------------------------------------------------------
# Workspace setup
# ---------------------------------------------------------------------------

def setup_workspace(
    run_dir: Path,
    task_config: dict,
    sample: dict,
    config: str,
) -> tuple[Path, Path]:
    """Create isolated project_dir and workspace_dir for a run.

    Returns (project_dir, workspace_dir).
    """
    cfg = CONFIG_MATRIX[config]
    task_type = task_config["task_type"]
    input_format = task_config.get("input_format", "png")

    # -- project_dir: agent's CWD with input file(s) --
    project_dir = Path(tempfile.mkdtemp(prefix="rsab_proj_"))
    (project_dir / "artifacts").mkdir()

    image_dir = BENCHMARK_DIR / task_config["image_dir"]
    image_filename = task_config.get("image_filename", "input.png")

    is_dual_time = "image_a_filename" in task_config and "image_b_filename" in task_config
    if is_dual_time:
        # Dual-time tasks (T2 change_detection, T4 burn_scar_detection):
        # each sample has image_A + image_B at the same shape.
        ext = "tif" if input_format == "tif" else "png"
        src_a = image_dir / sample["id"] / f"image_A.{ext}"
        src_b = image_dir / sample["id"] / f"image_B.{ext}"
        shutil.copy2(src_a, project_dir / f"image_A.{ext}")
        shutil.copy2(src_b, project_dir / f"image_B.{ext}")
    else:
        # Single-time tasks (T1 water, T3 land_classification): copy the multiband TIFF.
        if "image" in sample:
            src = image_dir.parent / sample["image"]  # samples_v1.json gives path
        else:
            src = image_dir / sample["id"] / image_filename
        # Resolve symlinks so we copy the real TIFF, not a dangling link
        shutil.copy2(src.resolve(), project_dir / image_filename)
    # Note: bands.json sidecar is NOT delivered to the agent. Channel order
    # is communicated via the task prompt template (per-task constant).

    # GT → run_dir only (agent never sees it)
    label_filename = task_config.get("label_filename", "label.png")
    if "label" in sample:
        gt_src = (BENCHMARK_DIR / task_config["label_dir"]).parent / sample["label"]
    else:
        gt_src = BENCHMARK_DIR / task_config["label_dir"] / sample["id"] / label_filename
    gt_dst = run_dir / "_gt_eval.png"
    if gt_src.exists():
        shutil.copy2(gt_src, gt_dst)

    # Perturbation: PNG-only (PIL doesn't handle multi-band uint16 TIFF cleanly).
    # For TIFF tasks we rely on natural Sentinel-2 scene diversity instead.
    perturbation_type = "none"
    if input_format == "png":
        import hashlib
        pert_seed = int(hashlib.sha256(sample.get("id", "").encode()).hexdigest()[:8], 16)
        perturbation_type = apply_perturbation(project_dir, task_type, gt_dst, seed=pert_seed)
    (run_dir / "_perturbation.txt").write_text(perturbation_type)

    # KB: no longer copies docs to project_dir — C1 uses SearchKB tool (RAG)

    # -- workspace_dir: skills + venv symlink --
    ws_dir = Path(tempfile.mkdtemp(prefix="rsab_ws_"))

    # Symlink real venv for Bash
    if REAL_VENV.exists():
        os.symlink(str(REAL_VENV), str(ws_dir / ".venv"))

    # Skills (only for SK configs)
    if cfg["sk"]:
        skill_name = TASK_SKILL_MAP.get(task_type)
        if skill_name:
            src = BENCHMARK_DIR / "skills" / skill_name / "SKILL.md"
            if src.exists():
                dst_dir = ws_dir / ".agent" / "skills" / skill_name
                dst_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst_dir / "SKILL.md")

    return project_dir, ws_dir


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------

def build_prompt(task_config: dict, sample: dict, config: str) -> str:
    cfg = CONFIG_MATRIX[config]
    # Tasks may declare a fixed image_size (T1/T2/T4) OR rely on per-sample
    # 'shape' from samples_v1.json (T3 / native-size OSCD). The prompt
    # template only sees {width}/{height} when the task declares a fixed
    # size; otherwise the template should not reference them at all.
    sample_shape = sample.get("shape")  # [H, W] when present
    fixed_size = task_config.get("image_size")
    if fixed_size:
        w, h = fixed_size
    elif sample_shape:
        h, w = sample_shape
    else:
        w, h = 0, 0  # unused — template must not reference {width}/{height}

    input_format = task_config.get("input_format", "png")
    image_filename = task_config.get("image_filename", f"input.{input_format}")
    output_filename = task_config.get("output_filename", "output.png")

    fmt = dict(
        image_path=image_filename,
        output_path=f"artifacts/{output_filename}",
        width=w, height=h,
        image_a_path=f"image_A.{input_format}",
        image_b_path=f"image_B.{input_format}",
        # Per-sample query for adaptive tasks (T7); empty for fixed tasks.
        query_text=sample.get("query_text", ""),
        target_class=sample.get("target_class", ""),
    )
    prompt = task_config["prompt_template"].format(**fmt)

    hints = []
    if cfg["kb"]:
        hints.append(
            "Tool available: **SearchDocs(query)** — hybrid search over a curated reference "
            "library (remote-sensing fundamentals, spectral-index formulas, Sentinel-2 band "
            "specs, library API docs). You can call it as many times as you need — issue "
            "narrow, targeted queries and follow up with new ones as your understanding "
            "evolves. Use one query per concept (e.g., 'MNDWI threshold values', 'Otsu "
            "thresholding scikit-image', 'water sediment Sentinel-2') rather than packing "
            "everything into one query. Most useful queries are short and specific."
        )
    if cfg["sk"]:
        skill_name = TASK_SKILL_MAP.get(task_config["task_type"], "unknown")
        hints.append(
            f"Tool available: **Skill(skill_name=\"{skill_name}\")** — loads a curated "
            f"reference for this task type with a recommended starting point, scene-aware "
            f"adjustments, self-checks, and common-failure fixes. The skill is guidance, "
            f"not a script: treat its defaults as a starting point, combine its adjustments "
            f"as the scene warrants, and feel free to deviate when the data tells you to."
        )
    if cfg.get("ws"):
        hints.append(
            "Tool available: **WebSearch(query)** — open-web search (ESA/Copernicus docs, "
            "Sentinel-Hub Custom Scripts, GEE tutorials, recent papers, practitioner Q&A). "
            "You can call it multiple times with different queries to gather different "
            "aspects (e.g., one query for the index formula, another for empirical "
            "thresholds, another for known pitfalls). Short specific queries beat long "
            "ones. Follow up when initial results are partial."
        )

    if hints:
        prompt += "\n\n" + "\n".join(hints)

    return prompt


# ---------------------------------------------------------------------------
# Output finder
# ---------------------------------------------------------------------------

_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

_SKIP_PATTERNS = {"edges", "gray", "gradient", "texture", "histogram",
                  "debug", "check", "overlay", "preview", "cluster",
                  "enhanced", "composite", "test", "temp", "tmp"}


def find_output(project_dir: Path, expected: str) -> Path | None:
    """Find agent output file.

    Strategy:
    1. Exact match: artifacts/output.png or output.png (and common extensions)
    2. Fallback: most recently modified image in artifacts/ or project root
    """
    stem = Path(expected).stem  # "output"

    # Priority 1: exact match with any image extension
    for ext in _IMAGE_EXTENSIONS:
        for candidate in [
            project_dir / "artifacts" / f"{stem}{ext}",
            project_dir / f"{stem}{ext}",
        ]:
            if candidate.exists():
                return candidate

    # Priority 2: search artifacts/ and project root for final-looking images
    search_dirs = []
    artifacts = project_dir / "artifacts"
    if artifacts.exists():
        search_dirs.append(artifacts)
    search_dirs.append(project_dir)

    skip_names = {"input", "image_A", "image_B", "_perturbation", "bands"}

    for search_dir in search_dirs:
        candidates = []
        for f in search_dir.iterdir():
            if not f.is_file() or f.suffix.lower() not in _IMAGE_EXTENSIONS:
                continue
            if f.stem in skip_names:
                continue
            if any(s in f.stem.lower() for s in _SKIP_PATTERNS):
                continue
            candidates.append(f)

        if candidates:
            candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return candidates[0]

    return None


# ---------------------------------------------------------------------------
# Single run
# ---------------------------------------------------------------------------

async def run_single(
    task_config: dict,
    sample: dict,
    model: str,
    config: str,
    result_dir: Path,
) -> dict:
    from agent import BenchDeps, agent

    sid = sample["id"]
    run_dir = result_dir / sid
    run_dir.mkdir(parents=True, exist_ok=True)

    project_dir, ws_dir = setup_workspace(run_dir, task_config, sample, config)
    prompt = build_prompt(task_config, sample, config)

    (run_dir / "config.json").write_text(json.dumps({
        "sample_id": sid, "task": task_config["task_type"],
        "config": config, "model": model, "prompt": prompt,
    }, indent=2))

    TOOL_CALL_LIMIT = 30         # productive budget visible to the agent
    PYDANTIC_TOOL_CEILING = 45   # framework-level hard cap; buffer over the
                                  # productive limit for SubmitAnswer attempts
                                  # and budget-exhausted refusals (those are
                                  # cheap text returns but pydantic-ai still
                                  # counts them).
    # No per-run cap on agent.run(): per RunPython subprocess timeouts (60-180s)
    # already bound runaway code, and the productive tool budget bounds total work.
    # Removing the wrapper avoids killing legitimate long thinks during transient
    # provider hangs.

    cfg = CONFIG_MATRIX[config]
    # Per-sample shape (T3/OSCD) takes precedence over fixed task image_size
    # (T1/T2/T4). Both store [H, W] but BenchDeps wants (W, H) — the size
    # passed to PIL.Image.size is (width, height).
    fixed_size = task_config.get("image_size")
    sample_shape = sample.get("shape")  # [H, W]
    if sample_shape:
        expected_size = (int(sample_shape[1]), int(sample_shape[0]))  # (W, H)
    elif fixed_size:
        expected_size = tuple(fixed_size)  # (W, H) per existing convention
    else:
        expected_size = None
    deps = BenchDeps(
        session_id=f"bench-{uuid4().hex[:8]}",
        project_dir=project_dir,
        workspace_path=ws_dir,
        venv_path=REAL_VENV if REAL_VENV.exists() else None,
        tool_log=[],
        start_time=time.monotonic(),
        tool_call_limit=TOOL_CALL_LIMIT,
        show_skill=cfg["sk"],
        show_kb=cfg["kb"],
        show_ws=cfg.get("ws", False),
        expected_output_path=task_config.get("output_filename") and f"artifacts/{task_config['output_filename']}" or "artifacts/output.png",
        expected_output_size=expected_size,
    )

    pai_model = create_model_instance(model)

    print(f"  Running: {sid} | {config} | {model}")
    status: str | None = None
    error_msg = None
    assistant_text = ""
    usage_data = {}
    elapsed = 0.0
    retry_history: list[dict] = []

    # Determinism settings: explicit temperature=0.6 (the provider-default
    # value we want for every backbone in the panel) plus seed=42 for the
    # deterministic LLM-sampling part of the pipeline. Some OpenAI-compatible
    # endpoints clamp or ignore `temperature`; the explicit setting documents
    # intent and matches the value reported in the paper. Variance across
    # repetitions is absorbed at the protocol level via multi-rep sampling.
    model_settings: dict = {"seed": 42, "temperature": 0.6}
    # Kimi / Moonshot SKUs require `extra_body.thinking` to enable the
    # reasoning channel under the OpenAI-compat shape.
    ml = model.lower()
    if ml.startswith("kimi-") or ml.startswith("moonshot-"):
        model_settings["extra_body"] = {"thinking": {"type": "enabled", "budget_tokens": 16000}}

    # Retry policy: up to 10 attempts on transient errors with exponential
    # backoff (longer base for 429 rate-limits). Retry waits are logged
    # separately to retry_history for diagnostics.
    MAX_RETRIES = 10
    BACKOFF_CAP = 600  # cap individual wait at 10 minutes

    for attempt in range(MAX_RETRIES):
        # Reset agent-visible state at the start of each attempt (fresh run).
        deps.tool_log.clear()
        deps.submitted = False
        deps.submission_notes = ""
        deps.submit_attempts.clear()
        deps.start_time = time.monotonic()
        attempt_start = time.monotonic()
        try:
            result = await agent.run(
                prompt, deps=deps, model=pai_model, message_history=[],
                usage_limits=UsageLimits(request_limit=None, tool_calls_limit=PYDANTIC_TOOL_CEILING),
                model_settings=model_settings,
            )
            elapsed = time.monotonic() - attempt_start
            # Agent returned text without calling SubmitAnswer — treat as voluntary stop
            assistant_text = result.output if isinstance(result.output, str) else str(result.output)
            u = result.usage()
            usage_data = {
                "total_tokens": u.total_tokens,
                "input_tokens": getattr(u, "input_tokens", None) or getattr(u, "request_tokens", 0),
                "output_tokens": getattr(u, "output_tokens", None) or getattr(u, "response_tokens", 0),
                "requests": u.requests,
            }
            status = "stopped_no_submit"  # agent ended without SubmitAnswer
            break
        except UsageLimitExceeded:
            elapsed = time.monotonic() - attempt_start
            # Two cases:
            #   (a) deps.submitted=True  → agent called SubmitAnswer → voluntary
            #   (b) deps.submitted=False → real budget exhaustion
            if deps.submitted:
                status = "submitted"
                assistant_text = deps.submission_notes
            else:
                status = "limit_reached"
                error_msg = f"Hit tool call limit ({TOOL_CALL_LIMIT})"
            break
        except Exception as e:
            elapsed = time.monotonic() - attempt_start
            err_msg = f"{type(e).__name__}: {e}"
            err_str = str(e)
            err_lower = err_str.lower()
            is_429 = "429" in err_str or "rate limit" in err_lower or "rate-limit" in err_lower
            is_retryable = is_429 or any(kw in err_str for kw in (
                "Timeout", "ConnectTimeout", "ReadTimeout", "WriteTimeout",
                "Connection error", "disconnected", "RemoteProtocolError",
                "ConnectError", "ServerDisconnectedError", "503", "502", "500",
            ))
            if attempt < MAX_RETRIES - 1 and is_retryable:
                # Exponential backoff. 429 gets a longer base because most
                # provider rate windows span minutes rather than seconds.
                base = 60 if is_429 else 30
                wait_s = min(base * (2 ** attempt), BACKOFF_CAP)
                kind = "429-rate-limit" if is_429 else "transient"
                retry_history.append({
                    "attempt": attempt + 1,
                    "elapsed_s_before_fail": round(elapsed, 2),
                    "kind": kind,
                    "error_preview": err_msg[:200],
                    "wait_s": wait_s,
                })
                print(f"  Retry {attempt+1}/{MAX_RETRIES} after {wait_s}s ({kind}): {err_msg[:120]}")
                await asyncio.sleep(wait_s)  # excluded from `elapsed`
                continue
            # Final failure (out of retries or non-retryable error)
            status = "error"
            error_msg = err_msg
            traceback.print_exc()
            break

    # Evaluate — always try, even after timeout/error (agent may have produced partial output)
    output_path = find_output(project_dir, task_config["output_filename"])
    metrics: dict = {"error": "no_output_file"}

    if output_path is not None:
        gt_path = run_dir / "_gt_eval.png"
        if gt_path.exists():
            try:
                from evaluation.metrics import evaluate_binary, evaluate_multiclass
                if task_config["evaluation"] == "binary":
                    metrics = evaluate_binary(output_path, gt_path)
                else:
                    metrics = evaluate_multiclass(
                        output_path, gt_path,
                        num_classes=task_config.get("num_classes", 3),
                        ignore_index=task_config.get("ignore_index", 255),
                    )
            except Exception as e:
                metrics = {"error": f"eval_failed: {e}"}
        else:
            metrics = {"error": "no_ground_truth"}
            print(f"  WARNING: GT file missing for {sid}")
    else:
        if status in ("submitted", "stopped_no_submit"):
            print(f"  WARNING: No output file for {sid}")

    # Refine status: distinguish "submitted but missing/invalid output"
    if status == "submitted" and "error" in metrics:
        status = "submitted_no_output"

    # Combined score: primary − 0.005 × tool_calls (quality dominates, efficiency bonus)
    primary = None
    if "error" not in metrics:
        primary = metrics.get("f1", metrics.get("oa"))
    if primary is not None:
        combined = round(primary - 0.005 * len(deps.tool_log), 4)
        metrics["primary_metric"] = primary
        metrics["combined_score"] = combined
    else:
        metrics["primary_metric"] = None
        metrics["combined_score"] = None

    # Archive workspace
    ws_archive = run_dir / "workspace"
    if project_dir.exists():
        shutil.copytree(project_dir, ws_archive, symlinks=False,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        shutil.rmtree(project_dir, ignore_errors=True)
    if ws_dir.exists():
        shutil.rmtree(ws_dir, ignore_errors=True)

    # Save logs
    perturbation = "none"
    pert_file = run_dir / "_perturbation.txt"
    if pert_file.exists():
        perturbation = pert_file.read_text().strip()

    # `elapsed_seconds` reports the time inside the most-recent agent.run() call only.
    # `retry_history` records prior failed attempts (with their wait times); cumulative
    # retry wait time is `sum(r["wait_s"] for r in retry_history)` and is NOT included
    # in `elapsed_seconds`.
    retry_wait_total = sum(r.get("wait_s", 0) for r in retry_history)

    (run_dir / "agent_log.json").write_text(json.dumps({
        "status": status, "elapsed_seconds": round(elapsed, 2),
        "usage": usage_data,
        "assistant_text": assistant_text[:5000],
        "submission_notes": deps.submission_notes,
        "submitted": deps.submitted,
        "submit_attempts": deps.submit_attempts,
        "tool_calls": deps.tool_log,
        "retry_history": retry_history,
        "retry_wait_total_s": retry_wait_total,
        "error": error_msg,
    }, indent=2, ensure_ascii=False))

    result_data = {
        "sample_id": sid, "status": status,
        "elapsed_seconds": round(elapsed, 2),
        "retry_count": len(retry_history),
        "retry_wait_total_s": retry_wait_total,
        "tool_calls": len(deps.tool_log),
        "submitted": deps.submitted,
        "usage": usage_data, "metrics": metrics,
        "perturbation": perturbation, "error": error_msg,
    }
    (run_dir / "metrics.json").write_text(json.dumps(result_data, indent=2))

    score_str = f"{primary:.4f}" if primary is not None else "N/A"
    combo_str = f"{metrics['combined_score']:.4f}" if metrics.get("combined_score") is not None else "N/A"
    icon = "✅" if status == "submitted" else "⚠️" if status == "stopped_no_submit" else "❌"
    print(f"  {icon} {sid}: {status} primary={score_str} combined={combo_str} time={elapsed:.1f}s tools={len(deps.tool_log)}")

    return result_data


# ---------------------------------------------------------------------------
# Experiment
# ---------------------------------------------------------------------------

async def run_experiment(task_name: str, config: str, model: str,
                         sample_ids: list[str] | None = None,
                         resume_dir: str | None = None,
                         concurrency: int = 1):
    task_file = BENCHMARK_DIR / "tasks" / f"{task_name}.json"
    if not task_file.exists():
        print(f"ERROR: {task_file} not found")
        return

    task_config = json.loads(task_file.read_text())
    # Sample list location:
    #   - new TIFF tasks: task_config["samples_file"] points to datasets_tif/<task>/samples_v1.json
    #   - legacy PNG tasks: tasks/<task>_samples.json
    if "samples_file" in task_config:
        samples_path = BENCHMARK_DIR / task_config["samples_file"]
    else:
        samples_path = BENCHMARK_DIR / "tasks" / f"{task_name}_samples.json"
    samples = json.loads(samples_path.read_text())

    if sample_ids:
        samples = [s for s in samples if s["id"] in sample_ids]

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    if resume_dir:
        # Resume: reuse existing result directory, skip completed samples
        result_dir = BENCHMARK_DIR / "results" / resume_dir
        if not result_dir.exists():
            print(f"ERROR: Resume directory not found: {result_dir}")
            return
        completed_ids = set()
        for d in result_dir.iterdir():
            if d.is_dir() and (d / "metrics.json").exists():
                completed_ids.add(d.name)
        before = len(samples)
        samples = [s for s in samples if s["id"] not in completed_ids]
        print(f"Resuming: {before - len(samples)} already done, {len(samples)} remaining")
        exp_id = resume_dir
    else:
        model_short = model.replace("/", "-").replace(":", "-")
        # Append a 6-char unique suffix so concurrent processes that hit the
        # same second don't collide on the result directory.
        suffix = uuid4().hex[:6]
        exp_id = f"{task_name}_{config}_{model_short}_{ts}_{suffix}"
        result_dir = BENCHMARK_DIR / "results" / exp_id
        result_dir.mkdir(parents=True, exist_ok=True)

    (result_dir / "experiment_config.json").write_text(json.dumps({
        "experiment_id": exp_id, "task_name": task_name,
        "config": config, "model": model,
        "total_samples": len(samples), "timestamp": ts,
    }, indent=2))

    print(f"\nExperiment: {exp_id}")
    print(f"Task: {task_name} | Config: {config} | Model: {model} | Samples: {len(samples)} | Concurrency: {concurrency}")
    print(f"Output: {result_dir}\n")

    if concurrency <= 1:
        results = []
        for i, sample in enumerate(samples):
            print(f"[{i+1}/{len(samples)}] {'='*50}")
            r = await run_single(task_config, sample, model, config, result_dir)
            results.append(r)
    else:
        # Parallel: bounded by semaphore so we don't blast the provider
        sem = asyncio.Semaphore(concurrency)
        completed = 0

        async def _bounded(idx: int, sample: dict) -> dict:
            nonlocal completed
            async with sem:
                print(f"[start {idx+1}/{len(samples)}] sample={sample.get('id')}")
                r = await run_single(task_config, sample, model, config, result_dir)
                completed += 1
                print(f"[done  {completed}/{len(samples)}] sample={sample.get('id')}")
                return r

        results = await asyncio.gather(
            *[_bounded(i, s) for i, s in enumerate(samples)]
        )

    # Summary — status taxonomy:
    #   submitted          : agent called SubmitAnswer + valid output (strict eval)
    #   submitted_no_output: agent called SubmitAnswer but no/invalid output
    #   stopped_no_submit  : agent ended without calling SubmitAnswer
    #   limit_reached      : ran out of tool budget
    #   timeout / error    : infra failures
    submitted = [r for r in results if r["status"] == "submitted"]
    submitted_no_output = [r for r in results if r["status"] == "submitted_no_output"]
    stopped_no_submit = [r for r in results if r["status"] == "stopped_no_submit"]
    limit_reached = [r for r in results if r["status"] == "limit_reached"]
    timeouts = [r for r in results if r["status"] == "timeout"]
    errors = [r for r in results if r["status"] == "error"]
    has_output = [r for r in results if "error" not in r["metrics"]]

    summary = {
        "experiment_id": exp_id, "task_name": task_name,
        "config": config, "model": model,
        "total": len(results),
        "submitted": len(submitted),
        "submitted_no_output": len(submitted_no_output),
        "stopped_no_submit": len(stopped_no_submit),
        "limit_reached": len(limit_reached),
        "has_output": len(has_output),
        "timeouts": len(timeouts),
        "errors": len(errors),
    }

    # Strict: only voluntarily-submitted runs with valid output
    # Lenient: any run that produced a valid output file
    strict_output = [r for r in submitted if "error" not in r["metrics"]]
    lenient_output = has_output

    def _avg(pool, key):
        return round(sum(r["metrics"][key] for r in pool) / len(pool), 4)

    if task_config["evaluation"] == "binary":
        for label, pool in [("strict", strict_output), ("lenient", lenient_output)]:
            if pool:
                summary[f"avg_f1_{label}"] = _avg(pool, "f1")
                summary[f"avg_iou_{label}"] = _avg(pool, "iou")
                summary[f"avg_combined_{label}"] = _avg(pool, "combined_score")
    elif task_config["evaluation"] == "multiclass":
        for label, pool in [("strict", strict_output), ("lenient", lenient_output)]:
            if pool:
                summary[f"avg_oa_{label}"] = _avg(pool, "oa")
                summary[f"avg_combined_{label}"] = _avg(pool, "combined_score")

    if has_output:
        summary["avg_tool_calls"] = round(sum(r["tool_calls"] for r in has_output) / len(has_output), 2)

    all_runs = [r for r in results if r.get("usage")]
    if all_runs:
        summary["total_tokens"] = sum(r["usage"].get("total_tokens", 0) for r in all_runs)
        summary["total_time"] = round(sum(r["elapsed_seconds"] for r in results), 1)

    summary["results"] = results
    (result_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"DONE: {exp_id}")
    print(
        f"Submitted: {len(submitted)} | Submit-no-output: {len(submitted_no_output)} | "
        f"Stopped-no-submit: {len(stopped_no_submit)} | Limit: {len(limit_reached)} | "
        f"Output: {len(has_output)}/{len(results)} | Timeout: {len(timeouts)} | Error: {len(errors)}"
    )
    for k in (
        "avg_f1_strict", "avg_f1_lenient", "avg_iou_strict", "avg_iou_lenient",
        "avg_oa_strict", "avg_oa_lenient",
        "avg_combined_strict", "avg_combined_lenient",
        "avg_tool_calls",
    ):
        if k in summary:
            print(f"{k}: {summary[k]}")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="RS-AgentBench Runner")
    parser.add_argument("--task", required=True, choices=["water", "change", "landcover", "burn", "query"])
    parser.add_argument("--config", default="C0", choices=list(CONFIG_MATRIX.keys()))
    parser.add_argument("--model", default="z-ai/glm-5.1")
    parser.add_argument("--sample", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--repeat", type=int, default=1, help="Number of repetitions")
    parser.add_argument("--resume", type=str, default=None,
                        help="Resume a previous experiment by its result directory name (skip completed samples)")
    parser.add_argument("--concurrency", type=int, default=1,
                        help="Number of samples to process in parallel within this cell (1 = sequential)")
    args = parser.parse_args()

    if not args.sample and not args.all:
        print("Specify --sample <id> or --all")
        sys.exit(1)

    async def _run_all_reps():
        # All reps share one event loop so HTTP clients / subprocess
        # transports can clean up between reps without the loop closing.
        for rep in range(args.repeat):
            if args.repeat > 1:
                print(f"\n{'#'*60}")
                print(f"# Repetition {rep+1}/{args.repeat}")
                print(f"{'#'*60}")
            await run_experiment(
                task_name=args.task, config=args.config,
                model=args.model, sample_ids=args.sample,
                resume_dir=args.resume if rep == 0 else None,
                concurrency=args.concurrency,
            )

    asyncio.run(_run_all_reps())


if __name__ == "__main__":
    main()
