"""F9 — Pairwise-contrast forest (3 panels horizontal).

Three side-by-side forest panels (post C6/C7 swap; C7 is full stack):
  (a)  Δ(C3 − C0)   — SK alone vs bare
  (b)  Δ(C5 − C3)   — KB-on-top-of-SK (the 14B transition signature)
  (c)  Δ(C7 − C3)   — adding both KB+WS on top of SK (full stack lever)

Each panel: y = 30 rows (6 models × 5 tasks), x = paired-bootstrap Δ with
95% CI. Models grouped by horizontal separator. The visual punch:
panel (b) is where the 14B story lives — 14B rows have CIs that exclude
zero positive (KB does add value on top of SK), while 8B is ~zero and
upper-panel is ~zero (saturated).

Span: full-width (~7 in), ~5.0 in tall.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_COLORS, MODEL_ORDER, TASK_ORDER, TASK_LABELS

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

setup()

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/pairwise_contrasts.csv"))

# Order rows
df["m_idx"] = df["model"].map({m: i for i, m in enumerate(MODEL_ORDER)})
df["t_idx"] = df["task"].map({t: i for i, t in enumerate(TASK_ORDER)})

PANELS = [
    ("C3_vs_C0", r"$\Delta(C_3 - C_0)$  SK alone",        (-0.10, 0.75)),
    ("C5_vs_C3", r"$\Delta(C_5 - C_3)$  KB+SK vs SK",     (-0.20, 0.20)),
    ("C7_vs_C3", r"$\Delta(C_7 - C_3)$  full vs SK",      (-0.20, 0.20)),
]
n_rows = len(MODEL_ORDER) * len(TASK_ORDER)  # 30

fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True,
                          gridspec_kw={"wspace": 0.15})

for ax_idx, (cname, ctitle, xlims) in enumerate(PANELS):
    ax = axes[ax_idx]
    sub = df[df["contrast"] == cname].sort_values(["m_idx", "t_idx"]).reset_index(drop=True)
    if len(sub) == 0:
        ax.set_title(f"{ctitle}\n(no data)", fontsize=8)
        continue

    # Plot each row
    ax.axvline(0, color="#bbb", linewidth=0.6, linestyle=":", zorder=1)
    for i, r in sub.iterrows():
        color = MODEL_COLORS[r["model"]]
        sig = (r["ci_low"] > 0) or (r["ci_high"] < 0)
        ax.errorbar(
            r["delta"], i,
            xerr=[[r["delta"] - r["ci_low"]], [r["ci_high"] - r["delta"]]],
            fmt="o", color=color, markersize=4.5,
            markerfacecolor=color if sig else "white",
            markeredgecolor=color, markeredgewidth=1.0,
            capsize=2.0, elinewidth=0.9, capthick=0.6, zorder=3,
        )

    # Model group dividers
    for j, m in enumerate(MODEL_ORDER):
        m_rows = sub[sub["model"] == m]
        if len(m_rows) == 0: continue
        idx_arr = np.array(m_rows.index)
        if j < len(MODEL_ORDER) - 1:
            ax.axhline(int(idx_arr.max()) + 0.5, color="#ccc",
                       linewidth=0.5, zorder=0)

    ax.set_xlim(*xlims)
    ax.set_ylim(n_rows - 0.5, -0.5)
    ax.set_title(ctitle, fontsize=8.5, pad=4)
    ax.tick_params(axis="x", labelsize=7)

    if ax_idx == 0:
        # Left axis: per-row inline labels "model · task", model coloured
        ax.set_yticks(range(n_rows))
        labels = []
        for i_row in range(n_rows):
            m = MODEL_ORDER[i_row // len(TASK_ORDER)]
            t = TASK_ORDER[i_row % len(TASK_ORDER)]
            labels.append(t.capitalize() if t != "query" else "Compositional")
        ax.set_yticklabels(labels, fontsize=6.5)
        # Model name labels — placed far-left (outside tick labels)
        for j, m in enumerate(MODEL_ORDER):
            m_rows = sub[sub["model"] == m]
            if len(m_rows) == 0: continue
            idx_arr = np.array(m_rows.index)
            y_mid = float(idx_arr.mean())
            ax.text(-0.55, y_mid, m, fontsize=7.0,
                    color=MODEL_COLORS[m], fontweight="bold",
                    ha="right", va="center",
                    transform=ax.get_yaxis_transform(), clip_on=False)
    else:
        # sharey=True: do NOT overwrite yticklabels, just hide tick labels on this axis
        ax.tick_params(axis="y", labelleft=False, length=0)

# X-label across all panels
fig.text(0.5, 0.02, r"$\Delta$ F1 (paired bootstrap, 95% CI)",
         ha="center", fontsize=8)

# Significance legend (top-right of last panel)
from matplotlib.lines import Line2D
legend_handles = [
    Line2D([0], [0], marker="o", color="#444", markerfacecolor="#444",
           markersize=4.5, linestyle="", label="CI excludes 0"),
    Line2D([0], [0], marker="o", color="#444", markerfacecolor="white",
           markeredgewidth=1.0, markersize=4.5, linestyle="",
           label="CI straddles 0"),
]
axes[2].legend(handles=legend_handles, loc="lower right", fontsize=6.0,
               frameon=False, handlelength=1.0)

# Annotate the 14B story on panel (b)
axes[1].annotate(
    "14B: KB+SK >\nSK alone\n(transition\nregime signature)",
    xy=(0.08, 5), xycoords=("data", "data"),
    xytext=(0.13, 8), textcoords=("data", "data"),
    fontsize=6.2, color=MODEL_COLORS["qwen3-14b"], fontweight="bold",
    ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color=MODEL_COLORS["qwen3-14b"],
                    lw=0.7, alpha=0.7),
)

plt.subplots_adjust(left=0.22, right=0.98, top=0.94, bottom=0.07)
out_pdf = os.path.join(os.path.dirname(__file__), "../F9_pairwise_forest.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")
