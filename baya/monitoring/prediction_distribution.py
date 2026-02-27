from __future__ import annotations

import numpy as np


def summarize_distribution(preds) -> dict:
    arr = np.asarray(preds)
    return {"mean": float(arr.mean()), "std": float(arr.std())}
