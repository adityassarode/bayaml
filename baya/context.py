"""
Baya Context

Single source of truth for runtime state.
NO validation during declaration.
Validation happens only in ensure_* guards.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any, Dict, Tuple

import pandas as pd


class Context:
    """
    Central runtime state container.
    """

    def __init__(self, workspace: Optional[str | Path] = None) -> None:
        self.workspace: Optional[Path] = (
            Path(workspace).resolve() if workspace else None
        )

        # Core data
        self._dataframe: Optional[pd.DataFrame] = None
        self._target: Optional[str] = None

        # Model
        self.model: Optional[Any] = None
        self.model_type: Optional[str] = None

        # Split
        self.X_train: Optional[Any] = None
        self.X_test: Optional[Any] = None
        self.y_train: Optional[Any] = None
        self.y_test: Optional[Any] = None

        # Metrics
        self.metrics: Dict[str, Any] = {}

        # Lifecycle
        self._is_fitted: bool = False

    # =================================================
    # Declaration (NO VALIDATION HERE)
    # =================================================

    def set_dataframe(self, df: pd.DataFrame) -> None:
        self._dataframe = df
        self.reset_model_state()

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        return self._dataframe

    def set_target(self, target: Optional[str]) -> None:
        self._target = target
        self.reset_model_state()

    def get_target(self) -> Optional[str]:
        return self._target

    # =================================================
    # Guards (VALIDATION ONLY HERE)
    # =================================================

    def ensure_dataframe(self) -> None:
        if self._dataframe is None:
            raise RuntimeError("Dataset not loaded.")

    def ensure_target(self) -> None:
        self.ensure_dataframe()
        if self._target is None:
            raise RuntimeError("Target not defined.")
        if self._target not in self._dataframe.columns:
            raise RuntimeError(
                f"Target column '{self._target}' not found in dataset."
            )

    def ensure_split(self) -> None:
        if self.X_train is None or self.y_train is None:
            raise RuntimeError("Data not split before training.")

    # =================================================
    # Split control
    # =================================================

    def set_split(
        self,
        X_train: Any,
        X_test: Any,
        y_train: Any,
        y_test: Any,
    ) -> None:
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self._is_fitted = False

    # =================================================
    # Lifecycle
    # =================================================

    def mark_fitted(self) -> None:
        self._is_fitted = True

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    def reset_model_state(self) -> None:
        self.model = None
        self.model_type = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.metrics.clear()
        self._is_fitted = False

    # =================================================

    def __repr__(self) -> str:
        rows = len(self._dataframe) if self._dataframe is not None else 0
        return f"<BayaContext rows={rows} target={self._target}>"