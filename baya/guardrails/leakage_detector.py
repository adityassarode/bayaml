from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Any


class LeakageError(Exception):
    """Raised when potential target leakage is detected."""
    pass


def detect_leakage(
    *,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    threshold: float = 0.999,
) -> None:
    """
    Detect near-perfect correlation between features and target.

    Must be called on TRAIN data only.
    Does NOT mutate input.
    """

    if X_train.empty:
        raise LeakageError("X_train is empty.")

    if y_train.empty:
        raise LeakageError("y_train is empty.")

    if len(X_train) != len(y_train):
        raise LeakageError("X_train and y_train length mismatch.")

    # Ensure numeric target
    if not np.issubdtype(y_train.dtype, np.number):
        return  # Only numeric leakage detection supported

    y = y_train.to_numpy()

    for col in X_train.columns:
        series = X_train[col]

        if not np.issubdtype(series.dtype, np.number):
            continue

        x = series.to_numpy()

        # Skip constant columns
        if np.nanstd(x) == 0:
            continue

        # NaN-safe mask
        mask = ~np.isnan(x) & ~np.isnan(y)
        if mask.sum() < 2:
            continue

        corr = abs(np.corrcoef(x[mask], y[mask])[0, 1])

        if np.isnan(corr):
            continue

        if corr >= threshold:
            raise LeakageError(
                f"Feature '{col}' is highly correlated with target "
                f"(corr={corr:.6f}). Potential leakage detected."
            )