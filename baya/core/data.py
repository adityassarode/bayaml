"""
Baya Data Module

Handles:
- Loading datasets
- Inspecting datasets
- Basic exploration utilities
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from ..context import Context


class DataModule:
    """
    Data loading and inspection operations.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Loading Methods
    # -------------------------------------------------

    def loadCSV(self, path: str | Path, **kwargs) -> "DataModule":
        df = pd.read_csv(path, **kwargs)
        self.context.dataframe = df
        return self

    def loadExcel(self, path: str | Path, **kwargs) -> "DataModule":
        df = pd.read_excel(path, **kwargs)
        self.context.dataframe = df
        return self

    def loadJSON(self, path: str | Path, **kwargs) -> "DataModule":
        df = pd.read_json(path, **kwargs)
        self.context.dataframe = df
        return self

    def loadSQL(
        self,
        query: str,
        connection,
        **kwargs,
    ) -> "DataModule":
        df = pd.read_sql(query, connection, **kwargs)
        self.context.dataframe = df
        return self

    # -------------------------------------------------
    # Inspection Methods
    # -------------------------------------------------

    def preview(self, rows: int = 5) -> pd.DataFrame:
        """
        Return first few rows.
        """
        self.context.ensure_dataframe()
        return self.context.dataframe.head(rows)

    def describe(self) -> pd.DataFrame:
        """
        Return summary statistics.
        """
        self.context.ensure_dataframe()
        return self.context.dataframe.describe(include="all")

    def info(self) -> None:
        """
        Print DataFrame info.
        """
        self.context.ensure_dataframe()
        print(self.context.dataframe.info())

    def shape(self) -> tuple[int, int]:
        """
        Return (rows, columns)
        """
        self.context.ensure_dataframe()
        return self.context.dataframe.shape

    def columns(self) -> list[str]:
        """
        Return column names.
        """
        self.context.ensure_dataframe()
        return list(self.context.dataframe.columns)

    # -------------------------------------------------
    # Target Handling
    # -------------------------------------------------

    def setTarget(self, column: str) -> "DataModule":
        """
        Set target column for modeling.
        """
        self.context.ensure_dataframe()

        if column not in self.context.dataframe.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")

        self.context.target = column
        return self

    def getTarget(self) -> Optional[str]:
        return self.context.target

    # -------------------------------------------------
    # Basic Stats
    # -------------------------------------------------

    def missingSummary(self) -> pd.Series:
        """
        Return missing value count per column.
        """
        self.context.ensure_dataframe()
        return self.context.dataframe.isnull().sum()

    def valueCounts(self, column: str) -> pd.Series:
        """
        Value counts for a column.
        """
        self.context.ensure_dataframe()

        if column not in self.context.dataframe.columns:
            raise ValueError(f"Column '{column}' not found.")

        return self.context.dataframe[column].value_counts()

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<DataModule rows={rows} cols={cols}>"
