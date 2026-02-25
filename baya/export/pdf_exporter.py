"""
PDF Exporter

Exports:
- DataFrame to PDF table
- Dictionary (metrics/report) to PDF
- Matplotlib figure to PDF
"""

from __future__ import annotations

from typing import Dict, Any, Optional
from pathlib import Path

import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import matplotlib.figure

from ..context import Context


class PDFExporter:
    """
    Handles exporting data and reports to PDF.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Export DataFrame as Table
    # -------------------------------------------------

    def toPDF(
        self,
        path: str,
        title: Optional[str] = None,
    ) -> "PDFExporter":
        """
        Export current DataFrame to PDF as formatted table.
        """
        self.context.ensure_dataframe()
        df: pd.DataFrame = self.context.dataframe

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=pagesizes.A4,
        )

        elements = []
        styles = getSampleStyleSheet()

        if title:
            elements.append(Paragraph(title, styles["Heading1"]))
            elements.append(Spacer(1, 12))

        data = [df.columns.tolist()] + df.head(50).values.tolist()

        table = Table(data, repeatRows=1)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                ]
            )
        )

        elements.append(table)
        doc.build(elements)

        return self

    # -------------------------------------------------
    # Export Dictionary (Metrics / Report)
    # -------------------------------------------------

    def exportDict(
        self,
        data: Dict[str, Any],
        path: str,
        title: str = "Report",
    ) -> "PDFExporter":
        """
        Export dictionary content into formatted PDF.
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=pagesizes.A4,
        )

        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(title, styles["Heading1"]))
        elements.append(Spacer(1, 12))

        for key, value in data.items():
            line = f"<b>{key}:</b> {value}"
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1, 6))

        doc.build(elements)

        return self

    # -------------------------------------------------
    # Export Matplotlib Figure
    # -------------------------------------------------

    def exportFigure(
        self,
        figure: matplotlib.figure.Figure,
        path: str,
    ) -> "PDFExporter":
        """
        Export matplotlib figure directly to PDF.
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        figure.savefig(output_path, format="pdf")

        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<PDFExporter rows={rows} cols={cols}>"
