from __future__ import annotations
import numpy as np


def _validate(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    if y_true.shape != y_pred.shape:
        raise ValueError("Shape mismatch in regression metrics")

    return y_true, y_pred


def mae(y_true, y_pred) -> float:
    y_true, y_pred = _validate(y_true, y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))


def mse(y_true, y_pred) -> float:
    y_true, y_pred = _validate(y_true, y_pred)
    return float(np.mean((y_true - y_pred) ** 2))


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mse(y_true, y_pred)))


def r2(y_true, y_pred) -> float:
    y_true, y_pred = _validate(y_true, y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1 - ss_res / ss_tot)


METRICS = {
    "mae": mae,
    "mse": mse,
    "rmse": rmse,
    "r2": r2,
}