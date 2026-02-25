"""
Graph Exporter (Project Integrated)

Exports the last generated visualization from GraphManager.

Supports:
- PNG
- JPG
- PDF
- SVG
- HTML (plotly)

Usage:
    p.visual.histogram("Age")
    p.export.graph("age.png")
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.figure
import plotly.graph_objects as go

from ..context import Context
from .image_exporter import ImageExporter


class GraphExporter:
    """
    Exports last graph generated in the project.
    """

    def __init__(self, context: Context) -> None:
        self.context = context
        self._image_exporter = ImageExporter()

    # -------------------------------------------------
    # Export Graph
    # -------------------------------------------------

    def graph(
        self,
        path: str,
        dpi: int = 300,
    ) -> "GraphExporter":
        """
        Export last generated graph.

        Automatically detects backend.
        """
        figure = self.context.get_last_figure()

        if figure is None:
            raise RuntimeError(
                "No graph available. Generate a visualization first."
            )

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Matplotlib
        if isinstance(figure, matplotlib.figure.Figure):
            self._image_exporter.exportMatplotlib(
                figure,
                str(output_path),
                dpi=dpi,
            )
            return self

        # Plotly
        if isinstance(figure, go.Figure):
            self._image_exporter.exportPlotly(
                figure,
                str(output_path),
            )
            return self

        raise TypeError("Unsupported figure type for graph export.")

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return "<GraphExporter>"
