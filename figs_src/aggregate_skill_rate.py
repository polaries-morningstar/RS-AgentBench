"""Precompute Skill-invocation rate per (model, cfg) for fig:skill-rate (F11).

For each archive, walks all SK-on cells (C3/C5/C6/C7), reads each trial's
agent_log.json, counts whether the "Skill" tool was invoked at least once,
and aggregates the rate per (model, cfg). Saves to
`paper/draft/figs/data/skill_invocation_rate.csv`.

This is the data substrate for the 14B Transition mechanism figure — the
single MOST mechanistic finding of the paper, currently only present as a
hand-typed table in §A.E.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict
import csv

BENCH = Path("/Users/polaries/Work/AutoSpec/benchmark")
OUT = Path("/Users/polaries/Work/AutoSpec/paper/draft/figs/data/skill_invocation_rate.csv")

ARCHIVES = {
    "qwen3-8b":          "archive.E1.20260512_144024.qwen3-8b",
    "qwen3-14b":         "archive.E1.20260513_120116.qwen3-14b",
    "qwen3.6-27b":       "archive.E1.20260509_172625.qwen3.6-27b",
    "qwen3.6-35b-a3b":   "archive.E1.20260516_104240.qwen3.6-35b-a3b",
    "deepseek-v4-flash": "archive.E1.20260509_182107.deepseek-v4-flash",
    "deepseek-v4-pro":   "archive.E1.20260515_142947.deepseek-v4-pro",
    "kimi-k2.6":         "archive.E1.20260509_210641.kimi-k2.6",
}

SK_CFGS = ["C3", "C5", "C6", "C7"]

n_total = defaultdict(int)
n_sk = defaultdict(int)

for model, arc_name in ARCHIVES.items():
    arc = BENCH / arc_name
    if not arc.exists():
        print(f"WARN: archive missing for {model}: {arc}")
        continue
    for cell_dir in (arc / "results").iterdir():
        if not cell_dir.is_dir():
            continue
        parts = cell_dir.name.split("_")
        if len(parts) < 3:
            continue
        task, cfg = parts[0], parts[1]
        if cfg not in SK_CFGS:
            continue
        for sample_dir in cell_dir.iterdir():
            if not sample_dir.is_dir():
                continue
            log = sample_dir / "agent_log.json"
            if not log.exists():
                continue
            try:
                j = json.loads(log.read_text())
                tcs = j.get("tool_calls", []) or []
                tool_names = [tc.get("tool") for tc in tcs]
                n_total[(model, cfg)] += 1
                if "Skill" in tool_names:
                    n_sk[(model, cfg)] += 1
            except Exception:
                pass

# Write CSV
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    w = csv.writer(f)
    w.writerow(["model", "cfg", "n_trials", "n_skill_invoked", "skill_rate"])
    for model in ARCHIVES:
        for cfg in SK_CFGS:
            n = n_total.get((model, cfg), 0)
            ns = n_sk.get((model, cfg), 0)
            rate = ns / n if n > 0 else 0.0
            w.writerow([model, cfg, n, ns, f"{rate:.4f}"])
print(f"wrote {OUT}")

# Print summary
print("\n=== Skill-invocation rate per (model, cfg) ===")
print(f"{'model':22s} | {'C3':>6s} {'C5':>6s} {'C6':>6s} {'C7':>6s}")
for model in ARCHIVES:
    parts = []
    for cfg in SK_CFGS:
        n = n_total.get((model, cfg), 0)
        ns = n_sk.get((model, cfg), 0)
        if n > 0:
            parts.append(f"{100*ns/n:>5.1f}%")
        else:
            parts.append("   --")
    print(f"{model:22s} | " + " ".join(parts))
