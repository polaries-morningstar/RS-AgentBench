"""F_naive_compare — Deployable-margin heatmap + per-model sidebar.

For each (model, task), count how many of the 8 cfgs sit at or above the
published spectral-index baseline. Color = above-naive cfg count / 8.
The right panel adds horizontal bars summing each row (out of 40), so the
deployment ranking across the seven backbones is visible at a glance.

Span: full-width (~7.2 in), short height.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER, TASK_ORDER, TASK_LABELS

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

setup()

DATA = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/naive_compare.csv"))

# Build per-task matrix: rows = MODEL_ORDER, cols = TASK_ORDER
mat = np.zeros((len(MODEL_ORDER), len(TASK_ORDER)), dtype=int)
for i, m in enumerate(MODEL_ORDER):
    for j, t in enumerate(TASK_ORDER):
        sub = DATA[(DATA.model == m) & (DATA.task == t)]
        above = int((sub.sub_naive == False).sum())
        mat[i, j] = above

# Row sum = total above-naive cells out of 40
row_above = mat.sum(axis=1)

# Two-panel figure: heatmap on the left, horizontal bar summary on the right
fig, (ax_hm, ax_bar) = plt.subplots(
    1, 2, figsize=(7.2, 2.6),
    gridspec_kw={"width_ratios": [2.6, 1.0], "wspace": 0.10},
)

# ---- Left panel: heatmap ---------------------------------------------------
cmap = plt.cm.RdYlGn
im = ax_hm.imshow(mat, cmap=cmap, vmin=0, vmax=8, aspect="auto")

for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat[i, j]
        text_color = "#222" if 2 <= v <= 6 else "white"
        ax_hm.text(j, i, f"{v}", ha="center", va="center",
                   fontsize=8.5, color=text_color, fontweight="bold")

task_short = [TASK_LABELS[t].split()[0] for t in TASK_ORDER]
ax_hm.set_xticks(range(len(TASK_ORDER)))
ax_hm.set_xticklabels(task_short, fontsize=7.5, rotation=0)
ax_hm.xaxis.tick_top()
ax_hm.xaxis.set_label_position("top")

ax_hm.set_yticks(range(len(MODEL_ORDER)))
ax_hm.set_yticklabels(MODEL_ORDER, fontsize=7)

for s in ax_hm.spines.values():
    s.set_visible(False)
ax_hm.tick_params(length=0)

# Compact colorbar attached to heatmap
cbar = fig.colorbar(im, ax=ax_hm, fraction=0.035, pad=0.01,
                    shrink=0.88, ticks=[0, 4, 8])
cbar.set_label("cfgs $\\geq$ naive (out of 8)", fontsize=6.5, labelpad=2)
cbar.ax.tick_params(labelsize=6)
cbar.outline.set_linewidth(0.4)

# ---- Right panel: per-model summary bars ----------------------------------
# Color bars by row_above value using the same diverging cmap to anchor the
# reading: red = weak, green = strong, mirroring the heatmap.
bar_colors = [cmap(v / 40) for v in row_above]
y = np.arange(len(MODEL_ORDER))
ax_bar.barh(y, row_above, color=bar_colors, edgecolor="#333", linewidth=0.4)
ax_bar.invert_yaxis()  # match heatmap top-to-bottom order

# Value labels at bar ends
for i, v in enumerate(row_above):
    ax_bar.text(v + 0.8, i, f"{v}/40", va="center", ha="left",
                fontsize=7.5, color="#222")

ax_bar.set_yticks([])  # model names already shown on heatmap
ax_bar.set_xlim(0, 44)
ax_bar.set_xticks([0, 10, 20, 30, 40])
ax_bar.tick_params(axis="x", labelsize=6.5, length=2)
ax_bar.set_xlabel("Above-naive cells (of 40)", fontsize=7, labelpad=2)
ax_bar.xaxis.set_label_position("top")
ax_bar.xaxis.tick_top()
ax_bar.axvline(20, color="#888", linewidth=0.6, linestyle=":")  # 50% reference

for s in ["top", "right", "left"]:
    ax_bar.spines[s].set_visible(False)
ax_bar.spines["bottom"].set_linewidth(0.5)

plt.subplots_adjust(left=0.13, right=0.96, top=0.84, bottom=0.06)
out_pdf = os.path.join(os.path.dirname(__file__), "../F_naive_compare.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")

print("\nMatrix (rows = MODEL_ORDER, cols = TASK_ORDER, value = cfgs above naive):")
print(" " * 25 + "  ".join(f"{TASK_LABELS[t][:8]:>8s}" for t in TASK_ORDER) + "  | total")
for i, m in enumerate(MODEL_ORDER):
    row_str = "  ".join(f"{mat[i,j]:>8d}" for j in range(len(TASK_ORDER)))
    print(f"{m:25s} {row_str}  | {row_above[i]:2d}/40")
