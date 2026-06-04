"""Extract compact per-trial digests for a 50-trial κ subsample.

Samples 50 trials from labels_pool.json (seed=42, stratified by model when possible),
locates each trial's agent_log.json under benchmark/archive.E1.*/results/,
and writes a condensed digest (no notes, no original label) to /tmp/kappa_subsample.json
for blind second-rater labeling.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

LABELS = Path("/Users/polaries/Work/AutoSpec/paper/archive/data/failure_labels/labels_pool.json")
BENCHMARK_ROOT = Path("/Users/polaries/Work/AutoSpec/benchmark")
OUT = Path("/tmp/kappa_subsample.json")
N_SAMPLE = 50
SEED = 42


def find_agent_log(model: str, task: str, cfg: str, sample: str):
    """Locate the agent_log.json for one trial. Tries model and prefixed-model variants."""
    model_variants = [model, f"kimi-{model}" if not model.startswith("kimi-kimi") else model]
    for mv in model_variants:
        pattern = f"results/{task}_{cfg}_{mv}_*/{sample}/agent_log.json"
        for archive in BENCHMARK_ROOT.glob(f"archive.E1.*.{model}"):
            for log in archive.glob(pattern):
                return log
        for archive in BENCHMARK_ROOT.glob("archive.E1.*"):
            for log in archive.glob(pattern):
                return log
    return None


def compress_log(log_path: Path, max_code_chars: int = 800) -> dict:
    """Extract a compact digest from agent_log.json."""
    try:
        data = json.loads(log_path.read_text())
    except Exception as e:
        return {"_error": f"read fail: {e}"}

    tool_calls = data.get("tool_calls") or data.get("trace") or []
    tool_names = []
    code_snippets = []
    errors = []
    skill_invocations = 0
    for tc in tool_calls:
        name = tc.get("tool") or tc.get("name") or ""
        tool_names.append(name)
        if name in ("Skill",):
            skill_invocations += 1
        if name in ("RunPython", "run_python"):
            code = tc.get("code_preview") or (tc.get("input", {}) or {}).get("code", "")
            if code:
                code_snippets.append(code[:max_code_chars])
        # Tool-call level error
        status = tc.get("status") or ""
        if status not in ("ok", "", None):
            err = tc.get("stderr") or tc.get("error") or tc.get("output_preview") or status
            if err:
                errors.append(str(err)[:400])

    final_text = data.get("assistant_text") or data.get("final_text") or ""
    sub_notes = data.get("submission_notes") or ""
    err_top = data.get("error") or ""
    retries = data.get("retry_history") or []

    return {
        "tool_sequence": tool_names[:40],
        "n_tool_calls": len(tool_calls),
        "n_skill_invocations": skill_invocations,
        "code_previews": code_snippets[-3:],
        "errors_recent": errors[-3:],
        "top_error": str(err_top)[:300],
        "submission_notes": str(sub_notes)[:300],
        "final_text_preview": str(final_text)[:500],
        "n_retries": len(retries),
        "status": data.get("status"),
    }


def main():
    labels = json.loads(LABELS.read_text())
    rng = random.Random(SEED)
    # Stratified by model — 7 trials per model when possible, then 1 extra from random
    by_model = {}
    for row in labels:
        by_model.setdefault(row["model"], []).append(row)
    n_per_model = N_SAMPLE // len(by_model)
    extra = N_SAMPLE - n_per_model * len(by_model)

    sampled = []
    for m, rows in sorted(by_model.items()):
        pick = rng.sample(rows, min(n_per_model, len(rows)))
        sampled.extend(pick)
    # add extras from remaining
    remaining = [r for r in labels if r not in sampled]
    sampled.extend(rng.sample(remaining, extra))
    assert len(sampled) == N_SAMPLE

    digests = []
    found, missing = 0, 0
    for row in sampled:
        log = find_agent_log(row["model"], row["task"], row["cfg"], row["sample"])
        digest = {
            "trial_id": row["trial_id"],
            "model": row["model"],
            "task": row["task"],
            "cfg": row["cfg"],
            "sample": row["sample"],
            "submitted": row["submitted"],
            "primary_metric": row["primary_metric"],
            "_original_label": row["label"],  # for κ comparison after second-rater pass
        }
        if log:
            digest["_log_path"] = str(log.relative_to(BENCHMARK_ROOT))
            digest.update(compress_log(log))
            found += 1
        else:
            digest["_missing"] = True
            missing += 1
        digests.append(digest)

    OUT.write_text(json.dumps(digests, indent=2, default=str))
    print(f"Wrote {len(digests)} digests to {OUT}")
    print(f"  found logs: {found}")
    print(f"  missing logs: {missing}")


if __name__ == "__main__":
    main()
