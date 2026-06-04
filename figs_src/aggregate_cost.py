"""
Pre-aggregate per-trial effort metrics (tool calls, output tokens) from the
released archive.

Outputs:
  - data/cost_cells.csv: per (model, cfg) effort stats
  - data/cost_trials.parquet: per-trial effort rows used by the figures
"""
from __future__ import annotations
import os, json, glob
from pathlib import Path
import pandas as pd
import numpy as np

BENCH = Path("/Users/polaries/Work/AutoSpec/benchmark")
DATA_OUT = Path(__file__).resolve().parent.parent / "data"
DATA_OUT.mkdir(exist_ok=True)

# Per-model output throughput (tokens/sec) used to map the recorded duration
# into an output-token estimate. Backbone-specific constants enter only here.
TPS = {
    "qwen3-8b":           80,
    "qwen3-14b":          70,
    "qwen3.6-27b":        50,
    "qwen3.6-35b-a3b":    60,
    "deepseek-v4-flash":  40,
    "deepseek-v4-pro":    35,  # higher-reasoning tier; slower output
    "kimi-k2.6":          25,
}

MODELS = list(TPS.keys())
CFGS = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]
TASKS = ["water", "change", "landcover", "burn", "query"]

rows = []
for archive_dir in glob.glob(str(BENCH / "archive.E1.*")):
    # Skip the deprecated 35B archive (canonical replaced 5/8 → 5/16 re-run)
    if "_DEPRECATED" in archive_dir:
        continue
    # Skip the verification-only sweeps (8B/14B drift evidence, not panel data)
    if "VERIFY" in archive_dir:
        continue
    arc = Path(archive_dir)
    # Skip quarantines
    for cell_dir in glob.glob(str(arc / "results" / "*_*_*")):
        cd = Path(cell_dir)
        if "_quarantine" in str(cd):
            continue
        parts = cd.name.split("_")
        if len(parts) < 3:
            continue
        task = parts[0]
        cfg = parts[1]
        if task not in TASKS or cfg not in CFGS:
            continue
        # Resolve model from the archive name (most reliable) rather than
        # from the cell-dir name (which has provider-prefix artefacts like
        # "kimi-kimi-k2.6" or "qwen3.6-flash" for a3b). Order matters:
        # check more-specific names ("v4-pro") BEFORE less-specific ones
        # ("v4-flash") to avoid mismatches.
        archive_basename = arc.name
        model = None
        if "qwen3-8b" in archive_basename:
            model = "qwen3-8b"
        elif "qwen3-14b" in archive_basename:
            model = "qwen3-14b"
        elif "qwen3.6-35b-a3b" in archive_basename or "qwen3.6-flash" in archive_basename:
            model = "qwen3.6-35b-a3b"
        elif "qwen3.6-27b" in archive_basename:
            model = "qwen3.6-27b"
        elif "deepseek-v4-pro" in archive_basename:
            model = "deepseek-v4-pro"
        elif "deepseek-v4-flash" in archive_basename:
            model = "deepseek-v4-flash"
        elif "kimi-k2.6" in archive_basename:
            model = "kimi-k2.6"
        if model is None:
            continue

        for sample_dir in glob.glob(str(cd / "*")):
            sd = Path(sample_dir)
            if not sd.is_dir():
                continue
            mp = sd / "metrics.json"
            lp = sd / "agent_log.json"
            if not mp.exists():
                continue
            try:
                m = json.loads(mp.read_text())
            except Exception:
                continue

            # Per paper §5.0 census口径: submitted trials whose scoring
            # crashed (primary_metric=None) are scored F1=0 and INCLUDED
            # in aggregates, not dropped. Trials that never produced a
            # metrics.json (agent-loop crashes upstream of submission)
            # are not represented at all in archive — they show up only
            # in the attempts-vs-submitted gap headlined in §4.6.
            submitted_flag = bool(m.get("submitted", False))
            primary = (m.get("metrics") or {}).get("primary_metric")
            if primary is None:
                if not submitted_flag:
                    continue  # never submitted → exclude from analysis
                primary = 0.0  # submitted but scoring failed → F1=0

            elapsed = m.get("elapsed_seconds", 0)
            n_searchdocs = m.get("correction_n_searchdocs", 0)
            n_tool = m.get("tool_calls", 0)
            retries = m.get("retry_count", 0)
            submit_attempts = 1
            if lp.exists():
                try:
                    a = json.loads(lp.read_text())
                    sa = a.get("submit_attempts", [])
                    if isinstance(sa, list):
                        submit_attempts = max(1, len(sa))
                    tc_list = a.get("tool_calls", [])
                    if isinstance(tc_list, list):
                        if isinstance(n_tool, int) and n_tool == 0:
                            n_tool = len(tc_list)
                        # Fallback: count SearchDocs at aggregate time if
                        # the migration didn't run on this trial
                        if "correction_n_searchdocs" not in m:
                            n_searchdocs = sum(
                                1 for tc in tc_list
                                if tc.get("tool") == "SearchDocs"
                            )
                except Exception:
                    pass

            rows.append({
                "model": model,
                "cfg": cfg,
                "task": task,
                "sample": sd.name,
                "f1": float(primary),
                "elapsed_s": float(elapsed),
                "n_searchdocs": int(n_searchdocs),
                "tool_calls": int(n_tool),
                "retry_count": int(retries),
                "submit_attempts": int(submit_attempts),
                "submitted": bool(m.get("submitted", False)),
            })

df = pd.DataFrame(rows)
print(f"Loaded {len(df)} trials across {df['model'].nunique()} models, "
      f"{df['cfg'].nunique()} cfgs, {df['task'].nunique()} tasks.")

# Per-trial output-token estimate from the per-model throughput rates above.
df["tokens_est"] = df.apply(lambda r: r["elapsed_s"] * TPS[r["model"]], axis=1)

# Per (model, cfg) summary — effort metrics only, no USD derivatives
cell = df.groupby(["model", "cfg"]).agg(
    n=("f1", "size"),
    f1_mean=("f1", "mean"),
    elapsed_median=("elapsed_s", "median"),
    elapsed_p90=("elapsed_s", lambda x: float(np.percentile(x, 90))),
    tool_calls_median=("tool_calls", "median"),
    tool_calls_p90=("tool_calls", lambda x: float(np.percentile(x, 90))),
    retry_rate=("retry_count", lambda x: float((x > 0).mean())),
    submit_attempts_mean=("submit_attempts", "mean"),
    tokens_est_median=("tokens_est", "median"),
).reset_index()

cell.to_csv(DATA_OUT / "cost_cells.csv", index=False)
print(f"Wrote {DATA_OUT / 'cost_cells.csv'}")

# Per-model summary
per_model = df.groupby("model").agg(
    n=("f1", "size"),
    f1_mean=("f1", "mean"),
    elapsed_median=("elapsed_s", "median"),
    elapsed_p90=("elapsed_s", lambda x: float(np.percentile(x, 90))),
    tool_calls_median=("tool_calls", "median"),
    retry_rate=("retry_count", lambda x: float((x > 0).mean())),
).reset_index()
print("\n=== Per-model summary ===")
print(per_model.to_string(index=False))

# Per-cfg summary (averaged across models)
per_cfg = df.groupby("cfg").agg(
    n=("f1", "size"),
    f1_mean=("f1", "mean"),
    elapsed_median=("elapsed_s", "median"),
    tool_calls_median=("tool_calls", "median"),
).reset_index()
print("\n=== Per-cfg summary ===")
print(per_cfg.to_string(index=False))

# Diagnostic: 8B integration tax on C4 vs C0
print("\n=== 8B integration-tax check (qwen3-8b only) ===")
sub = df[df["model"] == "qwen3-8b"]
diag = sub.groupby("cfg").agg(
    f1_mean=("f1", "mean"),
    elapsed_median=("elapsed_s", "median"),
    tool_calls_median=("tool_calls", "median"),
    retry_rate=("retry_count", lambda x: float((x > 0).mean())),
).reset_index()
print(diag.to_string(index=False))

# Diagnostic: SK channel efficiency — C3 vs C7 for the large models
print("\n=== SK efficiency check: C3 vs C7 per model ===")
for m in MODELS:
    sub = df[df["model"] == m]
    c3 = sub[sub["cfg"] == "C3"]
    c7 = sub[sub["cfg"] == "C7"]
    if len(c3) == 0 or len(c7) == 0:
        continue
    print(f"  {m:<22s} C3: F1={c3['f1'].mean():.3f} tools={c3['tool_calls'].median():.0f} "
          f"elapsed={c3['elapsed_s'].median():.0f}s | "
          f"C7: F1={c7['f1'].mean():.3f} tools={c7['tool_calls'].median():.0f} "
          f"elapsed={c7['elapsed_s'].median():.0f}s")

# Save the long-form trial table too for figures
df.to_parquet(DATA_OUT / "cost_trials.parquet")
print(f"\nWrote {DATA_OUT / 'cost_trials.parquet'} ({len(df)} rows)")
