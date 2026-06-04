"""F2 -- Task gallery: 3 rows (RGB / GT / Agent) x 5 columns (T1..T5).

Vertical arrangement gives a clean RGB->GT->Agent visual flow per task.
Row labels are horizontal on the left; column headers (task + model x cfg
+ primary metric) sit below the agent row. T3 reports OA per Table 1; the
other four tasks report pixel F1.

  T1 water:     cape_town_za     kimi-k2.6 x C4         (F1=0.99)
  T2 change:    oscd_test_09     qwen3.6-27b x C1       (F1=0.75)
  T3 landcover: manila_ph        deepseek-v4-flash x C5 (OA=0.88)
  T4 burn:      burn_06          qwen3.6-35b-a3b x C1   (F1=0.87)
  T5 query:     yangtze_delta_cn deepseek-v4-flash x C6 (F1=0.90)
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _style import setup

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import rasterio

setup()

BENCH = "/Users/polaries/Work/AutoSpec/benchmark"

# (task_label, task_sub_with_metric, dataset_dir, agent_output_png, gt_name, input_name, query_overlay)
COLS = [
    ("T1 Water",
     r"kimi-k2.6 $\times C_4$  ($F_1{=}0.99$)",
     f"{BENCH}/datasets_tif/water/data/cape_town_za",
     f"{BENCH}/archive.E1.20260509_210641.kimi-k2.6/results/water_C4_kimi-kimi-k2.6_20260509_192357_da4c35/cape_town_za/workspace/artifacts/output.png",
     "label.png", "input.tif", None),
    ("T2 Change",
     r"qwen3.6-27b $\times C_1$  ($F_1{=}0.75$)",
     f"{BENCH}/datasets_tif/change/data/oscd_test_09",
     f"{BENCH}/archive.E1.20260509_172625.qwen3.6-27b/results/change_C1_qwen3.6-27b_20260508_191631_edc377/oscd_test_09/workspace/artifacts/output.png",
     "mask.png", "image_A.tif", None),
    ("T3 Land cover",
     r"ds-v4-flash $\times C_5$  (OA${=}0.88$)",
     f"{BENCH}/datasets_tif/landcover/data/manila_ph",
     f"{BENCH}/archive.E1.20260509_182107.deepseek-v4-flash/results/landcover_C5_deepseek-v4-flash_20260509_125147_13d860/manila_ph/workspace/artifacts/output.png",
     "label.png", "input.tif", None),
    ("T4 Burn",
     r"qwen3.6-35b-a3b $\times C_1$  ($F_1{=}0.87$)",
     f"{BENCH}/datasets_tif/burn/data/burn_06",
     f"{BENCH}/archive.E1.20260516_104240.qwen3.6-35b-a3b/results/burn_C1_qwen3.6-35b-a3b_20260515_163051_d52612/burn_06/workspace/artifacts/output.png",
     "mask.png", "image_A.tif", None),
    ("T5 Spatial query",
     r"ds-v4-flash $\times C_6$  ($F_1{=}0.90$)",
     f"{BENCH}/datasets_tif/query/data/yangtze_delta_cn__t5",
     f"{BENCH}/archive.E1.20260509_182107.deepseek-v4-flash/results/query_C6_deepseek-v4-flash_20260511_112115_c168be/yangtze_delta_cn__t5/workspace/artifacts/output.png",
     "label.png", "input.tif",
     "Identify built-up surfaces\nwithin 200\\,m of permanent water."),
]


def load_rgb_from_tif(tif_path: str) -> np.ndarray:
    with rasterio.open(tif_path) as src:
        bands = src.count
        if bands >= 3:
            r = src.read(3); g = src.read(2); b = src.read(1)
        else:
            r = g = b = src.read(1)
        arr = np.stack([r, g, b], axis=-1).astype(np.float32)
        for c in range(3):
            lo, hi = np.percentile(arr[..., c], [2, 98])
            if hi > lo:
                arr[..., c] = np.clip((arr[..., c] - lo) / (hi - lo), 0, 1)
        return arr


def load_mask_png(png_path: str) -> np.ndarray:
    img = Image.open(png_path)
    if img.mode == "P":
        return np.array(img)
    if img.mode in ("L", "1"):
        return np.array(img)
    arr = np.array(img.convert("RGB"))
    return (arr.max(-1) > 127).astype(np.uint8) * 255


def show_mask(ax, mask: np.ndarray, multiclass: bool):
    if multiclass:
        cmap_arr = np.full((*mask.shape, 3), 35, dtype=np.uint8)
        cmap_arr[mask == 1] = (45, 110, 200)
        cmap_arr[mask == 2] = (110, 175, 95)
        cmap_arr[mask == 3] = (210, 165, 120)
        ax.imshow(cmap_arr)
    else:
        m = (mask > 0).astype(np.uint8) * 255
        ax.imshow(m, cmap="gray", vmin=0, vmax=255)


# -- Layout: 3 image rows + 1 footer row x (row-label col + 5 task cols)
fig = plt.figure(figsize=(7.0, 3.55))
ntasks = len(COLS)
nrows = 3

gs = fig.add_gridspec(
    nrows + 1, ntasks + 1,
    width_ratios=[0.07] + [1] * ntasks,
    height_ratios=[1] * nrows + [0.22],
    wspace=0.03, hspace=0.04,
    left=0.005, right=0.998, top=0.995, bottom=0.005,
)

ROW_LABELS = ["RGB", "GT", "Agent"]

# Row labels (HORIZONTAL text on the left)
for ri in range(nrows):
    ax_rl = fig.add_subplot(gs[ri, 0])
    ax_rl.axis("off")
    ax_rl.text(0.92, 0.5, ROW_LABELS[ri],
               ha="right", va="center",
               fontsize=8.5, fontweight="bold")

# Image cells
for ci, (task_lbl, task_sub, ddir, agent_png, gt_name, in_name, query) in enumerate(COLS):
    multiclass = (ci == 2)

    for ri, kind in enumerate(["rgb", "gt", "ag"]):
        ax = fig.add_subplot(gs[ri, ci + 1])
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_linewidth(0.3); sp.set_color("#888")

        if kind == "rgb":
            try:
                rgb = load_rgb_from_tif(os.path.join(ddir, in_name))
                ax.imshow(rgb)
            except Exception as e:
                ax.text(0.5, 0.5, f"rgb err", ha="center", va="center",
                        fontsize=4, transform=ax.transAxes)
            if query is not None:
                ax.text(0.04, 0.96, query, transform=ax.transAxes,
                        ha="left", va="top", fontsize=4.4, color="white",
                        bbox=dict(facecolor="black", edgecolor="none",
                                  alpha=0.55, pad=1.0))
        elif kind == "gt":
            try:
                m_gt = load_mask_png(os.path.join(ddir, gt_name))
                show_mask(ax, m_gt, multiclass)
            except Exception as e:
                ax.text(0.5, 0.5, f"gt err", ha="center", va="center",
                        fontsize=4, transform=ax.transAxes)
        else:
            try:
                m_ag = load_mask_png(agent_png)
                show_mask(ax, m_ag, multiclass)
            except Exception as e:
                ax.text(0.5, 0.5, f"ag err", ha="center", va="center",
                        fontsize=4, transform=ax.transAxes)

    # Column footer (task name + model x cfg + metric) BELOW the agent row
    ax_f = fig.add_subplot(gs[nrows, ci + 1])
    ax_f.axis("off")
    ax_f.text(0.5, 0.75, task_lbl, ha="center", va="center",
              fontsize=8.0, fontweight="bold")
    ax_f.text(0.5, 0.18, task_sub, ha="center", va="center",
              fontsize=5.8, color="#555")

out_pdf = os.path.join(os.path.dirname(__file__), "../F2_gallery.pdf")
out_png = out_pdf.replace(".pdf", ".png")
fig.savefig(out_pdf, bbox_inches="tight", pad_inches=0.02)
fig.savefig(out_png, dpi=200, bbox_inches="tight", pad_inches=0.02)
print(f"wrote {out_pdf}")
print(f"wrote {out_png}")
