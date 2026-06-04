"""
T5 engineering UB robustness check — for paper §4.3 / §5.4 / §7.

Three hand-written compositional routers, all with structural-tuple oracle
access (target_class, constraint_class, spatial_op, K) but varying the
spectral-rule choice that an LLM agent would otherwise have to invent:

  Router-A (baseline / current UB): fixed per-class spectral thresholds.
  Router-B (OTSU): per-image Otsu threshold on the relevant spectral index
                   for each class — adaptive, no manual tuning.
  Router-C (loose + morph): loosened thresholds + morphological opening/closing
                            cleanup on each class mask — recall-favoring.

All three share the same distance-transform-and-intersect backbone. If the
three routers converge to a similar F1 across the 10 T5 samples, the
~0.19 UB ceiling is bounded by structural factors (WorldCover label noise,
spectral-index inadequacy) rather than by the specific threshold choices.
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
from scipy.ndimage import distance_transform_edt, binary_opening, binary_closing

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


# ============================================================================
# Router-A — current published UB (paper §4.3)
# ============================================================================
def _class_mask_A(img, class_id):
    ndvi = _ndvi(img); ndbi = _ndbi(img); mndwi = _mndwi(img)
    if class_id == 80:    return mndwi > 0
    elif class_id == 50:  return ndbi > 0
    elif class_id == 10:  return ndvi > 0.5
    elif class_id == 30:  return (ndvi > 0.2) & (ndvi < 0.5)
    elif class_id == 40:  return (ndvi > 0.3) & (ndbi < 0)
    elif class_id == 60:  return (ndvi < 0.15) & (mndwi < 0)
    else:                 return np.zeros(img.shape[1:], dtype=bool)


# ============================================================================
# Router-B — per-image OTSU on the relevant spectral index
# ============================================================================
def _otsu_threshold(arr, nbins=256):
    """Manual Otsu — finds threshold that maximises inter-class variance.

    Falls back to 0 if the array is degenerate. Implementation is the
    standard histogram-based Otsu, identical in semantics to
    skimage.filters.threshold_otsu but with no extra dependency.
    """
    finite = np.isfinite(arr)
    vals = arr[finite]
    if vals.size < 100 or vals.max() - vals.min() < 1e-3:
        return 0.0
    hist, edges = np.histogram(vals, bins=nbins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    w = hist.astype(np.float64)
    total = w.sum()
    if total <= 0:
        return 0.0
    w /= total
    mu = (centers * w).sum()
    w_bg = np.cumsum(w)
    mu_bg = np.cumsum(centers * w)
    # avoid division by zero
    denom = w_bg * (1.0 - w_bg)
    valid = denom > 1e-12
    sigma_b2 = np.where(valid, (mu * w_bg - mu_bg) ** 2 / np.where(valid, denom, 1.0), 0.0)
    return float(centers[int(np.argmax(sigma_b2))])


def _class_mask_B(img, class_id):
    ndvi = _ndvi(img); ndbi = _ndbi(img); mndwi = _mndwi(img)
    if class_id == 80:    return mndwi > _otsu_threshold(mndwi)
    elif class_id == 50:  return ndbi  > _otsu_threshold(ndbi)
    elif class_id == 10:  return ndvi  > _otsu_threshold(ndvi)
    elif class_id == 30:  # mid NDVI — keep band structure but OTSU on the lower edge
        t = _otsu_threshold(ndvi)
        return (ndvi > t * 0.6) & (ndvi < t * 1.2)
    elif class_id == 40:
        t_ndvi = _otsu_threshold(ndvi)
        t_ndbi = _otsu_threshold(ndbi)
        return (ndvi > t_ndvi * 0.7) & (ndbi < t_ndbi)
    elif class_id == 60:
        t_ndvi = _otsu_threshold(ndvi)
        return (ndvi < t_ndvi * 0.5) & (mndwi < 0)
    else:
        return np.zeros(img.shape[1:], dtype=bool)


# ============================================================================
# Router-C — loosened thresholds + morphological opening/closing
# ============================================================================
def _morph_clean(mask, opening_size=2, closing_size=3):
    struct_o = np.ones((opening_size, opening_size), dtype=bool)
    struct_c = np.ones((closing_size, closing_size), dtype=bool)
    return binary_closing(binary_opening(mask, structure=struct_o),
                          structure=struct_c)


def _class_mask_C(img, class_id):
    ndvi = _ndvi(img); ndbi = _ndbi(img); mndwi = _mndwi(img)
    if class_id == 80:    m = mndwi > -0.1            # looser
    elif class_id == 50:  m = ndbi  > -0.1            # looser
    elif class_id == 10:  m = ndvi  > 0.35            # looser (was 0.5)
    elif class_id == 30:  m = (ndvi > 0.15) & (ndvi < 0.55)
    elif class_id == 40:  m = (ndvi > 0.2) & (ndbi < 0.05)
    elif class_id == 60:  m = (ndvi < 0.2) & (mndwi < 0)
    else:                 return np.zeros(img.shape[1:], dtype=bool)
    return _morph_clean(m)


# ============================================================================
# Shared compositional backbone
# ============================================================================
def _compose(img, sample, class_mask_fn):
    target = class_mask_fn(img, sample["target_class"])
    constraint = class_mask_fn(img, sample["constraint_class"])
    K = sample["K_pixels"]
    op = sample["spatial_op"]

    if constraint.sum() == 0:
        if op == "within":
            return np.zeros_like(target, dtype=np.uint8)
        return (target.astype(np.uint8) * 255)

    dist = distance_transform_edt(~constraint)
    spatial = (dist <= K) if op == "within" else (dist > K)
    return ((target & spatial).astype(np.uint8) * 255)


ROUTERS = [
    ("Router-A (baseline)",        _class_mask_A),
    ("Router-B (OTSU)",            _class_mask_B),
    ("Router-C (loose + morph)",   _class_mask_C),
]


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    root = BENCH_DIR / "results" / f"_t5_ub_robust_{ts}"
    root.mkdir(parents=True, exist_ok=True)
    print(f"Output root: {root}\n")

    samples = json.loads((BENCH_DIR / "datasets_tif/query/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/query"

    summary = {}
    per_sample_table = {}

    for rname, cls_fn in ROUTERS:
        rdir = root / rname.replace(" ", "_").replace("(", "").replace(")", "").replace("+", "_")
        rows = []
        for s in samples:
            sd = rdir / s["id"]; sd.mkdir(parents=True, exist_ok=True)
            img = _load_tif(data_dir / s["image"])
            mask = _compose(img, s, cls_fn)
            Image.fromarray(mask).save(sd / "output.png")
            m = evaluate_binary(sd / "output.png", data_dir / s["label"])
            m["sample_id"] = s["id"]; m["primary_metric"] = m["f1"]
            rows.append(m)
            per_sample_table.setdefault(s["id"], {})[rname] = float(m["f1"])

        f1s = np.array([r["primary_metric"] for r in rows])
        summary[rname] = {
            "n": len(f1s),
            "f1_mean":   float(f1s.mean()),
            "f1_median": float(np.median(f1s)),
            "f1_min":    float(f1s.min()),
            "f1_max":    float(f1s.max()),
            "f1_std":    float(f1s.std(ddof=1)),
            "per_sample": [
                {"id": r["sample_id"], "f1": float(r["primary_metric"])}
                for r in rows
            ],
        }
        print(f"  {rname:<32s} F1 mean={f1s.mean():.3f} median={np.median(f1s):.3f} "
              f"min={f1s.min():.3f} max={f1s.max():.3f} std={f1s.std(ddof=1):.3f}")

    print()
    means = {k: v["f1_mean"] for k, v in summary.items()}
    ub_range = max(means.values()) - min(means.values())
    print(f"  UB cross-router range = ±{ub_range / 2:.3f} F1 "
          f"({min(means.values()):.3f} – {max(means.values()):.3f})")

    summary["__ub_cross_router__"] = {
        "means": means,
        "range": float(max(means.values()) - min(means.values())),
        "midpoint": float((max(means.values()) + min(means.values())) / 2),
    }
    summary["__per_sample_table__"] = per_sample_table

    (root / "ub_robustness_summary.json").write_text(json.dumps(summary, indent=2))

    # Compact markdown for pasting into the paper
    md = ["# T5 UB cross-router robustness\n"]
    md.append("| Router | F1 mean | F1 median | min | max | std |")
    md.append("|---|---|---|---|---|---|")
    for rname in [r[0] for r in ROUTERS]:
        s = summary[rname]
        md.append(f"| {rname} | {s['f1_mean']:.3f} | {s['f1_median']:.3f} | "
                  f"{s['f1_min']:.3f} | {s['f1_max']:.3f} | {s['f1_std']:.3f} |")
    md.append(f"\n**UB range across routers: "
              f"{min(means.values()):.3f} – {max(means.values()):.3f} "
              f"(±{ub_range/2:.3f} F1 around midpoint {(max(means.values())+min(means.values()))/2:.3f}).**\n")
    (root / "PAPER_PASTE.md").write_text("\n".join(md))
    print(f"\nWrote {root / 'PAPER_PASTE.md'}")


if __name__ == "__main__":
    main()
