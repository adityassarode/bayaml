"""
Seaborn Backend for Baya Visualization

Provides:
- Histogram
- Scatter plot
- Boxplot
- Heatmap
- Countplot
"""

from __future__ import annotations

from typing import Optional

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class SeabornBackend:
    """
    Seaborn visualization backend.
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
        sns.histplot(data=data.dropna(), bins=bins, ax=ax)
        ax.set_title(title or "Histogram")
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
        hue: Optional[str] = None,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=x, y=y, hue=hue, ax=ax)
        ax.set_title(title or "Scatter Plot")
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
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        sns.boxplot(data=data, x=x, y=y, ax=ax)
        ax.set_title(title or "Box Plot")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Heatmap
    # -------------------------------------------------

    def heatmap(
        self,
        matrix: pd.DataFrame,
        annot: bool = False,
        cmap: str = "viridis",
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        sns.heatmap(matrix, annot=annot, cmap=cmap, ax=ax)
        ax.set_title(title or "Heatmap")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Count Plot
    # -------------------------------------------------

    def countplot(
        self,
        data: pd.DataFrame,
        column: str,
        title: Optional[str] = None,
    ):
        fig, ax = plt.subplots()
        sns.countplot(data=data, x=column, ax=ax)
        ax.set_title(title or f"Count of {column}")
        self._last_figure = fig
        return fig

    # -------------------------------------------------
    # Show
    # -------------------------------------------------

    def show(self):
        """
        Display last figure.
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
