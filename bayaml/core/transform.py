from __future__ import annotations

import numpy as np

from ..context import Context


class TransformModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def log(self, column: str, new_name: str | None = None) -> "TransformModule":
        df = self._ctx.ensure_dataframe().copy()
        target = new_name or f"log_{column}"
        df[target] = np.log(df[column].replace(0, np.nan))
        self._ctx.set_dataframe(df)
        return self

    def drop(self, columns: list[str]) -> "TransformModule":
        df = self._ctx.ensure_dataframe().drop(columns=columns)
        self._ctx.set_dataframe(df)
        return self
