"""Fetch Sentinel-2 L2A multiband tiles + matching ESA WorldCover GT.

For each AOI:
  1. Search Planetary Computer for the cleanest S2 L2A scene in 2024-2025.
  2. Read 10 spectral bands (B02, B03, B04, B05, B06, B07, B08, B8A, B11, B12).
     20 m bands are resampled to 10 m via bilinear so all bands share the
     same 1024 × 1024 grid.
  3. Crop to a 1024 × 1024 px window centred on the AOI in the scene's UTM CRS.
  4. Write as a multiband GeoTIFF preserving CRS + transform.
  5. Search & crop ESA WorldCover (10 m) for the same footprint, reproject
     to S2's UTM grid using nearest neighbour, save as 1-band uint8 GeoTIFF.

Written to: benchmark/datasets_tif/shared/<aoi_name>/{input.tif, worldcover.tif, meta.json}
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import numpy as np
import pystac_client
import planetary_computer as pc
import rasterio
from rasterio.transform import Affine
from rasterio.warp import Resampling, reproject, transform_bounds
from rasterio.windows import Window, from_bounds

from aois import get_aois  # type: ignore[import-not-found]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PC_STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

S2_BANDS_10M = ["B02", "B03", "B04", "B08"]                   # 10 m native
S2_BANDS_20M = ["B05", "B06", "B07", "B8A", "B11", "B12"]     # 20 m, will resample to 10 m
S2_BANDS_ALL = S2_BANDS_10M + S2_BANDS_20M                    # 10 bands total

# Output grid: 1024 × 1024 px @ 10 m = 10.24 km × 10.24 km
TILE_SIZE_PX = 1024
TILE_RES_M = 10.0

DATE_RANGE = "2024-01-01/2025-12-31"
MAX_CLOUD = 15      # initial filter
MAX_ITEMS = 30      # how many candidates to inspect

OUT_ROOT = Path(__file__).resolve().parent.parent / "datasets_tif" / "shared"


# ---------------------------------------------------------------------------
# STAC search with retry (PC API is flaky)
# ---------------------------------------------------------------------------

def _open_catalog():
    return pystac_client.Client.open(PC_STAC_URL, modifier=pc.sign_inplace)


def _search_with_retry(catalog, *, attempts: int = 4, **kwargs):
    last_err = None
    for i in range(attempts):
        try:
            return list(catalog.search(**kwargs).items())
        except Exception as e:  # noqa: BLE001
            last_err = e
            wait = 5 * (i + 1)
            print(f"    STAC search failed ({type(e).__name__}); retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"STAC search failed after {attempts} attempts: {last_err}")


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _utm_crs_for_lonlat(lon: float, lat: float) -> str:
    """Return EPSG code for the UTM zone that contains (lon, lat)."""
    zone = int((lon + 180) / 6) + 1
    epsg = 32600 + zone if lat >= 0 else 32700 + zone
    return f"EPSG:{epsg}"


def _centred_window_in_utm(lon: float, lat: float, utm_crs: str) -> tuple[float, float, float, float]:
    """1024 × 1024 px @ 10 m bbox in UTM, centred on (lon, lat)."""
    # First reproject the AOI point to UTM
    x, y = transform_bounds("EPSG:4326", utm_crs, lon, lat, lon, lat)[:2]
    half = TILE_SIZE_PX * TILE_RES_M / 2  # 5120 m
    return (x - half, y - half, x + half, y + half)  # (minx, miny, maxx, maxy)


# ---------------------------------------------------------------------------
# Sentinel-2 fetch
# ---------------------------------------------------------------------------

def find_best_scene(catalog, lon: float, lat: float):
    """Return the lowest-cloud S2 L2A item covering the AOI in DATE_RANGE."""
    bbox = [lon - 0.05, lat - 0.05, lon + 0.05, lat + 0.05]
    items = _search_with_retry(
        catalog,
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=DATE_RANGE,
        query={"eo:cloud_cover": {"lt": MAX_CLOUD}},
        max_items=MAX_ITEMS,
    )
    if not items:
        # Loosen cloud cover filter
        items = _search_with_retry(
            catalog,
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=DATE_RANGE,
            query={"eo:cloud_cover": {"lt": 40}},
            max_items=MAX_ITEMS,
        )
    if not items:
        raise RuntimeError(f"No S2 L2A scenes at ({lon}, {lat}) in {DATE_RANGE}")
    items.sort(key=lambda x: x.properties.get("eo:cloud_cover", 100))
    return items[0]


def _read_band_to_grid(asset_url: str, dst_bbox_utm: tuple, dst_crs: str,
                       dst_size_px: int = TILE_SIZE_PX) -> np.ndarray:
    """Open a band asset and resample/crop to the target UTM grid."""
    minx, miny, maxx, maxy = dst_bbox_utm
    dst_transform = Affine(TILE_RES_M, 0.0, minx, 0.0, -TILE_RES_M, maxy)

    with rasterio.open(asset_url) as src:
        dst = np.zeros((dst_size_px, dst_size_px), dtype=np.uint16)
        reproject(
            source=rasterio.band(src, 1),
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=dst_transform,
            dst_crs=dst_crs,
            resampling=Resampling.bilinear,
        )
    return dst


def fetch_s2_tile(item, lon: float, lat: float) -> tuple[np.ndarray, dict]:
    """Read 10 bands stacked as (10, H, W). Returns (data, meta)."""
    utm_crs = _utm_crs_for_lonlat(lon, lat)
    bbox_utm = _centred_window_in_utm(lon, lat, utm_crs)

    arrs = []
    for band in S2_BANDS_ALL:
        asset = item.assets[band]
        a = _read_band_to_grid(asset.href, bbox_utm, utm_crs)
        arrs.append(a)
        print(f"      {band}: shape={a.shape} min={a.min()} max={a.max()}")

    data = np.stack(arrs, axis=0)  # (bands, H, W)

    transform = Affine(TILE_RES_M, 0.0, bbox_utm[0], 0.0, -TILE_RES_M, bbox_utm[3])
    meta = {
        "crs": utm_crs,
        "transform": transform,
        "bbox_utm": bbox_utm,
        "scene_id": item.id,
        "datetime": item.datetime.isoformat() if item.datetime else None,
        "cloud_cover": item.properties.get("eo:cloud_cover"),
        "bands": S2_BANDS_ALL,
    }
    return data, meta


def write_multiband_tif(path: Path, data: np.ndarray, meta: dict):
    """Write (bands, H, W) array as multiband GeoTIFF."""
    bands, h, w = data.shape
    profile = {
        "driver": "GTiff",
        "dtype": "uint16",
        "count": bands,
        "height": h,
        "width": w,
        "crs": meta["crs"],
        "transform": meta["transform"],
        "compress": "deflate",
        "predictor": 2,
        "tiled": True,
    }
    with rasterio.open(path, "w", **profile) as dst:
        for i in range(bands):
            dst.write(data[i], i + 1)
            dst.set_band_description(i + 1, meta["bands"][i])


# ---------------------------------------------------------------------------
# WorldCover fetch (single uint8 raster, reproject to S2 grid)
# ---------------------------------------------------------------------------

def fetch_worldcover(catalog, meta: dict) -> np.ndarray:
    """Return WorldCover map cropped + reprojected to the S2 tile grid."""
    crs = meta["crs"]
    minx, miny, maxx, maxy = meta["bbox_utm"]
    # Reproject UTM bbox to WGS84 for STAC search
    bbox_ll = transform_bounds(crs, "EPSG:4326", minx, miny, maxx, maxy)

    items = _search_with_retry(
        catalog,
        collections=["esa-worldcover"],
        bbox=bbox_ll,
        max_items=4,
    )
    if not items:
        raise RuntimeError(f"No WorldCover for bbox {bbox_ll}")
    # Prefer the most recent year (2021 v2 if available)
    items.sort(key=lambda it: it.properties.get("esa_worldcover:product_version", ""), reverse=True)

    dst_transform = meta["transform"]
    dst = np.zeros((TILE_SIZE_PX, TILE_SIZE_PX), dtype=np.uint8)

    for it in items:
        asset = it.assets["map"]
        with rasterio.open(asset.href) as src:
            tmp = np.zeros_like(dst)
            reproject(
                source=rasterio.band(src, 1),
                destination=tmp,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=dst_transform,
                dst_crs=crs,
                resampling=Resampling.nearest,
            )
            # Only fill pixels not yet covered (different WC tiles cover
            # disjoint footprints — overlay them)
            mask = (dst == 0) & (tmp != 0)
            dst[mask] = tmp[mask]

    return dst


def write_singleband_tif(path: Path, data: np.ndarray, meta: dict, dtype="uint8"):
    h, w = data.shape
    profile = {
        "driver": "GTiff",
        "dtype": dtype,
        "count": 1,
        "height": h,
        "width": w,
        "crs": meta["crs"],
        "transform": meta["transform"],
        "compress": "deflate",
        "tiled": True,
    }
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data, 1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_aoi(aoi: dict, catalog, out_root: Path, force: bool = False) -> dict:
    out_dir = out_root / aoi["name"]
    out_dir.mkdir(parents=True, exist_ok=True)
    input_tif = out_dir / "input.tif"
    wc_tif = out_dir / "worldcover.tif"
    meta_json = out_dir / "meta.json"

    if input_tif.exists() and wc_tif.exists() and meta_json.exists() and not force:
        print(f"  [{aoi['name']}] cached — skipping")
        return json.loads(meta_json.read_text())

    print(f"  [{aoi['name']}] searching S2 ...")
    item = find_best_scene(catalog, aoi["lon"], aoi["lat"])
    print(f"    → {item.id} cloud={item.properties.get('eo:cloud_cover'):.1f}%")

    print(f"  [{aoi['name']}] reading 10 bands ...")
    data, meta = fetch_s2_tile(item, aoi["lon"], aoi["lat"])
    write_multiband_tif(input_tif, data, meta)

    print(f"  [{aoi['name']}] reading WorldCover ...")
    wc = fetch_worldcover(catalog, meta)
    write_singleband_tif(wc_tif, wc, meta)

    # Class breakdown
    unique, counts = np.unique(wc, return_counts=True)
    cls_dist = {int(c): int(n) for c, n in zip(unique, counts)}

    out_meta = {
        "aoi": aoi,
        "scene_id": meta["scene_id"],
        "scene_datetime": meta["datetime"],
        "cloud_cover_pct": meta["cloud_cover"],
        "bands": meta["bands"],
        "tile_size_px": TILE_SIZE_PX,
        "tile_res_m": TILE_RES_M,
        "crs": meta["crs"],
        "bbox_utm": list(meta["bbox_utm"]),
        "worldcover_class_pixels": cls_dist,
    }
    meta_json.write_text(json.dumps(out_meta, indent=2, ensure_ascii=False))
    return out_meta


def main():
    parser = argparse.ArgumentParser(description="Fetch S2 + WorldCover for benchmark AOIs")
    parser.add_argument("--aoi", help="Process a single AOI by name (e.g., lake_geneva_ch)")
    parser.add_argument("--force", action="store_true", help="Re-download even if cached")
    args = parser.parse_args()

    aois = get_aois()
    if args.aoi:
        aois = [a for a in aois if a["name"] == args.aoi]
        if not aois:
            print(f"AOI '{args.aoi}' not found")
            return

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    catalog = _open_catalog()

    print(f"Processing {len(aois)} AOI(s) → {OUT_ROOT}")
    results = {}
    for aoi in aois:
        try:
            results[aoi["name"]] = process_aoi(aoi, catalog, OUT_ROOT, force=args.force)
        except Exception as e:  # noqa: BLE001
            print(f"  [{aoi['name']}] FAILED: {type(e).__name__}: {e}")
            results[aoi["name"]] = {"error": str(e)}

    # Summary
    print("\n=== Summary ===")
    for name, m in results.items():
        if "error" in m:
            print(f"  ✗ {name}: {m['error']}")
        else:
            cls = m["worldcover_class_pixels"]
            top = sorted(cls.items(), key=lambda kv: -kv[1])[:3]
            print(f"  ✓ {name}  {m['cloud_cover_pct']:.1f}% cloud  top classes: {top}")


if __name__ == "__main__":
    main()
