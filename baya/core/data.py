"""
Baya Data Module
Ingestion boundary only.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Union, Optional

import pandas as pd

from ..context import Context


class DataModule:
    def __init__(self, context: Context) -> None:
        self.ctx = context

    # =================================================
    # Ingestion
    # =================================================

    def load(self, source: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
        if isinstance(source, pd.DataFrame):
            df = source.copy()
        else:
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(path)

            suffix = path.suffix.lower()

            if suffix == ".csv":
                df = pd.read_csv(path)
            elif suffix in (".xlsx", ".xls"):
                df = pd.read_excel(path)
            elif suffix == ".json":
                df = pd.read_json(path)
            else:
                raise ValueError(f"Unsupported file type: {suffix}")

        self.ctx.set_dataframe(df)
        return df

    def from_dict(self, data: Dict[str, Any]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        self.ctx.set_dataframe(df)
        return df

    # =================================================
    # Target
    # =================================================

    def set_target(self, column: str) -> None:
        self.ctx.set_target(column)

    def get_target(self) -> Optional[str]:
        return self.ctx.get_target()

    # =================================================

    def preview(self, rows: int = 5) -> pd.DataFrame:
        self.ctx.ensure_dataframe()
        return self.ctx.get_dataframe().head(rows)

    def __repr__(self) -> str:
        df = self.ctx.get_dataframe()
        rows, cols = df.shape if df is not None else (0, 0)
        return f"<DataModule rows={rows} cols={cols}>"