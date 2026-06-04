"""F10 — deepseek-v4 family contrast (pro 49B/1.6T vs flash 13B/284B).

Visualises the §5.2 finding: pro and flash sit within ±0.04 F1 of each
other on every configuration despite pro being a much larger model
(49B active / 1.6T total vs 13B active / 284B total). Pro is slightly
ABOVE flash on the open-ended channels (C0/C1/C4) and slightly BELOW on
the SK-on channels (C3/C5/C7). Panel-mean Δ ≈ +0.003. Reading: at the
largest scales in the panel, both regime axes are flat — Saturated.

Output:
  figs/F10_v4_family.pdf
  figs/F10_v4_family.png
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _style import setup, MODEL_COLORS, CFG_ORDER, CFG_SHORT

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

setup()

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = Path(__file__).resolve().parent.parent
TASKS = ["water", "change", "landcover", "burn", "query"]

cm = pd.read_csv(DATA / "cell_means.csv")
v4 = cm[cm["model"].isin(["deepseek-v4-flash", "deepseek-v4-pro"])].copy()

# Panel-mean per (model, cfg): average across 5 tasks
panel = v4.groupby(["model", "cfg"])["mean"].mean().unstack(level="model")
panel = panel.loc[CFG_ORDER]   # ensure x-axis ordering C0..C7

flash_color = MODEL_COLORS["deepseek-v4-flash"]
pro_color   = MODEL_COLORS["deepseek-v4-pro"]

fig, ax = plt.subplots(figsize=(3.4, 2.6))

x = np.arange(len(CFG_ORDER))
flash = panel["deepseek-v4-flash"].values
pro   = panel["deepseek-v4-pro"].values

# Slope segments — one per cfg, flash above pro (always negative slope)
for xi, (f, p) in enumerate(zip(flash, pro)):
    ax.plot([xi, xi], [f, p], color="#888", linewidth=0.7, alpha=0.5, zorder=2)

# Markers + connecting lines per model
ax.plot(x, flash, marker="o", markersize=6, linewidth=1.4,
        color=flash_color, label="deepseek-v4-flash (13B/284B)",
        markerfacecolor=flash_color, markeredgecolor="white",
        markeredgewidth=0.7, zorder=4)
ax.plot(x, pro, marker="s", markersize=6, linewidth=1.4,
        color=pro_color, label="deepseek-v4-pro (49B/1.6T)",
        markerfacecolor=pro_color, markeredgecolor="white",
        markeredgewidth=0.7, zorder=4)

# Annotate each Δ to the right of segment, only when |Δ|≥0.005 to reduce clutter
for xi, (f, p) in enumerate(zip(flash, pro)):
    delta = p - f
    if abs(delta) < 0.005:
        continue
    midy = (f + p) / 2
    ax.text(xi + 0.16, midy, f"{delta:+.02f}", fontsize=6.0,
            color="#666", va="center", ha="left")

ax.set_xticks(x)
ax.set_xticklabels([CFG_SHORT[c] for c in CFG_ORDER], fontsize=8)
ax.set_xlabel("Configuration (KB×WS×SK factorial)", fontsize=8.5)
ax.set_ylabel("Panel-mean F1 (avg across 5 tasks)", fontsize=8.5)
# Tight y-axis: data spans 0.425-0.460, give a little headroom for annotations
ax.set_ylim(0.41, 0.47)
ax.set_xlim(-0.4, len(CFG_ORDER) - 0.4)
ax.legend(loc="lower right", fontsize=7)

# Annotate the cfg-level pattern
ax.text(0.02, 0.97,
        "Pro > Flash on open-ended channels (C0/C1/C4)\n"
        "Pro < Flash on SK-on channels (C3/C5/C7)\n"
        "Panel-mean Δ = +0.003 F1; both Saturated",
        transform=ax.transAxes, fontsize=6.5, color="#444",
        va="top", ha="left", fontstyle="italic")

fig.tight_layout()
fig.savefig(OUT / "F10_v4_family.pdf")
fig.savefig(OUT / "F10_v4_family.png", dpi=300)
print(f"wrote {OUT}/F10_v4_family.pdf")
print(f"wrote {OUT}/F10_v4_family.png")
print(f"\nPer-cfg deltas (pro - flash):")
for cfg in CFG_ORDER:
    f = panel.loc[cfg, "deepseek-v4-flash"]
    p = panel.loc[cfg, "deepseek-v4-pro"]
    print(f"  {cfg}: flash={f:.3f}  pro={p:.3f}  Δ={p-f:+.3f}")
