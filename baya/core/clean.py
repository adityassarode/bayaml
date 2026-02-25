"""
Baya Clean Module

Handles:
- Missing values
- Null removal
- Duplicate removal
- Column renaming
- Type conversion
- Row filtering
"""

from __future__ import annotations

from typing import Any, Callable

import pandas as pd

from ..context import Context


class CleanModule:
    """
    Data cleaning operations.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Missing Values
    # -------------------------------------------------

    def fillMissing(
        self,
        column: str,
        strategy: str | Any,
    ) -> "CleanModule":
        """
        Fill missing values in a column.

        strategy:
            "mean"
            "median"
            "mode"
            custom value
        """
        self.context.ensure_dataframe()
        df = self.context.dataframe

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        if strategy == "mean":
            value = df[column].mean()
        elif strategy == "median":
            value = df[column].median()
        elif strategy == "mode":
            value = df[column].mode()[0]
        else:
            value = strategy  # custom value

        df[column] = df[column].fillna(value)

        return self

    # -------------------------------------------------
    # Drop Nulls
    # -------------------------------------------------

    def dropNulls(
        self,
        axis: int = 0,
        how: str = "any",
    ) -> "CleanModule":
        """
        Remove rows or columns containing null values.

        axis:
            0 = rows
            1 = columns

        how:
            "any"
            "all"
        """
        self.context.ensure_dataframe()

        self.context.dataframe = self.context.dataframe.dropna(
            axis=axis,
            how=how,
        )

        return self

    # -------------------------------------------------
    # Drop Duplicates
    # -------------------------------------------------

    def dropDuplicates(
        self,
        subset: list[str] | None = None,
        keep: str = "first",
    ) -> "CleanModule":
        """
        Remove duplicate rows.
        """
        self.context.ensure_dataframe()

        self.context.dataframe = self.context.dataframe.drop_duplicates(
            subset=subset,
            keep=keep,
        )

        return self

    # -------------------------------------------------
    # Rename Columns
    # -------------------------------------------------

    def renameColumn(
        self,
        old_name: str,
        new_name: str,
    ) -> "CleanModule":
        """
        Rename a column.
        """
        self.context.ensure_dataframe()

        if old_name not in self.context.dataframe.columns:
            raise ValueError(f"Column '{old_name}' not found.")

        self.context.dataframe = self.context.dataframe.rename(
            columns={old_name: new_name}
        )

        return self

    # -------------------------------------------------
    # Change Data Type
    # -------------------------------------------------

    def changeType(
        self,
        column: str,
        dtype: Any,
    ) -> "CleanModule":
        """
        Change column data type.
        """
        self.context.ensure_dataframe()

        if column not in self.context.dataframe.columns:
            raise ValueError(f"Column '{column}' not found.")

        self.context.dataframe[column] = self.context.dataframe[column].astype(
            dtype
        )

        return self

    # -------------------------------------------------
    # Filter Rows
    # -------------------------------------------------

    def filterRows(
        self,
        condition: str | Callable[[pd.DataFrame], pd.Series],
    ) -> "CleanModule":
        """
        Filter rows using:
            - query string
            - lambda returning boolean mask
        """
        self.context.ensure_dataframe()

        df = self.context.dataframe

        if isinstance(condition, str):
            df = df.query(condition)
        else:
            mask = condition(df)
            df = df[mask]

        self.context.dataframe = df

        return self

    # -------------------------------------------------
    # Reset Index
    # -------------------------------------------------

    def resetIndex(self) -> "CleanModule":
        """
        Reset DataFrame index.
        """
        self.context.ensure_dataframe()
        self.context.dataframe = self.context.dataframe.reset_index(drop=True)
        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<CleanModule rows={rows} cols={cols}>"
