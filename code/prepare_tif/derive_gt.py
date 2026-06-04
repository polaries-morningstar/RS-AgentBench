"""Derive task-specific ground-truth labels from shared WorldCover rasters.

Reads each AOI's `worldcover.tif` (single-band uint8, raw WC class IDs) and
produces a label PNG per task per AOI.

Tasks
-----
- T1 water       : binary, foreground = WC ∈ {80, 90, 95}        (water+wetland+mangrove)
- T2 vegetation  : binary, foreground = WC ∈ {10, 20, 30, 40}    (tree+shrub+grass+crop)
- T4 landcover   : 4-class, codes 0/1/2/3 + 255 ignore
                    0 = water        (WC 80, 90, 95)
                    1 = vegetation   (WC 10, 20, 30, 40, 100)
                    2 = built        (WC 50)
                    3 = other        (WC 60, 70 — bare, snow)

Output layout
-------------
benchmark/datasets_tif/<task>/data/<aoi_name>/
    label.png       (uint8 single-band, sized to match input.tif)

Plus a per-task samples_v1.json that lists which AOI is which sample,
including foreground % and class-density stratum (for stratified sampling).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

from aois import get_aois  # type: ignore[import-not-found]


SHARED_ROOT = Path(__file__).resolve().parent.parent / "datasets_tif" / "shared"
TASK_ROOT = Path(__file__).resolve().parent.parent / "datasets_tif"

# Class membership
WC_WATER = (80, 90, 95)
WC_VEG = (10, 20, 30, 40)
WC_BUILT = (50,)
WC_OTHER = (60, 70, 100)
WC_NODATA = (0,)


def load_worldcover(aoi_name: str) -> np.ndarray:
    p = SHARED_ROOT / aoi_name / "worldcover.tif"
    with rasterio.open(p) as src:
        return src.read(1)


def make_t1_water(wc: np.ndarray) -> np.ndarray:
    """Binary mask: 255 where water, 0 otherwise."""
    return np.where(np.isin(wc, WC_WATER), 255, 0).astype(np.uint8)


def make_t2_vegetation(wc: np.ndarray) -> np.ndarray:
    """Binary mask: 255 where vegetation, 0 otherwise."""
    return np.where(np.isin(wc, WC_VEG), 255, 0).astype(np.uint8)


def make_t4_landcover(wc: np.ndarray) -> np.ndarray:
    """4-class label image with ignore=255.

    Output codes:
      0 = water
      1 = vegetation
      2 = built
      3 = other (bare/snow)
      255 = nodata / ignore
    """
    out = np.full_like(wc, 255, dtype=np.uint8)
    out[np.isin(wc, WC_WATER)] = 0
    out[np.isin(wc, WC_VEG)] = 1
    out[np.isin(wc, WC_BUILT)] = 2
    out[np.isin(wc, WC_OTHER)] = 3
    return out


def class_summary(wc: np.ndarray) -> dict:
    total = wc.size
    return {
        "water_pct": float(np.isin(wc, WC_WATER).sum() / total * 100),
        "veg_pct": float(np.isin(wc, WC_VEG).sum() / total * 100),
        "built_pct": float(np.isin(wc, WC_BUILT).sum() / total * 100),
        "other_pct": float(np.isin(wc, WC_OTHER).sum() / total * 100),
        "nodata_pct": float(np.isin(wc, WC_NODATA).sum() / total * 100),
    }


def density_stratum(pct: float, low: float = 15, high: float = 35) -> str:
    """Classify foreground density into low / mid / high tertiles."""
    if pct < low:
        return "low"
    if pct < high:
        return "mid"
    return "high"


def class_entropy(wc: np.ndarray) -> float:
    """Shannon entropy over 4-class T4 distribution (water/veg/built/other)."""
    cls = make_t4_landcover(wc)
    probs = []
    for c in range(4):
        n = (cls == c).sum()
        if n > 0:
            probs.append(n / cls.size)
    return float(-sum(p * np.log2(p) for p in probs))


def write_label_png(arr: np.ndarray, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).save(out_path)


# Sentinel-2 band metadata for the bands.json sidecar (handed to the agent)
S2_BAND_INFO = {
    "B02": {"name": "Blue", "wavelength_nm": 492, "native_resolution_m": 10},
    "B03": {"name": "Green", "wavelength_nm": 559, "native_resolution_m": 10},
    "B04": {"name": "Red", "wavelength_nm": 665, "native_resolution_m": 10},
    "B05": {"name": "RedEdge1", "wavelength_nm": 704, "native_resolution_m": 20},
    "B06": {"name": "RedEdge2", "wavelength_nm": 740, "native_resolution_m": 20},
    "B07": {"name": "RedEdge3", "wavelength_nm": 783, "native_resolution_m": 20},
    "B08": {"name": "NIR", "wavelength_nm": 833, "native_resolution_m": 10},
    "B8A": {"name": "NarrowNIR", "wavelength_nm": 865, "native_resolution_m": 20},
    "B11": {"name": "SWIR1", "wavelength_nm": 1610, "native_resolution_m": 20},
    "B12": {"name": "SWIR2", "wavelength_nm": 2190, "native_resolution_m": 20},
}


def make_bands_json(aoi_name: str) -> dict:
    """Read input.tif band order and produce a sidecar mapping channel index → band info."""
    p = SHARED_ROOT / aoi_name / "input.tif"
    with rasterio.open(p) as src:
        descs = src.descriptions  # tuple of band names like ("B02", "B03", ...)
    bands = []
    for i, code in enumerate(descs):
        info = dict(S2_BAND_INFO.get(code, {}))
        info["index"] = i  # 0-based for numpy axis=0
        info["band_index_1based"] = i + 1  # 1-based for rasterio.read(N)
        info["code"] = code
        bands.append(info)
    return {
        "source": "Sentinel-2 L2A surface reflectance (Microsoft Planetary Computer)",
        "all_resampled_to_m": 10,
        "dtype": "uint16",
        "scale_factor": 10000,  # divide by 10000 to get reflectance 0-1
        "bands": bands,
    }


def derive_for_aoi(aoi: dict) -> dict:
    name = aoi["name"]
    wc = load_worldcover(name)
    summary = class_summary(wc)
    entropy = class_entropy(wc)

    # Per-task: write label + create symlink to shared input.tif + copy bands.json sidecar
    shared_input = SHARED_ROOT / name / "input.tif"
    bands_json = make_bands_json(name)

    for task_name, mask in [
        ("water", make_t1_water(wc)),
        ("vegetation", make_t2_vegetation(wc)),
        ("landcover", make_t4_landcover(wc)),
    ]:
        sample_dir = TASK_ROOT / task_name / "data" / name
        sample_dir.mkdir(parents=True, exist_ok=True)
        write_label_png(mask, sample_dir / "label.png")
        # Symlink to the shared multiband TIFF
        link = sample_dir / "input.tif"
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(shared_input.resolve())
        # Bands sidecar so the agent knows which channel is which
        (sample_dir / "bands.json").write_text(json.dumps(bands_json, indent=2))

    return {
        "name": name,
        "summary": summary,
        "entropy": entropy,
        "t1_water_stratum": density_stratum(summary["water_pct"]),
        "t2_vegetation_stratum": density_stratum(summary["veg_pct"]),
    }


def build_task_samples(stats: list[dict]):
    """Write samples_v1.json for each task with stratification info."""
    tasks = {
        "water": ("T1 water", "t1_water_stratum", "water_pct"),
        "vegetation": ("T2 vegetation", "t2_vegetation_stratum", "veg_pct"),
        "landcover": ("T4 landcover (4-class)", None, None),
    }
    for task_name, (display, stratum_key, pct_key) in tasks.items():
        samples = []
        for s in stats:
            entry = {
                "id": s["name"],
                "image": f"data/{s['name']}/input.tif",     # symlink target (resolved at copy-time)
                "label": f"data/{s['name']}/label.png",
            }
            if stratum_key:
                entry["fg_pct"] = round(s["summary"][pct_key], 2)
                entry["density_stratum"] = s[stratum_key]
            else:
                entry["entropy"] = round(s["entropy"], 3)
                entry["class_pct"] = {k.replace("_pct", ""): round(v, 2) for k, v in s["summary"].items()
                                       if k.endswith("_pct") and not k.startswith("nodata")}
            samples.append(entry)

        out_path = TASK_ROOT / task_name / "samples_v1.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(samples, indent=2, ensure_ascii=False))
        print(f"  wrote {out_path}")


def main():
    aois = get_aois()
    stats = []
    print(f"Deriving GT for {len(aois)} AOI(s) ...")
    for aoi in aois:
        try:
            s = derive_for_aoi(aoi)
            stats.append(s)
            print(f"  ✓ {s['name']}: water={s['summary']['water_pct']:.1f}% veg={s['summary']['veg_pct']:.1f}% "
                  f"built={s['summary']['built_pct']:.1f}% entropy={s['entropy']:.2f}")
        except FileNotFoundError as e:
            print(f"  ✗ {aoi['name']}: {e}")

    print()
    print("Building per-task samples_v1.json ...")
    build_task_samples(stats)

    # Print stratification overview
    print("\n=== Stratification overview ===")
    print("\nT1 water density (low<15%, mid 15-35%, high≥35%):")
    for s in stats:
        print(f"  {s['name']:<22} water={s['summary']['water_pct']:>5.1f}% → {s['t1_water_stratum']}")

    print("\nT2 vegetation density:")
    for s in stats:
        print(f"  {s['name']:<22} veg={s['summary']['veg_pct']:>5.1f}% → {s['t2_vegetation_stratum']}")

    print("\nT4 class entropy (higher = more diverse):")
    for s in sorted(stats, key=lambda x: -x["entropy"]):
        print(f"  {s['name']:<22} entropy={s['entropy']:>4.2f}")


if __name__ == "__main__":
    main()
