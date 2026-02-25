"""
Baya Encode Module

Handles:
- Categorical encoding
- Target encoding
- Text vectorization
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from ..context import Context


class EncodeModule:
    """
    Encoding operations for categorical and text data.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

        # Store fitted encoders inside context
        if not hasattr(self.context, "encoders"):
            self.context.encoders = {}

    # -------------------------------------------------
    # Categorical Encoding
    # -------------------------------------------------

    def encodeCategorical(
        self,
        columns: list[str],
        drop_original: bool = True,
    ) -> "EncodeModule":
        """
        One-hot encode categorical columns.
        """
        self.context.ensure_dataframe()
        df = self.context.dataframe

        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found.")

        encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        encoded_array = encoder.fit_transform(df[columns])

        encoded_df = pd.DataFrame(
            encoded_array,
            columns=encoder.get_feature_names_out(columns),
            index=df.index,
        )

        if drop_original:
            df = df.drop(columns=columns)

        df = pd.concat([df, encoded_df], axis=1)

        self.context.dataframe = df
        self.context.encoders["categorical"] = encoder

        return self

    # -------------------------------------------------
    # Target Encoding
    # -------------------------------------------------

    def encodeTarget(self) -> "EncodeModule":
        """
        Encode target column using LabelEncoder.
        """
        self.context.ensure_dataframe()
        self.context.ensure_target()

        target_col = self.context.target
        df = self.context.dataframe

        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found.")

        encoder = LabelEncoder()
        df[target_col] = encoder.fit_transform(df[target_col])

        self.context.dataframe = df
        self.context.encoders["target"] = encoder

        return self

    # -------------------------------------------------
    # Text Encoding
    # -------------------------------------------------

    def encodeText(
        self,
        column: str,
        max_features: Optional[int] = 1000,
        drop_original: bool = True,
    ) -> "EncodeModule":
        """
        Convert text column into TF-IDF features.
        """
        self.context.ensure_dataframe()
        df = self.context.dataframe

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found.")

        vectorizer = TfidfVectorizer(max_features=max_features)
        text_matrix = vectorizer.fit_transform(df[column].astype(str))

        text_df = pd.DataFrame(
            text_matrix.toarray(),
            columns=[f"{column}_tfidf_{i}" for i in range(text_matrix.shape[1])],
            index=df.index,
        )

        if drop_original:
            df = df.drop(columns=[column])

        df = pd.concat([df, text_df], axis=1)

        self.context.dataframe = df
        self.context.encoders[f"text_{column}"] = vectorizer

        return self

    # -------------------------------------------------
    # Transform New Data
    # -------------------------------------------------

    def transformCategorical(
        self,
        columns: list[str],
    ) -> pd.DataFrame:
        """
        Transform new data using previously fitted categorical encoder.
        """
        if "categorical" not in self.context.encoders:
            raise ValueError("No categorical encoder fitted.")

        encoder = self.context.encoders["categorical"]
        df = self.context.dataframe

        encoded_array = encoder.transform(df[columns])

        return pd.DataFrame(
            encoded_array,
            columns=encoder.get_feature_names_out(columns),
            index=df.index,
        )

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<EncodeModule rows={rows} cols={cols}>"
