from __future__ import annotations

import numpy as np


def inertia(_, y_pred) -> float:
    return float(np.var(np.asarray(y_pred)))
