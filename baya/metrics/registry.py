from __future__ import annotations
import numpy as np


def _validate(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    if y_true.shape != y_pred.shape:
        raise ValueError("Shape mismatch in classification metrics")

    return y_true, y_pred


def accuracy(y_true, y_pred) -> float:
    y_true, y_pred = _validate(y_true, y_pred)
    return float(np.mean(y_true == y_pred))


def precision(y_true, y_pred) -> float:
    y_true, y_pred = _validate(y_true, y_pred)
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    if tp + fp == 0:
        return 0.0
    return float(tp / (tp + fp))


def recall(y_true, y_pred) -> float:
    y_true, y_pred = _validate(y_true, y_pred)
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    if tp + fn == 0:
        return 0.0
    return float(tp / (tp + fn))


METRICS = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
}