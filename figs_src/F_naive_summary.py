"""F_naive_summary — Per-model paired violins of deployable margin.

For each backbone we plot two side-by-side violins of the per-cell
signed deployable margin (agent score minus that task's naive
spectral-index baseline):

  Left  (gray)  — SK-off cells (C0, C1, C2, C4); 20 cells
  Right (teal)  — SK-on  cells (C3, C5, C6, C7); 20 cells

A red dashed line at y=0 marks the naive baseline. Median bars on
each violin make the SK-induced upward shift visible at each model;
the qwen3-14b pair lies almost entirely below the line and the
deepseek-v4-pro pair almost entirely above it.

Span: full-width figure* (~7 in x ~2.8 in).
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import numpy as np

setup()
np.random.seed(42)  # for jittered inner strip points

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
cells = pd.read_csv(os.path.join(DATA_DIR, "cell_means.csv"))
naive = pd.read_csv(os.path.join(DATA_DIR, "naive_compare.csv"))

df = pd.merge(cells, naive[["model", "task", "cfg", "naive", "sub_naive"]],
              on=["model", "task", "cfg"])
df["margin"] = df["mean"] - df["naive"]
df["sk_on"] = df["cfg"].isin(["C3", "C5", "C6", "C7"])

# Short labels for the x-axis to keep things from crowding.
SHORT = {
    "qwen3-8b":          "qwen3-8b",
    "qwen3-14b":         "qwen3-14b",
    "qwen3.6-27b":       "qwen3.6-27b",
    "qwen3.6-35b-a3b":   "qwen3.6-35b-a3b",
    "deepseek-v4-flash": "v4-flash",
    "kimi-k2.6":         "kimi-k2.6",
    "deepseek-v4-pro":   "v4-pro",
}

OFF_COLOR = "#cfd8dc"   # cool gray for SK-off
OFF_EDGE  = "#5e6b73"
ON_COLOR  = "#2A9D8F"   # flagship teal for SK-on (matches F_scaling C3)
ON_EDGE   = "#1a3d3a"

fig, ax = plt.subplots(figsize=(7.0, 2.85))

xs = np.arange(len(MODEL_ORDER))
violin_dx = 0.21       # horizontal offset of each violin from the model centre
violin_width = 0.36

for i, m in enumerate(MODEL_ORDER):
    sub = df[df.model == m]
    sk_off = sub[~sub.sk_on]["margin"].to_numpy()
    sk_on  = sub[ sub.sk_on]["margin"].to_numpy()

    # Left violin — SK-off
    p_off = ax.violinplot([sk_off], positions=[i - violin_dx],
                          widths=violin_width, showmedians=True,
                          showextrema=False)
    for body in p_off["bodies"]:
        body.set_facecolor(OFF_COLOR)
        body.set_edgecolor(OFF_EDGE)
        body.set_linewidth(0.5)
        body.set_alpha(0.92)
    p_off["cmedians"].set_color("#222")
    p_off["cmedians"].set_linewidth(1.2)

    # Right violin — SK-on
    p_on = ax.violinplot([sk_on], positions=[i + violin_dx],
                         widths=violin_width, showmedians=True,
                         showextrema=False)
    for body in p_on["bodies"]:
        body.set_facecolor(ON_COLOR)
        body.set_edgecolor(ON_EDGE)
        body.set_linewidth(0.5)
        body.set_alpha(0.92)
    p_on["cmedians"].set_color("white")
    p_on["cmedians"].set_linewidth(1.2)

    # Faint inner jitter to acknowledge that each violin summarises 20 cells
    rng_off = np.random.normal(0, 0.05, len(sk_off))
    ax.scatter(np.full(len(sk_off), i - violin_dx) + rng_off, sk_off,
               s=4, color=OFF_EDGE, alpha=0.6, linewidths=0, zorder=4)
    rng_on = np.random.normal(0, 0.05, len(sk_on))
    ax.scatter(np.full(len(sk_on), i + violin_dx) + rng_on, sk_on,
               s=4, color=ON_EDGE, alpha=0.6, linewidths=0, zorder=4)

# Naive baseline reference at y=0
ax.axhline(0, color="#d62728", linewidth=0.9,
           linestyle=(0, (5, 3)), zorder=1)
ax.text(len(MODEL_ORDER) - 0.55, 0.012, "naive baseline",
        fontsize=6.5, color="#d62728", va="bottom", ha="right",
        fontweight="bold")

ax.set_xticks(xs)
ax.set_xticklabels([SHORT[m] for m in MODEL_ORDER], fontsize=7)
ax.set_xlim(-0.6, len(MODEL_ORDER) - 0.4)

ax.set_ylabel("Cell margin: score $-$ naive baseline", fontsize=8)
ax.set_ylim(-0.45, 0.13)
ax.set_yticks([-0.4, -0.3, -0.2, -0.1, 0.0, 0.1])
ax.tick_params(axis="y", labelsize=6.5, length=2.5)
ax.grid(True, axis="y", alpha=0.18, linewidth=0.5)
ax.set_axisbelow(True)

for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_linewidth(0.5)
ax.spines["bottom"].set_linewidth(0.5)

legend_handles = [
    Patch(facecolor=OFF_COLOR, edgecolor=OFF_EDGE,
          label="SK-off (C0, C1, C2, C4)"),
    Patch(facecolor=ON_COLOR,  edgecolor=ON_EDGE,
          label="SK-on  (C3, C5, C6, C7)"),
]
ax.legend(handles=legend_handles, loc="lower left", fontsize=6.8,
          frameon=False, handlelength=1.2, handletextpad=0.4)

plt.subplots_adjust(left=0.08, right=0.985, top=0.96, bottom=0.13)
out_pdf = os.path.join(os.path.dirname(__file__), "../F_naive_summary.pdf")
fig.savefig(out_pdf)
fig.savefig(out_pdf.replace(".pdf", ".png"), dpi=300)
print(f"wrote {out_pdf}")

# Print summary statistics for inspection
print("\nPer-model SK-off vs SK-on margin summary:")
for m in MODEL_ORDER:
    sub = df[df.model == m]
    off = sub[~sub.sk_on]["margin"].values
    on  = sub[ sub.sk_on]["margin"].values
    print(f"  {m:25s} off med={np.median(off):+.3f} ({(off > 0).sum()}/20 above)"
          f"   on med={np.median(on):+.3f} ({(on > 0).sum()}/20 above)")
