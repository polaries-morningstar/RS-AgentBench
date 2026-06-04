"""F5 — Failure-mode taxonomy: 4-pattern horizontal stacked bar.

Redesign rationale
------------------
The original 9-color stacked bar overloaded a single-column figure with
fine-grained categories. The new design collapses the 11-class schema into
the four super-categories that drive the §5.5 narrative
(code / plan / timeout / other), one stacked bar per backbone with N=50.
Sub-category breakdowns inside the plan-level segment are annotated for
the two anomalies the body text relies on: qwen3-14b's skill-not-invoked
streak and v4-pro's class-confusion peak.

Span: single column (~3.4 in wide), ~2.6 in tall on ACM sigconf.
"""
from __future__ import annotations
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from pathlib import Path

setup()

LD = Path(os.path.dirname(__file__)) / ".." / "data" / "failure_labels"

# Unified 350-trial labels: see labels_pool.json (one row per failed trial,
# fields: trial_id, model, task, cfg, sample, submitted, primary_metric,
# label, confidence, notes). Labels are the canonical category assignments.
poolB = pd.DataFrame(json.loads((LD / "labels_pool.json").read_text()))
poolB = poolB.rename(columns={"label": "manual"})

# --- 4 super-categories ---
# Naming rationale:
#   - "parameter-tuning" groups band-index + ndvi-threshold: the agent's
#     code runs cleanly, but a NUMERICAL parameter (which Sentinel-2 band,
#     or what cutoff for the index) is wrong. These are NOT runtime errors;
#     the failure lives at the parameter-choice surface inside otherwise-
#     runnable code.
#   - "plan-level" groups class-confusion / compositional / skill-not-
#     invoked: the agent's entire approach (which class? which composition?
#     use the SOP or not?) is the problem.
#   - "budget-exhausted" reflects the per-trial tool-call budget being
#     consumed by retrieve loops before any code commit.
#   - "other / null" is the residual: true runtime errors (hallucinated
#     function, malformed output, wrong input file — all rare; 4/350 in
#     total) plus the rubric's `other` and `crs_ignored` (zero manual
#     instances).
SUPER = [
    ("tuning",  "parameter-tuning",   ["band_index", "ndvi_threshold"],
                                      "#E76F51"),  # warm coral
    ("plan",    "plan-level",         ["class_confusion", "compositional_plan",
                                       "skill_not_invoked"],
                                      "#2A9D8F"),  # flagship teal
    ("budget",  "budget-exhausted",   ["timeout_stall"],
                                      "#E9C46A"),  # mustard
    ("other",   "other / null",       ["hallucinated_fn", "malformed_output",
                                       "wrong_input", "crs_ignored", "other"],
                                      "#BFC8CE"),  # cool gray
]
# Darker teal for the skill-not-invoked sub-portion of plan (only non-zero
# on qwen3-14b; called out separately because §5.4 traces the 14 B finding
# to that 15-trial sub-pool).
SNI_COLOR = "#1A3D3A"

# Per-model counts at the super-cat level
def super_counts(model):
    cnt = poolB[poolB.model == model].manual.value_counts().to_dict()
    out = {sid: 0 for sid, _, _, _ in SUPER}
    out_sub = {}
    for sid, _, members, _ in SUPER:
        out[sid] = sum(cnt.get(k, 0) for k in members)
        for k in members:
            if cnt.get(k, 0) > 0:
                out_sub[k] = cnt[k]
    return out, out_sub


# ---------- Plot ----------
fig, ax = plt.subplots(figsize=(3.4, 2.0))

y = np.arange(len(MODEL_ORDER))
bar_h = 0.66

# Stacked horizontal bars. For the plan segment, draw the
# skill-not-invoked sub-portion in a darker teal as a contiguous sub-segment
# (no hatching — hatching reads as a different layer rather than a
# sub-segment of the same category).
for i, m in enumerate(MODEL_ORDER):
    cnt, sub = super_counts(m)
    left = 0.0
    for sid, _, _, color in SUPER:
        w = cnt[sid]
        if w == 0:
            continue
        if sid == "plan":
            sni_w = sub.get("skill_not_invoked", 0)
            plan_other_w = w - sni_w
            # plan-other (non-SNI) first
            if plan_other_w > 0:
                ax.barh(i, plan_other_w, left=left, height=bar_h,
                        color=color, edgecolor="white", linewidth=0.4)
                if plan_other_w >= 4:
                    ax.text(left + plan_other_w / 2, i, f"{plan_other_w}",
                            ha="center", va="center", fontsize=6.5,
                            color="white", fontweight="bold")
            # SNI sub-segment, darker
            if sni_w > 0:
                ax.barh(i, sni_w, left=left + plan_other_w, height=bar_h,
                        color=SNI_COLOR, edgecolor="white", linewidth=0.4)
                if sni_w >= 4:
                    ax.text(left + plan_other_w + sni_w / 2, i,
                            f"{sni_w} SNI",
                            ha="center", va="center", fontsize=6.0,
                            color="white", fontweight="bold")
        else:
            ax.barh(i, w, left=left, height=bar_h,
                    color=color, edgecolor="white", linewidth=0.4)
            if w >= 4:
                ax.text(left + w / 2, i, f"{w}",
                        ha="center", va="center", fontsize=6.5,
                        color="white" if sid in ("tuning", "budget") else "#333",
                        fontweight="bold")
        left += w

# Y-axis: model names
ax.set_yticks(y)
ax.set_yticklabels(MODEL_ORDER, fontsize=7.2)
ax.invert_yaxis()

# X-axis: 0..50 with percentage equivalents
ax.set_xlim(0, 50)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_xticklabels(["0", "10\n(20%)", "20\n(40%)", "30\n(60%)", "40\n(80%)", "50\n(100%)"],
                   fontsize=6.3)
ax.set_xlabel("Failed trials labelled (N = 50 / model)", fontsize=7.6, labelpad=2)

# Spines + grid
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_linewidth(0.4)
ax.spines["bottom"].set_linewidth(0.4)
ax.tick_params(axis="y", length=0, pad=2)
ax.tick_params(axis="x", length=2.5, pad=1)
ax.grid(True, axis="x", alpha=0.13, linewidth=0.4)
ax.set_axisbelow(True)

# Legend: 4 super-categories + the SNI sub-shade
legend_handles = [Patch(facecolor=color, edgecolor="white", label=label)
                  for _, label, _, color in SUPER]
legend_handles.append(Patch(facecolor=SNI_COLOR, edgecolor="white",
                             label="skill-not-invoked (sub-plan)"))
ax.legend(handles=legend_handles,
          loc="upper center", bbox_to_anchor=(0.5, 1.20),
          ncol=3, fontsize=5.9, frameon=False,
          handlelength=1.0, handleheight=1.0,
          handletextpad=0.3, columnspacing=0.8)

plt.subplots_adjust(left=0.27, right=0.98, top=0.82, bottom=0.18)
out_pdf = os.path.join(os.path.dirname(__file__), "../F5_failure_modes.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")

# Summary print
print("\n=== Per-model super-category breakdown ===")
for m in MODEL_ORDER:
    cnt, sub = super_counts(m)
    print(f"  {m:<22}  tuning={cnt['tuning']:>2}  plan={cnt['plan']:>2}  "
          f"budget={cnt['budget']:>2}  other={cnt['other']:>2}   "
          f"plan-detail={sub}")
