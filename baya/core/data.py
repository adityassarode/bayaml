from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from ..context import Context


class DataModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def load(self, source: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
        if isinstance(source, pd.DataFrame):
            df = source.copy()
        else:
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(str(path))
            suffix = path.suffix.lower()
            if suffix == ".csv":
                df = pd.read_csv(path)
            elif suffix in (".xlsx", ".xls"):
                df = pd.read_excel(path)
            elif suffix == ".json":
                df = pd.read_json(path)
            else:
                raise ValueError(f"Unsupported format: {suffix}")
        if df.empty:
            raise ValueError("Dataset is empty.")
        self._ctx.set_dataframe(df)
        return df

    def from_dict(self, data: Dict[str, Any]) -> pd.DataFrame:
        return self.load(pd.DataFrame(data))

    def set_target(self, target: Optional[str]) -> None:
        if target:
            self._ctx.set_target(target)

    def preview(self, rows: int = 5) -> pd.DataFrame:
        return self._ctx.ensure_dataframe().head(rows)
