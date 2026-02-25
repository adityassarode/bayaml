from __future__ import annotations

import pandas as pd


class DataValidationError(Exception):
    pass


def validate_dataframe(
    df: pd.DataFrame,
    *,
    target: str,
) -> None:
    if df is None or df.empty:
        raise DataValidationError("Dataset is empty.")

    if target not in df.columns:
        raise DataValidationError(f"Target column '{target}' not found.")

    if df.columns.duplicated().any():
        raise DataValidationError("Duplicate column names detected.")

    null_columns = df.columns[df.isna().all()]
    if len(null_columns) > 0:
        raise DataValidationError(
            f"Columns fully null: {list(null_columns)}"
        )