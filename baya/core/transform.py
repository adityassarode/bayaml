"""
Baya Transform Module

Handles:
- Feature engineering
- Mathematical transformations
- Feature interactions
- Binning
- Custom feature generation
"""

from __future__ import annotations

from typing import Callable, Any, List

import numpy as np
import pandas as pd

from ..context import Context


class TransformModule:
    """
    Feature engineering operations.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Internal
    # -------------------------------------------------

    def _ensure_df(self) -> pd.DataFrame:
        self.context.ensure_dataframe()
        return self.context.dataframe

    # -------------------------------------------------
    # Add Column
    # -------------------------------------------------

    def addFeature(
        self,
        name: str,
        function: Callable[[pd.DataFrame], Any],
    ) -> "TransformModule":
        """
        Create a new feature using a function.

        Example:
            p.transform.addFeature(
                "log_income",
                lambda df: np.log(df["Income"])
            )
        """
        df = self._ensure_df()

        df[name] = function(df)
        return self

    # -------------------------------------------------
    # Log Transform
    # -------------------------------------------------

    def log(
        self,
        column: str,
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Apply log transform to column.
        """

        df = self._ensure_df()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        target = new_name or f"log_{column}"

        df[target] = np.log(df[column].replace(0, np.nan))

        return self

    # -------------------------------------------------
    # Power Transform
    # -------------------------------------------------

    def power(
        self,
        column: str,
        exponent: float,
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Raise column to power.
        """

        df = self._ensure_df()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        target = new_name or f"{column}_pow_{exponent}"
        df[target] = np.power(df[column], exponent)

        return self

    # -------------------------------------------------
    # Square Root
    # -------------------------------------------------

    def sqrt(
        self,
        column: str,
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Apply square root transform.
        """

        df = self._ensure_df()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        target = new_name or f"sqrt_{column}"
        df[target] = np.sqrt(df[column])

        return self

    # -------------------------------------------------
    # Interaction Feature
    # -------------------------------------------------

    def interaction(
        self,
        col1: str,
        col2: str,
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Create interaction feature (col1 * col2).
        """

        df = self._ensure_df()

        if col1 not in df.columns or col2 not in df.columns:
            raise ValueError("One or more columns not found.")

        target = new_name or f"{col1}_x_{col2}"
        df[target] = df[col1] * df[col2]

        return self

    # -------------------------------------------------
    # Binning
    # -------------------------------------------------

    def bin(
        self,
        column: str,
        bins: int | List[float],
        labels: List[str] | None = None,
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Bin numeric column.
        """

        df = self._ensure_df()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        target = new_name or f"{column}_binned"

        df[target] = pd.cut(df[column], bins=bins, labels=labels)

        return self

    # -------------------------------------------------
    # Normalize Column
    # -------------------------------------------------

    def normalize(
        self,
        column: str,
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Min-max normalize a single column.
        """

        df = self._ensure_df()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        col = df[column]
        target = new_name or f"{column}_norm"

        df[target] = (col - col.min()) / (col.max() - col.min())

        return self

    # -------------------------------------------------
    # Apply to Column
    # -------------------------------------------------

    def apply(
        self,
        column: str,
        function: Callable[[Any], Any],
        new_name: str | None = None,
    ) -> "TransformModule":
        """
        Apply custom function to a column.
        """

        df = self._ensure_df()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        target = new_name or f"{column}_custom"

        df[target] = df[column].apply(function)

        return self

    # -------------------------------------------------
    # Drop Column
    # -------------------------------------------------

    def drop(
        self,
        columns: List[str],
    ) -> "TransformModule":
        """
        Drop one or more columns.
        """

        df = self._ensure_df()

        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found.")

        self.context.dataframe = df.drop(columns=columns)

        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<TransformModule rows={rows} cols={cols}>"
