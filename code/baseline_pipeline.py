"""
RS-AgentBench fixed-pipeline baseline.

Replaces the LLM agent with **textbook spectral-index thresholding** (no learning,
no LLM, no agent). Used to ground the agent's value: if a 5-line domain-expert
script outperforms a $80/run agent, the agent's value proposition needs revisiting.

Tasks and formulas (no tuning — all thresholds are textbook):
  T1 water:     MNDWI = (B03 - B11) / (B03 + B11);  water if MNDWI > 0
                (Xu 2006, "Modification of normalised difference water index ...")
  T2 change:    CVA magnitude across all 10 bands; Otsu threshold
                (Singh 1989, "Digital change detection techniques using remotely
                sensed data")
  T3 landcover: rule-tree on NDVI / MNDWI / NDBI;
                  water  if MNDWI > 0
                  veg    elif NDVI  > 0.30
                  built  elif NDBI  > 0
                  other  else
                (Tucker 1979 NDVI; Xu 2006 MNDWI; Zha 2003 NDBI)
  T4 burn:      dNBR = NBR_pre - NBR_post; burn if dNBR > 0.27
                (Key & Benson 2006 "Landscape Assessment", USGS standard)

Channel layout (all tasks): 0=B02 1=B03 2=B04 3=B08 4=B05 5=B06 6=B07 7=B8A 8=B11 9=B12
Reflectance scaled by 10000.

Output: results/<task>_baseline_<TS>/<sample>/{output.png, metrics.json}
followed by an aggregate summary.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from datetime import datetime

import numpy as np
import rasterio
from PIL import Image
from skimage.filters import threshold_otsu

BENCH_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH_DIR))
from evaluation.metrics import evaluate_binary, evaluate_multiclass

# Band indices (0-indexed) — consistent across tasks
B_BLUE = 0   # B02
B_GREEN = 1  # B03
B_RED = 2    # B04
B_NIR = 3    # B08
B_NIR2 = 7   # B8A
B_SWIR1 = 8  # B11
B_SWIR2 = 9  # B12

SCALE = 10000.0


def _load_tif(path: Path) -> np.ndarray:
    """Load 10-band Sentinel-2 TIF as (10, H, W) float32 reflectance [0,~1.5]."""
    with rasterio.open(path) as src:
        arr = src.read().astype(np.float32) / SCALE
    return arr


def _safe_div(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    """Safe division avoiding div-by-zero; returns 0 where denom is 0."""
    out = np.zeros_like(num, dtype=np.float32)
    mask = den != 0
    out[mask] = num[mask] / den[mask]
    return out


def _ndvi(img: np.ndarray) -> np.ndarray:
    return _safe_div(img[B_NIR] - img[B_RED], img[B_NIR] + img[B_RED])


def _mndwi(img: np.ndarray) -> np.ndarray:
    return _safe_div(img[B_GREEN] - img[B_SWIR1], img[B_GREEN] + img[B_SWIR1])


def _ndbi(img: np.ndarray) -> np.ndarray:
    return _safe_div(img[B_SWIR1] - img[B_NIR], img[B_SWIR1] + img[B_NIR])


def _nbr(img: np.ndarray) -> np.ndarray:
    return _safe_div(img[B_NIR] - img[B_SWIR2], img[B_NIR] + img[B_SWIR2])


# ---------------------------------------------------------------------------
# Task pipelines
# ---------------------------------------------------------------------------

def water_pipeline(img: np.ndarray) -> np.ndarray:
    """MNDWI > 0 → water. Returns uint8 mask (0/255)."""
    mask = _mndwi(img) > 0
    return (mask.astype(np.uint8) * 255)


def change_pipeline(img_a: np.ndarray, img_b: np.ndarray) -> np.ndarray:
    """Change Vector Analysis: L2 norm of spectral difference, Otsu threshold."""
    diff = img_b - img_a  # (10, H, W)
    cva_mag = np.sqrt((diff ** 2).sum(axis=0))  # (H, W)
    # Otsu on the magnitude — fully automatic threshold
    try:
        thr = float(threshold_otsu(cva_mag))
    except Exception:
        thr = float(np.median(cva_mag) + 2 * np.std(cva_mag))
    return ((cva_mag > thr).astype(np.uint8) * 255)


def landcover_pipeline(img: np.ndarray) -> np.ndarray:
    """Rule-tree on indices. Returns uint8 mask with values 0,1,2,3."""
    mndwi = _mndwi(img)
    ndvi = _ndvi(img)
    ndbi = _ndbi(img)
    out = np.full(img.shape[1:], 3, dtype=np.uint8)  # default = other
    out[ndbi > 0] = 2          # built-up
    out[ndvi > 0.30] = 1       # vegetation (overrides built where both signal)
    out[mndwi > 0] = 0         # water (overrides everything)
    return out


def burn_pipeline(img_pre: np.ndarray, img_post: np.ndarray) -> np.ndarray:
    """dNBR > 0.27 → burn (Key & Benson 2006 'low-moderate' threshold)."""
    nbr_pre = _nbr(img_pre)
    nbr_post = _nbr(img_post)
    dnbr = nbr_pre - nbr_post
    return ((dnbr > 0.27).astype(np.uint8) * 255)


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_water(out_dir: Path) -> list[dict]:
    samples = json.loads((BENCH_DIR / "datasets_tif/water/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/water"
    rows = []
    for s in samples:
        sid = s["id"]
        sd = out_dir / sid
        sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        img = _load_tif(data_dir / s["image"])
        mask = water_pipeline(img)
        Image.fromarray(mask).save(sd / "output.png")
        gt = data_dir / s["label"]
        m = evaluate_binary(sd / "output.png", gt)
        m["sample_id"] = sid
        m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["f1"]
        (sd / "metrics.json").write_text(json.dumps(m, indent=2))
        rows.append(m)
    return rows


def run_change(out_dir: Path) -> list[dict]:
    samples = json.loads((BENCH_DIR / "datasets_tif/change/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/change"
    rows = []
    for s in samples:
        sid = s["id"]
        sd = out_dir / sid
        sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        img_a = _load_tif(data_dir / s["image_a"])
        img_b = _load_tif(data_dir / s["image_b"])
        mask = change_pipeline(img_a, img_b)
        Image.fromarray(mask).save(sd / "output.png")
        gt = data_dir / s["label"]
        m = evaluate_binary(sd / "output.png", gt)
        m["sample_id"] = sid
        m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["f1"]
        (sd / "metrics.json").write_text(json.dumps(m, indent=2))
        rows.append(m)
    return rows


def run_landcover(out_dir: Path) -> list[dict]:
    samples = json.loads((BENCH_DIR / "datasets_tif/landcover/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/landcover"
    rows = []
    for s in samples:
        sid = s["id"]
        sd = out_dir / sid
        sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        img = _load_tif(data_dir / s["image"])
        mask = landcover_pipeline(img)
        Image.fromarray(mask).save(sd / "output.png")
        gt = data_dir / s["label"]
        m = evaluate_multiclass(sd / "output.png", gt, num_classes=4, ignore_index=255)
        m["sample_id"] = sid
        m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["oa"]
        (sd / "metrics.json").write_text(json.dumps(m, indent=2))
        rows.append(m)
    return rows


def run_burn(out_dir: Path) -> list[dict]:
    samples = json.loads((BENCH_DIR / "datasets_tif/burn/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/burn"
    rows = []
    for s in samples:
        sid = s["id"]
        sd = out_dir / sid
        sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        img_pre = _load_tif(data_dir / s["image_a"])
        img_post = _load_tif(data_dir / s["image_b"])
        mask = burn_pipeline(img_pre, img_post)
        Image.fromarray(mask).save(sd / "output.png")
        gt = data_dir / s["label"]
        m = evaluate_binary(sd / "output.png", gt)
        m["sample_id"] = sid
        m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["f1"]
        (sd / "metrics.json").write_text(json.dumps(m, indent=2))
        rows.append(m)
    return rows


def main() -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    root = BENCH_DIR / "results" / f"_baseline_{ts}"
    root.mkdir(parents=True, exist_ok=True)
    print(f"baseline output root: {root}")
    print()

    summary = {}
    for task, runner in [
        ("water", run_water),
        ("change", run_change),
        ("landcover", run_landcover),
        ("burn", run_burn),
    ]:
        print(f"=== {task} ===")
        td = root / task
        rows = runner(td)
        primary = [r["primary_metric"] for r in rows]
        co_metric = "iou" if "iou" in rows[0] else "kappa"
        co = [r.get(co_metric, 0.0) for r in rows]
        summary[task] = {
            "n": len(rows),
            "primary_mean": float(np.mean(primary)),
            "primary_median": float(np.median(primary)),
            "primary_min": float(np.min(primary)),
            "primary_max": float(np.max(primary)),
            "co_metric_name": co_metric,
            "co_mean": float(np.mean(co)),
            "elapsed_total_s": round(sum(r["elapsed_seconds"] for r in rows), 3),
            "per_sample": [
                {"id": r["sample_id"], "primary": r["primary_metric"], co_metric: r.get(co_metric, 0.0)}
                for r in rows
            ],
        }
        print(f"  n={len(rows)}  primary_mean={summary[task]['primary_mean']:.3f} "
              f"({co_metric}_mean={summary[task]['co_mean']:.3f})  "
              f"wall={summary[task]['elapsed_total_s']:.2f}s")

    (root / "summary.json").write_text(json.dumps(summary, indent=2))
    print()
    print(f"summary written: {root}/summary.json")


if __name__ == "__main__":
    main()
