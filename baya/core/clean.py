from __future__ import annotations

from typing import Any, Callable, Optional

import pandas as pd

from ..context import Context


class CleanModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def fill_missing(self, column: str, strategy: Any = "mean") -> "CleanModule":
        df = self._ctx.ensure_dataframe().copy()
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")
        if strategy == "mean":
            value = df[column].mean()
        elif strategy == "median":
            value = df[column].median()
        elif strategy == "mode":
            value = df[column].mode().iloc[0]
        else:
            value = strategy
        df[column] = df[column].fillna(value)
        self._ctx.set_dataframe(df)
        return self

    def drop_nulls(self, axis: int = 0, how: str = "any") -> "CleanModule":
        df = self._ctx.ensure_dataframe().dropna(axis=axis, how=how)
        self._ctx.set_dataframe(df)
        return self

    def drop_duplicates(self, subset: Optional[list[str]] = None, keep: str = "first") -> "CleanModule":
        df = self._ctx.ensure_dataframe().drop_duplicates(subset=subset, keep=keep)
        self._ctx.set_dataframe(df)
        return self

    def filter_rows(self, condition: str | Callable[[pd.DataFrame], pd.Series]) -> "CleanModule":
        df = self._ctx.ensure_dataframe()
        out = df.query(condition) if isinstance(condition, str) else df[condition(df)]
        self._ctx.set_dataframe(out)
        return self

    # backwards compat aliases
    def fillMissing(self, column: str, strategy: Any) -> "CleanModule":
        return self.fill_missing(column, strategy)
