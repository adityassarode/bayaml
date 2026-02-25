from __future__ import annotations
import pandas as pd


class SchemaError(Exception):
    pass


def validate_schema(reference: pd.DataFrame, new: pd.DataFrame) -> None:
    ref_cols = list(reference.columns)
    new_cols = list(new.columns)

    if ref_cols != new_cols:
        missing = set(ref_cols) - set(new_cols)
        extra = set(new_cols) - set(ref_cols)

        raise SchemaError(
            f"Schema mismatch | Missing: {missing} | Extra: {extra}"
        )