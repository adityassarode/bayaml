"""
CSV Exporter

Exports pandas DataFrame to CSV format.
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

import pandas as pd

from ..context import Context


class CSVExporter:
    """
    Handles exporting DataFrame to CSV.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Export CSV
    # -------------------------------------------------

    def toCSV(
        self,
        path: str,
        index: bool = False,
        sep: str = ",",
        encoding: str = "utf-8",
    ) -> "CSVExporter":
        """
        Export current DataFrame to CSV.

        Parameters:
        - path: output file path
        - index: include index column
        - sep: delimiter
        - encoding: file encoding
        """
        self.context.ensure_dataframe()

        df: pd.DataFrame = self.context.dataframe

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(
            output_path,
            index=index,
            sep=sep,
            encoding=encoding,
        )

        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<CSVExporter rows={rows} cols={cols}>"
