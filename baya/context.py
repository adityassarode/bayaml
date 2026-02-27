from __future__ import annotations

from typing import Optional, Any, Dict, Tuple, List
from pathlib import Path
import pandas as pd

from .integrations.base_backend import BaseBackend


class Context:
    """
    Central controlled state container.

    Architectural guarantees:
    - No mutation after execution lock
    - No dataset mutation after split
    - No seed mutation after split
    - No target mutation after split
    - No model rebinding after fit
    - Deterministic state transitions
    """

    # =====================================================
    # Initialization
    # =====================================================

    def __init__(
        self,
        *,
        workspace: Optional[Path] = None,
        seed: int = 42,
    ) -> None:

        # -------------------------
        # Core Data
        # -------------------------
        self._dataframe: Optional[pd.DataFrame] = None
        self._target: Optional[str] = None

        # -------------------------
        # Split State
        # -------------------------
        self._X_train: Optional[Any] = None
        self._X_test: Optional[Any] = None
        self._y_train: Optional[Any] = None
        self._y_test: Optional[Any] = None
        self._is_split: bool = False
        self._feature_columns: Optional[List[str]] = None

        # -------------------------
        # Modeling State
        # -------------------------
        self._model: Optional[Any] = None
        self._backend: Optional[BaseBackend] = None
        self._is_fitted: bool = False

        # -------------------------
        # Inference State
        # -------------------------
        self._predictions: Optional[Any] = None
        self._prediction_scope: Optional[str] = None  # "test" | "external"

        # -------------------------
        # Evaluation State
        # -------------------------
        self._metrics: Dict[str, Any] = {}
        self._task_type: Optional[str] = None  # "classification" | "regression"

        # -------------------------
        # Deterministic Control
        # -------------------------
        self._seed: int = seed

        # -------------------------
        # Workspace
        # -------------------------
        self._workspace: Optional[Path] = workspace

        # -------------------------
        # Execution Lock
        # -------------------------
        self._locked: bool = False

    # =====================================================
    # Internal Guards
    # =====================================================

    def _ensure_mutable(self) -> None:
        if self._locked:
            raise RuntimeError("Context is locked. No further mutation allowed.")

    # =====================================================
    # Execution Lock
    # =====================================================

    def lock(self) -> None:
        """
        Locks the context permanently.
        Called by Executor at training boundary.
        """
        self._locked = True

    @property
    def is_locked(self) -> bool:
        return self._locked

    # =====================================================
    # Workspace
    # =====================================================

    def get_workspace(self) -> Optional[Path]:
        return self._workspace

    # =====================================================
    # Seed Control
    # =====================================================

    def set_seed(self, seed: int) -> None:
        if self._is_split:
            raise RuntimeError("Cannot change seed after dataset split.")
        self._ensure_mutable()
        self._seed = seed

    def get_seed(self) -> int:
        return self._seed

    # =====================================================
    # Data Control
    # =====================================================

    def set_dataframe(self, df: pd.DataFrame) -> None:
        if self._is_split:
            raise RuntimeError("Cannot change dataset after split.")
        self._ensure_mutable()
        self._dataframe = df.copy()
        self.reset_split_state()
        self.reset_model_state()

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        return self._dataframe

    def ensure_dataframe(self) -> None:
        if self._dataframe is None:
            raise ValueError("No DataFrame loaded.")

    # =====================================================
    # Target Control
    # =====================================================

    def set_target(self, column: str) -> None:
        self.ensure_dataframe()

        if self._is_split:
            raise RuntimeError("Cannot change target after split.")

        if self._dataframe is None or column not in self._dataframe.columns:
            raise ValueError(f"Target column '{column}' not found.")

        self._ensure_mutable()

        self._target = column
        self._infer_task_type()
        self.reset_split_state()
        self.reset_model_state()

    def get_target(self) -> Optional[str]:
        return self._target

    def ensure_target(self) -> None:
        if self._target is None:
            raise ValueError("Target not set.")

    # =====================================================
    # Task Type
    # =====================================================

    def _infer_task_type(self) -> None:
        if self._dataframe is None or self._target is None:
            return

        series = self._dataframe[self._target]

        if series.dtype.kind in ("i", "b", "O"):
            self._task_type = "classification"
        else:
            self._task_type = "regression"

    def get_task_type(self) -> Optional[str]:
        return self._task_type

    # =====================================================
    # Split Control
    # =====================================================

    def set_split_data(
        self,
        X_train: Any,
        X_test: Any,
        y_train: Any,
        y_test: Any,
    ) -> None:
        if self._is_split:
            raise RuntimeError("Dataset already split.")

        self._ensure_mutable()

        self._X_train = X_train
        self._X_test = X_test
        self._y_train = y_train
        self._y_test = y_test
        self._is_split = True

        # Freeze feature schema
        if hasattr(X_train, "columns"):
            self._feature_columns = list(X_train.columns)

    def get_split_data(self) -> Tuple[Any, Any, Any, Any]:
        if not self._is_split:
            raise RuntimeError("Dataset not split yet.")

        return self._X_train, self._X_test, self._y_train, self._y_test

    def get_feature_columns(self) -> Optional[List[str]]:
        return self._feature_columns

    def reset_split_state(self) -> None:
        self._ensure_mutable()
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None
        self._feature_columns = None
        self._is_split = False

    @property
    def is_split(self) -> bool:
        return self._is_split

    # =====================================================
    # Model Control
    # =====================================================

    def set_model(self, model: Any, backend: BaseBackend) -> None:
        if self._is_fitted:
            raise RuntimeError("Cannot rebind model after training.")
        self._ensure_mutable()
        self._model = model
        self._backend = backend
        self._is_fitted = False

    def get_model(self) -> Optional[Any]:
        return self._model

    def get_backend(self) -> Optional[BaseBackend]:
        return self._backend

    def mark_fitted(self) -> None:
        self._is_fitted = True

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    # =====================================================
    # Prediction Control
    # =====================================================

    def set_predictions(self, preds: Any, *, scope: str = "test") -> None:
        self._ensure_mutable()
        self._predictions = preds
        self._prediction_scope = scope

    def get_predictions(self) -> Optional[Any]:
        return self._predictions

    def get_prediction_scope(self) -> Optional[str]:
        return self._prediction_scope

    # =====================================================
    # Metrics Control
    # =====================================================

    def set_metrics(self, metrics: Dict[str, Any]) -> None:
        self._ensure_mutable()
        self._metrics = metrics

    def get_metrics(self) -> Dict[str, Any]:
        return self._metrics

    # =====================================================
    # Reset
    # =====================================================

    def reset_model_state(self) -> None:
        self._ensure_mutable()
        self._model = None
        self._backend = None
        self._predictions = None
        self._prediction_scope = None
        self._metrics.clear()
        self._is_fitted = False