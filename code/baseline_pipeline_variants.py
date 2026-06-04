"""
RS-AgentBench fixed-pipeline **multi-baseline** cluster.

Replaces the LLM agent with **multiple textbook spectral-index methods**
(no learning, no LLM, no agent). Used to ground the agent's value: if a
cluster of 4 classical baselines per task contains one that matches/beats
the best LLM agent, the agent's value proposition needs revisiting.

For each task we run 4 published methods. The cluster is reported as:
  - best (max across variants)
  - median (middle of variants)
  - worst (min across variants)

A reviewer can argue with any single baseline, but cannot argue with a
**cluster of 4 published methods**.

Channel layout (all tasks): 0=B02 1=B03 2=B04 3=B08 4=B05 5=B06 6=B07 7=B8A 8=B11 9=B12
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
from sklearn.cluster import KMeans

BENCH_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH_DIR))
from evaluation.metrics import evaluate_binary, evaluate_multiclass

# Sentinel-2 band indices
B_BLUE, B_GREEN, B_RED, B_NIR = 0, 1, 2, 3
B_B05, B_B06, B_B07, B_NIR2 = 4, 5, 6, 7
B_SWIR1, B_SWIR2 = 8, 9
SCALE = 10000.0


def _load_tif(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        return src.read().astype(np.float32) / SCALE


def _safe_div(num: np.ndarray, den: np.ndarray) -> np.ndarray:
    out = np.zeros_like(num, dtype=np.float32)
    m = den != 0
    out[m] = num[m] / den[m]
    return out


# ---------------------------------------------------------------------------
# Spectral indices
# ---------------------------------------------------------------------------

def ndvi(img):  return _safe_div(img[B_NIR] - img[B_RED],   img[B_NIR] + img[B_RED])
def ndwi(img):  return _safe_div(img[B_GREEN] - img[B_NIR], img[B_GREEN] + img[B_NIR])     # McFeeters 1996
def mndwi(img): return _safe_div(img[B_GREEN] - img[B_SWIR1], img[B_GREEN] + img[B_SWIR1]) # Xu 2006
def ndbi(img):  return _safe_div(img[B_SWIR1] - img[B_NIR],  img[B_SWIR1] + img[B_NIR])    # Zha 2003
def nbr(img):   return _safe_div(img[B_NIR] - img[B_SWIR2],  img[B_NIR] + img[B_SWIR2])    # Key & Benson 2006

def awei_sh(img):
    """Automated Water Extraction Index — shadow variant (Feyisa 2014)."""
    return img[B_GREEN] + 2.5 * img[B_NIR] - 1.5 * (img[B_SWIR1] + img[B_SWIR2]) - 0.25 * img[B_BLUE]


# ---------------------------------------------------------------------------
# Task pipelines — 4 variants per task
# ---------------------------------------------------------------------------

# ---- WATER ----
def water_mndwi(img):       return ((mndwi(img) > 0).astype(np.uint8) * 255)               # Xu 2006
def water_ndwi(img):        return ((ndwi(img)  > 0).astype(np.uint8) * 255)               # McFeeters 1996
def water_awei(img):        return ((awei_sh(img) > 0).astype(np.uint8) * 255)             # Feyisa 2014
def water_otsu_mndwi(img):
    m = mndwi(img)
    try:    thr = float(threshold_otsu(m))
    except: thr = 0.0
    return ((m > thr).astype(np.uint8) * 255)

WATER_VARIANTS = [
    ("MNDWI>0",       water_mndwi),       # Xu 2006 textbook
    ("NDWI>0",        water_ndwi),        # McFeeters 1996 (older, arguably worse)
    ("AWEI_sh>0",     water_awei),        # Feyisa 2014 (latest)
    ("MNDWI+Otsu",    water_otsu_mndwi),  # data-driven
]


# ---- CHANGE ----
def change_cva_otsu(a, b):
    diff = b - a
    mag = np.sqrt((diff ** 2).sum(axis=0))
    try:    thr = float(threshold_otsu(mag))
    except: thr = float(np.median(mag) + 2 * np.std(mag))
    return ((mag > thr).astype(np.uint8) * 255)

def change_rgb_otsu(a, b):
    """RGB-only differencing (3 visible bands)."""
    diff = b[:3] - a[:3]
    mag = np.sqrt((diff ** 2).sum(axis=0))
    try:    thr = float(threshold_otsu(mag))
    except: thr = float(np.median(mag) + 2 * np.std(mag))
    return ((mag > thr).astype(np.uint8) * 255)

def change_ndvi_diff(a, b):
    """|ΔNDVI| > Otsu — vegetation-loss-sensitive."""
    d = np.abs(ndvi(b) - ndvi(a))
    try:    thr = float(threshold_otsu(d))
    except: thr = 0.1
    return ((d > thr).astype(np.uint8) * 255)

def change_b12_diff(a, b):
    """|ΔB12| (SWIR2) > Otsu — built-up/water/burn-sensitive."""
    d = np.abs(b[B_SWIR2] - a[B_SWIR2])
    try:    thr = float(threshold_otsu(d))
    except: thr = 0.05
    return ((d > thr).astype(np.uint8) * 255)

CHANGE_VARIANTS = [
    ("CVA10+Otsu",    change_cva_otsu),    # Singh 1989 textbook (10 bands)
    ("CVA-RGB+Otsu",  change_rgb_otsu),    # 3-band variant
    ("|ΔNDVI|+Otsu",  change_ndvi_diff),   # vegetation-change focus
    ("|ΔB12|+Otsu",   change_b12_diff),    # SWIR-only
]


# ---- LANDCOVER ----
def landcover_ruletree_030(img):
    """water>veg>built rule, NDVI threshold 0.30 (Tucker mid-range)."""
    out = np.full(img.shape[1:], 3, dtype=np.uint8)
    out[ndbi(img) > 0]   = 2
    out[ndvi(img) > 0.30] = 1
    out[mndwi(img) > 0]  = 0
    return out

def landcover_ruletree_020(img):
    """Same, but Tucker 1979 original 0.2 threshold."""
    out = np.full(img.shape[1:], 3, dtype=np.uint8)
    out[ndbi(img) > 0]   = 2
    out[ndvi(img) > 0.20] = 1
    out[mndwi(img) > 0]  = 0
    return out

def landcover_kmeans4(img):
    """Unsupervised k-means k=4 on all 10 bands (no class assignment)."""
    H, W = img.shape[1:]
    X = img.reshape(10, -1).T  # (H*W, 10)
    # Subsample for speed
    rng = np.random.default_rng(42)
    n = len(X)
    if n > 50000:
        idx = rng.choice(n, 50000, replace=False)
        km = KMeans(n_clusters=4, n_init=4, random_state=42).fit(X[idx])
    else:
        km = KMeans(n_clusters=4, n_init=4, random_state=42).fit(X)
    labels = km.predict(X).reshape(H, W).astype(np.uint8)
    # No semantic label assignment — Hungarian matching in evaluator handles this
    return labels

def landcover_otsu_indices(img):
    """Class boundaries from Otsu on each index, not fixed thresholds."""
    nv, mw, nb = ndvi(img), mndwi(img), ndbi(img)
    try:    thr_ndvi = float(threshold_otsu(nv))
    except: thr_ndvi = 0.30
    try:    thr_mndwi = float(threshold_otsu(mw))
    except: thr_mndwi = 0.0
    try:    thr_ndbi = float(threshold_otsu(nb))
    except: thr_ndbi = 0.0
    out = np.full(img.shape[1:], 3, dtype=np.uint8)
    out[nb > thr_ndbi]  = 2
    out[nv > thr_ndvi]  = 1
    out[mw > thr_mndwi] = 0
    return out

LANDCOVER_VARIANTS = [
    ("Rule NDVI=0.30",   landcover_ruletree_030),  # current default
    ("Rule NDVI=0.20",   landcover_ruletree_020),  # Tucker 1979 original
    ("KMeans k=4",       landcover_kmeans4),       # unsupervised
    ("Rule+Otsu",        landcover_otsu_indices),  # data-driven thresholds
]


# ---- BURN ----
def burn_dnbr_027(pre, post):
    return (((nbr(pre) - nbr(post)) > 0.27).astype(np.uint8) * 255)  # K&B moderate

def burn_dnbr_010(pre, post):
    return (((nbr(pre) - nbr(post)) > 0.10).astype(np.uint8) * 255)  # K&B low

def burn_dnbr_otsu(pre, post):
    d = nbr(pre) - nbr(post)
    try:    thr = float(threshold_otsu(d))
    except: thr = 0.27
    return ((d > thr).astype(np.uint8) * 255)

def burn_rbr(pre, post):
    """Relativized Burn Ratio (Parks 2014). RBR > 0.27 conservative."""
    nb_pre = nbr(pre)
    nb_post = nbr(post)
    rbr = _safe_div(nb_pre - nb_post, nb_pre + 1.001)
    return ((rbr > 0.10).astype(np.uint8) * 255)  # RBR threshold roughly maps to dNBR via /(NBR+1)

BURN_VARIANTS = [
    ("dNBR>0.27", burn_dnbr_027),  # K&B 2006 moderate (current default)
    ("dNBR>0.10", burn_dnbr_010),  # K&B 2006 low
    ("dNBR+Otsu", burn_dnbr_otsu), # data-driven
    ("RBR>0.10",  burn_rbr),       # Parks 2014 alternative
]


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_water_variant(name, fn, out_dir, samples, data_dir):
    rows = []
    for s in samples:
        sd = out_dir / s["id"]; sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        img = _load_tif(data_dir / s["image"])
        Image.fromarray(fn(img)).save(sd / "output.png")
        m = evaluate_binary(sd / "output.png", data_dir / s["label"])
        m["sample_id"] = s["id"]; m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["f1"]; m["variant"] = name
        rows.append(m)
    return rows

def run_change_variant(name, fn, out_dir, samples, data_dir):
    rows = []
    for s in samples:
        sd = out_dir / s["id"]; sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        a = _load_tif(data_dir / s["image_a"])
        b = _load_tif(data_dir / s["image_b"])
        Image.fromarray(fn(a, b)).save(sd / "output.png")
        m = evaluate_binary(sd / "output.png", data_dir / s["label"])
        m["sample_id"] = s["id"]; m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["f1"]; m["variant"] = name
        rows.append(m)
    return rows

def run_landcover_variant(name, fn, out_dir, samples, data_dir):
    rows = []
    for s in samples:
        sd = out_dir / s["id"]; sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        img = _load_tif(data_dir / s["image"])
        Image.fromarray(fn(img)).save(sd / "output.png")
        m = evaluate_multiclass(sd / "output.png", data_dir / s["label"], num_classes=4, ignore_index=255)
        m["sample_id"] = s["id"]; m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["oa"]; m["variant"] = name
        rows.append(m)
    return rows

def run_burn_variant(name, fn, out_dir, samples, data_dir):
    rows = []
    for s in samples:
        sd = out_dir / s["id"]; sd.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        a = _load_tif(data_dir / s["image_a"])
        b = _load_tif(data_dir / s["image_b"])
        Image.fromarray(fn(a, b)).save(sd / "output.png")
        m = evaluate_binary(sd / "output.png", data_dir / s["label"])
        m["sample_id"] = s["id"]; m["elapsed_seconds"] = round(time.time() - t0, 3)
        m["primary_metric"] = m["f1"]; m["variant"] = name
        rows.append(m)
    return rows


def main() -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    root = BENCH_DIR / "results" / f"_baseline_variants_{ts}"
    root.mkdir(parents=True, exist_ok=True)
    print(f"Output root: {root}\n")

    cluster: dict = {}
    for task, runner_fn, variants, eval_fn in [
        ("water",     run_water_variant,     WATER_VARIANTS,     evaluate_binary),
        ("change",    run_change_variant,    CHANGE_VARIANTS,    evaluate_binary),
        ("landcover", run_landcover_variant, LANDCOVER_VARIANTS, evaluate_multiclass),
        ("burn",      run_burn_variant,      BURN_VARIANTS,      evaluate_binary),
    ]:
        samples = json.loads((BENCH_DIR / f"datasets_tif/{task}/samples_v1.json").read_text())
        data_dir = BENCH_DIR / f"datasets_tif/{task}"
        print(f"=== {task} ({len(samples)} samples × {len(variants)} variants) ===")
        cluster[task] = {}
        for vname, vfn in variants:
            vd = root / task / vname.replace(">", "gt").replace("=", "_").replace("|", "abs").replace(" ", "_").replace("Δ", "d").replace("/", "_").replace("+", "_")
            vd.mkdir(parents=True, exist_ok=True)
            t0 = time.time()
            rows = runner_fn(vname, vfn, vd, samples, data_dir)
            primary = [r["primary_metric"] for r in rows]
            cluster[task][vname] = {
                "n": len(rows),
                "primary_mean": float(np.mean(primary)),
                "primary_median": float(np.median(primary)),
                "wall_total_s": round(time.time() - t0, 3),
                "per_sample": [{"id": r["sample_id"], "primary": r["primary_metric"]} for r in rows],
            }
            print(f"  {vname:<22s} → {cluster[task][vname]['primary_mean']:.3f}  "
                  f"(median {cluster[task][vname]['primary_median']:.3f}, "
                  f"wall {cluster[task][vname]['wall_total_s']:.2f}s)")
        # cluster stats
        means = [v["primary_mean"] for v in cluster[task].values()]
        cluster[task]["__cluster_stats__"] = {
            "best":   max(means),
            "median": float(np.median(means)),
            "worst":  min(means),
            "best_variant": max(cluster[task].items(),
                                key=lambda kv: kv[1]["primary_mean"] if isinstance(kv[1], dict) and "primary_mean" in kv[1] else -1)[0],
        }
        s = cluster[task]["__cluster_stats__"]
        print(f"  → cluster: best={s['best']:.3f} ({s['best_variant']}) | median={s['median']:.3f} | worst={s['worst']:.3f}")
        print()

    (root / "cluster_summary.json").write_text(json.dumps(cluster, indent=2))
    print(f"summary: {root}/cluster_summary.json")


if __name__ == "__main__":
    main()
