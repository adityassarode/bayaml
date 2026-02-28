from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


class Context:
    """Central runtime state container for a project run."""

    def __init__(
        self,
        *,
        workspace: Optional[Path] = None,
        seed: int = 42,
    ) -> None:
        self._workspace = workspace
        self._seed = int(seed)

        self._dataframe: Optional[pd.DataFrame] = None
        self._target: Optional[str] = None
        self._task_type: Optional[str] = None

        self._X_train: Any = None
        self._X_test: Any = None
        self._y_train: Any = None
        self._y_test: Any = None
        self._is_split = False

        self._model: Any = None
        self._backend: Any = None
        self._is_fitted = False

        self._predictions: Any = None
        self._prediction_scope: Optional[str] = None

        self._metrics: Dict[str, Any] = {}
        self._artifacts: Dict[str, Any] = {}
        self._last_figure: Any = None

        self._locked = False

    def _ensure_mutable(self) -> None:
        if self._locked:
            raise RuntimeError("Context is locked.")

    def lock(self) -> None:
        self._locked = True

    @property
    def is_locked(self) -> bool:
        return self._locked

    def get_workspace(self) -> Optional[Path]:
        return self._workspace

    def get_seed(self) -> int:
        return self._seed

    def set_seed(self, seed: int) -> None:
        if self._is_split:
            raise RuntimeError("Cannot change seed after split.")
        self._ensure_mutable()
        self._seed = int(seed)

    def set_dataframe(self, df: pd.DataFrame) -> None:
        self._ensure_mutable()
        if self._is_split:
            raise RuntimeError("Cannot replace dataframe after split.")
        self._dataframe = df.copy()
        self._recompute_task_type()

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        return self._dataframe

    def ensure_dataframe(self) -> pd.DataFrame:
        if self._dataframe is None:
            raise ValueError("No DataFrame loaded.")
        return self._dataframe

    def set_target(self, target: str) -> None:
        df = self.ensure_dataframe()
        if self._is_split:
            raise RuntimeError("Cannot change target after split.")
        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found.")
        self._ensure_mutable()
        self._target = target
        self._recompute_task_type()

    def get_target(self) -> Optional[str]:
        return self._target

    def ensure_target(self) -> str:
        if self._target is None:
            raise ValueError("Target not set.")
        return self._target

    def _recompute_task_type(self) -> None:
        if self._dataframe is None or self._target is None:
            return
        kind = self._dataframe[self._target].dtype.kind
        self._task_type = "classification" if kind in ("i", "b", "O") else "regression"

    def get_task_type(self) -> Optional[str]:
        return self._task_type

    def set_split_data(self, X_train: Any, X_test: Any, y_train: Any, y_test: Any) -> None:
        self._ensure_mutable()
        self._X_train, self._X_test, self._y_train, self._y_test = X_train, X_test, y_train, y_test
        self._is_split = True

    def get_split_data(self) -> Tuple[Any, Any, Any, Any]:
        if not self._is_split:
            raise RuntimeError("Dataset not split.")
        return self._X_train, self._X_test, self._y_train, self._y_test

    @property
    def is_split(self) -> bool:
        return self._is_split

    def set_model(self, model: Any, backend: Any) -> None:
        self._ensure_mutable()
        self._model = model
        self._backend = backend

    def get_model(self) -> Any:
        return self._model

    def get_backend(self) -> Any:
        return self._backend

    def mark_fitted(self) -> None:
        self._is_fitted = True

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    def set_predictions(self, preds: Any, scope: str = "test") -> None:
        self._predictions = preds
        self._prediction_scope = scope

    def get_predictions(self) -> Any:
        return self._predictions

    def get_prediction_scope(self) -> Optional[str]:
        return self._prediction_scope

    def set_metrics(self, metrics: Dict[str, Any]) -> None:
        self._metrics = dict(metrics)

    def get_metrics(self) -> Dict[str, Any]:
        return dict(self._metrics)

    def log_artifact(self, name: str, meta: Dict[str, Any]) -> None:
        self._artifacts[name] = dict(meta)

    def get_artifacts(self) -> Dict[str, Any]:
        return dict(self._artifacts)

    def set_last_figure(self, figure: Any) -> None:
        self._last_figure = figure

    def get_last_figure(self) -> Any:
        return self._last_figure

    def reset_model_state(self) -> None:
        self._model = None
        self._backend = None
        self._is_fitted = False
        self._predictions = None
        self._prediction_scope = None
        self._metrics = {}
