from __future__ import annotations
import pandas as pd
import numpy as np


class LeakageError(Exception):
    pass


def detect_leakage(df: pd.DataFrame, target: str, threshold: float = 0.999) -> None:
    y = df[target]

    for col in df.columns:
        if col == target:
            continue

        if not np.issubdtype(df[col].dtype, np.number):
            continue

        corr = abs(np.corrcoef(df[col], y)[0, 1])

        if corr >= threshold:
            raise LeakageError(
                f"Feature '{col}' is almost perfectly correlated with target."
            )