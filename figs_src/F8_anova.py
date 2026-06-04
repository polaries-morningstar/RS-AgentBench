"""F8 — 2³ KB×WS×SK ANOVA decomposition.

Small-multiples grid: 6 model rows × 5 task columns. Each cell is a
horizontal stacked bar of variance partition (pct_total_ss) by the 7
ANOVA terms (KB, WS, SK, KB:WS, KB:SK, WS:SK, KB:WS:SK). Residual is the
remaining fraction (not plotted).

Visual punch:
  - 8B row × perception tasks: SK segment dominates (30-53% of SS)
  - 14B row × change/landcover: SK 6-9% + KB:SK or KB 4-5% (KB segments
    visible for the first time, contrast against 8B and saturated rows)
  - Saturated rows (35b-a3b → kimi): all bars near-zero, residual dominates

Span: full-width (~7 in), ~4.0 in tall.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER, TASK_ORDER, TASK_LABELS, MODEL_COLORS

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

setup()

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/factorial_anova.csv"))

# Map raw term names to display labels (drop _c suffix, prettify interactions)
TERM_LABEL = {
    "KB_c":           "KB",
    "WS_c":           "WS",
    "SK_c":           "SK",
    "KB_c:WS_c":      "KB·WS",
    "KB_c:SK_c":      "KB·SK",
    "WS_c:SK_c":      "WS·SK",
    "KB_c:WS_c:SK_c": "KB·WS·SK",
}
# Order for stacking: main effects first, then 2-way, then 3-way, then Residual
TERM_ORDER = ["SK_c", "KB_c", "WS_c", "KB_c:SK_c", "WS_c:SK_c", "KB_c:WS_c", "KB_c:WS_c:SK_c", "Residual"]
TERM_LABEL["Residual"] = "Residual (within-cell trial noise)"
TERM_COLORS = {
    "SK_c":           "#1f77b4",  # blue — dominant signal
    "KB_c":           "#ff7f0e",  # orange — KB main effect
    "WS_c":           "#2ca02c",  # green — WS main effect
    "KB_c:SK_c":      "#d62728",  # red — KB×SK
    "WS_c:SK_c":      "#9467bd",  # purple — WS×SK
    "KB_c:WS_c":      "#8c564b",  # brown — KB×WS
    "KB_c:WS_c:SK_c": "#7f7f7f",  # dark gray — 3-way
    "Residual":       "#e0e0e0",  # light gray — within-cell trial noise
}

n_models = len(MODEL_ORDER)
n_tasks = len(TASK_ORDER)
fig, axes = plt.subplots(n_models, n_tasks, figsize=(7.2, 4.0),
                          sharex=True, sharey=False)

for i, m in enumerate(MODEL_ORDER):
    for j, t in enumerate(TASK_ORDER):
        ax = axes[i, j]
        cell = df[(df["model"] == m) & (df["task"] == t)]
        # Build stacked bar (single bar, horizontal). Residual is included
        # so every bar sums to 100% — saturated cells visualise as a giant
        # light-gray Residual block, the 3-regime story restated.
        x = 0
        for term in TERM_ORDER:
            v = cell[cell["term"] == term]["pct_total_ss"].values
            if len(v) == 0 or pd.isna(v[0]):
                continue
            pct = float(v[0])
            if pct <= 0.01:
                continue  # only skip truly zero
            color = TERM_COLORS[term]
            ax.barh(0, pct, left=x, height=0.7,
                    color=color, edgecolor="white", linewidth=0.2)
            # Annotate large coloured segments only (not Residual)
            if pct >= 5 and term != "Residual":
                ax.text(x + pct/2, 0, f"{int(round(pct))}%",
                        fontsize=5.5, color="white", ha="center", va="center",
                        fontweight="bold")
            # Residual annotation only when it's the dominant block (>=85%)
            if term == "Residual" and pct >= 85:
                ax.text(x + pct/2, 0, f"{int(round(pct))}%",
                        fontsize=5.5, color="#555", ha="center", va="center",
                        fontweight="bold")
            x += pct
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.6, 0.6)
        ax.set_yticks([])
        ax.tick_params(axis="x", labelsize=6)
        for sp in ["top", "right", "left"]:
            ax.spines[sp].set_visible(False)
        if i < n_models - 1:
            ax.set_xticks([])
        else:
            ax.set_xticks([0, 50, 100])
            ax.set_xticklabels(["0", "50", "100%"], fontsize=5.5)
        if j == 0:
            # Model label on first column
            ax.set_ylabel(m, rotation=0, fontsize=6.8, ha="right", va="center",
                          color=MODEL_COLORS[m], fontweight="bold", labelpad=18)
        if i == 0:
            ax.set_title(TASK_LABELS[t].split(" ", 1)[-1], fontsize=8, pad=4)

# Legend at bottom
from matplotlib.patches import Patch
legend_handles = [Patch(facecolor=TERM_COLORS[t], label=TERM_LABEL[t])
                  for t in TERM_ORDER]
fig.legend(handles=legend_handles, loc="lower center", ncol=7,
           bbox_to_anchor=(0.5, -0.01), fontsize=6.8, frameon=False,
           handlelength=1.2, columnspacing=0.8, handletextpad=0.4)

# Super title
fig.suptitle(r"$2^3$ KB$\times$WS$\times$SK ANOVA: variance partition (% of total sum-of-squares)",
             fontsize=8.5, y=0.98)

plt.subplots_adjust(left=0.10, right=0.98, top=0.91, bottom=0.10,
                    hspace=0.30, wspace=0.18)
out_pdf = os.path.join(os.path.dirname(__file__), "../F8_anova.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")
