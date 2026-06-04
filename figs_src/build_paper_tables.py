"""Unified builder for all paper data tables (6-model panel).

Produces in figs/data/:
  - all_trials.parquet         : long-form per-trial table
  - cell_means.csv             : (model, task, cfg) F1 mean + 95% bootstrap CI
  - scaling_curve.csv          : (model, cfg) F1 averaged across tasks + CI
  - pairwise_contrasts.csv     : key cfg deltas per (model, task) + paired CI
  - factorial_anova.csv        : 2³ KB×WS×SK decomposition per (model, task)
  - sk_forest.csv              : SK main effect per (model, task) for forest plot
  - pareto_frontier.csv        : (model, cfg) F1 vs effort for cost-quality plane

Source of truth: 6 archive.E1.* directories. Aggregate口径:
    include trial if (primary_metric != None) OR (submitted=True)
    (submitted but unscored → F1=0).
"""
from __future__ import annotations
import json
import glob
import warnings
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

BENCH = Path("/Users/polaries/Work/AutoSpec/benchmark")
OUT = Path("/Users/polaries/Work/AutoSpec/paper/draft/figs/data")
OUT.mkdir(exist_ok=True)

ARCHIVES = {
    "qwen3-8b":          "archive.E1.20260512_144024.qwen3-8b",
    "qwen3-14b":         "archive.E1.20260513_120116.qwen3-14b",
    "qwen3.6-27b":       "archive.E1.20260509_172625.qwen3.6-27b",
    "qwen3.6-35b-a3b":   "archive.E1.20260516_104240.qwen3.6-35b-a3b",  # canonical replaced 5/8 → 5/16 re-run; old archive renamed *_DEPRECATED
    "deepseek-v4-flash": "archive.E1.20260509_182107.deepseek-v4-flash",
    "deepseek-v4-pro":   "archive.E1.20260515_142947.deepseek-v4-pro",
    "kimi-k2.6":         "archive.E1.20260509_210641.kimi-k2.6",
}

# Model size metadata (active params, total params in B). For MoE: active_B
# corresponds to active experts per forward pass.
MODEL_SIZES = {
    "qwen3-8b":          (8,   8),
    "qwen3-14b":         (14,  14),
    "qwen3.6-27b":       (27,  27),
    "qwen3.6-35b-a3b":   (3,   35),  # A3B = 3B active, 35B total MoE
    "deepseek-v4-flash": (37,  671),  # DeepSeek-V4 family MoE — rough public estimates
    "deepseek-v4-pro":   (49,  1600),  # 49B active / 1.6T total — different scale tier from v4-flash
    "kimi-k2.6":         (32,  1000), # Kimi K2 — public 1T-class with sparse activation
}

CFG_BITS = {
    "C0": (0,0,0), "C1": (1,0,0), "C2": (0,1,0), "C3": (0,0,1),
    "C4": (1,1,0), "C5": (1,0,1), "C6": (0,1,1), "C7": (1,1,1),
}
TASKS = ["water","change","landcover","burn","query"]
CFGS = list(CFG_BITS.keys())


# ============================================================================
# Step 1: build all_trials.parquet — single source of truth
# ============================================================================
def build_all_trials() -> pd.DataFrame:
    rows = []
    for model, arc_name in ARCHIVES.items():
        arc = BENCH / arc_name
        # Per (task, cfg, sample) running rep_id
        rep_ctr = defaultdict(int)
        for mp_path in sorted(glob.glob(str(arc / "results" / "*" / "*" / "metrics.json"))):
            mp = Path(mp_path)
            m = json.loads(mp.read_text())
            primary = (m.get("metrics") or {}).get("primary_metric")
            submitted = bool(m.get("submitted", False))
            if primary is None:
                if not submitted:
                    continue  # exclude: never submitted AND no metric
                f1 = 0.0
            else:
                f1 = float(primary)
            cell_dir = mp.parent.parent.name
            parts = cell_dir.split("_")
            task, cfg = parts[0], parts[1]
            sample = mp.parent.name
            rep_id = rep_ctr[(model, task, cfg, sample)]
            rep_ctr[(model, task, cfg, sample)] += 1
            kb, ws, sk = CFG_BITS[cfg]
            rows.append({
                "model": model,
                "task": task,
                "cfg": cfg,
                "kb": kb, "ws": ws, "sk": sk,
                "sample": sample,
                "rep_id": rep_id,
                "f1": f1,
                "primary_metric": f1,  # alias for legacy figure scripts
                "submitted": submitted,
                "scored": primary is not None,
                "elapsed_s": float(m.get("elapsed_seconds", 0)),
                "tool_calls": int(m.get("tool_calls", 0)),
                "retry_count": int(m.get("retry_count", 0)),
                "n_searchdocs": int(m.get("correction_n_searchdocs", 0)),
            })
    df = pd.DataFrame(rows)
    print(f"all_trials: {len(df)} rows across {df['model'].nunique()} models, "
          f"{df['cfg'].nunique()} cfgs, {df['task'].nunique()} tasks")
    df.to_parquet(OUT / "all_trials.parquet")
    print(f"Wrote {OUT / 'all_trials.parquet'}")
    return df


# ============================================================================
# Step 2: cell_means.csv with sample-paired bootstrap CI
# ============================================================================
def bootstrap_mean_ci(values: np.ndarray, n_boot: int = 2000, ci: float = 0.95,
                      rng: np.random.Generator | None = None) -> tuple[float, float, float]:
    if rng is None:
        rng = np.random.default_rng(42)
    if len(values) == 0:
        return (float("nan"), float("nan"), float("nan"))
    boots = rng.choice(values, size=(n_boot, len(values)), replace=True).mean(axis=1)
    lo = float(np.percentile(boots, 100 * (1 - ci) / 2))
    hi = float(np.percentile(boots, 100 * (1 - (1 - ci) / 2)))
    return float(values.mean()), lo, hi


def build_cell_means(df: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for (model, task, cfg), sub in df.groupby(["model", "task", "cfg"]):
        vals = sub["f1"].values
        mean, lo, hi = bootstrap_mean_ci(vals, rng=rng)
        rows.append({
            "model": model, "task": task, "cfg": cfg,
            "n": len(sub),
            "mean": mean, "ci_low": lo, "ci_high": hi,
            "elapsed_median": float(sub["elapsed_s"].median()),
            "tool_calls_median": float(sub["tool_calls"].median()),
            "submitted_rate": float(sub["submitted"].mean()),
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "cell_means.csv", index=False)
    print(f"Wrote {OUT / 'cell_means.csv'} ({len(out)} rows = "
          f"{out['model'].nunique()} models × {out['task'].nunique()} tasks × "
          f"{out['cfg'].nunique()} cfgs)")
    return out


# ============================================================================
# Step 3: scaling_curve.csv (F1 vs model size, per cfg, averaged across tasks)
# ============================================================================
def build_scaling_curve(df: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    # For each (model, cfg), bootstrap F1 mean averaging across tasks
    # We resample at the (task, sample) cluster level to respect non-independence
    for (model, cfg), sub in df.groupby(["model", "cfg"]):
        # cluster-bootstrap by (task, sample) pairs
        clusters = sub.groupby(["task", "sample"])["f1"].mean().reset_index()
        vals = clusters["f1"].values
        mean, lo, hi = bootstrap_mean_ci(vals, rng=rng)
        active_B, total_B = MODEL_SIZES[model]
        rows.append({
            "model": model, "cfg": cfg,
            "active_B": active_B, "total_B": total_B,
            "f1_mean": mean, "ci_low": lo, "ci_high": hi, "n_trials": len(sub),
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "scaling_curve.csv", index=False)
    print(f"Wrote {OUT / 'scaling_curve.csv'} ({len(out)} rows = "
          f"{out['model'].nunique()} models × {out['cfg'].nunique()} cfgs)")
    return out


# ============================================================================
# Step 4: pairwise_contrasts.csv (paired bootstrap on (sample) clusters)
# ============================================================================
def build_pairwise_contrasts(df: pd.DataFrame) -> pd.DataFrame:
    """Compute paired contrasts: for each (model, task, contrast), get Δ + CI.
    
    Pair on `sample` (each sample is observed under all 8 cfgs ×  5 reps).
    Bootstrap-resample samples → compute mean(cfg_a) - mean(cfg_b) on resample.
    """
    contrasts = [
        ("C3_vs_C0", "C3", "C0"),  # SK alone
        ("C1_vs_C0", "C1", "C0"),  # KB alone
        ("C2_vs_C0", "C2", "C0"),  # WS alone
        ("C5_vs_C3", "C5", "C3"),  # KB+SK over SK
        ("C6_vs_C3", "C6", "C3"),  # WS+SK over SK (post C6/C7 swap)
        ("C7_vs_C3", "C7", "C3"),  # full over SK (post C6/C7 swap)
        ("C7_vs_C0", "C7", "C0"),  # full over bare (post C6/C7 swap)
        ("C4_vs_C0", "C4", "C0"),  # KB+WS over bare
    ]
    rng = np.random.default_rng(42)
    rows = []
    # Pre-compute per (model, task, cfg, sample) mean F1
    sample_means = df.groupby(["model", "task", "cfg", "sample"])["f1"].mean().reset_index()
    for (model, task), sub in sample_means.groupby(["model", "task"]):
        # Wide: rows=sample, cols=cfg
        wide = sub.pivot(index="sample", columns="cfg", values="f1")
        for name, ca, cb in contrasts:
            if ca not in wide.columns or cb not in wide.columns:
                continue
            paired = wide[[ca, cb]].dropna()
            if len(paired) == 0:
                continue
            diffs = (paired[ca] - paired[cb]).values
            mean, lo, hi = bootstrap_mean_ci(diffs, rng=rng)
            rows.append({
                "model": model, "task": task, "contrast": name,
                "delta": mean, "ci_low": lo, "ci_high": hi,
                "n_samples": len(paired),
            })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "pairwise_contrasts.csv", index=False)
    print(f"Wrote {OUT / 'pairwise_contrasts.csv'} ({len(out)} rows)")
    return out


# ============================================================================
# Step 5: factorial_anova.csv (2³ KB×WS×SK decomposition)
# ============================================================================
def build_factorial_anova(df: pd.DataFrame) -> pd.DataFrame:
    """Per (model, task), fit OLS F1 ~ KB*WS*SK and report sum-of-squares.
    
    Uses centered (-1, +1) coding for clean orthogonal decomposition.
    """
    try:
        import statsmodels.formula.api as smf
        from statsmodels.stats.anova import anova_lm
    except ImportError:
        print("⚠️  statsmodels not installed — skipping factorial_anova.csv")
        return pd.DataFrame()
    
    rows = []
    for (model, task), sub in df.groupby(["model", "task"]):
        sub = sub.copy()
        # Center coding -1/+1 for orthogonality
        sub["KB_c"] = sub["kb"].astype(int) * 2 - 1
        sub["WS_c"] = sub["ws"].astype(int) * 2 - 1
        sub["SK_c"] = sub["sk"].astype(int) * 2 - 1
        try:
            ols = smf.ols("f1 ~ KB_c * WS_c * SK_c", data=sub).fit()
            aov = anova_lm(ols, typ=2)
            total_ss = aov["sum_sq"].sum()
            for term in aov.index:
                ss = float(aov.loc[term, "sum_sq"])
                df_val = float(aov.loc[term, "df"])
                F = float(aov.loc[term, "F"]) if "F" in aov.columns and pd.notna(aov.loc[term, "F"]) else float("nan")
                p = float(aov.loc[term, "PR(>F)"]) if "PR(>F)" in aov.columns and pd.notna(aov.loc[term, "PR(>F)"]) else float("nan")
                pct = 100 * ss / total_ss if total_ss > 0 else float("nan")
                rows.append({
                    "model": model, "task": task,
                    "term": term, "SS": ss, "df": df_val,
                    "F": F, "p_value": p, "pct_total_ss": pct,
                })
        except Exception as e:
            print(f"  ⚠️ ANOVA failed for {model}/{task}: {e}")
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "factorial_anova.csv", index=False)
    print(f"Wrote {OUT / 'factorial_anova.csv'} ({len(out)} rows)")
    return out


# ============================================================================
# Step 6: sk_forest.csv (SK main effect for forest plot)
# ============================================================================
def build_sk_forest(df: pd.DataFrame) -> pd.DataFrame:
    """SK main effect = mean(F1 | SK=1) - mean(F1 | SK=0), per (model, task).
    
    Sample-paired bootstrap CI.
    """
    rng = np.random.default_rng(42)
    rows = []
    sample_means = df.groupby(["model", "task", "sample", "sk"])["f1"].mean().reset_index()
    for (model, task), sub in sample_means.groupby(["model", "task"]):
        wide = sub.pivot_table(index="sample", columns="sk", values="f1", aggfunc="mean")
        if 0 not in wide.columns or 1 not in wide.columns:
            continue
        paired = wide[[0, 1]].dropna()
        if len(paired) == 0:
            continue
        diffs = (paired[1] - paired[0]).values
        mean, lo, hi = bootstrap_mean_ci(diffs, rng=rng)
        rows.append({
            "model": model, "task": task,
            "sk_effect": mean, "ci_low": lo, "ci_high": hi,
            "n_samples": len(paired),
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "sk_forest.csv", index=False)
    print(f"Wrote {OUT / 'sk_forest.csv'} ({len(out)} rows)")
    return out


# ============================================================================
# Step 7: pareto_frontier.csv (cost-quality plane)
# ============================================================================
def build_pareto_frontier(df: pd.DataFrame) -> pd.DataFrame:
    """Per (model, cfg) F1 mean + elapsed median + on-frontier marker.
    
    Pareto frontier: non-dominated points in (elapsed → low, F1 → high) plane.
    """
    rows = []
    for (model, cfg), sub in df.groupby(["model", "cfg"]):
        rows.append({
            "model": model, "cfg": cfg,
            "f1_mean": float(sub["f1"].mean()),
            "elapsed_median": float(sub["elapsed_s"].median()),
            "elapsed_mean": float(sub["elapsed_s"].mean()),
            "tool_calls_median": float(sub["tool_calls"].median()),
        })
    out = pd.DataFrame(rows)
    # Mark Pareto frontier (across all model×cfg combos)
    pts = out[["elapsed_median", "f1_mean"]].values
    on_frontier = np.zeros(len(out), dtype=bool)
    for i, (ei, fi) in enumerate(pts):
        dominated = False
        for j, (ej, fj) in enumerate(pts):
            if i == j: continue
            if ej <= ei and fj >= fi and (ej < ei or fj > fi):
                dominated = True
                break
        on_frontier[i] = not dominated
    out["on_frontier"] = on_frontier
    out.to_csv(OUT / "pareto_frontier.csv", index=False)
    print(f"Wrote {OUT / 'pareto_frontier.csv'} ({len(out)} rows, {on_frontier.sum()} on frontier)")
    return out


# ============================================================================
# Main
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Building paper data tables from 6-model archive panel")
    print("=" * 70)
    print()
    df = build_all_trials()
    print()
    cell_means = build_cell_means(df)
    print()
    scaling = build_scaling_curve(df)
    print()
    contrasts = build_pairwise_contrasts(df)
    print()
    anova = build_factorial_anova(df)
    print()
    sk = build_sk_forest(df)
    print()
    pareto = build_pareto_frontier(df)
    print()
    print("=" * 70)
    print(f"All tables written to: {OUT}")
