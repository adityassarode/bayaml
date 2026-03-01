from __future__ import annotations

import numpy as np


def _validate(y_true, y_pred):
    yt = np.asarray(y_true)
    yp = np.asarray(y_pred)
    if yt.shape != yp.shape:
        raise ValueError("Shape mismatch.")
    return yt, yp


def accuracy(y_true, y_pred) -> float:
    yt, yp = _validate(y_true, y_pred)
    return float(np.mean(yt == yp))


def precision(y_true, y_pred) -> float:
    yt, yp = _validate(y_true, y_pred)
    tp = np.sum((yt == 1) & (yp == 1))
    fp = np.sum((yt != 1) & (yp == 1))
    return float(tp / (tp + fp)) if (tp + fp) else 0.0


def recall(y_true, y_pred) -> float:
    yt, yp = _validate(y_true, y_pred)
    tp = np.sum((yt == 1) & (yp == 1))
    fn = np.sum((yt == 1) & (yp != 1))
    return float(tp / (tp + fn)) if (tp + fn) else 0.0


def f1(y_true, y_pred) -> float:
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return float(2 * p * r / (p + r)) if (p + r) else 0.0
