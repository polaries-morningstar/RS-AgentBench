"""Convert CaBuAr ChaBuD-test HDF5 (HF DarthReca/california_burned_areas)
into 10-band dual-time TIFF pairs preserving CaBuAr's pre-patched 512×512
size, with the channel order T1/T2/T3 expects.

Output:
  datasets_tif/burn/data/<id>/image_A.tif    (10 bands, uint16, 512×512, pre-fire)
  datasets_tif/burn/data/<id>/image_B.tif    (10 bands, uint16, 512×512, post-fire)
  datasets_tif/burn/data/<id>/mask.png       (uint8, 0/255 binary burned)
  datasets_tif/burn/samples_v1.json          (sample metadata incl. shape)

Source layout (CaBuAr 12-band L1C minus B10):
  B01, B02, B03, B04, B05, B06, B07, B08, B8A, B09, B11, B12
Output layout (T1/T2/T3 canonical 10-band):
  B02, B03, B04, B08, B05, B06, B07, B8A, B11, B12
→ indices [1, 2, 3, 7, 4, 5, 6, 8, 10, 11] from the CaBuAr 12-band stack.

Note: CaBuAr stores arrays as (H, W, C) — different from OSCD (C, H, W).
We transpose to (C, H, W) before reordering.

Sample selection: CaBuAr ChaBuD-test has 68 uids (all with both pre_fire
and post_fire). We stratify by burn_pct into low / mid / high tiers and
pick 3/4/3 samples per tier deterministically (sorted by uid string).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import h5py  # noqa: F401  (loaded after hdf5plugin)
import hdf5plugin  # required for BZip2 decompression of CaBuAr HDF5
import numpy as np
import rasterio
from rasterio.transform import Affine

ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = ROOT / "datasets_tif/burn"
DATA_DIR = OUT_ROOT / "data"
SAMPLES_JSON = OUT_ROOT / "samples_v1.json"

# CaBuAr 12-band → our 10-band layout
CHANNEL_REORDER = [1, 2, 3, 7, 4, 5, 6, 8, 10, 11]

# Stratification tiers for sample selection
N_LOW, N_MID, N_HIGH = 3, 4, 3
MIN_PCT = 0.05        # measurement floor: ≥ ~131 burn-pixels in a 512×512 patch.
                      # Below this, pixel F1 is dominated by single-FP noise — not a
                      # difficulty signal. Documented in PROTOCOL_CHANGELOG (v1.2.1).
MAX_PCT = 99.5        # measurement ceiling: ≤ 99.5% burn (≥ ~1310 unburned pixels).
                      # Above this, F1 is trivially saturated by an "all-burned" prediction
                      # — the agent's segmentation skill is not measured. Documented in
                      # PROTOCOL_CHANGELOG (v1.2.2).
LOW_MAX_PCT = 1.0     # MIN_PCT < burn_pct ≤ 1%  (hard subset; tests recall on small burns)
MID_MAX_PCT = 20.0    # 1% < burn_pct ≤ 20%
                      # 20% < burn_pct ≤ MAX_PCT goes to high tier


def reorder_image_10band(img_hwc_uint16: np.ndarray) -> np.ndarray:
    """CaBuAr arrays are (H, W, 12) — transpose to (12, H, W) then select bands."""
    img_chw = np.transpose(img_hwc_uint16, (2, 0, 1))  # → (12, H, W)
    return img_chw[CHANNEL_REORDER].copy()


def binarize_mask(mask_hwc_or_hw: np.ndarray) -> np.ndarray:
    """CaBuAr masks are (H, W, 1) bool → squeeze to (H, W) and scale to 0/255."""
    if mask_hwc_or_hw.ndim == 3:
        mask_hwc_or_hw = mask_hwc_or_hw[..., 0]
    return (mask_hwc_or_hw > 0).astype(np.uint8) * 255


def write_geotiff(arr_10band_uint16: np.ndarray, out_path: Path):
    """Write (10, H, W) uint16 as multi-band GeoTIFF with placeholder
    10 m affine — we don't have CaBuAr's CRS, but rasterio readers care
    about shape and pixel size, not the CRS, for our purposes."""
    bands, H, W = arr_10band_uint16.shape
    transform = Affine.scale(10.0, -10.0)
    with rasterio.open(
        out_path,
        "w",
        driver="GTiff",
        height=H,
        width=W,
        count=bands,
        dtype="uint16",
        compress="deflate",
        transform=transform,
    ) as dst:
        for i in range(bands):
            dst.write(arr_10band_uint16[i], i + 1)
        dst.descriptions = ("B02", "B03", "B04", "B08", "B05", "B06", "B07", "B8A", "B11", "B12")


def select_uids(h5_path: Path, n_low: int, n_mid: int, n_high: int) -> list[tuple[str, float]]:
    """Scan all uids, compute burn_pct, stratify and pick deterministically."""
    with h5py.File(h5_path, "r") as f:
        catalog: list[tuple[str, float]] = []
        for uid in f.keys():
            grp = f[uid]
            if "pre_fire" not in grp or "post_fire" not in grp or "mask" not in grp:
                continue
            mask = np.asarray(grp["mask"])
            burn_pct = float((mask > 0).mean() * 100.0)
            catalog.append((uid, burn_pct))

    # Apply measurement floor + ceiling before stratification.
    # Floor: burn_pct < MIN_PCT (~131 px in a 512×512 patch) produces F1 values
    # dominated by single-FP noise. Ceiling: burn_pct > MAX_PCT means a trivial
    # "all-burned" prediction wins on F1, regardless of segmentation skill.
    n_below = sum(1 for c in catalog if c[1] < MIN_PCT)
    n_above = sum(1 for c in catalog if c[1] > MAX_PCT)
    catalog_in_band = [c for c in catalog if MIN_PCT <= c[1] <= MAX_PCT]
    if n_below:
        print(f"  measurement-floor drop:   {n_below} uids with burn_pct < {MIN_PCT}%")
    if n_above:
        print(f"  measurement-ceiling drop: {n_above} uids with burn_pct > {MAX_PCT}%")

    low = sorted([c for c in catalog_in_band if c[1] <= LOW_MAX_PCT])
    mid = sorted([c for c in catalog_in_band if LOW_MAX_PCT < c[1] <= MID_MAX_PCT])
    high = sorted([c for c in catalog_in_band if c[1] > MID_MAX_PCT])
    print(f"  catalog: {len(catalog_in_band)} uids ({len(low)} low / {len(mid)} mid / {len(high)} high)")

    def pick_evenly(tier: list[tuple[str, float]], n: int) -> list[tuple[str, float]]:
        if not tier:
            return []
        if len(tier) <= n:
            return tier
        # Even spacing across the tier (sorted by burn_pct via uid lex order is rough,
        # so re-sort by burn_pct first for cleaner stratification)
        tier_by_pct = sorted(tier, key=lambda c: c[1])
        idxs = [int(round(i * (len(tier_by_pct) - 1) / max(n - 1, 1))) for i in range(n)]
        return [tier_by_pct[i] for i in idxs]

    chosen = pick_evenly(low, n_low) + pick_evenly(mid, n_mid) + pick_evenly(high, n_high)
    return chosen


def main():
    from huggingface_hub import hf_hub_download

    print("Resolving chabud_test.h5 from HF cache (downloading if needed)...", flush=True)
    h5_path = Path(hf_hub_download(
        "DarthReca/california_burned_areas",
        "raw/patched/chabud_test.h5",
        repo_type="dataset",
    ))
    print(f"  resolved: {h5_path}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Selecting 10 samples (3 low / 4 mid / 3 high burn_pct)...")
    chosen = select_uids(h5_path, N_LOW, N_MID, N_HIGH)
    if len(chosen) < 10:
        sys.exit(f"Only {len(chosen)} samples available — adjust tier breakpoints.")

    samples_meta = []
    with h5py.File(h5_path, "r") as f:
        for i, (uid, burn_pct_full) in enumerate(chosen):
            print(f"[{i+1}/{len(chosen)}] {uid}  burn_pct={burn_pct_full:.2f}%")
            grp = f[uid]
            pre_hwc = np.asarray(grp["pre_fire"], dtype=np.uint16)    # (H, W, 12)
            post_hwc = np.asarray(grp["post_fire"], dtype=np.uint16)
            mask_hwc = np.asarray(grp["mask"])                         # (H, W, 1) bool

            H, W, _ = pre_hwc.shape
            assert post_hwc.shape == pre_hwc.shape, f"pre/post shape mismatch on {uid}"
            assert mask_hwc.shape[:2] == (H, W), f"mask shape mismatch on {uid}"

            a = reorder_image_10band(pre_hwc)
            b = reorder_image_10band(post_hwc)
            m = binarize_mask(mask_hwc)
            burn_pct = float((m > 0).mean())

            sample_id = f"burn_{i:02d}"
            sample_dir = DATA_DIR / sample_id
            sample_dir.mkdir(parents=True, exist_ok=True)
            write_geotiff(a, sample_dir / "image_A.tif")
            write_geotiff(b, sample_dir / "image_B.tif")
            from PIL import Image
            Image.fromarray(m).save(sample_dir / "mask.png")

            samples_meta.append({
                "id": sample_id,
                "image_a": f"data/{sample_id}/image_A.tif",
                "image_b": f"data/{sample_id}/image_B.tif",
                "label": f"data/{sample_id}/mask.png",
                "burn_pct": round(burn_pct, 4),
                "source_uid": uid,
                "shape": [int(H), int(W)],
            })

    SAMPLES_JSON.write_text(json.dumps(samples_meta, indent=2))
    print(f"\nWrote {len(samples_meta)} samples to {DATA_DIR}")
    print(f"Manifest: {SAMPLES_JSON}")


if __name__ == "__main__":
    main()
