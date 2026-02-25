from __future__ import annotations

import pandas as pd
from typing import Dict


class SchemaValidationError(Exception):
    pass


def validate_column_types(
    df: pd.DataFrame,
    expected_types: Dict[str, str],
) -> None:
    for col, expected in expected_types.items():
        if col not in df.columns:
            raise SchemaValidationError(
                f"Missing column '{col}'"
            )

        actual = str(df[col].dtype)

        if actual != expected:
            raise SchemaValidationError(
                f"Column '{col}' dtype mismatch: "
                f"expected {expected}, got {actual}"
            )