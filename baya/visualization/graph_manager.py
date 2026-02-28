from __future__ import annotations

from ..context import Context
from .matplotlib_backend import MatplotlibBackend


class GraphManager:
    def __init__(self, context: Context) -> None:
        self._ctx = context
        self._mpl = MatplotlibBackend()

    def histogram(self, column: str):
        df = self._ctx.ensure_dataframe()
        fig = self._mpl.histogram(df, column)
        self._ctx.set_last_figure(fig)
        return fig

    def scatter(self, x: str, y: str):
        df = self._ctx.ensure_dataframe()
        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Columns {x!r} and/or {y!r} not found.")
        fig = self._mpl.scatter(df, x, y)
        self._ctx.set_last_figure(fig)
        return fig
