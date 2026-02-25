from __future__ import annotations
import numpy as np


def inertia(y_true, y_pred) -> float:
    # placeholder metric — real clustering metrics require features
    return float(np.var(y_pred))


METRICS = {
    "inertia": inertia,
}