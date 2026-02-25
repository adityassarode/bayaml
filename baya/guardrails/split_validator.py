# baya/guardrails/split_validator.py

from __future__ import annotations

from typing import Any
import pandas as pd

from ..context import Context


class SplitError(Exception):
    """Raised when split integrity validation fails."""
    pass


def validate_split(context: Context) -> None:
    """
    Validate deterministic split integrity.

    Rules:
        - Split must exist
        - No empty splits
        - X/y alignment
        - No overlap between train/test
        - Target consistency
    """

    if not context.is_split:
        raise SplitError("Dataset must be split before training.")

    X_train, X_test, y_train, y_test = context.get_split_data()

    # -------------------------------------------------
    # Empty checks
    # -------------------------------------------------
    if len(X_train) == 0 or len(X_test) == 0:
        raise SplitError("Train/Test split cannot be empty.")

    # -------------------------------------------------
    # Shape consistency
    # -------------------------------------------------
    if len(X_train) != len(y_train):
        raise SplitError("X_train and y_train size mismatch.")

    if len(X_test) != len(y_test):
        raise SplitError("X_test and y_test size mismatch.")

    # -------------------------------------------------
    # Overlap detection
    # -------------------------------------------------
    train_index = set(X_train.index)
    test_index = set(X_test.index)

    if train_index.intersection(test_index):
        raise SplitError("Train/Test overlap detected.")

    # -------------------------------------------------
    # Target consistency
    # -------------------------------------------------
    target = context.get_target()

    if target is None:
        raise SplitError("Target not defined in context.")

    # -------------------------------------------------
    # Deterministic safeguard
    # -------------------------------------------------
    if context.get_seed() is None:
        raise SplitError("Seed must be defined for deterministic split.")