"""Aggregate RS-AgentBench results across cells (publication-grade).

Usage:
    uv run python aggregate.py [--since TS] [--model SLUG] [--task TASK]
                                [--csv path] [--no-wilcoxon] [--no-holm]
                                [--full]

A "cell" is one (task, config, model) triple. A trial is one (sample, rep)
within that cell. We collect every per-trial primary metric, then report
the metric set defined in METRICS.md §C.

Headline columns (always shown):
    model, task, cfg, n_reps, n_trials, sub%
    primary_mean, primary_CI95, sd_per_trial,
    co_metric (IoU for binary, Kappa for multiclass),
    pass^1, pass^5,
    tools_med, elap_med_s, tokens_med,
    Δ_vs_C0, wilcoxon_raw, wilcoxon_holm, cohen_d

Use --full to also dump:
    - precision/recall/accuracy means (binary)
    - per-class F1 (multiclass)
    - status breakdown
    - strict vs lenient comparison
    - combined score
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import statistics as st
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

PRIMARY_KEY = "primary_metric"
RESULTS_DIR = Path("results")
SUMMARY_NAME = "summary.json"
PASS_THRESHOLD = 0.5    # MIN primary to count a rep as "successful" for Pass^k
N_BOOTSTRAP = 1000


# ---------------------------------------------------------------------------
# Filters and parsing
# ---------------------------------------------------------------------------

def parse_since(s: str) -> float:
    s = s.strip()
    for fmt in ("%Y%m%d_%H%M%S", "%Y%m%d_%H%M", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt).timestamp()
        except ValueError:
            continue
    raise SystemExit(f"--since: unrecognised timestamp '{s}' (use YYYYMMDD[_HHMM[SS]])")


def parse_cell_dir(name: str) -> tuple[str, str, str] | None:
    """Result dir name is <task>_<cfg>_<model>_<timestamp>[_<uuid>]."""
    parts = name.split("_")
    if len(parts) < 4:
        return None
    task, cfg = parts[0], parts[1]
    ts_idx = next(
        (i for i, p in enumerate(parts)
         if len(p) == 8 and p.isdigit() and p.startswith("20")),
        None,
    )
    if ts_idx is None or ts_idx <= 2:
        return None
    return task, cfg, "_".join(parts[2:ts_idx])


# ---------------------------------------------------------------------------
# Statistical primitives
# ---------------------------------------------------------------------------

_BOOTSTRAP_RNG = np.random.default_rng(42)

def bootstrap_ci(values: list[float], n_resample: int = N_BOOTSTRAP,
                 alpha: float = 0.05) -> tuple[float, float]:
    """Percentile-method bootstrap CI on the mean."""
    if not values:
        return float("nan"), float("nan")
    if len(values) == 1:
        return values[0], values[0]
    arr = np.asarray(values, dtype=float)
    means = _BOOTSTRAP_RNG.choice(arr, size=(n_resample, arr.size),
                                  replace=True).mean(axis=1)
    return float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))


def wilcoxon_paired(a: list[float], b: list[float]) -> float | None:
    if len(a) != len(b) or len(a) < 6:
        return None
    try:
        from scipy import stats
    except ImportError:
        return None
    if all(bi - ai == 0 for ai, bi in zip(a, b)):
        return None
    try:
        _, p = stats.wilcoxon(a, b, alternative="two-sided", zero_method="wilcox")
    except ValueError:
        return None
    return float(p)


def cohen_d_paired(a: list[float], b: list[float]) -> float | None:
    """Cohen's d on paired samples — uses the SD of the differences."""
    if len(a) != len(b) or len(a) < 2:
        return None
    diffs = [bi - ai for ai, bi in zip(a, b)]
    sd_diff = st.stdev(diffs)
    if sd_diff == 0:
        return float("inf") if st.mean(diffs) != 0 else 0.0
    return st.mean(diffs) / sd_diff


def holm_bonferroni(p_values: list[float]) -> list[float | None]:
    """Apply Holm-Bonferroni step-down adjustment to a family of p-values.

    Skips None entries (treated as 'not tested') and returns adjusted p in the
    original input order. Adjusted p ≥ raw p; capped at 1.0.
    """
    indexed = [(i, p) for i, p in enumerate(p_values) if p is not None]
    if not indexed:
        return [None] * len(p_values)
    indexed.sort(key=lambda x: x[1])
    n = len(indexed)
    adj = [None] * len(p_values)
    running_max = 0.0
    for rank, (orig_idx, p) in enumerate(indexed):
        adj_p = min(p * (n - rank), 1.0)
        adj_p = max(adj_p, running_max)  # enforce monotonicity
        running_max = adj_p
        adj[orig_idx] = adj_p
    return adj


# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------

def collect_trials(args) -> dict[tuple[str, str, str], dict]:
    """Walk results/ and gather all trials per (task, cfg, model) cell."""
    if not RESULTS_DIR.exists():
        sys.exit(f"results dir missing: {RESULTS_DIR.resolve()}")
    since = parse_since(args.since) if args.since else 0.0

    cells: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {"trials": [], "n_summary_files": 0,
                 "task_evaluation": None}
    )

    for sum_path in sorted(glob.glob(str(RESULTS_DIR / "*" / SUMMARY_NAME))):
        run_dir = Path(sum_path).parent
        try:
            ctime = run_dir.stat().st_mtime
        except OSError:
            continue
        if ctime < since:
            continue

        parsed = parse_cell_dir(run_dir.name)
        if parsed is None:
            continue
        task, cfg, model = parsed
        if args.model and args.model not in model:
            continue
        if args.task and args.task != task:
            continue

        try:
            with open(sum_path) as f:
                sdata = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        cell = cells[(task, cfg, model)]
        cell["n_summary_files"] += 1
        # Cache the rep_dir name so Pass^k can sort reps deterministically.
        rep_id = run_dir.name

        for r in sdata.get("results", []):
            metrics = r.get("metrics") or {}
            primary = metrics.get(PRIMARY_KEY)
            if primary is None and r.get("status") == "submitted":
                primary = metrics.get("oa") or metrics.get("overall_accuracy")
            usage = r.get("usage") or {}
            cell["trials"].append({
                "sample_id": r.get("sample_id"),
                "status": r.get("status"),
                "primary": primary,
                "f1": metrics.get("f1"),
                "iou": metrics.get("iou"),
                "precision": metrics.get("precision"),
                "recall": metrics.get("recall"),
                "accuracy": metrics.get("accuracy"),
                "oa": metrics.get("oa"),
                "kappa": metrics.get("kappa"),
                "mean_f1": metrics.get("mean_f1"),
                "per_class_f1": metrics.get("per_class_f1") or {},
                "combined": metrics.get("combined_score"),
                "tools": r.get("tool_calls", 0),
                "elapsed": r.get("elapsed_seconds", 0.0),
                "tokens": usage.get("total_tokens", 0) if isinstance(usage, dict) else 0,
                "rep_id": rep_id,
            })
        # Cache evaluation kind once per task. Trials don't store it; the
        # summary.json doesn't either, but `f1` vs `oa` membership reveals it.

    # Infer task evaluation kind (binary vs multiclass) from any trial.
    for key, payload in cells.items():
        if payload["task_evaluation"] is not None:
            continue
        for t in payload["trials"]:
            if t["f1"] is not None:
                payload["task_evaluation"] = "binary"
                break
            if t["oa"] is not None:
                payload["task_evaluation"] = "multiclass"
                break
    return cells


# ---------------------------------------------------------------------------
# Aggregations
# ---------------------------------------------------------------------------

def per_sample_means(trials: list[dict], metric_key: str = "primary") -> dict[str, float]:
    """Return {sample_id: mean of `metric_key` across reps} for trials with a value."""
    by_sample: dict[str, list[float]] = defaultdict(list)
    for t in trials:
        v = t.get(metric_key)
        if v is not None:
            by_sample[t["sample_id"]].append(v)
    return {sid: sum(vs) / len(vs) for sid, vs in by_sample.items() if vs}


def pass_at_k(trials: list[dict], k: int, threshold: float = PASS_THRESHOLD) -> float | None:
    """Pass^k as defined in METRICS.md §C.2.

    For each sample, sort its trials by rep_id, take the first k, and require
    ALL k to be `submitted` with primary ≥ threshold. Return the per-sample
    indicator's mean.
    """
    by_sample: dict[str, list[dict]] = defaultdict(list)
    for t in trials:
        by_sample[t["sample_id"]].append(t)

    valid_samples = 0
    pass_count = 0
    for sid, rep_trials in by_sample.items():
        rep_trials = sorted(rep_trials, key=lambda x: x.get("rep_id", ""))
        if len(rep_trials) < k:
            continue
        valid_samples += 1
        first_k = rep_trials[:k]
        if all(rt.get("status") == "submitted"
               and rt.get("primary") is not None
               and rt["primary"] >= threshold
               for rt in first_k):
            pass_count += 1
    if valid_samples == 0:
        return None
    return pass_count / valid_samples


def status_breakdown(trials: list[dict]) -> dict[str, int]:
    counts = defaultdict(int)
    for t in trials:
        counts[t.get("status", "unknown")] += 1
    return dict(counts)


def per_rep_mean_sd(trials: list[dict]) -> float | None:
    """SD across rep-level cell means (cell stability)."""
    by_rep: dict[str, list[float]] = defaultdict(list)
    for t in trials:
        if t["primary"] is not None:
            by_rep[t["rep_id"]].append(t["primary"])
    rep_means = [sum(vs) / len(vs) for vs in by_rep.values() if vs]
    if len(rep_means) < 2:
        return None
    return st.stdev(rep_means)


def cell_stats(payload: dict) -> dict:
    """Compute the full set of cell-level stats."""
    trials = payload["trials"]
    eval_kind = payload["task_evaluation"]
    if not trials:
        return {}

    submitted = [t for t in trials if t["status"] == "submitted"]
    has_output_status = {"submitted", "stopped_no_submit", "limit_reached", "timeout"}
    # "Has output" is approximated by "had a metric computed". Trials with
    # primary=None typically had no output file or hit error.
    eval_pool = [t for t in trials if t["primary"] is not None]

    out = {
        "n_trials": len(trials),
        "n_eval": len(eval_pool),
        "n_submitted": len(submitted),
        "submitted_pct": 100.0 * len(submitted) / len(trials),
        "tools_med": st.median([t["tools"] for t in trials]),
        "elapsed_med": st.median([t["elapsed"] for t in trials]),
        "status_breakdown": status_breakdown(trials),
        "evaluation": eval_kind,
    }

    tokens = [t["tokens"] for t in trials if t.get("tokens")]
    out["tokens_med"] = st.median(tokens) if tokens else None
    out["tokens_total"] = sum(tokens) if tokens else 0

    if not eval_pool:
        return out

    primaries = [t["primary"] for t in eval_pool]
    out["primary_mean"] = st.mean(primaries)
    out["primary_sd_trial"] = st.stdev(primaries) if len(primaries) > 1 else 0.0
    ci_low, ci_high = bootstrap_ci(primaries)
    out["primary_ci_low"] = ci_low
    out["primary_ci_high"] = ci_high
    out["primary_sd_rep_mean"] = per_rep_mean_sd(trials)

    # Co-metric: IoU for binary, Kappa for multiclass
    if eval_kind == "binary":
        ious = [t["iou"] for t in eval_pool if t["iou"] is not None]
        precs = [t["precision"] for t in eval_pool if t["precision"] is not None]
        recs = [t["recall"] for t in eval_pool if t["recall"] is not None]
        accs = [t["accuracy"] for t in eval_pool if t["accuracy"] is not None]
        out["iou_mean"] = st.mean(ious) if ious else None
        out["iou_ci"] = bootstrap_ci(ious) if len(ious) > 1 else (out["iou_mean"], out["iou_mean"])
        out["precision_mean"] = st.mean(precs) if precs else None
        out["recall_mean"] = st.mean(recs) if recs else None
        out["accuracy_mean"] = st.mean(accs) if accs else None
        out["co_metric_label"] = "IoU"
        out["co_metric_mean"] = out["iou_mean"]
        out["co_metric_ci"] = out.get("iou_ci")
    elif eval_kind == "multiclass":
        kappas = [t["kappa"] for t in eval_pool if t["kappa"] is not None]
        mean_f1s = [t["mean_f1"] for t in eval_pool if t["mean_f1"] is not None]
        out["kappa_mean"] = st.mean(kappas) if kappas else None
        out["kappa_ci"] = bootstrap_ci(kappas) if len(kappas) > 1 else None
        out["mean_f1_mean"] = st.mean(mean_f1s) if mean_f1s else None
        # Per-class F1 averaging
        per_class_acc: dict[str, list[float]] = defaultdict(list)
        for t in eval_pool:
            for cid, v in (t["per_class_f1"] or {}).items():
                per_class_acc[cid].append(v)
        out["per_class_f1_mean"] = {
            cid: round(st.mean(vs), 4) for cid, vs in sorted(per_class_acc.items())
        }
        out["co_metric_label"] = "Kappa"
        out["co_metric_mean"] = out["kappa_mean"]
        out["co_metric_ci"] = out.get("kappa_ci")

    # Combined score
    combined = [t["combined"] for t in eval_pool if t["combined"] is not None]
    out["combined_mean"] = st.mean(combined) if combined else None

    # Pass^k
    out["pass_1"] = pass_at_k(trials, 1)
    out["pass_3"] = pass_at_k(trials, 3)
    out["pass_5"] = pass_at_k(trials, 5)

    return out


# ---------------------------------------------------------------------------
# Comparison vs C0
# ---------------------------------------------------------------------------

def compare_vs_c0(c0_trials: list[dict],
                  cx_trials: list[dict]) -> dict:
    """Per-sample-mean comparison: Δ, Wilcoxon raw, Cohen's d.

    Holm-Bonferroni adjustment is applied later, across the family of
    {C1, C2, C3} comparisons within (task, model).
    """
    c0_means = per_sample_means(c0_trials, "primary")
    cx_means = per_sample_means(cx_trials, "primary")
    common = sorted(set(c0_means) & set(cx_means))
    if len(common) < 2:
        return {"delta": None, "wilcoxon_raw": None, "cohen_d": None,
                "n_pairs": len(common)}
    a = [c0_means[s] for s in common]
    b = [cx_means[s] for s in common]
    delta = sum(bi - ai for ai, bi in zip(a, b)) / len(a)
    return {
        "delta": delta,
        "wilcoxon_raw": wilcoxon_paired(a, b),
        "cohen_d": cohen_d_paired(a, b),
        "n_pairs": len(common),
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def fmt_p(p: float | None) -> str:
    if p is None:
        return "—"
    sig = ""
    if p < 0.001: sig = " ***"
    elif p < 0.01: sig = " **"
    elif p < 0.05: sig = " *"
    elif p < 0.1: sig = " ."
    return f"{p:.3f}{sig}"


def fmt_ci(low: float | None, high: float | None) -> str:
    if low is None or high is None or math.isnan(low) or math.isnan(high):
        return "—"
    return f"[{low:.3f}, {high:.3f}]"


def fmt_num(v, prec: int = 3) -> str:
    if v is None:
        return "—"
    if isinstance(v, float) and math.isnan(v):
        return "—"
    if isinstance(v, float):
        return f"{v:.{prec}f}"
    return str(v)


def render_headline(cells: dict, with_wilcoxon: bool, with_holm: bool,
                    csv_path: str | None) -> None:
    if not cells:
        print("No matching cells. Adjust --since / --model / --task.")
        return

    grouped: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for (task, cfg, model), payload in cells.items():
        grouped[(task, model)][cfg] = payload

    cols = ["model", "task", "cfg", "n_reps", "n_trials", "sub%",
            "primary_mean", "CI95", "co_metric",
            "pass^1", "pass^5",
            "tools_med", "elap_med_s", "tokens_med"]
    if with_wilcoxon:
        cols += ["Δ_vs_C0", "wilcoxon_raw", "cohen_d"]
    if with_holm:
        cols += ["wilcoxon_holm"]

    print("| " + " | ".join(cols) + " |")
    print("| " + " | ".join("---" for _ in cols) + " |")

    csv_rows: list[list[str]] = []

    for (task, model), cells_in_group in sorted(grouped.items()):
        c0 = cells_in_group.get("C0")
        # Pre-compute every Cx vs C0 comparison so we can Holm-correct as a
        # family within (task, model).
        cmp_cache: dict[str, dict] = {}
        if c0 and with_wilcoxon:
            for cfg, payload in cells_in_group.items():
                if cfg == "C0":
                    continue
                cmp_cache[cfg] = compare_vs_c0(c0["trials"], payload["trials"])
        if with_holm and cmp_cache:
            cfg_order = sorted(cmp_cache.keys())
            raw_ps = [cmp_cache[c]["wilcoxon_raw"] for c in cfg_order]
            adj_ps = holm_bonferroni(raw_ps)
            for cfg, adj in zip(cfg_order, adj_ps):
                cmp_cache[cfg]["wilcoxon_holm"] = adj

        for cfg in sorted(cells_in_group):
            payload = cells_in_group[cfg]
            stats = cell_stats(payload)
            co_label = stats.get("co_metric_label", "—")
            co_str = (f"{co_label}={fmt_num(stats.get('co_metric_mean'))}"
                      if stats.get("co_metric_mean") is not None else "—")
            row = [
                model,
                task,
                cfg,
                str(payload["n_summary_files"]),
                str(stats.get("n_trials", 0)),
                f"{stats.get('submitted_pct', 0):.0f}%",
                fmt_num(stats.get("primary_mean")),
                fmt_ci(stats.get("primary_ci_low"), stats.get("primary_ci_high")),
                co_str,
                fmt_num(stats.get("pass_1"), 2),
                fmt_num(stats.get("pass_5"), 2),
                fmt_num(stats.get("tools_med"), 0),
                fmt_num(stats.get("elapsed_med"), 1),
                fmt_num(stats.get("tokens_med"), 0),
            ]
            if with_wilcoxon:
                if cfg == "C0":
                    row += ["—", "—", "—"]
                else:
                    cmp = cmp_cache.get(cfg, {})
                    row += [
                        fmt_num(cmp.get("delta")),
                        fmt_p(cmp.get("wilcoxon_raw")),
                        fmt_num(cmp.get("cohen_d"), 2),
                    ]
            if with_holm:
                if cfg == "C0":
                    row += ["—"]
                else:
                    row += [fmt_p(cmp_cache.get(cfg, {}).get("wilcoxon_holm"))]
            print("| " + " | ".join(row) + " |")
            csv_rows.append(row)

    if csv_path and csv_rows:
        with open(csv_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(csv_rows)
        print(f"\nCSV written to: {csv_path}", file=sys.stderr)


def render_full_supplement(cells: dict) -> None:
    """Verbose dump for the supplement (after the headline table)."""
    if not cells:
        return
    grouped: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for (task, cfg, model), payload in cells.items():
        grouped[(task, model)][cfg] = payload

    print("\n\n## Supplement — additional metrics")
    for (task, model), cells_in_group in sorted(grouped.items()):
        for cfg in sorted(cells_in_group):
            payload = cells_in_group[cfg]
            stats = cell_stats(payload)
            print(f"\n### {model} | {task} | {cfg}")
            print(f"  n_trials={stats.get('n_trials')}  n_eval={stats.get('n_eval')}  n_submitted={stats.get('n_submitted')}")
            print(f"  primary_mean={fmt_num(stats.get('primary_mean'))}  "
                  f"sd_per_trial={fmt_num(stats.get('primary_sd_trial'))}  "
                  f"sd_per_rep_mean={fmt_num(stats.get('primary_sd_rep_mean'))}")
            print(f"  combined_mean={fmt_num(stats.get('combined_mean'))}")
            print(f"  status_breakdown: {stats.get('status_breakdown')}")
            if stats.get("evaluation") == "binary":
                print(f"  IoU_mean={fmt_num(stats.get('iou_mean'))}  "
                      f"precision_mean={fmt_num(stats.get('precision_mean'))}  "
                      f"recall_mean={fmt_num(stats.get('recall_mean'))}  "
                      f"accuracy_mean={fmt_num(stats.get('accuracy_mean'))}")
            elif stats.get("evaluation") == "multiclass":
                print(f"  Kappa_mean={fmt_num(stats.get('kappa_mean'))}  "
                      f"meanF1={fmt_num(stats.get('mean_f1_mean'))}  "
                      f"per_class_f1={stats.get('per_class_f1_mean')}")
            print(f"  pass^1={fmt_num(stats.get('pass_1'),2)}  "
                  f"pass^3={fmt_num(stats.get('pass_3'),2)}  "
                  f"pass^5={fmt_num(stats.get('pass_5'),2)}")
            print(f"  tokens_total={stats.get('tokens_total')}  tokens_med={fmt_num(stats.get('tokens_med'),0)}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--since", help="Only include result dirs newer than YYYYMMDD or YYYYMMDD_HHMM[SS]")
    ap.add_argument("--model", help="Substring filter on model name")
    ap.add_argument("--task", choices=["water", "change", "landcover", "burn"])
    ap.add_argument("--csv", help="Write the headline table to this CSV path as well")
    ap.add_argument("--no-wilcoxon", action="store_true", help="Skip Wilcoxon / Cohen's d / Δ_vs_C0 columns")
    ap.add_argument("--no-holm", action="store_true", help="Skip Holm-Bonferroni adjusted p column")
    ap.add_argument("--full", action="store_true", help="Also dump the supplement section (per-class F1, status breakdown, sd, tokens)")
    args = ap.parse_args()

    cells = collect_trials(args)
    render_headline(
        cells,
        with_wilcoxon=not args.no_wilcoxon,
        with_holm=not args.no_holm,
        csv_path=args.csv,
    )
    if args.full:
        render_full_supplement(cells)


if __name__ == "__main__":
    main()
