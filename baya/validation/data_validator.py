from __future__ import annotations


def validate_dataframe(df) -> None:
    if df is None or len(df) == 0:
        raise ValueError("DataFrame is empty.")
