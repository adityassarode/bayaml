from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from ..context import Context


class EncodeModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def label(self, column: str) -> "EncodeModule":
        df = self._ctx.ensure_dataframe().copy()
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")
        enc = LabelEncoder()
        df[column] = enc.fit_transform(df[column].astype(str))
        self._ctx.set_dataframe(df)
        return self

    def one_hot(self, column: str, drop_first: bool = False) -> "EncodeModule":
        df = self._ctx.ensure_dataframe().copy()
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")
        out = pd.get_dummies(df, columns=[column], drop_first=drop_first)
        self._ctx.set_dataframe(out)
        return self

    def tfidf(self, column: str, max_features: int = 50, prefix: Optional[str] = None) -> "EncodeModule":
        df = self._ctx.ensure_dataframe().copy()
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")
        vec = TfidfVectorizer(max_features=max_features)
        mat = vec.fit_transform(df[column].astype(str)).toarray()
        names = [f"{prefix or column}_tfidf_{i}" for i in range(mat.shape[1])]
        tfidf_df = pd.DataFrame(mat, columns=names, index=df.index)
        out = pd.concat([df.drop(columns=[column]), tfidf_df], axis=1)
        self._ctx.set_dataframe(out)
        return self
