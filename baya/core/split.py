"""
Baya Split Module

Handles:
- Train/Test splitting
- Cross-validation
"""

from __future__ import annotations

from typing import Optional, Any

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score

from ..context import Context


class SplitModule:
    """
    Data splitting operations.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Train/Test Split
    # -------------------------------------------------

    def splitData(
        self,
        test_size: float = 0.2,
        random_state: Optional[int] = 42,
        shuffle: bool = True,
    ) -> "SplitModule":
        """
        Split dataset into train and test sets.
        """

        self.context.ensure_dataframe()
        self.context.ensure_target()

        df = self.context.dataframe
        target_col = self.context.target

        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found.")

        X = df.drop(columns=[target_col])
        y = df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            shuffle=shuffle,
        )

        self.context.X_train = X_train
        self.context.X_test = X_test
        self.context.y_train = y_train
        self.context.y_test = y_test

        return self

    # -------------------------------------------------
    # Cross Validation
    # -------------------------------------------------

    def crossValidate(
        self,
        model: Any,
        cv: int = 5,
        scoring: Optional[str] = None,
    ) -> pd.Series:
        """
        Perform k-fold cross-validation.
        """

        self.context.ensure_dataframe()
        self.context.ensure_target()

        df = self.context.dataframe
        target_col = self.context.target

        X = df.drop(columns=[target_col])
        y = df[target_col]

        scores = cross_val_score(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
        )

        return pd.Series(scores, name="cv_scores")

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        if self.context.X_train is not None:
            rows = len(self.context.X_train)
        else:
            rows = 0

        return f"<SplitModule train_rows={rows}>"
