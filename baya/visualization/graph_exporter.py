"""
Graph Exporter

Exports visualization figures to multiple formats:

Supported:
- PNG
- JPG
- PDF
- SVG
- HTML (for Plotly)

Automatically detects figure type.
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

import matplotlib.figure
import plotly.graph_objects as go


class GraphExporter:
    """
    Handles exporting figures created by GraphManager.
    """

    def __init__(self) -> None:
        pass

    # -------------------------------------------------
    # Export Main
    # -------------------------------------------------

    def export(
        self,
        figure,
        path: str,
        format: Optional[str] = None,
        dpi: int = 300,
    ) -> None:
        """
        Export figure automatically based on type.

        Parameters:
        - figure: matplotlib.figure.Figure or plotly.graph_objects.Figure
        - path: output file path
        - format: optional override format (png, jpg, pdf, svg, html)
        - dpi: resolution (matplotlib only)
        """

        path_obj = Path(path)

        if format is None:
            format = path_obj.suffix.replace(".", "").lower()

        # -------------------------------------------------
        # Matplotlib Figure
        # -------------------------------------------------

        if isinstance(figure, matplotlib.figure.Figure):
            self._export_matplotlib(figure, path_obj, format, dpi)
            return

        # -------------------------------------------------
        # Plotly Figure
        # -------------------------------------------------

        if isinstance(figure, go.Figure):
            self._export_plotly(figure, path_obj, format)
            return

        raise TypeError("Unsupported figure type for export.")

    # -------------------------------------------------
    # Matplotlib Export
    # -------------------------------------------------

    def _export_matplotlib(
        self,
        figure: matplotlib.figure.Figure,
        path: Path,
        format: str,
        dpi: int,
    ) -> None:
        figure.savefig(path, format=format, dpi=dpi)

    # -------------------------------------------------
    # Plotly Export
    # -------------------------------------------------

    def _export_plotly(
        self,
        figure: go.Figure,
        path: Path,
        format: str,
    ) -> None:
        if format == "html":
            figure.write_html(str(path))
            return

        # Static export requires kaleido
        try:
            figure.write_image(str(path), format=format)
        except Exception as e:
            raise RuntimeError(
                "Plotly static export requires 'kaleido'. "
                "Install using: pip install kaleido"
            ) from e

    # -------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------

    def toPNG(self, figure, path: str):
        self.export(figure, path, format="png")

    def toJPG(self, figure, path: str):
        self.export(figure, path, format="jpg")

    def toPDF(self, figure, path: str):
        self.export(figure, path, format="pdf")

    def toSVG(self, figure, path: str):
        self.export(figure, path, format="svg")

    def toHTML(self, figure, path: str):
        self.export(figure, path, format="html")

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return "<GraphExporter>"
