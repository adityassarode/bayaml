"""
Baya Scale Module

Handles:
- Standard scaling
- MinMax scaling
- Normalization
"""

from __future__ import annotations

from typing import Optional, List

import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer

from ..context import Context


class ScaleModule:
    """
    Feature scaling operations.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

        if not hasattr(self.context, "scalers"):
            self.context.scalers = {}

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _get_feature_columns(self, columns: Optional[List[str]]) -> List[str]:
        """
        Determine which columns to scale.
        If None → scale all numeric except target.
        """
        self.context.ensure_dataframe()
        df = self.context.dataframe

        if columns is not None:
            return columns

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if self.context.target in numeric_cols:
            numeric_cols.remove(self.context.target)

        return numeric_cols

    # -------------------------------------------------
    # Standard Scaling
    # -------------------------------------------------

    def scaleStandard(
        self,
        columns: Optional[List[str]] = None,
    ) -> "ScaleModule":
        """
        Apply StandardScaler (zero mean, unit variance).
        """
        cols = self._get_feature_columns(columns)
        df = self.context.dataframe

        scaler = StandardScaler()
        df[cols] = scaler.fit_transform(df[cols])

        self.context.dataframe = df
        self.context.scalers["standard"] = scaler

        return self

    # -------------------------------------------------
    # MinMax Scaling
    # -------------------------------------------------

    def scaleMinMax(
        self,
        columns: Optional[List[str]] = None,
        feature_range: tuple = (0, 1),
    ) -> "ScaleModule":
        """
        Scale features to a range (default 0–1).
        """
        cols = self._get_feature_columns(columns)
        df = self.context.dataframe

        scaler = MinMaxScaler(feature_range=feature_range)
        df[cols] = scaler.fit_transform(df[cols])

        self.context.dataframe = df
        self.context.scalers["minmax"] = scaler

        return self

    # -------------------------------------------------
    # Normalize (Row-wise)
    # -------------------------------------------------

    def normalize(
        self,
        columns: Optional[List[str]] = None,
        norm: str = "l2",
    ) -> "ScaleModule":
        """
        Normalize samples (row-wise).
        """
        cols = self._get_feature_columns(columns)
        df = self.context.dataframe

        normalizer = Normalizer(norm=norm)
        df[cols] = normalizer.fit_transform(df[cols])

        self.context.dataframe = df
        self.context.scalers["normalize"] = normalizer

        return self

    # -------------------------------------------------
    # Transform New Data
    # -------------------------------------------------

    def transform(
        self,
        columns: List[str],
        scaler_type: str = "standard",
    ) -> pd.DataFrame:
        """
        Transform using previously fitted scaler.
        """
        if scaler_type not in self.context.scalers:
            raise ValueError(f"No scaler fitted for type '{scaler_type}'.")

        scaler = self.context.scalers[scaler_type]
        df = self.context.dataframe

        transformed = scaler.transform(df[columns])

        return pd.DataFrame(
            transformed,
            columns=columns,
            index=df.index,
        )

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<ScaleModule rows={rows} cols={cols}>"
