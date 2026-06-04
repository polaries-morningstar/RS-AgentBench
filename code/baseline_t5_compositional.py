"""
Baseline cluster for T5 (compositional spatial query).

Each variant is one classical pipeline applied uniformly to all 10 samples.
Variants 1-3 are "naive" — single formula, ignores per-sample query.
Variant 4 is "engineering upper bound" — manually written if-else router that
looks up the per-sample target/reference/op from samples_v1.json and runs
the optimal pipeline. This is what an expert engineer would write IF they
were willing to spend time per-query.

If the LLM C0 (clean prompt, no skill) approaches V4 without per-query
engineering, that demonstrates compositional zero-shot capability.
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
from scipy.ndimage import distance_transform_edt

BENCH_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH_DIR))
from evaluation.metrics import evaluate_binary

B_BLUE, B_GREEN, B_RED, B_NIR = 0, 1, 2, 3
B_SWIR1, B_SWIR2 = 8, 9


def _load_tif(p):
    with rasterio.open(p) as src:
        return src.read().astype(np.float32) / 10000.0


def _div(n, d, eps=1e-9):
    return n / (d + eps)


def _ndvi(img): return _div(img[B_NIR] - img[B_RED], img[B_NIR] + img[B_RED])
def _ndbi(img): return _div(img[B_SWIR1] - img[B_NIR], img[B_SWIR1] + img[B_NIR])
def _mndwi(img): return _div(img[B_GREEN] - img[B_SWIR1], img[B_GREEN] + img[B_SWIR1])


def _class_mask(img, class_id):
    """Approximate WorldCover class via spectral indices."""
    ndvi = _ndvi(img); ndbi = _ndbi(img); mndwi = _mndwi(img)
    if class_id == 80:    # water
        return mndwi > 0
    elif class_id == 50:  # built-up
        return ndbi > 0
    elif class_id == 10:  # tree (high NDVI)
        return ndvi > 0.5
    elif class_id == 30:  # grassland (mid NDVI)
        return (ndvi > 0.2) & (ndvi < 0.5)
    elif class_id == 40:  # cropland
        return (ndvi > 0.3) & (ndbi < 0)
    elif class_id == 60:  # bare
        return (ndvi < 0.15) & (mndwi < 0)
    else:
        return np.zeros(img.shape[1:], dtype=bool)


def v1_always_ndbi(img, sample):
    """Always extract built-up — ignores query."""
    return ((_ndbi(img) > 0).astype(np.uint8) * 255)

def v2_always_mndwi(img, sample):
    return ((_mndwi(img) > 0).astype(np.uint8) * 255)

def v3_always_ndvi(img, sample):
    return ((_ndvi(img) > 0.3).astype(np.uint8) * 255)

def v4_compositional_router(img, sample):
    """Engineering upper bound: parse sample's structured fields and compose."""
    target_cls = sample["target_class"]
    constraint_cls = sample["constraint_class"]
    op = sample["spatial_op"]
    K = sample["K_pixels"]

    target_mask = _class_mask(img, target_cls)
    constraint_mask = _class_mask(img, constraint_cls)

    if constraint_mask.sum() == 0:
        if op == "within":
            return np.zeros_like(target_mask, dtype=np.uint8)
        else:
            return (target_mask.astype(np.uint8) * 255)

    dist = distance_transform_edt(~constraint_mask)
    if op == "within":
        spatial = dist <= K
    else:
        spatial = dist > K
    return ((target_mask & spatial).astype(np.uint8) * 255)


VARIANTS = [
    ("Always NDBI",                     v1_always_ndbi),
    ("Always MNDWI",                    v2_always_mndwi),
    ("Always NDVI",                     v3_always_ndvi),
    ("Compositional router (UB)",       v4_compositional_router),
]


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    root = BENCH_DIR / "results" / f"_baseline_t5_{ts}"
    root.mkdir(parents=True, exist_ok=True)
    print(f"Output root: {root}\n")

    samples = json.loads((BENCH_DIR / "datasets_tif/query/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/query"

    cluster = {}
    for vname, vfn in VARIANTS:
        vd = root / vname.replace(" ", "_").replace("(", "").replace(")", "")
        rows = []
        for s in samples:
            sd = vd / s["id"]; sd.mkdir(parents=True, exist_ok=True)
            t0 = time.time()
            img = _load_tif(data_dir / s["image"])
            mask = vfn(img, s)
            Image.fromarray(mask).save(sd / "output.png")
            m = evaluate_binary(sd / "output.png", data_dir / s["label"])
            m["sample_id"] = s["id"]; m["primary_metric"] = m["f1"]
            rows.append(m)
        primary = [r["primary_metric"] for r in rows]
        cluster[vname] = {
            "n": len(rows),
            "primary_mean": float(np.mean(primary)),
            "precision_mean": float(np.mean([r["precision"] for r in rows])),
            "recall_mean": float(np.mean([r["recall"] for r in rows])),
            "per_sample": [{"id": r["sample_id"], "primary": r["primary_metric"]} for r in rows],
        }
        print(f"  {vname:<32s} F1={cluster[vname]['primary_mean']:.3f} "
              f"P={cluster[vname]['precision_mean']:.3f} R={cluster[vname]['recall_mean']:.3f}")

    means = [v["primary_mean"] for v in cluster.values()]
    print()
    print(f"  Naive single-formula best: {max(means[:3]):.3f}")
    print(f"  Compositional router (UB): {means[3]:.3f}")
    cluster["__cluster_stats__"] = {
        "naive_best": max(means[:3]),
        "compositional_upper_bound": means[3],
    }
    (root / "cluster_summary.json").write_text(json.dumps(cluster, indent=2))


if __name__ == "__main__":
    main()
