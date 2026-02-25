"""
Plotly Backend for Baya Visualization

Provides interactive visualizations:
- Histogram
- Scatter
- Boxplot
- Heatmap

Exports:
- HTML
- PNG / JPG (requires kaleido)
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class PlotlyBackend:
    """
    Plotly interactive visualization backend.
    """

    def __init__(self) -> None:
        self._last_figure: Optional[go.Figure] = None

    # -------------------------------------------------
    # Histogram
    # -------------------------------------------------

    def histogram(
        self,
        data: pd.Series,
        bins: int = 30,
        title: Optional[str] = None,
    ) -> go.Figure:
        fig = px.histogram(
            data_frame=data.dropna().to_frame(name="value"),
            x="value",
            nbins=bins,
            title=title or "Histogram",
        )
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Scatter
    # -------------------------------------------------

    def scatter(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:
        fig = px.scatter(
            data,
            x=x,
            y=y,
            color=color,
            title=title or "Scatter Plot",
        )
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Boxplot
    # -------------------------------------------------

    def boxplot(
        self,
        data: pd.DataFrame,
        x: Optional[str] = None,
        y: Optional[str] = None,
        color: Optional[str] = None,
        title: Optional[str] = None,
    ) -> go.Figure:
        fig = px.box(
            data,
            x=x,
            y=y,
            color=color,
            title=title or "Box Plot",
        )
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Heatmap
    # -------------------------------------------------

    def heatmap(
        self,
        matrix: pd.DataFrame,
        title: Optional[str] = None,
    ) -> go.Figure:
        fig = px.imshow(
            matrix,
            text_auto=False,
            aspect="auto",
            title=title or "Heatmap",
        )
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Show
    # -------------------------------------------------

    def show(self):
        """
        Display interactive figure.
        """
        if self._last_figure:
            self._last_figure.show()

    # -------------------------------------------------
    # Save HTML
    # -------------------------------------------------

    def save_html(self, path: str):
        """
        Save figure as interactive HTML.
        """
        if self._last_figure:
            self._last_figure.write_html(path)

    # -------------------------------------------------
    # Save Static Image (requires kaleido)
    # -------------------------------------------------

    def save_image(self, path: str, format: str = "png"):
        """
        Save static image (png, jpg, svg, pdf).

        Requires: pip install kaleido
        """
        if self._last_figure:
            self._last_figure.write_image(path, format=format)

    # -------------------------------------------------
    # Get Last Figure
    # -------------------------------------------------

    def get_last_figure(self) -> Optional[go.Figure]:
        return self._last_figure
