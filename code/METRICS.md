# RS-AgentBench Metrics Reference

This document defines every metric reported by the benchmark, where it
comes from in the data pipeline, and how `aggregate.py` derives it.

Cross-reference: [PROTOCOL.md](PROTOCOL.md) §8 freezes which metrics are
headline vs supplementary.

---

## A. Quality metrics (per-trial, written to `metrics.json`)

These are computed by `evaluation/metrics.py` from the agent's predicted
mask vs the ground-truth mask. They live inside `result["metrics"]` for
every trial in `summary.json`.

### A.1 Binary tasks (T1 water / T2 vegetation / T3 change)

| Metric | Formula | Range | Why we use it | Source |
|---|---|---|---|---|
| **F1** | `2·P·R / (P+R)` | [0, 1] | Harmonic mean of precision and recall — single-number quality summary, robust to mild class imbalance. **Headline metric for binary tasks.** | `metrics.py:evaluate_binary` |
| **IoU** (Jaccard) | `TP / (TP+FP+FN)` | [0, 1] | Stricter than F1 (no double-counting of correct background); standard for segmentation papers. **Co-headline with F1.** | `metrics.py:evaluate_binary` |
| **Precision** | `TP / (TP+FP)` | [0, 1] | "Of pixels we said are foreground, how many actually are?" Diagnoses over-prediction. | `metrics.py:evaluate_binary` |
| **Recall** | `TP / (TP+FN)` | [0, 1] | "Of true foreground pixels, how many did we catch?" Diagnoses under-prediction. | `metrics.py:evaluate_binary` |
| **Accuracy** | `(TP+TN) / total` | [0, 1] | Reported for completeness but **misleading** under heavy class imbalance (water rarely > 30% of a tile) — F1/IoU are the real summary. | `metrics.py:evaluate_binary` |
| TP/FP/FN/TN | raw pixel counts | ≥ 0 | Diagnostic only; not headline. | `metrics.py:evaluate_binary` |

### A.2 Multiclass task (T4 land_classification, 4 classes)

| Metric | Formula | Range | Why we use it | Source |
|---|---|---|---|---|
| **OA** (Overall Accuracy) | `correct_pixels / total` | [0, 1] | Standard land-cover headline. | `metrics.py:evaluate_multiclass` |
| **Kappa** (Cohen's) | `(po − pe) / (1 − pe)` where `po` = OA and `pe` = expected agreement under random labelling | [-1, 1] | Controls for chance agreement. Critical when class priors are skewed; reviewers reject OA-only multiclass papers. **Co-headline.** | `metrics.py:evaluate_multiclass` |
| **Mean F1** | mean of per-class F1 | [0, 1] | Equal-weighted; rewards balanced performance across classes. | `metrics.py:evaluate_multiclass` |
| **Per-class F1** | F1 per class id (0..3) | [0, 1] each | Diagnoses which class is failing (e.g., `built` typically lowest). Reported as a table in the paper supplement. | `metrics.py:evaluate_multiclass` |

A Hungarian permutation pass is applied before scoring so that K-means-style
agents (with arbitrary cluster IDs) get credit for getting the *partitioning*
right even if their label IDs don't match GT 0/1/2/3. This is documented in
PROTOCOL.md §7 and `metrics.py:_hungarian_remap`.

---

## B. Process metrics (per-trial, written to `metrics.json` + agent_log)

| Metric | Definition | How obtained |
|---|---|---|
| **status** | One of `submitted`, `submitted_no_output`, `stopped_no_submit`, `limit_reached`, `timeout`, `error`. | Set by `runner.run_single` based on agent termination. |
| **elapsed_seconds** | Duration in seconds from agent start to termination. | `runner.run_single`. |
| **tool_calls** | Count of all tool invocations (RunPython + Skill + SearchDocs + WebSearch + SubmitAnswer attempts). | `runner.run_single` from `deps.tool_log`. |
| **tool_log** | Full per-call log: tool name, args preview, status, error if any. | `agent.py` (every `@agent.tool` appends to `ctx.deps.tool_log`). |
| **submit_attempts** | Sequence of all SubmitAnswer attempts incl. rejections (wrong size, missing file, etc.). | `agent.py:SubmitAnswer`. |
| **usage.total_tokens** | Total tokens spent on LLM calls (when provider returns it). | pydantic-ai usage object → `result.usage()`. Some OpenAI-compatible endpoints omit this field. |

### B.1 Combined score (efficiency-aware quality)

`combined_score = primary − 0.005 × tool_calls`

- `primary` is F1 (binary) or OA (multiclass).
- The 0.005 weight is small intentionally: we don't want to drown the
  quality signal. It exists so a model that needs 30 tool calls to reach
  F1=0.6 is penalised relative to one that reaches F1=0.6 in 5 calls.
- **Never shown to the agent** (no reward hacking).
- Computed in `runner.py:run_single` and written into each trial's metrics.

---

## C. Cell-level summary metrics (in `summary.json` + `aggregate.py`)

A "cell" is one (model, condition, task) tuple. Each cell normally contains
50 trials (10 samples × 5 reps).

### C.1 Headline (always reported)

| Metric | What it summarises | How computed |
|---|---|---|
| **mean primary** | Cell-average F1 (binary) or OA (multiclass), strict pool | mean over per-trial primary across submitted-with-output trials |
| **CI95** | Bootstrap 95 % CI on the cell mean | `aggregate.py:bootstrap_ci`, 1000 percentile resamples (seed=42) |
| **mean IoU** (binary) / **mean Kappa** (multiclass) | Co-headline, captures tighter quality | per-trial → cell mean |
| **per-trial sd** | Variance across all 50 trials in the cell | std of per-trial primary |
| **per-rep-mean sd** | Variance across reps' means | std of [rep_mean for rep in reps] |
| **submission rate** | % trials that voluntarily called SubmitAnswer with valid output | `n_submitted / n_trials` |
| **tools_med** | Median tool calls per trial | median over trials |
| **elapsed_med** | Median per-trial duration in seconds | median over trials |
| **tokens_med** | Median tokens per trial (when available) | median of `usage.total_tokens` |
| **status breakdown** | Counts of {submitted, no_output, stopped, limit_reached, timeout, error} | grouped count |

### C.2 Reliability (Pass^k, k = 1..5)

PROTOCOL §8 requires this. Definition:

> For each sample, look at the k reps under that cell. Pass^k = the
> probability (averaged over samples) that **all k reps** produced a
> `submitted` status with primary ≥ τ, where τ = 0.5.

```
Pass^k(cell) = (1/n_samples) · Σ_s 1[ all k reps of sample s succeeded ]
```

Pass^1 says "for a typical sample, what's the chance one rep succeeds?"
Pass^5 says "what's the chance all 5 reps succeed?" — the harshest reliability
view. We report Pass^1, Pass^3, Pass^5 in the table; Pass^2/Pass^4 in supplement.

`aggregate.py:pass_at_k` reorganises trials by sample, sorts reps by their
result-dir timestamp (deterministic order), takes the first k reps, and
checks the all-pass condition.

### C.3 Comparison stats (cell vs C0 baseline within same task+model)

| Metric | Definition | When meaningful |
|---|---|---|
| **Δ_vs_C0** | Mean of (Cx_mean − C0_mean) computed per-sample | always |
| **Wilcoxon paired p** | Two-sided Wilcoxon signed-rank on per-sample means (C0 vs Cx) | requires ≥ 6 paired samples — we have 10 |
| **Cohen's d** | `(mean_x − mean_0) / pooled_sd` on per-sample means | always |
| **Holm-Bonferroni adjusted p** | Wilcoxon p adjusted within the family {C1, C2, C3} per (task, model) | reported alongside raw p |

Effect-size interpretation (Cohen): `\|d\| < 0.2` negligible, `0.2-0.5` small,
`0.5-0.8` medium, `> 0.8` large.

---

## D. Aggregation pipeline (where each number lives)

```
per-pixel arrays (in PIL.Image)
        │
        ▼ metrics.py:evaluate_{binary,multiclass}
trial-level metrics.json  ◄── F1, IoU, Precision, Recall, Accuracy,
        │                     OA, Kappa, Mean F1, Per-class F1,
        │                     primary_metric, combined_score, TP/FP/FN/TN
        │
        ▼ runner.py:run_experiment
cell-level summary.json   ◄── strict/lenient pools, avg_f1, avg_iou,
        │                     avg_oa, avg_combined, avg_tool_calls,
        │                     status counts, total_tokens, total_time
        │
        ▼ aggregate.py
publication table         ◄── mean ± CI, Pass^k, Δ_vs_C0, Wilcoxon p,
                              Holm-adj p, Cohen's d, tokens, status%
```

---

## E. What goes into the paper vs supplement

### Paper (E1 main, E2 cross-model)

For each cell:
- **mean primary ± 95% CI** (F1 for binary, OA for multiclass)
- **mean IoU** (binary) / **mean Kappa** (multiclass)
- **Pass^1 / Pass^5**
- **Δ_vs_C0**, **Wilcoxon p (Holm-adj)**, **Cohen's d**
- **submission rate**, **median tool calls**

### Supplement

- Per-class F1 (multiclass, all 4 classes)
- Strict vs Lenient comparison
- Status breakdown per cell
- Median tokens per cell
- All raw p-values, before and after Holm correction
- Per-trial sd vs per-rep-mean sd
- Failure mode tagging (when 11-class taxonomy is added later)
- Combined score (efficiency-quality tradeoff)

---

## F. What we deliberately do NOT report

These are tempting but rejected:

- **Mean of strict + lenient blended**: misleading; we report both separately.
- **Single F1 across all tasks ("benchmark score")**: tasks differ; aggregating obscures the analysis.
- **Token-cost-per-F1**: provider-dependent and rate-volatile; not a stable comparison.
- **Sample-level p-values**: too many; we test at the cell level.
- **Statistical significance of effect sizes**: violates the convention that effect sizes are descriptive, not inferential.
