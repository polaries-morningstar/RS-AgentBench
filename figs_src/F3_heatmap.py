"""F3 — Per-cell F1 heatmap across (model × config × task).

Five horizontal subplots, one per task. Each subplot is a 5-row × 8-column
heatmap of per-cell mean F1. Rows sorted by total parameter count (ascending
top-to-bottom). Bold border on the per-row best cell. Single shared color
scale across all five panels for cross-task comparison.

Span: full-width (~7 in), ~0.55p tall on ACM sigconf.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER, TASK_ORDER, TASK_LABELS, CFG_ORDER

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

setup()

DATA = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/cell_means.csv"))

# Build per-task matrix: rows = MODEL_ORDER, cols = CFG_ORDER
def build_mat(task):
    sub = DATA[DATA.task == task]
    mat = np.full((len(MODEL_ORDER), len(CFG_ORDER)), np.nan)
    for i, m in enumerate(MODEL_ORDER):
        for j, c in enumerate(CFG_ORDER):
            v = sub[(sub.model == m) & (sub.cfg == c)]["mean"]
            if len(v) > 0:
                mat[i, j] = v.values[0]
    return mat

fig, axes = plt.subplots(1, 5, figsize=(7.2, 2.6),
                          gridspec_kw={"wspace": 0.18})

vmax = float(DATA["mean"].max())
vmin = 0.0
cmap = "YlOrBr"  # color-blind safe sequential

# Short config labels for axis (under heatmap). Post C6/C7 swap: C6=W+S, C7=all.
CFG_SHORT = ["bare", "KB", "WS", "SK", "K+W", "K+S", "W+S", "all"]
# y-tick labels match MODEL_ORDER (weak→strong) — DO NOT hard-code a separate
# list, or row labels desync from the data when MODEL_ORDER changes.
MODEL_SHORT_LEFT = list(MODEL_ORDER)

for ax_idx, task in enumerate(TASK_ORDER):
    ax = axes[ax_idx]
    mat = build_mat(task)

    im = ax.imshow(mat, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")

    # Bold black border on per-row best cell; cell text ONLY on best cell + C0
    for i in range(mat.shape[0]):
        if np.all(np.isnan(mat[i])):
            continue
        best_j = int(np.nanargmax(mat[i]))
        for j in range(mat.shape[1]):
            v = mat[i, j]
            if np.isnan(v):
                continue
            if j == best_j or j == 0:  # show value on C0 + best cell only
                text_color = "white" if v > 0.55 else "#222"
                label = f".{int(round(v*100)):02d}" if v < 1 else "1.00"
                weight = "bold" if j == best_j else "normal"
                ax.text(j, i, label,
                        ha="center", va="center", fontsize=6.5,
                        color=text_color, fontweight=weight)
        rect = mpatches.Rectangle((best_j - 0.5, i - 0.5), 1, 1,
                                   linewidth=1.4, edgecolor="black", facecolor="none",
                                   zorder=5)
        ax.add_patch(rect)

    ax.set_title(TASK_LABELS[task], fontsize=8.5, pad=4)
    ax.set_xticks(range(len(CFG_ORDER)))
    ax.set_xticklabels(CFG_SHORT, fontsize=5.5, rotation=45, ha="right")
    if ax_idx == 0:
        ax.set_yticks(range(len(MODEL_ORDER)))
        ax.set_yticklabels(MODEL_SHORT_LEFT, fontsize=6.5)
    else:
        ax.set_yticks([])

    # Strip "spines" for a cleaner heatmap look
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)

# Shared colorbar
cbar_ax = fig.add_axes([0.92, 0.18, 0.012, 0.7])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("F1 / OA", fontsize=7)
cbar.ax.tick_params(labelsize=6)
cbar.outline.set_linewidth(0.4)

# Title across the figure (figure-level title — caption goes in LaTeX)
fig.suptitle(
    r"7 models $\times$ 8 configurations $\times$ 5 tasks. Bold border = best configuration per (model, task).",
    fontsize=8, y=1.02,
)

plt.subplots_adjust(left=0.10, right=0.90, top=0.85, bottom=0.18)
out_pdf = os.path.join(os.path.dirname(__file__), "../F3_heatmap.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")
