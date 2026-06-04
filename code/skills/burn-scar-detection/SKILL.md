---
name: burn-scar-detection
description: Detect burned (fire-damaged) pixels between a pre-fire (image_A.tif) and a post-fire (image_B.tif) Sentinel-2 GeoTIFF and save a binary burn mask to artifacts/output.png. Provides a dNBR baseline with adaptive thresholding; combine with NDVI / SWIR-difference cues if scene-specific signals warrant.
---

# Burn-Scar Detection on Sentinel-2 (pre / post)

## Inputs and outputs

- Inputs: `image_A.tif` (acquired BEFORE the fire) and `image_B.tif` (acquired AFTER the fire), both 10-band Sentinel-2 surface reflectance with the same channel order:
  `0=B02, 1=B03, 2=B04, 3=B08, 4=B05, 5=B06, 6=B07, 7=B8A, 8=B11, 9=B12`,
  uint16, scale 10 000.
- Output: `artifacts/output.png`, single-band uint8, 512×512,
  burned = 255, unburned = 0.

## How to use this skill (workflow)

Burn detection is the **most knowledge-sensitive** of the 4 tasks — the
NBR formula and the B08/B12 SWIR indexing are easy to get wrong, and the
errors silently produce a wrong-direction signal. **Don't paste the
starting-point recipe and submit immediately.** Use this cycle:

1. **Inspect first** (1 RunPython call). Open both images, print per-band
   means. Compute `nbr_pre`, `nbr_post`, `dnbr`. Print
   `dnbr.min/mean/max/std`. **Critical sanity check**: on a clearly burned
   patch, `dnbr.mean()` should be POSITIVE (because pre-fire NBR > post-fire
   NBR). If it's negative, you flipped pre/post — fix before going further.
2. **Apply the starting point**. Run the dNBR thresholding recipe.
3. **Run the self-check** below. The band-index check (item 5) is the most
   frequently violated — verify it visually.
4. **Adjust** (1–3 more RunPython calls). The toolbox covers cloud over
   post-fire, fully-burned scenes (Otsu degenerates), tiny burns (lower
   threshold or use percentile), morphological cleanup.
5. **Submit** when self-checks pass.

Aim for **3–6 RunPython calls**. The single most common failure for this
task is using B11 (index 8) instead of B12 (index 9) — re-verify against
`src.descriptions` before submitting.

The two indices that matter:
- **B08 (NIR)** is at **index 3** in the channel stack.
- **B11 (SWIR1)** is at **index 8**, **B12 (SWIR2)** is at **index 9**.
- Standard burn-area indices use **B08 (NIR) + B12 (SWIR2)**, not B11.

## Starting point — dNBR with adaptive threshold

Healthy vegetation reflects strongly in NIR (B08) and weakly in SWIR2 (B12); after a fire, the NIR drops and SWIR2 rises sharply because the leaf canopy is gone and the exposed char + dry soil are SWIR-bright. The **Normalized Burn Ratio** captures this:

```
NBR = (NIR - SWIR2) / (NIR + SWIR2)
    = (B08 - B12) / (B08 + B12)
```

NBR ranges from −1 to +1. Healthy vegetation: roughly +0.4 to +0.8. Recent burn scar: roughly −0.3 to +0.1.

The change quantity, **dNBR**, is computed as **pre minus post** (so burned pixels have positive dNBR):

```
dNBR = NBR_pre - NBR_post   # i.e. NBR(A) - NBR(B), since A is pre-fire
```

USGS-style severity table for dNBR (after scaling by 1000 if you need it; here we keep raw float):

| dNBR (raw float) | Severity                |
|------------------|-------------------------|
| < 0.10           | unburned                |
| 0.10 – 0.27      | low severity            |
| 0.27 – 0.66      | **moderate severity**   |
| > 0.66           | high severity           |

A reasonable starting threshold is **0.27** (low/mod boundary). When the histogram is clearly bimodal, Otsu often picks a tighter, scene-adapted split.

```python
import rasterio, numpy as np
from PIL import Image
from skimage.filters import threshold_otsu

NIR_IDX, SWIR2_IDX = 3, 9   # B08, B12

def read10(path):
    with rasterio.open(path) as src:
        return src.read().astype(np.float32) / 10000.0   # (10, H, W)

def nbr(img):
    nir = img[NIR_IDX]
    swir2 = img[SWIR2_IDX]
    return (nir - swir2) / (nir + swir2 + 1e-6)

A = read10('image_A.tif')   # pre-fire
B = read10('image_B.tif')   # post-fire

dnbr = nbr(A) - nbr(B)        # positive on burn

# Adaptive threshold: try Otsu, fall back to fixed 0.27 if Otsu degenerates
default_thr = 0.27
try:
    t_otsu = threshold_otsu(dnbr.ravel())
    # Trust Otsu only when it lands in a plausible burn range
    threshold = t_otsu if 0.10 <= t_otsu <= 0.66 else default_thr
except Exception:
    threshold = default_thr
mask = dnbr > threshold

Image.fromarray((mask.astype(np.uint8) * 255)).save('artifacts/output.png')
```

This baseline reaches F1 ≥ 0.4 on a typical CaBuAr-test patch with > 1 % burned area. You are encouraged to do better — combine dNBR with NDVI loss or SWIR difference, post-process with morphology, or stratify by severity tier.

## Scene-aware adjustments — combine as needed

Inspect both images, the dNBR histogram, and burn extent before saving. **Multiple rows can apply at once**. Treat the table as a toolbox.

| Observable signal | Adjustment |
|---|---|
| dNBR histogram clearly bimodal (clear valley around 0.2–0.4) | Trust `threshold_otsu(dnbr.ravel())` directly without the fallback |
| Whole patch is burned (mean dNBR ≫ 0.5, near-zero unburned tail) | Use a fixed conservative threshold like 0.10 — Otsu degenerates when one class dominates |
| Patch has very little burn (< 1 %, dNBR mostly < 0.05) | Lower threshold to ~0.15 OR use percentile of the upper tail (`np.percentile(dnbr, 99)`) — Otsu may pick noise |
| Cloud over post-fire image (B[0,B02] mean > 0.20) | Mask out pixels where post-fire B02 reflectance > 0.25 as "no-data" before thresholding |
| Output mask too speckly (many isolated single pixels) | Apply `binary_opening` with 3×3 disk to suppress speckle (real burns are spatially contiguous) |
| Mask has holes inside obviously burned regions | Apply `binary_closing` with 3×3 or 5×5 disk |
| Want extra confidence | OR-combine with NDVI loss: `mask | ((NDVI(A) - NDVI(B)) > 0.20)` where `NDVI = (B08-B04)/(B08+B04)` |
| Want to suppress water / shadow false positives | Mask out pixels where pre-fire NDVI(A) < 0 (those weren't vegetation in the first place, so they can't have "burned") |

If you have a better idea (per-band z-score, RBR = relative burn ratio, IR-MAD), use it.

## Self-check before saving

Run all five. **Failing any one means do NOT submit yet — diagnose, fix,
re-run.**

1. **Sign convention** (most common failure): `dNBR = NBR_pre - NBR_post`.
   Print `dnbr.mean()`. On a patch that is *visually* burned (e.g.
   post-fire image looks dark / red-ish, pre-fire looks green), `dnbr.mean()`
   should be POSITIVE. If it's negative, you flipped pre and post — swap A
   and B and re-compute.
2. **Coverage sanity**: `0.0001 ≤ mask.mean() ≤ 0.95`.
   - `< 0.0001`: threshold too strict OR sign flipped. Try Otsu, drop the
     fallback to 0.10 if histogram suggests it, or check the sign.
   - `> 0.95`: either the patch is genuinely fully burned (rare — verify on
     image) OR sign flipped. Almost never legitimate above 0.7 unless source
     metadata says full-burn.
3. **Threshold is data-driven**: print `dnbr.min/mean/max/std`,
   `threshold_otsu(dnbr)`, your final `threshold`. If `t_otsu` is in
   [0.10, 0.66], use it; otherwise use the 0.27 default but document the
   fallback in your reasoning.
4. **Output shape & dtype**: `(512, 512)`, uint8, values strictly `{0, 255}`.
5. **Band index audit** (also a common failure): B08 = index 3, B12 = **index 9**
   (the LAST band, NOT index 8 which is B11). Confirm by printing
   `src.descriptions` from rasterio after `rasterio.open(...)` — it should
   list `B12` at position 9. If you grabbed B11 for SWIR2, you'll get a
   weak / wrong-direction signal even with correct sign convention.

## Common pitfalls

1. **Confused B11 and B12** → `dnbr = nbr_with_B11(A) - nbr_with_B11(B)`. NBR is defined on **B12** (SWIR2). B11 is SWIR1, narrower water absorption; gives a weak burn signal. B12 is at **index 9** in our 10-band stack.
2. **Flipped pre/post** → computed `NBR(B) - NBR(A)`, ended up with negative-on-burn signal, threshold > 0 catches nothing. The task spec is `image_A.tif` = pre, `image_B.tif` = post.
3. **Forgot to divide by 10 000** → reflectance values are in `[0, 10 000]` not `[0, 1]`. NBR formula still mathematically returns a normalized −1..+1 ratio (the scale cancels), but if you mix scaled and unscaled values across operations the indices break. Divide once and stick with float reflectance.
4. **Used NDVI instead of NBR** → NDVI also drops after fire, but the post-fire SWIR2 *increase* is the cleaner signal for ash and char. NBR is the standard burn metric for a reason.
5. **Saved raw dNBR floats** → evaluator reads as continuous and the comparison against the binary GT collapses. Apply threshold, save as `(mask * 255).astype(uint8)`.
6. **Stuck on threshold = 0.27 when Otsu clearly says 0.42** for this scene. The 0.27 number is a USGS textbook default; let the data choose when the histogram is informative.
7. **Took absolute difference instead of signed difference** → `np.abs(NBR(A) - NBR(B))` flags any large change (including vegetation regrowth, water level shift, cloud). The signed `NBR(A) - NBR(B)` is what isolates burn.
