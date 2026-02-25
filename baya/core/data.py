"""
Baya Data Module
Ingestion boundary only.

Responsibilities:
- Load data into Context
- Provide read-only inspection utilities
- Delegate all state mutation to Context
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Union, Optional

import pandas as pd

from ..context import Context


class DataModule:
    """
    Data ingestion boundary.

    This module MUST NOT:
    - Mutate context internals directly
    - Store internal state
    - Perform modeling logic
    - Perform splitting
    - Perform transformations

    All state changes go through Context.
    """

    def __init__(self, context: Context) -> None:
        self._ctx: Context = context

    # =================================================
    # Ingestion
    # =================================================

    def load(
        self,
        source: Union[str, Path, pd.DataFrame],
    ) -> pd.DataFrame:

        if isinstance(source, pd.DataFrame):
            df: pd.DataFrame = source.copy()

        else:
            path = Path(source)

            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")

            suffix: str = path.suffix.lower()

            if suffix == ".csv":
                df = pd.read_csv(path)

            elif suffix in (".xlsx", ".xls"):
                df = pd.read_excel(path)

            elif suffix == ".json":
                df = pd.read_json(path)

            else:
                raise ValueError(f"Unsupported file type: '{suffix}'")

        if df.empty:
            raise ValueError("Loaded dataset is empty.")

        # Controlled mutation via Context
        self._ctx.set_dataframe(df)

        return df

    def from_dict(self, data: Dict[str, Any]) -> pd.DataFrame:
        df: pd.DataFrame = pd.DataFrame(data)

        if df.empty:
            raise ValueError("Provided dataset is empty.")

        self._ctx.set_dataframe(df)
        return df

    # =================================================
    # Target Handling
    # =================================================

    def set_target(self, column: Optional[str]) -> None:
        """
        Delegate target setting to Context.

        Context decides validation timing.
        """
        if column is None:
            return

        self._ctx.set_target(column)

    def get_target(self) -> Optional[str]:
        return self._ctx.get_target()

    # =================================================
    # Inspection (Read-Only)
    # =================================================

    def preview(self, rows: int = 5) -> pd.DataFrame:
        self._ctx.ensure_dataframe()
        df = self._ctx.get_dataframe()
        assert df is not None
        return df.head(rows)

    def shape(self) -> tuple[int, int]:
        self._ctx.ensure_dataframe()
        df = self._ctx.get_dataframe()
        assert df is not None
        return df.shape

    def columns(self) -> list[str]:
        self._ctx.ensure_dataframe()
        df = self._ctx.get_dataframe()
        assert df is not None
        return list(df.columns)

    # =================================================
    # Representation
    # =================================================

    def __repr__(self) -> str:
        df = self._ctx.get_dataframe()
        rows, cols = df.shape if df is not None else (0, 0)
        return f"<DataModule rows={rows} cols={cols}>"