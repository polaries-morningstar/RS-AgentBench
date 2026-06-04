---
name: change-detection
description: Detect change between two co-registered Sentinel-2 GeoTIFFs (image_A.tif earlier, image_B.tif later) and save a binary change mask to artifacts/output.png. Provides a histogram-matched CVA baseline with adaptive thresholding; combine with index-difference detectors as the change semantics warrant.
---

# Bi-temporal Change Detection on Sentinel-2

## Inputs and outputs

- Inputs: `image_A.tif` (earlier) and `image_B.tif` (later), both 10-band
  Sentinel-2 surface reflectance, same channel order:
  `0=B02, 1=B03, 2=B04, 3=B08, 4=B05, 5=B06, 6=B07, 7=B8A, 8=B11, 9=B12`,
  uint16, scale 10 000.
- Output: `artifacts/output.png`, single-band uint8, **same H×W as the input
  images** (variable per sample — query with `rasterio.open(...).shape`),
  change = 255, no-change = 0.

## How to use this skill (workflow)

Bi-temporal CD is harder than it looks — most C0 attempts fail because
they threshold raw radiometric difference and capture illumination noise.
This skill gives you a robust pipeline + adjustment toolbox. **Don't paste
the starting-point recipe and submit immediately.** Use this cycle:

1. **Inspect both images first** (1 RunPython call). Print per-band means
   for A vs B (large gap = atmospheric/illumination difference, must be
   normalised). Print `cva.min/mean/max/std` after step 2 too. This tells you
   which adjustments to layer on.
2. **Apply the starting point**. Histogram-match B to A, compute CVA, pick
   adaptive threshold.
3. **Run the self-check** below. If any fails — and especially if
   `mask.mean()` is suspiciously close to 0 or to 1 — do NOT submit; go
   to step 4.
4. **Adjust using the toolbox** (1–3 more RunPython calls). The change
   semantics determine which row(s) apply: urban / fire / vegetation loss
   each have a different OR-combine.
5. **Submit** once self-checks pass and the mask coverage is plausible
   (urban CD: typically 0.5–10 %; massive change events: higher).

Aim for **3–6 RunPython calls**. The hardest cases (sparse changes < 1 %)
need the adjustments — submitting the starting-point mask alone is a known
failure mode.

## Starting point — Histogram match + CVA + adaptive threshold

The hardest part of bi-temporal change detection is **separating real surface
change from atmospheric / illumination differences**. Histogram-matching B
to A's distribution per band wipes out most of the "fake" diff. CVA then
gives a multi-band magnitude per pixel.

The threshold on the magnitude is the most critical knob — and it should be
**driven by the data**, not a fixed percentile. The 95th percentile assumes
5 % of pixels changed, which is often wrong. Use the smaller of (Otsu, 95th
percentile) as a robust default, and combine with index-difference cues
when the change semantics are known.

```python
import rasterio, numpy as np
from PIL import Image
from skimage.exposure import match_histograms
from skimage.filters import threshold_otsu

def read10(path):
    with rasterio.open(path) as src:
        return src.read().astype(np.float32) / 10000.0   # (10, H, W)

A = read10('image_A.tif')
B = read10('image_B.tif')

# Per-band histogram match B to A
B_norm = np.zeros_like(B)
for i in range(B.shape[0]):
    B_norm[i] = match_histograms(B[i], A[i])

# Change Vector Analysis (Euclidean magnitude)
diff = B_norm - A
cva = np.sqrt(np.sum(diff ** 2, axis=0))             # (H, W)

# Adaptive threshold: prefer Otsu when bimodal, but cap at the 95th percentile
# to avoid Otsu picking a tiny tail when the distribution is unimodal.
p95 = np.percentile(cva, 95)
try:
    t_otsu = threshold_otsu(cva.ravel())
    threshold = min(t_otsu, p95) if t_otsu > np.percentile(cva, 50) else p95
except Exception:
    threshold = p95
mask = cva > threshold

Image.fromarray((mask.astype(np.uint8) * 255)).save('artifacts/output.png')
```

This baseline typically reaches F1 ≥ 0.4 on OSCD-style urban change tasks.
You are encouraged to do better — combine CVA with index differences when the
change type is known, or post-process with morphology.

## Scene-aware adjustments — combine as needed

Inspect both images, the magnitude histogram, and any task hints before
saving. **Multiple rows can apply at once**. Treat the table as a toolbox.

| Observable signal | Adjustment |
|---|---|
| Magnitude histogram clearly bimodal (clear valley) | Use `threshold_otsu(cva.ravel())` directly (drop the percentile cap) |
| Targeted change type known: urban growth | OR-combine with NDBI difference: `mask | ((NDBI(B_norm) - NDBI(A)) > 0.10)` |
| Fire scar / vegetation loss suspected | OR-combine with dNBR: `mask | ((NBR(A) - NBR(B_norm)) > 0.27)` where `NBR = (B08-B12)/(B08+B12+1e-10)` |
| Cloud difference between dates suspected (B02 mean very different even after matching) | Skip pixels where `abs(B[0] - A[0]) > 0.20` (likely cloud) by setting them to no-change |
| Output mask too speckly (lots of single-pixel hits) | Apply `binary_opening` with 3×3 disk to remove speckle |
| Output mask too sparse compared to expectation | Lower threshold, OR drop the 95th-percentile cap and trust Otsu, OR combine multiple index differences with OR |
| Mask has obvious holes inside changed regions | Apply `binary_closing` with 3×3 disk, or take the largest connected components per class |

If you have a better idea (e.g., per-band z-score, MAD, IR-MAD), use it.

## Self-check before saving

Run all five. **Failing any one means do NOT submit — go back to the
adjustments table, fix what's wrong, and re-run.**

1. **Coverage sanity**: `0.0001 ≤ mask.mean() ≤ 0.30`. Urban CD tiles are
   typically 1–10 % changed.
   - `< 0.0001` (essentially empty): threshold too strict. Drop to Otsu, OR
     drop the percentile cap, OR OR-combine with an index difference.
   - `> 0.30` (over-flagging): histogram match probably failed. Check
     `B_norm.mean(axis=(1,2))` ≈ `A.mean(axis=(1,2))` per band; if not, the
     normalisation step didn't work — re-run it.
2. **Output shape & dtype**: shape MUST equal the input images' shape (use
   `rasterio.open('image_A.tif').shape` to confirm). Single-band uint8,
   values strictly in `{0, 255}`.
3. **Threshold is data-driven**: print `cva.mean(), cva.std(), threshold,
   threshold_otsu(cva), np.percentile(cva, 95)`. If your final threshold is
   far below Otsu/p95 you're over-flagging; far above means under-flagging.
   Pick based on the histogram, not on a literature default.
4. **Histogram match worked**: print `(B_norm - A).mean()` per band. Should
   be close to 0 for unchanged regions. If it's not, re-do the histogram
   matching before thresholding.
5. **Speckle is plausible**: if `mask.mean() > 0` but the mask consists
   mostly of single-pixel scatter, apply `binary_opening(mask, disk(1))`.
   Real surface change is spatially contiguous.

## Common pitfalls

1. **Skipped histogram matching** → mask covers most of the image because
   atmospheric differences dominate. Always normalise first.
2. **Used absolute magnitude on raw uint16** → magnitudes huge, percentile
   meaningless. Always divide by 10 000 first to get reflectance.
3. **Compared on visualisation channels (RGB only)** → loses NIR/SWIR
   signal where most surface change shows. Use all 10 bands in CVA.
4. **Saved CVA magnitudes (not the binary mask)** → evaluator reads as
   continuous, output looks like noise. Apply threshold and save as 0/255.
5. **Stuck on a fixed 95th-percentile threshold** when the histogram is
   bimodal and Otsu finds a much better split — let the data choose.
