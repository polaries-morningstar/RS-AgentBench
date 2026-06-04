"""F7 — SK main-effect forest plot, redesigned for the appendix.

35 rows = 5 task groups × 7 models (in total-parameter order).
Per row: per-(model, task) SK main effect = mean F1 | SK=1 minus
mean F1 | SK=0, with scene-level paired-bootstrap 95% CI from
sk_forest.csv.

Key design choices:
  - Grouped by TASK (not model). The reader's question reading
    Appendix E is "where does SK matter," and task-grouping
    surfaces that pattern directly (water + change show large
    positive effects on most backbones; burn shows near-zero
    effects; T5 query is mid).
  - Filled circles = CI excludes zero (significant); hollow =
    CI spans zero. No colour gradient — significance/no is the
    primary axis.
  - 8B uses a square marker to flag the determinism-derived CI
    (SK-on outputs are pixel-identical, §5.4 short-circuit).
  - Task sub-headers bold, narrow gap between tasks for visual
    grouping.

Span: single column (~3.4 in wide), ~5.0 in tall on ACM sigconf.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER, TASK_ORDER, TASK_LABELS

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

setup()

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/sk_forest.csv"))

# Order: by TASK_ORDER (outer), MODEL_ORDER (inner) — this groups
# all 7 models within each task panel, then moves to next task.
df["t_idx"] = df["task"].map({t: i for i, t in enumerate(TASK_ORDER)})
df["m_idx"] = df["model"].map({m: i for i, m in enumerate(MODEL_ORDER)})
df = df.sort_values(["t_idx", "m_idx"]).reset_index(drop=True)

# Short model labels for y-tick
MODEL_SHORT = {
    "qwen3-8b":           "qwen3-8b",
    "qwen3-14b":          "qwen3-14b",
    "qwen3.6-27b":        "qwen3.6-27b",
    "qwen3.6-35b-a3b":    "qwen3.6-35b-a3b",
    "deepseek-v4-flash":  "deepseek-v4-flash",
    "kimi-k2.6":          "kimi-k2.6",
    "deepseek-v4-pro":    "deepseek-v4-pro",
}

# Compute y positions with task gaps
TASK_GAP = 0.8  # extra vertical spacing between task groups
y_pos = []
task_dividers = []  # y positions where horizontal dividers between tasks go
task_label_y = []   # y position of each task header
cur_y = 0.0
prev_task = None
for i, r in df.iterrows():
    if prev_task is not None and r["task"] != prev_task:
        task_dividers.append(cur_y + 0.5)
        cur_y += TASK_GAP
    y_pos.append(cur_y)
    prev_task = r["task"]
    cur_y += 1.0
y_pos = np.array(y_pos)
n_total_h = cur_y

# Compute task-group y midpoints for the sub-header annotations
task_mid_y = {}
for t in TASK_ORDER:
    idx = df.index[df["task"] == t].tolist()
    if not idx:
        continue
    task_mid_y[t] = (y_pos[idx[0]] + y_pos[idx[-1]]) / 2.0

# ---------- Plot ----------
fig, ax = plt.subplots(figsize=(3.4, 5.1))
ax.invert_yaxis()

# Vertical zero reference (very subtle)
ax.axvline(0, color="#999", linewidth=0.6, linestyle=(0, (2, 2)), zorder=1)

# Soft alternating task-band backgrounds for visual grouping
for i, t in enumerate(TASK_ORDER):
    if t not in task_mid_y:
        continue
    idx = df.index[df["task"] == t].tolist()
    y_top = y_pos[idx[0]] - 0.5
    y_bot = y_pos[idx[-1]] + 0.5
    if i % 2 == 0:
        ax.axhspan(y_top, y_bot, color="#f5f7f8", zorder=0)

# Plot each row
PRIMARY = "#264653"   # deep teal
HOLLOW_EDGE = "#5e6b73"
DET_8B = "#E76F51"    # coral for 8B determinism flag

for i, r in df.iterrows():
    sig = (r["ci_low"] > 0) or (r["ci_high"] < 0)
    is_8b = r["model"] == "qwen3-8b"
    marker = "s" if is_8b else "o"
    base_color = DET_8B if is_8b else PRIMARY
    yi = y_pos[i]
    ax.errorbar(
        r["sk_effect"], yi,
        xerr=[[r["sk_effect"] - r["ci_low"]],
              [r["ci_high"] - r["sk_effect"]]],
        fmt=marker,
        markersize=4.2 if not is_8b else 4.6,
        color=base_color,
        markerfacecolor=base_color if sig else "white",
        markeredgecolor=base_color, markeredgewidth=0.9,
        capsize=1.6, elinewidth=0.7, capthick=0.5, zorder=3,
    )

# Y-tick labels: model names
ax.set_yticks(y_pos)
ax.set_yticklabels([MODEL_SHORT[r["model"]] for _, r in df.iterrows()],
                   fontsize=6.0)
ax.tick_params(axis="y", length=0, pad=2)

# Task-group sub-headers on the right side
for t, ymid in task_mid_y.items():
    label = TASK_LABELS[t]
    ax.text(1.02, ymid, label,
            transform=ax.get_yaxis_transform(),
            fontsize=7.5, fontweight="bold", color="#264653",
            ha="left", va="center", clip_on=False,
            rotation=90)

# Task dividers (subtle)
for yd in task_dividers:
    ax.axhline(yd, color="#d6d8db", linewidth=0.4, zorder=0)

# X-axis
ax.set_xlabel("SK main effect (per-task primary metric)",
              fontsize=7.5, labelpad=2)
ax.set_xlim(-0.08, 0.30)
ax.set_xticks([-0.05, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
ax.tick_params(axis="x", labelsize=6.5, length=2.5)

# Hide top/right spines, thin remaining
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_linewidth(0.4)
ax.spines["bottom"].set_linewidth(0.4)

ax.set_ylim(n_total_h - 0.5, -0.5)
ax.grid(False)

# Legend
from matplotlib.lines import Line2D
legend_handles = [
    Line2D([0], [0], marker="o", color=PRIMARY,
           markerfacecolor=PRIMARY, markersize=4.2,
           linestyle="", label="CI excludes 0"),
    Line2D([0], [0], marker="o", color=PRIMARY,
           markerfacecolor="white", markeredgewidth=0.9,
           markersize=4.2, linestyle="", label="CI spans 0"),
    Line2D([0], [0], marker="s", color=DET_8B,
           markerfacecolor=DET_8B, markersize=4.6,
           linestyle="",
           label="qwen3-8b (deterministic SK)"),
]
ax.legend(handles=legend_handles,
          loc="upper center", bbox_to_anchor=(0.5, -0.06),
          ncol=3, fontsize=5.6, frameon=False,
          handlelength=1.0, handletextpad=0.3, columnspacing=0.7)

plt.subplots_adjust(left=0.28, right=0.86, top=0.985, bottom=0.10)
out_pdf = os.path.join(os.path.dirname(__file__), "../F7_sk_forest.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")

# Print summary stats
print("\n=== Forest plot summary ===")
for t in TASK_ORDER:
    sub = df[df["task"] == t]
    sig_count = sum(1 for _, r in sub.iterrows()
                    if (r["ci_low"] > 0) or (r["ci_high"] < 0))
    print(f"  {t}: {sig_count}/{len(sub)} models with CI excluding 0")
