from __future__ import annotations

import numpy as np


def _validate(y_true, y_pred):
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    if yt.shape != yp.shape:
        raise ValueError("Shape mismatch.")
    return yt, yp


def mae(y_true, y_pred) -> float:
    yt, yp = _validate(y_true, y_pred)
    return float(np.mean(np.abs(yt - yp)))


def mse(y_true, y_pred) -> float:
    yt, yp = _validate(y_true, y_pred)
    return float(np.mean((yt - yp) ** 2))


def r2(y_true, y_pred) -> float:
    yt, yp = _validate(y_true, y_pred)
    ss_res = float(np.sum((yt - yp) ** 2))
    ss_tot = float(np.sum((yt - np.mean(yt)) ** 2))
    return float(1 - ss_res / ss_tot) if ss_tot else 0.0
