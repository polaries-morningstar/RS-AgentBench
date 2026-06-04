"""Convert OSCD MSI parquet (HF blanchon/OSCD_MSI) into 10-band TIFF pairs
preserving the native city-level crop size, with the channel order T1/T2/T4
expects.

Output:
  datasets_tif/change/data/<id>/image_A.tif    (10 bands, uint16, native HxW)
  datasets_tif/change/data/<id>/image_B.tif    (10 bands, uint16, native HxW)
  datasets_tif/change/data/<id>/mask.png       (uint8, 0/255 binary change)
  datasets_tif/change/samples_v1.json          (sample metadata incl. shape)

Channel reorder:
  OSCD provides 13 Sentinel-2 bands in ESA order:
    B01, B02, B03, B04, B05, B06, B07, B08, B8A, B09, B10, B11, B12
  T1/T2/T4 use 10 bands in this order:
    B02, B03, B04, B08, B05, B06, B07, B8A, B11, B12
  → indices [1, 2, 3, 7, 4, 5, 6, 8, 11, 12] from the OSCD 13-band stack.

Sizing: native OSCD city crops vary 241x385 to 824x716. We keep them as-is —
no resampling — so the imagery remains true 10 m/pixel Sentinel-2. The
runner must therefore look up the per-sample shape from samples_v1.json
when validating the agent's output.
"""
from __future__ import annotations

import io
import json
import os
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import Affine

ROOT = Path(__file__).resolve().parent.parent
PARQUET = ROOT / "datasets_tif/oscd_raw/data/test-00000-of-00001.parquet"
OUT_ROOT = ROOT / "datasets_tif/change"
DATA_DIR = OUT_ROOT / "data"
SAMPLES_JSON = OUT_ROOT / "samples_v1.json"

# T1/T2/T4 layout: B02, B03, B04, B08, B05, B06, B07, B8A, B11, B12
CHANNEL_REORDER = [1, 2, 3, 7, 4, 5, 6, 8, 11, 12]


def reorder_image_10band(img_13band_uint16: np.ndarray) -> np.ndarray:
    """Reorder OSCD's 13-band stack into our 10-band layout, preserving
    the native (H, W). No resampling — reflectance values stay exact."""
    return img_13band_uint16[CHANNEL_REORDER].copy()


def binarize_mask(mask: np.ndarray) -> np.ndarray:
    """Convert any binary mask (bool or 0/1 int) to uint8 0/255."""
    return (mask > 0).astype(np.uint8) * 255


def write_geotiff(arr_10band_uint16: np.ndarray, out_path: Path):
    """Write (10, H, W) uint16 array as multi-band GeoTIFF. We don't have
    the original CRS from OSCD parquet, so we use a placeholder 10m affine
    so any rasterio reader behaves predictably (`src.shape`, descriptions)."""
    bands, H, W = arr_10band_uint16.shape
    transform = Affine.scale(10.0, -10.0)  # placeholder 10m pixels
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


def main():
    if not PARQUET.exists():
        sys.exit(f"OSCD parquet missing at {PARQUET}. Run snapshot_download first.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Stream rows via pyarrow
    try:
        import pyarrow.parquet as pq
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing optional dependency 'pyarrow' required to read the OSCD "
            "parquet file. Install benchmark dependencies again, e.g. "
            "`cd benchmark && uv sync`, then rerun prepare_tif/fetch_oscd_to_tif.py."
        ) from exc
    from PIL import Image

    pf = pq.ParquetFile(PARQUET)
    samples_meta = []

    row_idx = 0
    for batch in pf.iter_batches(batch_size=1):
        d = batch.to_pylist()[0]
        print(f"[{row_idx+1}/10] decoding image pair ...", flush=True)
        img_a_full = np.asarray(d["image1"], dtype=np.uint16)  # (13, H, W)
        img_b_full = np.asarray(d["image2"], dtype=np.uint16)

        mask_struct = d["mask"]
        mask_bytes = mask_struct["bytes"] if isinstance(mask_struct, dict) else mask_struct
        mask_pil = Image.open(io.BytesIO(mask_bytes))
        mask_full = np.array(mask_pil)
        if mask_full.ndim == 3:
            mask_full = mask_full[..., 0]

        H_img, W_img = img_a_full.shape[1:]
        H_mask, W_mask = mask_full.shape
        # OSCD masks may have a slightly different shape from the imagery.
        # Pad mask to image shape with zeros (no change in unlabelled regions).
        if (H_mask, W_mask) != (H_img, W_img):
            print(
                f"  mask {mask_full.shape} != image {(H_img, W_img)}; padding mask",
                flush=True,
            )
            new = np.zeros((H_img, W_img), dtype=mask_full.dtype)
            new[: min(H_mask, H_img), : min(W_mask, W_img)] = mask_full[
                : min(H_mask, H_img), : min(W_mask, W_img)
            ]
            mask_full = new

        # Native size: just reorder bands, no resampling
        a_out = reorder_image_10band(img_a_full)
        b_out = reorder_image_10band(img_b_full)
        m_out = binarize_mask(mask_full)
        change_pct = float((m_out > 0).mean())

        sample_id = f"oscd_test_{row_idx:02d}"
        sample_dir = DATA_DIR / sample_id
        sample_dir.mkdir(parents=True, exist_ok=True)

        write_geotiff(a_out, sample_dir / "image_A.tif")
        write_geotiff(b_out, sample_dir / "image_B.tif")
        Image.fromarray(m_out).save(sample_dir / "mask.png")

        # Paths in the manifest are joined as `{label_dir}.parent / label`
        # by the runner, where label_dir = datasets_tif/change/data. The
        # convention shared with T1/T2/T4 samples_v1.json is to prefix with
        # 'data/' so the runner resolves to datasets_tif/change/data/<id>/...
        samples_meta.append(
            {
                "id": sample_id,
                "image_a": f"data/{sample_id}/image_A.tif",
                "image_b": f"data/{sample_id}/image_B.tif",
                "label": f"data/{sample_id}/mask.png",
                "change_pct": round(change_pct, 4),
                "source_row": row_idx,
                "shape": [int(H_img), int(W_img)],  # native HxW (used by runner)
            }
        )
        print(
            f"  ✓ {sample_id}: shape={H_img}x{W_img}, change_pct={change_pct:.4f}",
            flush=True,
        )

        del img_a_full, img_b_full, mask_full, a_out, b_out, m_out
        row_idx += 1

    SAMPLES_JSON.write_text(json.dumps(samples_meta, indent=2))
    print(f"\nWrote {len(samples_meta)} samples to {DATA_DIR}")
    print(f"Manifest: {SAMPLES_JSON}")


if __name__ == "__main__":
    main()
