"""F11 — Skill-invocation rate per (model, cfg).

Visualises the 14B Transition mechanism (the paper's CENTRAL mechanistic
finding): qwen3-14b is the unique upper-panel point where Skill invocation
rate is cfg-sensitive (14.8 → 57.6 / 28.8 / 59.2%), while every other
model invokes Skill near-deterministically (≥98%) across all 4 SK-on cfgs.

Output:
  figs/F11_skill_rate.pdf
  figs/F11_skill_rate.png
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import setup, MODEL_COLORS, MODEL_ORDER, MODEL_SHORT

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

setup()

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = Path(__file__).resolve().parent.parent

df = pd.read_csv(DATA / "skill_invocation_rate.csv")
SK_CFGS = ["C3", "C5", "C6", "C7"]

# Pivot to model x cfg matrix
pivot = df.pivot(index="model", columns="cfg", values="skill_rate")
pivot = pivot.loc[MODEL_ORDER, SK_CFGS] * 100  # to percent

fig, ax = plt.subplots(figsize=(4.5, 2.7))

n_models = len(MODEL_ORDER)
n_cfgs = len(SK_CFGS)
group_width = 0.78
bar_width = group_width / n_models

x = np.arange(n_cfgs)
for i, model in enumerate(MODEL_ORDER):
    color = MODEL_COLORS[model]
    offset = (i - n_models / 2 + 0.5) * bar_width
    values = pivot.loc[model].values
    bars = ax.bar(
        x + offset, values, bar_width * 0.9, color=color,
        edgecolor="white", linewidth=0.3,
        label=MODEL_SHORT.get(model, model),
        zorder=3,
    )

# Annotate the qwen3-14b bars specifically (the load-bearing finding)
for j, cfg in enumerate(SK_CFGS):
    val = pivot.loc["qwen3-14b", cfg]
    # find bar position
    i = MODEL_ORDER.index("qwen3-14b")
    offset = (i - n_models / 2 + 0.5) * bar_width
    ax.text(
        j + offset, val + 3, f"{val:.0f}%",
        ha="center", va="bottom", fontsize=6.5,
        color=MODEL_COLORS["qwen3-14b"], fontweight="bold",
    )

# Reference line at 98% (the saturation threshold)
ax.axhline(98, color="#888", linestyle=":", linewidth=0.7, alpha=0.7, zorder=2)
ax.text(
    -0.4, 98.5, "98% saturation threshold", fontsize=6, color="#666",
    va="bottom", ha="left", style="italic",
)

ax.set_xticks(x)
ax.set_xticklabels(SK_CFGS, fontsize=8)
ax.set_xlabel("Configuration (SK-enabled cells only)", fontsize=8.5)
ax.set_ylabel("Skill-invocation rate (%)", fontsize=8.5)
ax.set_ylim(0, 108)
ax.set_xlim(-0.5, len(SK_CFGS) - 0.5)
ax.legend(
    loc="lower center", bbox_to_anchor=(0.5, -0.42),
    ncol=4, fontsize=6.5, columnspacing=0.8, handlelength=0.8,
)

# Mechanism callout for qwen3-14b
ax.annotate(
    "qwen3-14b: only Transition-class\nbackbone (KB exposure triggers SK)",
    xy=(1.0 + (MODEL_ORDER.index("qwen3-14b") - n_models / 2 + 0.5) * bar_width, 57.6),
    xytext=(1.6, 75),
    fontsize=6.5, color=MODEL_COLORS["qwen3-14b"],
    arrowprops=dict(arrowstyle="->", color=MODEL_COLORS["qwen3-14b"], lw=0.6),
    ha="left", va="center",
)

fig.tight_layout()
fig.savefig(OUT / "F11_skill_rate.pdf")
fig.savefig(OUT / "F11_skill_rate.png", dpi=300)
print(f"wrote {OUT}/F11_skill_rate.pdf")
print(f"wrote {OUT}/F11_skill_rate.png")
