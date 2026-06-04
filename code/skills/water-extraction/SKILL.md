---
name: water-extraction
description: Extract a binary water mask from a 10-band Sentinel-2 surface-reflectance GeoTIFF and save it to artifacts/output.png. Provides a strong MNDWI-based starting point with adaptive thresholding; combine multiple cues when the scene calls for it.
---

# Water Body Extraction from Sentinel-2

## Inputs and outputs

- Input: `input.tif`, 10 bands @ 10 m, uint16, scale 10 000.
  Channel order: `0=B02, 1=B03, 2=B04, 3=B08, 4=B05, 5=B06, 6=B07, 7=B8A, 8=B11, 9=B12`.
- Output: `artifacts/output.png`, single-band uint8, 1024×1024, water = 255, else = 0.

## How to use this skill (workflow)

This skill gives you a strong starting point + adjustment toolbox. It is
**not** a one-shot recipe — submitting on the first attempt usually leaves
performance on the table. Use this cycle:

1. **Inspect first** (1 RunPython call). Open the image and print: per-band
   means, MNDWI's `min/mean/max/std`, coarse histogram (e.g. `np.histogram(mndwi, bins=10)`).
   This tells you which adjustment row(s) below apply BEFORE you commit to a default.
2. **Apply the starting point**. Run the baseline recipe to get a first mask.
3. **Run the self-check** below — all four items.  If any fails, do NOT submit;
   go to step 4.
4. **Adjust using the toolbox** (1–3 more RunPython calls). Apply one or
   more rows from the Scene-aware adjustments table. Re-run the self-check.
5. **Submit** once self-checks pass *and* (for non-trivial scenes) you have
   compared the starting-point mask against at least one alternative.

A good run typically uses **3–6 RunPython calls**. Submitting at call 2 with a
suspiciously empty or saturated mask is a known failure mode — the time budget
is there for you to iterate.

## Starting point — MNDWI with data-driven threshold

MNDWI (Modified NDWI, Xu 2006) is the strongest single-index baseline because
SWIR1 (B11) is absorbed by water but reflected by built and bare surfaces — so
this index separates water from cities + soil better than plain NDWI does.

The literal recipe `MNDWI > 0` works on temperate / coastal / urban tiles but
it's a **starting point, not the final answer**. Inspect the MNDWI distribution
and use Otsu or a percentile cut whenever the histogram suggests a better split
than zero.

```python
import rasterio, numpy as np
from PIL import Image
from skimage.filters import threshold_otsu

with rasterio.open('input.tif') as src:
    img = src.read().astype(np.float32) / 10000.0   # (10, H, W) reflectance 0-1

green, swir1 = img[1], img[8]                       # B03, B11
mndwi = (green - swir1) / (green + swir1 + 1e-10)

# Adaptive threshold: prefer Otsu when histogram is bimodal, otherwise fall
# back to the literature default of 0.0.
try:
    t = threshold_otsu(mndwi)
    if abs(t) > 0.5:                # Otsu can pick crazy values when one mode dominates
        t = 0.0
except Exception:
    t = 0.0
mask = mndwi > t

mask_u8 = (mask.astype(np.uint8) * 255)
Image.fromarray(mask_u8).save('artifacts/output.png')
```

This baseline alone reaches F1 ≥ 0.8 on temperate / coastal / urban tiles. You
are encouraged to do better — explore the bands, try alternative indices,
combine them with logical AND/OR.

## Scene-aware adjustments — combine as needed

Inspect MNDWI, NDWI, AWEI, and the bands BEFORE saving. **Multiple rows can
apply at once** — combine them when the scene shows multiple signals (e.g.,
arid + sediment-laden lake). Treat the table as a toolbox, not a multiple
choice.

| Observable signal (computed from arrays) | Adjustment |
|---|---|
| `mndwi.std() > 0.25` AND clearly bimodal histogram | Use `skimage.filters.threshold_otsu(mndwi)` instead of 0 |
| Arid / desert scene: `((img[3] - img[2])/(img[3]+img[2]+1e-10)).mean() < 0.10` AND `mndwi.max() < 0.3` | Lower threshold to `np.percentile(mndwi, 95) - 0.05` |
| Sediment / saline lake suspected: `mndwi.max() < 0.1` despite obvious water expected | AND-combine with NDWI: `(mndwi > -0.05) & ((img[1]-img[3])/(img[1]+img[3]+1e-10) > -0.1)` |
| Heavy mountain shadows: bright B02 with low B08 in non-water areas | Use AWEI_nsh `> 0`: `4*(img[1]-img[8]) - (0.25*img[3] + 2.75*img[9])` |
| Default still leaks built-up areas | AND-combine with low-NIR check: `mask & (img[3] < 0.15)` (water reflects little NIR) |

If you find a combination this list doesn't cover, use it. The table reflects
common cases, not the limit of what's allowed.

## Self-check before saving

Run all four. **Failing any one means do NOT submit yet — go back to the
adjustments table, change something, and re-run the checks.**

1. **Coverage sanity**: `0.001 ≤ mask.mean() ≤ 0.85`.
   - `< 0.001` (mask near-empty): threshold too strict OR sign inverted. Try
     a lower / Otsu / percentile threshold, OR check that you computed
     `(green − swir1)` not `(swir1 − green)`.
   - `> 0.85` (mask floods almost everything): threshold too loose OR wrong
     band index. Verify `green = img[1]` and `swir1 = img[8]`.
2. **Threshold is data-driven**: print `mndwi.min(), mndwi.mean(), mndwi.max(), threshold, threshold_otsu(mndwi)`.
   If your final threshold is the hard-coded 0 but Otsu gives something very
   different (and the histogram is bimodal), the data-driven value is almost
   always better — adopt it and re-run.
3. **Dtype/values**: `np.unique(np.array(Image.open('artifacts/output.png')))`
   must return `[0, 255]`. If it returns `[0, 1]` or `[False, True]`, multiply
   by 255 before saving.
4. **Largest-component dominance** (only when `mask.mean() > 0.05`): the
   largest connected component should hold > 30 % of total water pixels. If
   it doesn't, the mask is fragmented — apply `binary_closing` with a 3×3
   disk and re-check.

## Common pitfalls

1. **Mask is empty** → threshold inverted or units wrong. Print
   `mndwi.min(), mndwi.mean(), mndwi.max()` and re-check the formula sign.
2. **Mask covers > 90 %** → wrong band index. Verify `green = img[1]` and
   `swir1 = img[8]`, not the array codes.
3. **Saved as 0/1 instead of 0/255** → evaluator binarises at > 127, so 0/1
   masks read as all-zero. Multiply by 255 before saving.
4. **Used `cv2.imread('input.tif')`** — that returns 3-band 8-bit RGB, losing
   7 bands and the SWIR signal. Always use `rasterio.open(...).read()`.
5. **Stopped at the literal default without checking the histogram** — `MNDWI > 0`
   is a baseline. If `threshold_otsu(mndwi)` is clearly different and the
   histogram is bimodal, the data-driven threshold is almost always better.
