"""F_scaling — Regime taxonomy + scaling figure for §5.2.

Per Agent C's design:
  - Ordinal x-axis (positions 1..7) with model labels — eliminates
    log-param crowding of the Decisive/Transition regime bands.
  - All 8 configurations plotted, grouped by channel family:
      * C0          : bare (gray dashed)
      * SK-off only : KB / WS / KB+WS  (orange family: C1, C2, C4)
      * SK-on       : SK / KB+SK / WS+SK / full stack (teal family: C3, C5, C6, C7)
  - Equal-width regime bands proportional to model-count:
      Decisive  = position 1 (qwen3-8b)
      Transition= position 2 (qwen3-14b)
      Saturated = positions 3-7 (5 models)
  - Embedded variance-decomposition text annotation.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup, MODEL_ORDER

import matplotlib.pyplot as plt
import pandas as pd

setup()

# Data ----------------------------------------------------------------
CELL = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                "../data/cell_means.csv"))

# Per-model panel-mean F1 for ALL 8 cfgs
per_model = CELL.groupby(['model', 'cfg'])['mean'].mean().unstack('cfg')

# Model short-names for x-tick labels
MODEL_LABEL = {
    'qwen3-8b':          'qwen3-8b\n(8 B)',
    'qwen3-14b':         'qwen3-14b\n(14 B)',
    'qwen3.6-27b':       'qwen3.6-27b\n(27 B)',
    'qwen3.6-35b-a3b':   'qwen3.6-35b\na3b (35 B)',
    'deepseek-v4-flash': 'deepseek\nv4-flash\n(284 B)',
    'kimi-k2.6':         'kimi-k2.6\n(1 T)',
    'deepseek-v4-pro':   'deepseek\nv4-pro\n(1.6 T)',
}

# Color scheme: cluster by channel family
# SK-off configs (orange family, dashed)
# C0: pure bare; C1: KB; C2: WS; C4: KB+WS
SK_OFF_COLORS = {
    'C0': '#999999',  # neutral gray (bare baseline)
    'C1': '#F4A261',  # orange (KB only)
    'C2': '#E76F51',  # warm coral (WS only)
    'C4': '#B05F3C',  # dark orange (KB+WS)
}
# SK-on configs (teal family, solid)
# C3: SK only (HIGHLIGHT); C5: KB+SK; C6: WS+SK; C7: full stack
SK_ON_COLORS = {
    'C3': '#2A9D8F',  # bright teal (SK only — flagship)
    'C5': '#264653',  # dark teal (KB+SK)
    'C6': '#1F8579',  # darker teal (WS+SK)
    'C7': '#0D7B7B',  # very dark teal (full stack)
}

# Figure --------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.0, 2.4))

x_pos = list(range(1, len(MODEL_ORDER) + 1))  # 1..7

# Regime bands (equal-width per ordinal position)
ax.axvspan(0.5, 1.5, color='#fbe1e1', alpha=0.65, zorder=0)         # Decisive: pos 1
ax.axvspan(1.5, 2.5, color='#fff3c4', alpha=0.65, zorder=0)         # Transition: pos 2
ax.axvspan(2.5, 7.5, color='#dcecdc', alpha=0.65, zorder=0)         # Saturated: pos 3-7

# Regime labels at top
ax.text(1.0, 0.555, 'Decisive', ha='center', va='top',
        fontsize=8, color='#a83232', weight='bold')
ax.text(2.0, 0.555, 'Transition', ha='center', va='top',
        fontsize=8, color='#8a6c1c', weight='bold')
ax.text(5.0, 0.555, 'Saturated', ha='center', va='top',
        fontsize=8, color='#2a6d3a', weight='bold')

# Plot all SK-off cfgs (dashed, orange family)
for cfg in ['C1', 'C2', 'C4']:
    ys = [per_model.loc[m, cfg] for m in MODEL_ORDER]
    ax.plot(x_pos, ys, color=SK_OFF_COLORS[cfg], linestyle='--',
            linewidth=1.1, marker='o', markersize=3.5,
            markeredgewidth=0.4, alpha=0.85, zorder=3, label=cfg)

# Plot C0 baseline (gray thick dashed)
ys = [per_model.loc[m, 'C0'] for m in MODEL_ORDER]
ax.plot(x_pos, ys, color=SK_OFF_COLORS['C0'], linestyle='--',
        linewidth=1.7, marker='o', markersize=4.5,
        markeredgecolor='#555', markeredgewidth=0.5, zorder=3,
        label='C0 (bare)')

# Plot all SK-on cfgs (solid, teal family); C3 highlighted with stars
for cfg in ['C5', 'C6', 'C7']:
    ys = [per_model.loc[m, cfg] for m in MODEL_ORDER]
    ax.plot(x_pos, ys, color=SK_ON_COLORS[cfg], linestyle='-',
            linewidth=1.2, marker='s', markersize=3.5,
            markeredgewidth=0.4, alpha=0.85, zorder=4, label=cfg)

# C3 flagship line
ys = [per_model.loc[m, 'C3'] for m in MODEL_ORDER]
ax.plot(x_pos, ys, color=SK_ON_COLORS['C3'], linestyle='-',
        linewidth=2.3, marker='*', markersize=11,
        markeredgecolor='#1a3d3a', markeredgewidth=0.7,
        zorder=5, label='C3 (SK only)')

# Headline annotation: SK +0.25 at 8B
ax.annotate('', xy=(1, 0.43), xytext=(1, 0.18),
            arrowprops=dict(arrowstyle='<->', color='#1a3d3a',
                            lw=1.0, shrinkA=2, shrinkB=2))
ax.text(1.18, 0.295, 'SK\n$+0.25$', fontsize=8, ha='left',
        va='center', color='#1a3d3a', weight='bold')

# 14B Transition tease: KB+SK > SK alone
ax.text(2.65, 0.295, 'KB stacks\non SK\n$+0.052$', fontsize=7.5,
        ha='left', va='center', color='#264653')
ax.annotate('', xy=(2.05, 0.32), xytext=(2.6, 0.30),
            arrowprops=dict(arrowstyle='->', color='#264653',
                            lw=0.9, shrinkA=2, shrinkB=2))

# Variance text box — bottom-right above the legend
sigma_text = (
    r'$\sigma(\mathrm{task})\!=\!0.21$' '\n'
    r'$\sigma(\mathrm{model})\!=\!0.08$' '\n'
    r'$\sigma(\mathrm{cfg})\!=\!0.03$'
)
ax.text(0.985, 0.36, sigma_text, transform=ax.transAxes,
        ha='right', va='bottom', fontsize=7.0,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='#888', linewidth=0.5, alpha=0.95))

# Axes ----------------------------------------------------------------
ax.set_xticks(x_pos)
ax.set_xticklabels([MODEL_LABEL[m] for m in MODEL_ORDER],
                   fontsize=7.0, linespacing=0.95)
ax.set_xlim(0.5, 7.5)
ax.set_ylim(0.12, 0.58)
ax.set_ylabel('Panel-mean F1 (averaged over 5 tasks)')
ax.set_xlabel('')  # x labels are model names
ax.grid(True, axis='y', alpha=0.18, linewidth=0.5)
ax.set_axisbelow(True)

# Compact legend inside the Saturated band area (bottom-right)
# Reorder for row-first display: with ncol=4 column-first fill, [C0,C4,C1,C5,C2,C6,C3,C7]
# renders as top row [C0 C1 C2 C3] and bottom row [C4 C5 C6 C7].
handles, labels = ax.get_legend_handles_labels()
def _cfg_key(lab):
    return int(lab.split()[0][1:])
by_cfg = {_cfg_key(lab): (h, lab) for h, lab in zip(handles, labels)}
row_first = [0, 4, 1, 5, 2, 6, 3, 7]
handles = [by_cfg[i][0] for i in row_first]
labels  = [by_cfg[i][1] for i in row_first]
ax.legend(handles, labels, loc='lower right', fontsize=6.3, ncol=4,
          handlelength=1.6, handletextpad=0.3, columnspacing=0.7,
          frameon=True, framealpha=0.92, edgecolor='#aaa',
          borderaxespad=0.3, borderpad=0.25)

plt.tight_layout()
out_pdf = os.path.join(os.path.dirname(__file__), "../F_scaling.pdf")
out_png = os.path.join(os.path.dirname(__file__), "../F_scaling.png")
fig.savefig(out_pdf, dpi=300, bbox_inches='tight')
fig.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"Saved: {out_pdf}")
print(f"Saved: {out_png}")
