"""F4 — T5 compositional spatial query deep-dive.

Four panels arranged horizontally. Crucially: all legends are placed OUTSIDE
plot data area or in genuinely empty corners. No annotation crosses bars.

Span: full-width (~7 in), ~2.6 in tall on ACM sigconf.
"""
from __future__ import annotations
import sys, os, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_COLORS, MODEL_ORDER, CFG_ORDER

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import rasterio
from PIL import Image

setup()

BENCH = "/Users/polaries/Work/AutoSpec/benchmark"
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

df = pd.read_parquet(os.path.join(DATA_DIR, "all_trials.parquet"))
t5 = df[(df.task == "query") & df.submitted & df.primary_metric.notna()].copy()

# 3-panel layout (sample triptych moved to appendix per body page-budget).
fig = plt.figure(figsize=(7.4, 2.4))
gs = fig.add_gridspec(
    1, 3,
    width_ratios=[1.05, 1.00, 1.30],
    wspace=0.40,
)

# ============================================================
# Panel (a) — per-model C0 vs C3 grouped bar
#   Legend placed BELOW the plot to avoid overlapping bars.
# ============================================================
ax_a = fig.add_subplot(gs[0, 0])
agg = t5.groupby(["model", "cfg"])["primary_metric"].mean().unstack()
agg = agg.loc[MODEL_ORDER]

x = np.arange(len(MODEL_ORDER))
w = 0.35
ax_a.bar(x - w/2, agg["C0"], w, label=r"$C_0$ (bare)",
         color="#cfd8dc", edgecolor="#444", linewidth=0.5)
ax_a.bar(x + w/2, agg["C3"], w, label=r"$C_3$ (SK)",
         color="#0072B2", edgecolor="#003c5a", linewidth=0.5)

ax_a.axhline(0.12, color="#8c564b", linewidth=1.0, linestyle=(0, (4, 2)),
             label="naive (NDVI)")
ax_a.axhline(0.19, color="#d62728", linewidth=1.0, linestyle=(0, (1, 1.2)),
             label="UB (router)")

ax_a.set_xticks(x)
# Labels follow MODEL_ORDER (total-param ascending):
#   qwen3-8b, qwen3-14b, qwen3.6-27b, qwen3.6-35b-a3b, deepseek-v4-flash,
#   deepseek-v4-pro, kimi-k2.6
ax_a.set_xticklabels(["q3\n8b", "q3\n14b", "q3.6\n27b", "35b\na3b",
                      "ds-v4\nfl", "ds-v4\npro", "kimi\nk2.6"],
                     fontsize=6.5)
ax_a.set_ylabel("F1", fontsize=8)
ax_a.set_ylim(0, 0.30)
ax_a.set_title("(a) $C_0$ vs $C_3$ on T5", fontsize=9)
# Legend BELOW the plot — never overlaps bars
ax_a.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20),
            ncol=2, fontsize=6.5, frameon=False,
            handlelength=1.5, columnspacing=0.8, handletextpad=0.4)

# ============================================================
# Panel (b) — error decomposition stacked bar
#   Legend BELOW the plot in a 3-column row.
#   (Sample triptych moved to appendix.)
# ============================================================
ax_c = fig.add_subplot(gs[0, 1])

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

bottoms = np.zeros(len(CFG_ORDER))
for cat in CATS:
    values = np.array([counts[c][cat] for c in CFG_ORDER])
    ax_c.bar(CFG_ORDER, values, bottom=bottoms, color=CAT_COLORS[cat],
             label=cat, edgecolor="white", linewidth=0.4, width=0.72)
    bottoms += values

ax_c.set_xticklabels(CFG_ORDER, fontsize=7.5)
ax_c.set_ylabel("# failed T5 trials", fontsize=8)
ax_c.set_title("(b) T5 failure type by config", fontsize=9)
ax_c.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18),
            ncol=1, fontsize=6.3, frameon=False,
            handlelength=1.2, handletextpad=0.4, labelspacing=0.2)

# ============================================================
# Panel (c) — per-query F1 distribution (box plot)
#   Reference band annotated INSIDE upper plot, no legend overlap.
# ============================================================
ax_d = fig.add_subplot(gs[0, 2])

queries = sorted(t5["sample"].unique())
data_by_q = [t5[t5["sample"] == q]["primary_metric"].values for q in queries]
short_q = [q.replace("__t5", "").split("_")[0] for q in queries]

bp = ax_d.boxplot(data_by_q, vert=True, widths=0.55, patch_artist=True,
                   showfliers=False,
                   medianprops={"color": "black", "linewidth": 0.9})
for patch in bp["boxes"]:
    patch.set_facecolor("#cfd8dc")
    patch.set_edgecolor("#333")
    patch.set_linewidth(0.5)
for w in bp["whiskers"] + bp["caps"]:
    w.set_linewidth(0.5)

# Reference band.
# Naive and UB labels are placed INSIDE the plot in the empty zone above
# the small boxes (lake/manila/sydney are slivers at y≈0), so the
# annotations never clip and never collide with data.
ax_d.axhspan(0.12, 0.19, alpha=0.18, color="#E69F00", zorder=0)
ax_d.axhline(0.12, color="#8c564b", linewidth=0.8, linestyle=(0, (4, 2)), zorder=1)
ax_d.axhline(0.19, color="#d62728", linewidth=0.8, linestyle=(0, (1, 1.2)), zorder=1)
ax_d.text(4.6, 0.205, "UB 0.19", fontsize=6.3, color="#d62728",
          fontweight="bold", va="bottom", ha="left", zorder=4,
          bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                    edgecolor="none", alpha=0.85))
ax_d.text(4.6, 0.115, "naive 0.12", fontsize=6.3, color="#8c564b",
          fontweight="bold", va="top", ha="left", zorder=4,
          bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                    edgecolor="none", alpha=0.85))

ax_d.set_xticks(range(1, len(queries) + 1))
ax_d.set_xticklabels(short_q, fontsize=6.5, rotation=45, ha="right")
ax_d.set_ylabel(r"F1 (all $\mathrm{model} \times \mathrm{cfg}$)", fontsize=8)
ax_d.set_ylim(-0.02, 0.42)
ax_d.set_title("(c) Per-query F1 distribution", fontsize=9)

# ============================================================
# Save
# ============================================================
plt.subplots_adjust(left=0.05, right=0.98, top=0.91, bottom=0.20)
out_pdf = os.path.join(os.path.dirname(__file__), "../F4_t5_deepdive.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf)
fig.savefig(out_png, dpi=300)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")
