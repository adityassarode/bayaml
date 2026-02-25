from __future__ import annotations
import pandas as pd


class SplitError(Exception):
    pass


def validate_split(
    train: pd.DataFrame,
    test: pd.DataFrame,
    target_column: str
) -> None:
    if train is None or test is None:
        raise SplitError("Dataset must be split before training.")

    if len(train) == 0 or len(test) == 0:
        raise SplitError("Train/Test split cannot be empty.")

    overlap = set(train.index).intersection(set(test.index))
    if overlap:
        raise SplitError("Train/Test sets overlap detected.")

    if target_column not in train.columns or target_column not in test.columns:
        raise SplitError(f"Target column '{target_column}' missing after split.")