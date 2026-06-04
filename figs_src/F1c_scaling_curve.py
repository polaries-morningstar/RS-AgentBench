"""F1c — Scaling-curve teaser (Figure 1, 7-model panel).

New design: each model plots TWO points connected by a thin line:
  ○ hollow  = Δ(C3 − C0)  (SK alone)
  ● filled  = Δ(C5 − C0)  (KB + SK)

The gap between the two points = the "KB-on-top-of-SK lever".
  - 8B:           both points high, near-coincident (SK saturates everything)
  - 14B:          two points spread (SK gives +0.024, KB+SK gives +0.076)
                  → transition regime
  - 27B → 1T:     both points compressed near zero (saturated)

This visualises the THREE-regime structure (decisive / transition / saturated).
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_COLORS, MODEL_ORDER

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

setup()

# ---------------------------------------------------------------------------
# Load trial-level data and compute paired bootstrap CIs for Δ(C3-C0) and Δ(C5-C0).
# Sample-paired resample: for each model, draw (task, sample) clusters with
# replacement, average each (cfg) within drawn cluster, compute Δ, then average
# across 5 tasks.
# ---------------------------------------------------------------------------
df = pd.read_parquet(os.path.join(os.path.dirname(__file__), "../data/all_trials.parquet"))

# Per (model, task, sample) mean F1 for each cfg
cell = df.groupby(["model", "task", "sample", "cfg"])["f1"].mean().reset_index()
# Wide on cfg
wide = cell.pivot_table(index=["model", "task", "sample"], columns="cfg", values="f1").reset_index()

rng = np.random.default_rng(42)

def delta_with_ci(model: str, cfg_a: str, cfg_b: str, n_boot: int = 1000):
    """Panel-mean Δ = mean across 5 tasks of [mean over samples (cfg_a - cfg_b)]."""
    sub = wide[wide["model"] == model]
    pts = []
    for task, t_sub in sub.groupby("task"):
        diffs = (t_sub[cfg_a] - t_sub[cfg_b]).dropna().values
        if len(diffs) == 0: continue
        pts.append((task, diffs))
    if not pts: return float("nan"), float("nan"), float("nan")
    # Panel-mean of per-task means
    point = float(np.mean([d.mean() for _, d in pts]))
    boots = np.zeros(n_boot)
    for b in range(n_boot):
        per_task = []
        for _, d in pts:
            samp = rng.choice(d, size=len(d), replace=True)
            per_task.append(samp.mean())
        boots[b] = np.mean(per_task)
    lo, hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))
    return point, lo, hi


# Model size from scaling_curve.csv (active_B / total_B)
sc = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/scaling_curve.csv"))
size_map = sc[["model", "active_B", "total_B"]].drop_duplicates().set_index("model").to_dict("index")

rows = []
for m in MODEL_ORDER:
    d3, l3, h3 = delta_with_ci(m, "C3", "C0")
    d5, l5, h5 = delta_with_ci(m, "C5", "C0")
    rows.append({
        "model": m,
        "total_B": size_map[m]["total_B"],
        "active_B": size_map[m]["active_B"],
        "d_c3_c0": d3, "l_c3_c0": l3, "h_c3_c0": h3,
        "d_c5_c0": d5, "l_c5_c0": l5, "h_c5_c0": h5,
    })
PTS = pd.DataFrame(rows)
print(PTS.to_string(index=False))

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.5, 2.75))

# Zero reference line
ax.axhline(0, color="#bbb", linewidth=0.6, linestyle=":", zorder=1)

# Saturated-regime shading (27B and up) — labels pinned at the bottom edge
ax.axvspan(25, 3000, color="#f4f4f4", zorder=0)
ax.text(1700, -0.105, "saturated regime", fontsize=7, color="#666",
        ha="right", va="bottom", style="italic", fontweight="bold")

# 8B decisive regime shading
ax.axvspan(5, 11, color="#fff0e6", alpha=0.7, zorder=0)
ax.text(8, -0.105, "decisive", fontsize=7, color="#c66",
        ha="center", va="bottom", style="italic", fontweight="bold")

# 14B (transition) shading
ax.axvspan(11, 25, color="#f0e6e6", alpha=0.6, zorder=0)
ax.text(17, -0.105, "transition", fontsize=7, color="#964",
        ha="center", va="bottom", style="italic", fontweight="bold")

# Connecting line + dual points per model
for _, r in PTS.iterrows():
    color = MODEL_COLORS[r["model"]]
    x = r["total_B"]
    # Connecting segment (light)
    ax.plot([x, x], [r["d_c3_c0"], r["d_c5_c0"]],
            color=color, linewidth=1.3, alpha=0.55, zorder=2,
            solid_capstyle="round")
    # ΔC3-C0 — hollow circle (SK alone)
    ax.errorbar(x, r["d_c3_c0"],
                yerr=[[r["d_c3_c0"] - r["l_c3_c0"]], [r["h_c3_c0"] - r["d_c3_c0"]]],
                fmt="o", color=color, markersize=6.5,
                markerfacecolor="white", markeredgecolor=color, markeredgewidth=1.3,
                capsize=2.0, elinewidth=0.8, capthick=0.7, zorder=3)
    # ΔC5-C0 — filled diamond (KB+SK)
    ax.errorbar(x, r["d_c5_c0"],
                yerr=[[r["d_c5_c0"] - r["l_c5_c0"]], [r["h_c5_c0"] - r["d_c5_c0"]]],
                fmt="D", color=color, markersize=5.5,
                markerfacecolor=color, markeredgecolor="white", markeredgewidth=0.6,
                capsize=2.0, elinewidth=0.8, capthick=0.7, zorder=4)

# Per-point labels (alternating above/below to dodge collision)
# Compute the max(point) per model for label placement
LABEL_OFFSETS = {
    "qwen3-8b":          (10, -3, "left", "anchor_high"),
    "qwen3-14b":         (10, 4, "left", "anchor_high"),
    # 27B and 35B-a3b are adjacent in x: 27b ABOVE (left), 35b-a3b ABOVE (right)
    "qwen3.6-27b":       (-2, 14, "right", "anchor_high"),
    "qwen3.6-35b-a3b":   (2, 22, "left", "anchor_high"),
    # 284B v4-flash isolated → label right
    "deepseek-v4-flash": (10, 4, "left", "anchor_high"),
    # 1000B kimi and 1600B v4-pro adjacent → kimi ABOVE-LEFT, v4-pro BELOW-RIGHT
    "kimi-k2.6":         (-2, 14, "right", "anchor_high"),
    "deepseek-v4-pro":   (4, -12, "left", "anchor_low"),
}
for _, r in PTS.iterrows():
    dx, dy, ha, anchor = LABEL_OFFSETS[r["model"]]
    color = MODEL_COLORS[r["model"]]
    if anchor == "anchor_high":
        anchor_y = max(r["d_c3_c0"], r["d_c5_c0"])
    else:
        anchor_y = min(r["d_c3_c0"], r["d_c5_c0"])
    ax.annotate(r["model"],
                xy=(r["total_B"], anchor_y),
                xytext=(dx, dy), textcoords="offset points",
                fontsize=6.5, color=color, ha=ha, fontweight="bold")

# Legend (custom)
from matplotlib.lines import Line2D
legend_handles = [
    Line2D([0], [0], marker="o", color="#444", markerfacecolor="white",
           markeredgewidth=1.3, markersize=6.5, linestyle="",
           label=r"$\Delta_{C_3 - C_0}$  (SK alone)"),
    Line2D([0], [0], marker="D", color="#444", markerfacecolor="#444",
           markersize=5.5, linestyle="", label=r"$\Delta_{C_5 - C_0}$  (KB+SK)"),
]
ax.legend(handles=legend_handles, loc="upper right", bbox_to_anchor=(1.0, 1.0),
          fontsize=6.3, frameon=False, handlelength=1.0, labelspacing=0.3)

ax.set_xscale("log")
ax.set_xlim(5, 3000)
ax.set_xlabel("Total parameters (B, log)", fontsize=8.5)
ax.set_ylabel(r"Panel-mean $\Delta\,$F1 over $C_0$", fontsize=8.5)
ax.set_title("SK channel premium, with the KB-on-top-of-SK lever", fontsize=9, pad=6)
ax.set_ylim(-0.12, 0.36)

ax.set_xticks([8, 14, 30, 100, 300, 1000])
ax.set_xticklabels(["8", "14", "30", "100", "300", "1000"], fontsize=7.5)
ax.tick_params(axis="y", labelsize=7.5)

plt.tight_layout()
out_pdf = os.path.join(os.path.dirname(__file__), "../F1c_scaling_curve.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")
