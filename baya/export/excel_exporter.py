"""
Excel Exporter

Exports pandas DataFrame to Excel (.xlsx).
"""

from __future__ import annotations

from typing import Optional, Dict
from pathlib import Path

import pandas as pd

from ..context import Context


class ExcelExporter:
    """
    Handles exporting DataFrame to Excel format.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Export Single Sheet
    # -------------------------------------------------

    def toExcel(
        self,
        path: str,
        sheet_name: str = "Sheet1",
        index: bool = False,
    ) -> "ExcelExporter":
        """
        Export current DataFrame to Excel file.

        Parameters:
        - path: output file path
        - sheet_name: name of Excel sheet
        - index: include index column
        """
        self.context.ensure_dataframe()

        df: pd.DataFrame = self.context.dataframe

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)

        return self

    # -------------------------------------------------
    # Export Multiple Sheets
    # -------------------------------------------------

    def toMultiSheetExcel(
        self,
        path: str,
        sheets: Dict[str, pd.DataFrame],
        index: bool = False,
    ) -> "ExcelExporter":
        """
        Export multiple DataFrames to different sheets.

        Parameters:
        - path: output file path
        - sheets: dict {sheet_name: DataFrame}
        - index: include index column
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            for sheet_name, df in sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=index)

        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<ExcelExporter rows={rows} cols={cols}>"
