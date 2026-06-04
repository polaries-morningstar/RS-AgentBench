---
name: land-cover
description: Classify each pixel of a 10-band Sentinel-2 GeoTIFF into 4 classes (water/vegetation/built-up/other) and save as artifacts/output.png with class IDs 0/1/2/3. Provides sequential index-based decision rules with adaptive thresholds; combine spectral cues and unsupervised clustering as needed.
---

# 4-class Land-Cover Classification on Sentinel-2

## Inputs and outputs

- Input: `input.tif`, 10 bands @ 10 m, uint16, scale 10 000.
  Channel order: `0=B02, 1=B03, 2=B04, 3=B08, 4=B05, 5=B06, 6=B07, 7=B8A, 8=B11, 9=B12`.
- Output: `artifacts/output.png`, single-band uint8, 1024×1024 with class IDs:
  `0 = water, 1 = vegetation, 2 = built-up, 3 = other (bare/snow)`. Use 255 only for
  truly invalid pixels (typically none).

## How to use this skill (workflow)

Multi-class segmentation is the most over-engineering-prone of the 4 tasks —
agents that try to build sophisticated classifiers from scratch routinely run
out of time. **The goal is to get a good enough mask submitted, not to
rebuild scikit-learn.** Use this cycle:

1. **Inspect first** (1 RunPython call). Compute scene-level stats:
   `ndvi.mean()`, `mndwi.mean()`, `ndbi.mean()`, `(B02+B03+B04).mean()`. These
   four numbers tell you which adjustment row(s) below apply, *before* you
   commit to a default classifier.
2. **Apply the starting point** (1 RunPython call). Run the rule-based
   sequential classifier as-is. This always produces a complete classification.
3. **Run the self-check** below. Each check has a concrete fix listed; don't
   submit a mask that's failing a coverage sanity item.
4. **Adjust** (1–3 more RunPython calls). Apply table rows that matched your
   step-1 stats. K-means is a last-resort alternative when the rule-based
   approach mis-classifies most of the scene — don't reach for it first.
5. **Submit** when self-check passes and class proportions look plausible
   for the scene.

Aim for **3–6 RunPython calls**. The rule-based starting point is fast and
complete — most of the budget should be spent on inspecting + tuning, not on
re-implementing everything. K-means with 4-class assignment by centroid
inspection is a valid alternative path but only adds 1–2 calls vs. tuning
the rules; pick one path early.

## Starting point — sequential rule-based decisions

Classify in this fixed order: water → vegetation → built → other. Order
matters — water has the most distinct spectral signature, so peeling it off
first prevents leakage into other classes.

The thresholds below are **starting points**. The right values depend on the
scene; use Otsu / percentile / histogram inspection to tune when defaults
look off.

```python
import rasterio, numpy as np
from PIL import Image

with rasterio.open('input.tif') as src:
    img = src.read().astype(np.float32) / 10000.0   # (10, H, W)
B02, B03, B04, B08, B11 = img[0], img[1], img[2], img[3], img[8]

mndwi = (B03 - B11) / (B03 + B11 + 1e-10)
ndvi  = (B08 - B04) / (B08 + B04 + 1e-10)
ndbi  = (B11 - B08) / (B11 + B08 + 1e-10)

H, W = ndvi.shape
out = np.full((H, W), 3, dtype=np.uint8)             # default 'other'

water_mask = mndwi > 0.0
veg_mask   = (~water_mask) & (ndvi > 0.30)
# Built-up: NDBI > 0 alone over-flags bare soil; require moderate SWIR
# brightness as well. This is a default that works for most scenes; relax if
# the scene is mostly urban or tighten if mostly bare desert.
built_mask = (~water_mask) & (~veg_mask) & (ndbi > 0.0) & (B11 > 0.20)

out[water_mask] = 0
out[veg_mask]   = 1
out[built_mask] = 2

Image.fromarray(out).save('artifacts/output.png')
```

This baseline reaches OA ≥ 0.7 across diverse biomes. You are encouraged to
adapt the thresholds per scene and to combine multiple signals when the
default mis-classifies.

## Scene-aware adjustments — combine as needed

Compute scene statistics first; **multiple rows can apply at once**. Treat
the table as a toolbox.

| Observable signal | Adjustment |
|---|---|
| Arid scene (`ndvi.mean() < 0.15`) — vegetation is sparse | Lower vegetation threshold to `ndvi > 0.15` (otherwise everything becomes "other") |
| Snow-covered (`(B02+B03+B04).mean() > 1.5`) — bright everywhere | Snow goes into class 3; explicitly **exclude** snow from built mask: add `& ~((B02+B03+B04 > 1.5) & (ndvi < 0.1))` to `built_mask` |
| Dense urban (`ndbi.mean() > 0.10`) — many built pixels expected | Tighten built threshold to `ndbi > 0.05 AND B11 > 0.25` to avoid mistaking bare soil for built |
| Mostly water scene (`mndwi.mean() > 0.30`) — water > 50% expected | After defaults, recover thin water bodies: `out[(out!=0) & (B08 < 0.05) & (mndwi > -0.1)] = 0` |
| Bare soil being mis-labeled as built | AND-combine built with low-NDVI but require high SWIR: `built_mask = built_mask & (B11 > 0.22) & (ndvi < 0.20)` |
| MNDWI/NDVI/NDBI histograms clearly bimodal | Use `threshold_otsu` per index instead of 0 / 0.30 / 0 |
| K-means with 4 centroids gives much cleaner clusters than rules | Run K-means on stacked indices (MNDWI, NDVI, NDBI, B11), then map each centroid to the class it best matches by inspecting the centroid's spectral signature |

If multiple rows match, apply all of them. If you have a better idea (e.g.,
GMM, spectral angle, decision tree), use it.

## Self-check before saving

Run all five. **Failing any one means do NOT submit — fix the corresponding
adjustment and re-run.**

1. **Class proportions match scene type** — print
   `np.unique(out, return_counts=True)`. Sanity rules:
   - In a coastal city scene, `built > 0` and `water > 0` (if both are zero,
     the corresponding threshold is too strict).
   - In a desert scene, `other` should dominate; if `built > 50 %`, the NDBI
     threshold is too loose.
   - In a forest/agricultural scene, `vegetation` should dominate; if
     `vegetation = 0`, NDVI threshold is too strict — drop to ~0.15.
2. **No invalid IDs**: `set(np.unique(out)) ⊆ {0, 1, 2, 3, 255}`. Any other
   value (e.g. 64, 128) means a remapping bug — usually saving K-means
   cluster IDs without applying the centroid → class mapping.
3. **Output shape & dtype**: `(1024, 1024)`, uint8.
4. **Pixels are class IDs, not greyscale**: `np.array(Image.open(...))[0,0]`
   should be in `{0,1,2,3,255}`, NOT `{0,64,128,192,255}`. The evaluator reads
   raw pixel values — any rescaling silently breaks scoring.
5. **No "all-other" or "all-vegetation" outputs**: if `out` is dominated by a
   single class (>90 %), thresholds are mis-calibrated. Re-derive at least
   one threshold from data (`threshold_otsu(ndvi)` etc.).

## Common pitfalls

1. **Class IDs swapped** (e.g., wrote 1=water instead of 0=water) → OA collapses
   even though logic is sound. Verify the mapping line by line.
2. **Built dominates everywhere** → NDBI threshold too loose AND/OR built was
   classified BEFORE vegetation. Keep the order water → veg → built, AND require
   `B11 > 0.20` to exclude bare soil.
3. **Used K-means clusters as class IDs directly** → K-means cluster IDs are
   arbitrary integers; you must MAP them to 0/1/2/3 by inspecting each
   cluster centroid's spectral signature. Without that mapping, OA = chance.
4. **Saved as 0–255 grayscale** instead of 0–3 class IDs → evaluator reads
   raw pixel values; `out * 64` would silently rescale and break everything.
   Save the array as-is (single band uint8 with values in 0–3).
5. **Stuck on the default thresholds** when the histograms clearly suggest
   different values — adapt to the scene.
