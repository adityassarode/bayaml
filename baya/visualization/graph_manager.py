"""
Graph Manager

Controls visualization backend selection and routing.

Backends supported:
- matplotlib
- seaborn
- plotly
"""

from __future__ import annotations

from typing import Optional, Literal

from ..context import Context
from .matplotlib_backend import MatplotlibBackend
from .seaborn_backend import SeabornBackend
from .plotly_backend import PlotlyBackend


BackendType = Literal["matplotlib", "seaborn", "plotly"]


class GraphManager:
    """
    Central visualization controller.
    """

    def __init__(
        self,
        context: Context,
        backend: BackendType = "matplotlib",
    ) -> None:
        self.context = context
        self._backend_name = backend
        self._backend = self._create_backend(backend)

    # -------------------------------------------------
    # Backend Handling
    # -------------------------------------------------

    def _create_backend(self, backend: BackendType):
        if backend == "matplotlib":
            return MatplotlibBackend()
        if backend == "seaborn":
            return SeabornBackend()
        if backend == "plotly":
            return PlotlyBackend()

        raise ValueError(f"Unsupported backend: {backend}")

    def use(self, backend: BackendType) -> "GraphManager":
        """
        Switch visualization backend.
        """
        self._backend_name = backend
        self._backend = self._create_backend(backend)
        return self

    # -------------------------------------------------
    # Histogram
    # -------------------------------------------------

    def histogram(
        self,
        column: str,
        bins: int = 30,
        title: Optional[str] = None,
    ):
        self.context.ensure_dataframe()

        df = self.context.dataframe

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        fig = self._backend.histogram(
            df[column],
            bins=bins,
            title=title,
        )

        self.context.set_last_figure(fig)

        return fig

    # -------------------------------------------------
    # Scatter
    # -------------------------------------------------

    def scatter(
        self,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.context.ensure_dataframe()
        df = self.context.dataframe

        if x not in df.columns or y not in df.columns:
            raise ValueError("Invalid column name.")

        fig = self._backend.scatter(
            df,
            x=x,
            y=y,
            color=color,
            title=title,
        )

        self.context.set_last_figure(fig)

        return fig

    # -------------------------------------------------
    # Boxplot
    # -------------------------------------------------

    def boxplot(
        self,
        x: Optional[str] = None,
        y: Optional[str] = None,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.context.ensure_dataframe()
        df = self.context.dataframe

        fig = self._backend.boxplot(
            df,
            x=x,
            y=y,
            color=color,
            title=title,
        )

        self.context.set_last_figure(fig)

        return fig

    # -------------------------------------------------
    # Heatmap
    # -------------------------------------------------

    def heatmap(
        self,
        annot: bool = False,
        title: Optional[str] = None,
    ):
        self.context.ensure_dataframe()
        df = self.context.dataframe

        matrix = df.corr(numeric_only=True)

        fig = self._backend.heatmap(
            matrix,
            annot=annot if self._backend_name != "plotly" else None,
            title=title,
        )

        self.context.set_last_figure(fig)

        return fig

    # -------------------------------------------------
    # Show
    # -------------------------------------------------

    def show(self):
        return self._backend.show()

    # -------------------------------------------------
    # Get Last Figure
    # -------------------------------------------------

    def get_last_figure(self):
        return self.context.get_last_figure()

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return f"<GraphManager backend={self._backend_name}>"
