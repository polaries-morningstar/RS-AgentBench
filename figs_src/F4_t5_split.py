"""F4 split — three single-column T5 figures.

Splits the former 3-panel F4_t5_deepdive into independent single-column
figures so they can float to different positions:
  F4a_t5_bar.pdf       — bare C0 vs SK-only C3 per model, with UB line
  F4b_t5_failure.pdf   — error decomposition by failure type per cfg
  F4c_t5_perquery.pdf  — per-query F1 box plot

Span: single-column (~3.4 in) each.
"""
from __future__ import annotations
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER, CFG_ORDER

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

setup()

BENCH = "/Users/polaries/Work/AutoSpec/benchmark"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..")

df = pd.read_parquet(os.path.join(DATA_DIR, "all_trials.parquet"))
t5 = df[(df.task == "query") & df.submitted & df.primary_metric.notna()].copy()


# ============================================================
# (a) Per-model T5 conditions — vertical grouped bars.
#
# Three conditions per model:
#   • bare control C0      (gray)
#   • skill-only C3        (blue)
#   • best across 8 cfgs   (teal) — winning cfg annotated above
#
# Two-line full-name x-tick labels avoid abbreviations like
# "ds-v4-fl" or "q3.6"; vendor goes on line 1 and tier on line 2.
# The horizontal dashed line marks the spectral upper bound 0.19.
# ============================================================
fig_a, ax_a = plt.subplots(figsize=(3.4, 2.55))
agg = t5.groupby(["model", "cfg"])["primary_metric"].mean().unstack()
agg = agg.loc[MODEL_ORDER]

best_cfg = agg.idxmax(axis=1)
best_val = agg.max(axis=1)

x = np.arange(len(MODEL_ORDER))
w = 0.27

C0_COLOR = "#cfd8dc"
C3_COLOR = "#0072B2"
BEST_COLOR = "#2A9D8F"

ax_a.bar(x - w, agg["C0"], w, label=r"bare $C_0$",
         color=C0_COLOR, edgecolor="#444", linewidth=0.4)
ax_a.bar(x,     agg["C3"], w, label=r"skill-only $C_3$",
         color=C3_COLOR, edgecolor="#003c5a", linewidth=0.4)
ax_a.bar(x + w, best_val, w, label="best of all eight",
         color=BEST_COLOR, edgecolor="#1a3d3a", linewidth=0.4)

# Annotate winning cfg above the teal bar
for i, m in enumerate(MODEL_ORDER):
    ax_a.text(i + w, best_val[m] + 0.006, best_cfg[m],
              ha="center", va="bottom", fontsize=5.7,
              color="#1a3d3a", fontweight="bold")

# UB reference line
ax_a.axhline(0.19, color="#d62728", linewidth=0.9,
             linestyle=(0, (4, 2.5)), zorder=1)
ax_a.text(0.05, 0.193, "UB 0.19",
          fontsize=6.3, color="#d62728", fontweight="bold",
          va="bottom", ha="left")

# Two-line full-name labels: line 1 = vendor, line 2 = tier
LABELS = [
    "qwen3\n8b",
    "qwen3\n14b",
    "qwen3.6\n27b",
    "qwen3.6\n35b-a3b",
    "deepseek\nv4-flash",
    "deepseek\nv4-pro",
    "kimi\nk2.6",
]
ax_a.set_xticks(x)
ax_a.set_xticklabels(LABELS, fontsize=6.0)
ax_a.set_ylabel("F1", fontsize=8, labelpad=2)
ax_a.set_ylim(0, 0.30)
ax_a.set_yticks([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
ax_a.tick_params(axis="y", labelsize=6.3, length=2.5)
ax_a.tick_params(axis="x", length=0, pad=2)
for s in ("top", "right"):
    ax_a.spines[s].set_visible(False)
ax_a.spines["left"].set_linewidth(0.4)
ax_a.spines["bottom"].set_linewidth(0.4)
ax_a.grid(True, axis="y", alpha=0.15, linewidth=0.4)
ax_a.set_axisbelow(True)

ax_a.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16),
            ncol=3, fontsize=6.2, frameon=False,
            handlelength=1.2, columnspacing=0.8, handletextpad=0.4)

plt.subplots_adjust(left=0.12, right=0.97, top=0.97, bottom=0.27)
out_a = os.path.join(OUT_DIR, "F4a_t5_bar.pdf")
fig_a.savefig(out_a)
fig_a.savefig(out_a.replace(".pdf", ".png"), dpi=300)
print(f"wrote {out_a}")
print("\n=== Per-model T5 best cfg ===")
for m in MODEL_ORDER:
    print(f"  {m:<22}  C0={agg.loc[m,'C0']:.3f}  "
          f"C3={agg.loc[m,'C3']:.3f}  "
          f"best={best_val[m]:.3f} @ {best_cfg[m]}")


# ============================================================
# (b) Error decomposition stacked bar per cfg
# ============================================================
def classify_failure(metrics_path: str):
    log_path = metrics_path.replace("metrics.json", "agent_log.json")
    try:
        m = json.load(open(metrics_path))
    except Exception:
        return None
    if m.get("submitted"):
        prim = (m.get("metrics") or {}).get("primary_metric") or 0
        if prim >= 0.10: return None
        try:
            with open(log_path) as f: txt = f.read(80_000).lower()
        except Exception: txt = ""
        if "buffer" in txt or "distance_transform" in txt:
            return "wrong target class"
        return "wrong reference class"
    return "wrong operator"

CATS = ["wrong target class", "wrong reference class", "wrong operator"]
CAT_COLORS = {"wrong target class": "#D55E00",
              "wrong reference class": "#E69F00",
              "wrong operator":        "#0072B2"}
counts = {c: {cat: 0 for cat in CATS} for c in CFG_ORDER}
for f in glob.glob(f"{BENCH}/archive.E1.*/results/query_*/*/metrics.json"):
    bn = f.split("/results/")[1].split("/")[0]
    parts = bn.split("_")
    cfg = parts[1] if len(parts) >= 2 else None
    if cfg not in CFG_ORDER: continue
    cat = classify_failure(f)
    if cat: counts[cfg][cat] += 1

fig_b, ax_b = plt.subplots(figsize=(3.4, 2.3))
bottoms = np.zeros(len(CFG_ORDER))
for cat in CATS:
    values = np.array([counts[c][cat] for c in CFG_ORDER])
    ax_b.bar(CFG_ORDER, values, bottom=bottoms, color=CAT_COLORS[cat],
             label=cat, edgecolor="white", linewidth=0.4, width=0.72)
    bottoms += values

ax_b.set_xticklabels(CFG_ORDER, fontsize=7.5)
ax_b.set_ylabel("# failed T5 trials", fontsize=8)
ax_b.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18),
            ncol=1, fontsize=6.3, frameon=False,
            handlelength=1.2, handletextpad=0.4, labelspacing=0.2)

plt.subplots_adjust(left=0.16, right=0.97, top=0.96, bottom=0.36)
out_b = os.path.join(OUT_DIR, "F4b_t5_failure.pdf")
fig_b.savefig(out_b)
fig_b.savefig(out_b.replace(".pdf", ".png"), dpi=300)
print(f"wrote {out_b}")


# ============================================================
# (c) Per-query F1 distribution box plot
# ============================================================
fig_c, ax_c = plt.subplots(figsize=(3.4, 2.3))
queries = sorted(t5["sample"].unique())
data_by_q = [t5[t5["sample"] == q]["primary_metric"].values for q in queries]
short_q = [q.replace("__t5", "").split("_")[0] for q in queries]

bp = ax_c.boxplot(data_by_q, vert=True, widths=0.55, patch_artist=True,
                  showfliers=False,
                  medianprops={"color": "black", "linewidth": 0.9})
for patch in bp["boxes"]:
    patch.set_facecolor("#cfd8dc")
    patch.set_edgecolor("#333")
    patch.set_linewidth(0.5)
for w in bp["whiskers"] + bp["caps"]:
    w.set_linewidth(0.5)

ax_c.axhspan(0.12, 0.19, alpha=0.18, color="#E69F00", zorder=0)
ax_c.axhline(0.19, color="#d62728", linewidth=0.8, linestyle=(0, (1, 1.2)), zorder=1)
ax_c.text(4.6, 0.205, "UB 0.19", fontsize=6.3, color="#d62728",
          fontweight="bold", va="bottom", ha="left", zorder=4,
          bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                    edgecolor="none", alpha=0.85))

ax_c.set_xticks(range(1, len(queries) + 1))
ax_c.set_xticklabels(short_q, fontsize=6.3, rotation=45, ha="right")
ax_c.set_ylabel("F1 (all $\\mathrm{model}\\times\\mathrm{cfg}$)", fontsize=8)
ax_c.set_ylim(-0.02, 0.42)

plt.subplots_adjust(left=0.16, right=0.97, top=0.96, bottom=0.28)
out_c = os.path.join(OUT_DIR, "F4c_t5_perquery.pdf")
fig_c.savefig(out_c)
fig_c.savefig(out_c.replace(".pdf", ".png"), dpi=300)
print(f"wrote {out_c}")
