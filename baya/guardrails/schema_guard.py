from __future__ import annotations

import pandas as pd
from typing import List


class SchemaError(Exception):
    """Raised when dataset schema mismatch is detected."""
    pass


def validate_schema(
    *,
    reference: pd.DataFrame,
    new: pd.DataFrame,
) -> None:
    """
    Enforce strict schema equivalence.

    Validates:
        - Column names
        - Column order
        - Column dtypes

    Does NOT mutate input.
    """

    if reference.empty:
        raise SchemaError("Reference DataFrame is empty.")

    if new.empty:
        raise SchemaError("New DataFrame is empty.")

    ref_cols: List[str] = list(reference.columns)
    new_cols: List[str] = list(new.columns)

    # -------------------------------------------------
    # Column name & order validation
    # -------------------------------------------------
    if ref_cols != new_cols:
        missing = sorted(set(ref_cols) - set(new_cols))
        extra = sorted(set(new_cols) - set(ref_cols))

        raise SchemaError(
            f"Schema mismatch | "
            f"Missing: {missing} | "
            f"Extra: {extra} | "
            f"Order differs: {ref_cols != new_cols}"
        )

    # -------------------------------------------------
    # Dtype validation
    # -------------------------------------------------
    for col in ref_cols:
        ref_dtype = str(reference[col].dtype)
        new_dtype = str(new[col].dtype)

        if ref_dtype != new_dtype:
            raise SchemaError(
                f"Dtype mismatch for column '{col}' | "
                f"Expected: {ref_dtype} | "
                f"Found: {new_dtype}"
            )