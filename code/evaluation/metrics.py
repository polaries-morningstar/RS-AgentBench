"""
RS-AgentBench evaluation metrics.

Computes metrics for binary segmentation and multi-class classification tasks.
All metrics work on numpy arrays (predicted mask vs ground truth mask).

Usage:
    from benchmark.evaluation.metrics import evaluate_binary, evaluate_multiclass
    result = evaluate_binary(pred_path, gt_path)
    result = evaluate_multiclass(pred_path, gt_path, num_classes=3, ignore_index=255)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def _load_mask(path: str | Path) -> np.ndarray:
    """Load a mask image as single-channel numpy array.

    If the image is already grayscale, return as-is.
    If RGB, take the first channel (not luminance-weighted conversion).
    If RGBA, check if RGB channels are empty and alpha carries the data.
    """
    img = Image.open(path)
    arr = np.array(img)
    if arr.ndim == 2:
        return arr  # Already single-channel
    elif arr.ndim == 3:
        if arr.shape[2] == 4:
            # RGBA: check if RGB is empty and alpha has data
            rgb_sum = arr[:, :, :3].sum()
            alpha_sum = arr[:, :, 3].sum()
            if rgb_sum == 0 and alpha_sum > 0:
                return arr[:, :, 3]  # Alpha channel is the mask
        return arr[:, :, 0]  # Default: first channel
    return arr


def evaluate_binary(pred_path: str | Path, gt_path: str | Path) -> dict:
    """Evaluate binary segmentation (building extraction, water extraction, change detection).

    Assumes: foreground = 255 (or >127), background = 0.
    Returns dict with f1, iou, precision, recall, accuracy.
    """
    pred = _load_mask(pred_path)
    gt = _load_mask(gt_path)

    # Resize pred to match gt if needed
    if pred.shape != gt.shape:
        pred_img = Image.fromarray(pred).resize(
            (gt.shape[1], gt.shape[0]), Image.NEAREST
        )
        pred = np.array(pred_img)

    # Binarize — handle 0/1, 0/255, and other conventions robustly
    def _binarize(arr: np.ndarray) -> np.ndarray:
        unique = set(np.unique(arr))
        if unique <= {0, 1}:
            return arr.astype(bool)  # 0/1 convention
        elif unique <= {0, 255}:
            return arr > 127  # 0/255 convention
        else:
            # Unknown convention: use Otsu-like midpoint between min and max nonzero
            nonzero_vals = arr[arr > 0]
            if len(nonzero_vals) == 0:
                return np.zeros_like(arr, dtype=bool)
            threshold = nonzero_vals.min() / 2  # anything > 0 is foreground
            return arr > threshold

    pred_bin = _binarize(pred)
    gt_bin = _binarize(gt)

    tp = int(np.sum(pred_bin & gt_bin))
    fp = int(np.sum(pred_bin & ~gt_bin))
    fn = int(np.sum(~pred_bin & gt_bin))
    tn = int(np.sum(~pred_bin & ~gt_bin))

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    iou = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0.0
    accuracy = (tp + tn) / (tp + fp + fn + tn) if (tp + fp + fn + tn) > 0 else 0.0

    return {
        "f1": round(f1, 4),
        "iou": round(iou, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "accuracy": round(accuracy, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def evaluate_multiclass(
    pred_path: str | Path,
    gt_path: str | Path,
    num_classes: int = 3,
    ignore_index: int = 255,
) -> dict:
    """Evaluate multi-class classification (land cover).

    Handles cluster-to-class permutation via Hungarian algorithm
    to find the best label assignment.

    Returns dict with oa, kappa, per_class_f1, mean_f1.
    """
    pred = _load_mask(pred_path)
    gt = _load_mask(gt_path)

    if pred.shape != gt.shape:
        pred_img = Image.fromarray(pred).resize(
            (gt.shape[1], gt.shape[0]), Image.NEAREST
        )
        pred = np.array(pred_img)

    # Mask out ignore pixels
    valid = gt != ignore_index
    pred_valid = pred[valid]
    gt_valid = gt[valid]

    if len(gt_valid) == 0:
        return {"oa": 0.0, "kappa": 0.0, "mean_f1": 0.0, "per_class_f1": {}}

    # Always apply Hungarian matching to find best label assignment
    # This handles: permuted labels, out-of-range labels, over-segmentation
    pred_valid = _hungarian_remap(pred_valid, gt_valid, num_classes)

    # Overall accuracy
    oa = float(np.mean(pred_valid == gt_valid))

    # Cohen's Kappa
    confusion = np.zeros((num_classes, num_classes), dtype=np.int64)
    for i in range(num_classes):
        for j in range(num_classes):
            confusion[i, j] = int(np.sum((gt_valid == i) & (pred_valid == j)))

    n = confusion.sum()
    po = np.diag(confusion).sum() / n if n > 0 else 0
    pe = sum(confusion[i, :].sum() * confusion[:, i].sum() for i in range(num_classes)) / (n * n) if n > 0 else 0
    kappa = (po - pe) / (1 - pe) if (1 - pe) > 0 else 0.0

    # Per-class F1
    per_class_f1 = {}
    for c in range(num_classes):
        tp = int(np.sum((pred_valid == c) & (gt_valid == c)))
        fp = int(np.sum((pred_valid == c) & (gt_valid != c)))
        fn = int(np.sum((pred_valid != c) & (gt_valid == c)))
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        per_class_f1[str(c)] = round(f1, 4)

    mean_f1 = float(np.mean(list(per_class_f1.values())))

    return {
        "oa": round(oa, 4),
        "kappa": round(kappa, 4),
        "mean_f1": round(mean_f1, 4),
        "per_class_f1": per_class_f1,
    }


def _hungarian_remap(pred: np.ndarray, gt: np.ndarray, num_classes: int) -> np.ndarray:
    """Remap predicted labels to best-matching GT classes.

    Uses many-to-one mapping: each predicted label is assigned to the GT class
    with maximum overlap. This correctly handles K-means with K > num_classes.
    """
    pred_labels = np.unique(pred)

    # For each pred label, find the GT class with max overlap (many-to-one)
    remap = {}
    for pl in pred_labels:
        pred_mask = pred == pl
        best_class = 0
        best_overlap = -1
        for j in range(num_classes):
            overlap = int(np.sum(pred_mask & (gt == j)))
            if overlap > best_overlap:
                best_overlap = overlap
                best_class = j
        remap[int(pl)] = best_class

    # Apply remapping
    remapped = np.zeros_like(pred)
    for old, new in remap.items():
        remapped[pred == old] = new
    return remapped
