"""F1 — Teaser figure (Figure 1).

Two panels sharing y-axis (panel-mean F1) and covering the three
factorial axes:
  (a) Scaling × Channel: F1 vs backbone total parameters (log) for
      C0 (bare), C3 (SK only), C5 (KB+SK). Background bands mark
      the three regimes: Decisive (8B), Transition (14B), Saturated
      (>=27B).
  (b) Per-task SK lever: bare vs SK-on F1 for each of the five
      tasks, sorted by SK lever magnitude. The gap between the two
      bars is the SK lever per task (annotated above).

Replaces F1c_scaling_curve.pdf as Figure 1.
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
SCALE = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                 "../data/scaling_curve.csv"))

# Per-model panel-mean F1 for C0, C3, C5
per_model = CELL.groupby(['model', 'cfg'])['mean'].mean().unstack('cfg')
# Backbone total parameters for x-axis (log scale)
total_B = SCALE.groupby('model')['total_B'].first()

# Per-task panel-mean F1 for C0 and C3 (mean over 7 models)
per_task = CELL.groupby(['task', 'cfg'])['mean'].mean().unstack('cfg')

# Sort tasks by SK lever (C3 - C0) descending
task_lever = (per_task['C3'] - per_task['C0']).sort_values(ascending=False)
TASKS = list(task_lever.index)
TASK_LABEL = {'water':     'Water',
              'change':    'Change',
              'burn':      'Burn',
              'query':     'T5 Query',
              'landcover': 'Landcover'}

# Figure layout -------------------------------------------------------
fig, (ax_a, ax_b) = plt.subplots(
    1, 2, figsize=(7.2, 3.0),
    gridspec_kw={'width_ratios': [1.55, 1.0], 'wspace': 0.34},
)

# ====================================================================
# PANEL A: Scaling × Channel
# ====================================================================
xs    = [total_B[m] for m in MODEL_ORDER]
y_c0  = [per_model.loc[m, 'C0'] for m in MODEL_ORDER]
y_c3  = [per_model.loc[m, 'C3'] for m in MODEL_ORDER]
y_c5  = [per_model.loc[m, 'C5'] for m in MODEL_ORDER]

# Regime bands (log-scale x in B parameters)
REGIME_BANDS = [
    (6,    11,   '#fbe1e1', 'Decisive\n(qwen3-8b)'),     # 8B band
    (11,   22,   '#fff3c4', 'Transition\n(qwen3-14b)'),  # 14B band
    (22,   3000, '#dcecdc', 'Saturated ($\\geq$27B)'),   # >=27B band
]
for lo, hi, col, _ in REGIME_BANDS:
    ax_a.axvspan(lo, hi, color=col, alpha=0.70, zorder=0)

# Three cfg lines
ax_a.plot(xs, y_c0, color='#999', linestyle='--', linewidth=1.4,
          marker='o', markersize=4, markeredgecolor='#555',
          markeredgewidth=0.5, label='C0 (bare)', zorder=3)
ax_a.plot(xs, y_c5, color='#264653', linestyle='-', linewidth=1.6,
          marker='s', markersize=5, markeredgecolor='#222',
          markeredgewidth=0.4, label='C5 (KB+SK)', zorder=4)
ax_a.plot(xs, y_c3, color='#2A9D8F', linestyle='-', linewidth=2.2,
          marker='*', markersize=11, markeredgecolor='#1a3d3a',
          markeredgewidth=0.7, label='C3 (SK only)', zorder=5)

ax_a.set_xscale('log')
ax_a.set_xlim(5.5, 3000)
ax_a.set_ylim(0.10, 0.56)
ax_a.set_xlabel('Backbone total parameters (B)')
ax_a.set_ylabel('Panel-mean F1')
ax_a.set_title('(a) Scaling $\\times$ channel', loc='left',
               fontsize=10, weight='bold', pad=10)

# Regime labels above plot top (in margin), short labels to avoid overlap
ax_a.text(8,    0.545, 'Decisive', ha='center', va='top',
          fontsize=7.5, color='#a83232', weight='bold')
ax_a.text(14,   0.515, 'Transition', ha='center', va='top',
          fontsize=7.5, color='#8a6c1c', weight='bold')
ax_a.text(220,  0.545, 'Saturated', ha='center', va='top',
          fontsize=7.5, color='#2a6d3a', weight='bold')

# SK-lever annotation for qwen3-8b (the headline +0.25) — placed to the right of marker
ax_a.annotate('', xy=(8, 0.42), xytext=(8, 0.20),
              arrowprops=dict(arrowstyle='<->', color='#1a3d3a',
                              lw=0.9, shrinkA=2, shrinkB=2))
ax_a.text(9.0, 0.31, 'SK\n$+0.25$', fontsize=7.5, ha='left',
          va='center', color='#1a3d3a', weight='bold')

ax_a.legend(loc='lower right', fontsize=7.5, handlelength=2,
            handletextpad=0.5, borderaxespad=0.4)
ax_a.grid(True, which='major', alpha=0.18, linewidth=0.5)
ax_a.grid(False, which='minor')

# ====================================================================
# PANEL B: Per-task SK lever
# ====================================================================
x_pos = list(range(len(TASKS)))
bare  = [per_task.loc[t, 'C0'] for t in TASKS]
sk_on = [per_task.loc[t, 'C3'] for t in TASKS]
levers = [sk_on[i] - bare[i] for i in range(len(TASKS))]

bar_w = 0.38
ax_b.bar([x - bar_w / 2 for x in x_pos], bare, bar_w,
         color='#bdbdbd', edgecolor='#555', linewidth=0.5,
         label='C0 (bare)')
ax_b.bar([x + bar_w / 2 for x in x_pos], sk_on, bar_w,
         color='#2A9D8F', edgecolor='#1a3d3a', linewidth=0.5,
         label='C3 (SK only)')

# Annotate lever above each pair
for i, lever in enumerate(levers):
    top = max(bare[i], sk_on[i])
    ax_b.annotate(f'+{lever:.2f}',
                  xy=(i, top + 0.025), ha='center', va='bottom',
                  fontsize=7.5, color='#1a3d3a', weight='bold')

ax_b.set_xticks(x_pos)
ax_b.set_xticklabels([TASK_LABEL[t] for t in TASKS],
                     fontsize=7.5, rotation=20, ha='right')
ax_b.set_ylim(0.0, 0.95)
ax_b.set_ylabel('Panel-mean F1')
ax_b.set_title('(b) Per-task SK lever', loc='left',
               fontsize=10, weight='bold', pad=10)
ax_b.legend(loc='upper center', fontsize=7.5, handlelength=1.4,
            handletextpad=0.4, borderaxespad=0.3, ncol=2,
            bbox_to_anchor=(0.5, 0.99), frameon=False)
ax_b.grid(True, axis='y', alpha=0.18, linewidth=0.5)

plt.tight_layout()

out_pdf = os.path.join(os.path.dirname(__file__), "../F1_teaser.pdf")
out_png = os.path.join(os.path.dirname(__file__), "../F1_teaser.png")
fig.savefig(out_pdf, dpi=300, bbox_inches='tight')
fig.savefig(out_png, dpi=300, bbox_inches='tight')
print(f"Saved: {out_pdf}")
print(f"Saved: {out_png}")
