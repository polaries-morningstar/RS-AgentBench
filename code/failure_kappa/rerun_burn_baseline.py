"""Re-run T4 burn naive baseline with multiple dNBR thresholds.

Tests dNBR > {0.10, 0.27, 0.40} on the 10 archived burn samples and reports
per-sample + mean F1 for each threshold.

dNBR thresholds (Key & Benson 2006):
  0.10 = "low + above" (all burn)
  0.27 = "moderate + above" (the current paper baseline)
  0.40 = "moderate-high + above"
"""
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

BENCH_DIR = Path("/Users/polaries/Work/AutoSpec/paper/archive/code")
sys.path.insert(0, str(BENCH_DIR))
from evaluation.metrics import evaluate_binary  # type: ignore

DATA = Path("/Users/polaries/Work/AutoSpec/paper/archive/datasets_tif/burn")

B_NIR = 3
B_SWIR2 = 9
SCALE = 10000.0
THRESHOLDS = [0.10, 0.18, 0.27, 0.40]


def _load(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        return src.read().astype(np.float32) / SCALE


def _safe_div(num, den):
    out = np.zeros_like(num, dtype=np.float32)
    mask = den != 0
    out[mask] = num[mask] / den[mask]
    return out


def _nbr(img):
    return _safe_div(img[B_NIR] - img[B_SWIR2], img[B_NIR] + img[B_SWIR2])


def main():
    samples = json.loads((DATA / "samples_v1.json").read_text())
    results = {t: [] for t in THRESHOLDS}

    for s in samples:
        sid = s["id"]
        img_pre = _load(DATA / s["image_a"])
        img_post = _load(DATA / s["image_b"])
        nbr_pre = _nbr(img_pre)
        nbr_post = _nbr(img_post)
        dnbr = nbr_pre - nbr_post
        gt_path = DATA / s["label"]

        tmp_out = Path(f"/tmp/burn_{sid}.png")
        for thr in THRESHOLDS:
            mask = ((dnbr > thr).astype(np.uint8) * 255)
            Image.fromarray(mask).save(tmp_out)
            metrics = evaluate_binary(tmp_out, gt_path)
            f1 = float(metrics.get("f1", 0.0))
            results[thr].append({"sample": sid, "f1": f1})

    print(f"{'threshold':>10}  {'mean_F1':>8}  {'median':>8}  {'min':>6}  {'max':>6}")
    summary = {}
    for thr in THRESHOLDS:
        f1s = [r["f1"] for r in results[thr]]
        m = float(np.mean(f1s))
        med = float(np.median(f1s))
        summary[thr] = {"mean": m, "median": med, "min": min(f1s), "max": max(f1s),
                        "per_sample": results[thr]}
        print(f"  dNBR>{thr:.2f}  {m:>8.4f}  {med:>8.4f}  {min(f1s):>6.3f}  {max(f1s):>6.3f}")

    Path("/tmp/burn_threshold_sweep.json").write_text(json.dumps(summary, indent=2))
    print(f"\nDetail in /tmp/burn_threshold_sweep.json")


if __name__ == "__main__":
    main()
