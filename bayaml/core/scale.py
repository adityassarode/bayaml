from __future__ import annotations

from typing import Optional

from sklearn.preprocessing import MinMaxScaler, StandardScaler

from ..context import Context


class ScaleModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def _feature_columns(self, columns: Optional[list[str]]) -> list[str]:
        df = self._ctx.ensure_dataframe()
        if columns is not None:
            return columns
        target = self._ctx.get_target()
        cols = df.select_dtypes(include="number").columns.tolist()
        if target in cols:
            cols.remove(target)
        return cols

    def standard(self, columns: Optional[list[str]] = None) -> "ScaleModule":
        df = self._ctx.ensure_dataframe().copy()
        cols = self._feature_columns(columns)
        if cols:
            df[cols] = StandardScaler().fit_transform(df[cols])
        self._ctx.set_dataframe(df)
        return self

    def minmax(self, columns: Optional[list[str]] = None) -> "ScaleModule":
        df = self._ctx.ensure_dataframe().copy()
        cols = self._feature_columns(columns)
        if cols:
            df[cols] = MinMaxScaler().fit_transform(df[cols])
        self._ctx.set_dataframe(df)
        return self

    def scaleStandard(self, columns: Optional[list[str]] = None) -> "ScaleModule":
        return self.standard(columns)
