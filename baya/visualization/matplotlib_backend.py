"""
Matplotlib Backend for Baya Visualization

Provides:
- Histogram
- Scatter
- Line
- Boxplot
- Heatmap (via imshow fallback)
"""

from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class MatplotlibBackend:
    """
    Matplotlib visualization backend.
    """

    def __init__(self) -> None:
        self._last_figure = None

    # -------------------------------------------------
    # Histogram
    # -------------------------------------------------

    def histogram(
        self,
        data: pd.Series,
        bins: int = 30,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        ax.hist(data.dropna(), bins=bins)
        ax.set_title(title or "Histogram")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Scatter
    # -------------------------------------------------

    def scatter(
        self,
        x: pd.Series,
        y: pd.Series,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.set_xlabel(x.name or "X")
        ax.set_ylabel(y.name or "Y")
        ax.set_title(title or "Scatter Plot")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Line
    # -------------------------------------------------

    def line(
        self,
        x: Sequence,
        y: Sequence,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_title(title or "Line Plot")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Boxplot
    # -------------------------------------------------

    def boxplot(
        self,
        data: pd.Series,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        ax.boxplot(data.dropna())
        ax.set_title(title or "Box Plot")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Heatmap (basic)
    # -------------------------------------------------

    def heatmap(
        self,
        matrix: pd.DataFrame | np.ndarray,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        cax = ax.imshow(matrix, aspect="auto")
        fig.colorbar(cax)
        ax.set_title(title or "Heatmap")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Show
    # -------------------------------------------------

    def show(self):
        """
        Display last created figure.
        """
        if self._last_figure:
            plt.show()

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    def save(
        self,
        path: str,
        dpi: int = 300,
    ):
        """
        Save last created figure.
        """
        if self._last_figure:
            self._last_figure.savefig(path, dpi=dpi)

    # -------------------------------------------------
    # Get Last Figure
    # -------------------------------------------------

    def get_last_figure(self):
        return self._last_figure
