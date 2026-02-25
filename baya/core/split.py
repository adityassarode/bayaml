from __future__ import annotations

from typing import Any
import pandas as pd
from sklearn.model_selection import train_test_split

from ..context import Context


class SplitModule:
    """
    Dataset splitting operations.

    Deterministic.
    Context-driven.
    """

    def __init__(self, context: Context) -> None:
        self._ctx: Context = context

    # =====================================================
    # Random Split
    # =====================================================

    def random(self, *, test_size: float = 0.2) -> "SplitModule":
        """
        Deterministic random split using context seed.
        """

        self._ctx.ensure_dataframe()
        self._ctx.ensure_target()

        if self._ctx.is_split:
            raise RuntimeError("Dataset already split.")

        df: pd.DataFrame = self._ctx.get_dataframe()
        target: str = self._ctx.get_target()
        seed: int = self._ctx.get_seed()

        X = df.drop(columns=[target])
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=seed,
        )

        self._ctx.set_split_data(X_train, X_test, y_train, y_test)

        return self

    # =====================================================
    # Default Train/Test Split (80/20)
    # =====================================================

    def train_test(self) -> "SplitModule":
        """
        Default deterministic 80/20 split.
        """
        return self.random(test_size=0.2)