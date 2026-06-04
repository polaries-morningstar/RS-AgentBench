"""
T5 oracle UB — Router-D.

Reads the ESA WorldCover label raster DIRECTLY from
benchmark/datasets_tif/shared/<sample>/worldcover.tif, then applies the same
distance-transform + intersect pipeline as Routers A/B/C, using the same
structured tuple (target_class, constraint_class, op, K) per sample.

By construction the T5 GT (label.png) was generated from the SAME WorldCover
raster via the SAME pipeline, so the oracle should score F1 ≈ 1.0 modulo
distance-transform discretisation. The point is to separate, empirically:

  - spectral-router family ceiling (Routers A/B/C ≈ 0.19): the lossy
    spectral approximation of WorldCover classes from false-colour
    Sentinel-2 imagery.

  - oracle ceiling (Router-D ≈ 1.0): no approximation; reads WorldCover
    directly.

The 0.81 F1 gap (oracle − spectral) measures the spectral-approximation
deficit, not the GT label noise. This is the empirical evidence for the
§4.3 honesty rewrite.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import rasterio
from PIL import Image
from scipy.ndimage import distance_transform_edt

BENCH_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH_DIR))
from evaluation.metrics import evaluate_binary

SHARED_DIR = BENCH_DIR / "datasets_tif/shared"


def oracle_compose(wc, sample):
    """Identical to T5 build_one() except returns uint8 mask for evaluate_binary."""
    target_cls = sample["target_class"]
    constraint_cls = sample["constraint_class"]
    op = sample["spatial_op"]
    K = sample["K_pixels"]

    target_mask = (wc == target_cls)
    constraint_mask = (wc == constraint_cls)

    if constraint_mask.sum() == 0:
        gt = np.zeros_like(wc, dtype=bool) if op == "within" else target_mask
    else:
        dist = distance_transform_edt(~constraint_mask)
        if op == "within":
            gt = target_mask & (dist <= K)
        else:
            gt = target_mask & (dist > K)
    return (gt.astype(np.uint8) * 255)


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    root = BENCH_DIR / "results" / f"_t5_ub_oracle_{ts}"
    root.mkdir(parents=True, exist_ok=True)

    samples = json.loads((BENCH_DIR / "datasets_tif/query/samples_v1.json").read_text())
    data_dir = BENCH_DIR / "datasets_tif/query"

    rows = []
    for s in samples:
        sample_name = s["id"].replace("__t5", "")
        wc_path = SHARED_DIR / sample_name / "worldcover.tif"
        with rasterio.open(wc_path) as src:
            wc = src.read(1)

        mask = oracle_compose(wc, s)
        sd = root / s["id"]
        sd.mkdir(parents=True, exist_ok=True)
        Image.fromarray(mask).save(sd / "output.png")
        m = evaluate_binary(sd / "output.png", data_dir / s["label"])
        m["sample_id"] = s["id"]; m["primary_metric"] = m["f1"]
        rows.append(m)

    f1s = np.array([r["primary_metric"] for r in rows])

    print("Router-D (Oracle WorldCover-direct):")
    for r in rows:
        print(f"  {r['sample_id']:<32s}  F1={r['primary_metric']:.4f}")
    print()
    print(f"  Oracle F1 mean   = {f1s.mean():.4f}")
    print(f"  Oracle F1 median = {np.median(f1s):.4f}")
    print(f"  Oracle F1 min    = {f1s.min():.4f}")
    print(f"  Oracle F1 max    = {f1s.max():.4f}")
    print()
    print("=== Cross-router UB comparison ===")
    print(f"  Router-A (fixed spectral)        F1 = 0.192")
    print(f"  Router-B (Otsu spectral)         F1 = 0.187")
    print(f"  Router-C (loose spectral + morph) F1 = 0.198")
    print(f"  Router-D (oracle WorldCover)     F1 = {f1s.mean():.4f}")
    print()
    print(f"  Spectral-router family ceiling: 0.187–0.198")
    print(f"  Oracle ceiling:                 {f1s.mean():.4f}")
    print(f"  Spectral-approximation deficit: {f1s.mean() - 0.192:.4f} F1")

    summary = {
        "router_d_oracle": {
            "n": len(f1s),
            "f1_mean": float(f1s.mean()),
            "f1_median": float(np.median(f1s)),
            "f1_min": float(f1s.min()),
            "f1_max": float(f1s.max()),
            "per_sample": [{"id": r["sample_id"], "f1": float(r["f1"])} for r in rows],
        },
        "cross_router_summary": {
            "router_a_fixed_spectral":  0.192,
            "router_b_otsu_spectral":   0.187,
            "router_c_loose_spectral":  0.198,
            "router_d_oracle":          float(f1s.mean()),
            "spectral_family_range":    [0.187, 0.198],
            "spectral_approximation_deficit": float(f1s.mean() - 0.192),
        },
    }
    (root / "oracle_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {root / 'oracle_summary.json'}")


if __name__ == "__main__":
    main()
