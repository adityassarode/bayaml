"""
Image Exporter

Exports:
- Matplotlib figures
- Plotly figures
- Numpy image arrays

Supported formats:
- PNG
- JPG
- JPEG
- SVG
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.figure
import numpy as np
import plotly.graph_objects as go
from PIL import Image


class ImageExporter:
    """
    Handles exporting images and figures.
    """

    def __init__(self) -> None:
        pass

    # -------------------------------------------------
    # Export Matplotlib Figure
    # -------------------------------------------------

    def exportMatplotlib(
        self,
        figure: matplotlib.figure.Figure,
        path: str,
        dpi: int = 300,
    ) -> "ImageExporter":
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        figure.savefig(output_path, dpi=dpi)

        return self

    # -------------------------------------------------
    # Export Plotly Figure
    # -------------------------------------------------

    def exportPlotly(
        self,
        figure: go.Figure,
        path: str,
        format: Optional[str] = None,
    ) -> "ImageExporter":
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format is None:
            format = output_path.suffix.replace(".", "")

        if format == "html":
            figure.write_html(str(output_path))
            return self

        try:
            figure.write_image(str(output_path), format=format)
        except Exception as e:
            raise RuntimeError(
                "Plotly static export requires 'kaleido'. "
                "Install using: pip install kaleido"
            ) from e

        return self

    # -------------------------------------------------
    # Export Numpy Array as Image
    # -------------------------------------------------

    def exportArray(
        self,
        array: np.ndarray,
        path: str,
    ) -> "ImageExporter":
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image = Image.fromarray(array)
        image.save(output_path)

        return self

    # -------------------------------------------------
    # Generic Export
    # -------------------------------------------------

    def export(
        self,
        obj,
        path: str,
        dpi: int = 300,
    ) -> "ImageExporter":
        """
        Auto-detect object type and export.
        """
        if isinstance(obj, matplotlib.figure.Figure):
            return self.exportMatplotlib(obj, path, dpi=dpi)

        if isinstance(obj, go.Figure):
            return self.exportPlotly(obj, path)

        if isinstance(obj, np.ndarray):
            return self.exportArray(obj, path)

        raise TypeError("Unsupported object type for image export.")

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return "<ImageExporter>"
