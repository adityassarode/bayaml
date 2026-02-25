from __future__ import annotations
import pandas as pd
from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetStats:
    rows: int
    columns: int
    missing_values: int


class DatasetProfile:
    def summarize(self, df: pd.DataFrame) -> DatasetStats:
        return DatasetStats(
            rows=len(df),
            columns=len(df.columns),
            missing_values=int(df.isna().sum().sum()),
        )