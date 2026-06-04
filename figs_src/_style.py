"""Shared matplotlib style for all RS-AgentBench paper figures.

ACM sigconf body width is ~7 inches (full text width across two columns) and
~3.33 inches per single column. We target raster figures at 300 DPI and
prefer PDF (vector) output.

Design rules enforced:
  - Legends OUTSIDE plot data area or in genuinely empty corners.
  - Annotations never cross data.
  - One font hierarchy across all figures (consistent type).
  - Color-blind safe palette (Wong 2011 + ColorBrewer Dark2).
  - Generous whitespace between panels.
"""
from __future__ import annotations

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

# Tableau 10 palette — maximum hue separation across the 5 model points.
# Each pair (red↔orange, blue↔purple) sits ≥60° apart in hue, keeping
# distinct identity even at small marker sizes.
MODEL_COLORS = {
    "qwen3-8b":          "#d62728",  # red — small-model anchor
    "qwen3-14b":         "#8c564b",  # brown — transition regime
    "qwen3.6-35b-a3b":   "#2ca02c",  # green
    "qwen3.6-27b":       "#ff7f0e",  # orange
    "deepseek-v4-flash": "#1f77b4",  # blue
    "kimi-k2.6":         "#9467bd",  # purple
    "deepseek-v4-pro":   "#17becf",  # cyan — largest total-param point (1.6T MoE / 49B active)
}

# Failure-category palette. Each pair within the same hue family is split
# by saturation/lightness so adjacent stacked segments never blur together.
FAILURE_COLORS = {
    "ndvi_threshold":      "#ff7f0e",  # bright orange
    "compositional_plan":  "#1f77b4",  # blue
    "class_confusion":     "#17becf",  # cyan
    "skill_not_invoked":   "#2ca02c",  # green
    "hallucinated_fn":     "#d62728",  # red (clearly distinct from orange)
    "timeout_stall":       "#9467bd",  # purple
    "crs_ignored":         "#bcbd22",  # gold-olive
    "malformed_output":    "#e377c2",  # pink
    "band_index":          "#8c564b",  # brown
    "wrong_input":         "#7f7f7f",  # gray
    "other":               "#cccccc",  # light gray
}

# Model order: by total parameter count ascending (matches the x-axis of
# Figure 1c and Table 4 / Table 5). The 3B-active 35B MoE is placed by its
# total-parameter slot (35B), after qwen3.6-27b. Under active-parameter
# ordering, qwen3.6-35b-a3b (3B active) would precede 8B and 14B; we
# discuss that caveat in §7.
MODEL_ORDER = [
    "qwen3-8b",
    "qwen3-14b",
    "qwen3.6-27b",
    "qwen3.6-35b-a3b",
    "deepseek-v4-flash",
    "kimi-k2.6",
    "deepseek-v4-pro",      # 1.6T total — largest panel point, plotted last on scaling x-axis
]
MODEL_SHORT = {
    "qwen3-8b":          "qwen3-8b",
    "qwen3-14b":         "qwen3-14b",
    "qwen3.6-27b":       "qwen3.6-27b",
    "qwen3.6-35b-a3b":   "qwen3.6-35b-a3b",
    "deepseek-v4-flash": "deepseek-v4-flash",
    "deepseek-v4-pro":   "deepseek-v4-pro",
    "kimi-k2.6":         "kimi-k2.6",
}
TASK_ORDER = ["water", "change", "landcover", "burn", "query"]
TASK_LABELS = {
    "water":     "T1 Water",
    "change":    "T2 Change",
    "landcover": "T3 Landcover",
    "burn":      "T4 Burn",
    "query":     "T5 Compositional",
}
CFG_ORDER = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]
CFG_SHORT = {
    "C0": "C0", "C1": "C1", "C2": "C2", "C3": "C3",
    "C4": "C4", "C5": "C5", "C6": "C6", "C7": "C7",
}


def setup():
    """Set global matplotlib defaults consistent with ACM sigconf style."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.titlesize": 9.5,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "legend.frameon": False,
        "legend.handlelength": 1.2,
        "legend.handleheight": 1.0,
        "legend.labelspacing": 0.3,
        "axes.linewidth": 0.7,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
