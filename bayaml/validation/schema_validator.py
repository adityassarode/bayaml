from __future__ import annotations


def validate_column_types(df, required: dict) -> None:
    for col, dtype in required.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
        if str(df[col].dtype) != str(dtype):
            raise ValueError(f"Column '{col}' type mismatch.")
