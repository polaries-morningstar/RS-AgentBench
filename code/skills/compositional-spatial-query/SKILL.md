---
name: compositional-spatial-query
description: Identify pixels matching a per-sample natural-language compositional query in a 10-band Sentinel-2 image. Each query combines (a) a target land-cover class to extract, (b) a different reference class, (c) a spatial operator (e.g. "within Nm of", "farther than Nm from"). The agent must decompose the query, detect both classes spectrally, compute spatial proximity, and intersect.
---

# Compositional Spatial Query on Sentinel-2

## Inputs and outputs

- Input: `input.tif`, 10 bands @ 10m, uint16, scale 10 000.
  Channels: `0=B02, 1=B03, 2=B04, 3=B08, 4=B05, 5=B06, 6=B07, 7=B8A, 8=B11, 9=B12`.
- Output: `artifacts/output.png`, single-band uint8 binary, 1024×1024,
  target = 255, else = 0.

## Why this task is fundamentally compositional

The query has THREE parts that must be combined:

1. **Target class** — what kind of pixel goes into the mask.
2. **Reference class** — what to measure spatial proximity from.
3. **Spatial operator** — within K meters / farther than K meters.

A single spectral index addresses only step 1. The proximity step is
geometric (distance transform) and must be applied to a DIFFERENT class
mask. Failing to compose all three steps leads to one of these errors:

- Output the target class without spatial filter → low precision (many fg pixels are far from the reference).
- Output the proximity-buffered region without class filter → low precision (catches all classes inside the buffer).
- Output the reference class itself → near-zero precision and recall.

## Query decomposition checklist

Before writing code, parse the natural-language query:

| Question to extract | Example |
|---|---|
| What is the target class? | "**tree-covered areas**" → trees |
| What is the reference class? | "...within 200m of **cropland**" → cropland |
| Spatial operator? | "**within** Nm of" / "**farther than** Nm from" |
| K in pixels? | "200m" → 20 pixels (Sentinel-2 GSD = 10m) |

Convert meters → pixels: `K_px = K_m / 10`.

## Spectral signatures for common land-cover classes

| Class | Index | Default threshold |
|---|---|---|
| Permanent water | `MNDWI = (B03 - B11)/(B03 + B11)` | `> 0` |
| Tree cover / dense vegetation | `NDVI = (B08 - B04)/(B08 + B04)` | `> 0.5` |
| Grassland / sparse vegetation | NDVI | `0.2 < NDVI < 0.5` |
| Cropland | NDVI seasonally varies; for single date use `NDVI > 0.3` AND uniform texture | `> 0.3` (and not tree) |
| Built-up | `NDBI = (B11 - B08)/(B11 + B08)` | `> 0` |
| Bare / sparse | low NDVI + low NDWI: `NDVI < 0.15 AND MNDWI < 0` | — |

These thresholds are starting points. When the histogram is bimodal,
prefer Otsu (`from skimage.filters import threshold_otsu`).

## Four-stage pipeline (template code)

```python
import rasterio, numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

with rasterio.open('input.tif') as src:
    img = src.read().astype(np.float32) / 10000.0   # (10, H, W)

B02, B03, B04, B08 = img[0], img[1], img[2], img[3]
B11, B12 = img[8], img[9]

def _div(n, d, eps=1e-9): return n / (d + eps)
mndwi = _div(B03 - B11, B03 + B11)
ndvi  = _div(B08 - B04, B08 + B04)
ndbi  = _div(B11 - B08, B11 + B08)

# === Step 1 — target_mask (depends on the query's target class) ===
# Pick the right index/threshold based on what the query asks for.
target_mask = ...   # bool (H, W)

# === Step 2 — reference_mask (depends on the query's reference class) ===
reference_mask = ...   # bool (H, W)

# === Step 3 — distance transform ===
# distance_transform_edt(~mask) gives Euclidean distance (in pixels) from
# every pixel to the nearest pixel that IS in the mask.
if reference_mask.sum() > 0:
    dist = distance_transform_edt(~reference_mask)
else:
    dist = np.full(target_mask.shape, np.inf, dtype=np.float32)

# === Step 4 — spatial operator + intersect ===
K_pixels = ...   # convert from query's meters: K_pixels = K_m // 10
op = ...         # "within" or "farther"

if op == "within":
    spatial_mask = dist <= K_pixels
else:  # farther
    spatial_mask = dist > K_pixels

target = target_mask & spatial_mask

Image.fromarray((target.astype(np.uint8) * 255)).save('artifacts/output.png')
```

## Common pitfalls

1. **Confused target and reference** — if query is "tree within 200m of water", target = trees, reference = water. **NOT** the other way around.

2. **Used distance_transform_edt(mask) instead of (~mask)** — the former gives "distance from non-pixel to nearest non-pixel"; we want distance to the **nearest mask pixel**, hence the inversion.

3. **Forgot to multiply by 10 (or divide by 10)** — the query is in meters; the distance transform returns pixels at Sentinel-2 native 10m GSD. K_meters = K_pixels × 10.

4. **Wrong spatial operator** — "within" is `<=K`, "farther" is `>K`. Read the query carefully.

5. **Output ⊄ target_class** — every output pixel must satisfy the target spectral signature. If the output contains pixels that are not the target class, you forgot to AND with `target_mask`.

6. **Reference class is rare or missing** — if `reference_mask.sum() == 0`, then "within" returns empty (no fg), "farther" returns the full target_mask. Handle this edge case.

7. **Threshold tuning** — defaults may not fit every scene. If `target_mask.mean()` is suspicious (very low or very high), inspect the distribution of the index and consider Otsu.

## Self-checks before submitting

1. **target ⊂ target_class**: every fg pixel in the output mask must be of the target spectral class.
2. **target ⊂ spatial_mask**: every fg pixel must satisfy the spatial operator.
3. **Coverage sanity**: `0.0001 ≤ output.mean() ≤ 0.50`. Compositional queries typically yield 0.5%-30% coverage; near-empty or near-full is a red flag.
4. **Output shape & dtype**: 1024×1024 single-band uint8, values in {0, 255}.
