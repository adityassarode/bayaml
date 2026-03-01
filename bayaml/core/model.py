from __future__ import annotations

from typing import Any, Optional

import numpy as np

from ..context import Context
from ..integrations.model_registry import ModelRegistry


class ModelModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def create(self, name: str, **kwargs: Any) -> "ModelModule":
        backend, model_name = ModelRegistry.resolve(name)
        model = backend.create_model(model_name, **kwargs)
        self._ctx.set_model(model, backend)
        return self

    def train(self, **kwargs: Any) -> "ModelModule":
        if not self._ctx.is_split:
            raise RuntimeError("Split data before training.")
        model = self._ctx.get_model()
        backend = self._ctx.get_backend()
        if model is None or backend is None:
            raise RuntimeError("Create a model first.")
        X_train, _, y_train, _ = self._ctx.get_split_data()
        trained = backend.train(model=model, X_train=X_train, y_train=y_train, seed=self._ctx.get_seed(), **kwargs)
        self._ctx.set_model(trained, backend)
        self._ctx.mark_fitted()

        if self._ctx.is_split and self._ctx.get_predictions() is None:
            self.predict()

        return self

    def predict(self, X: Optional[Any] = None) -> np.ndarray:
        if not self._ctx.is_fitted:
            raise RuntimeError("Model not trained.")
        model = self._ctx.get_model()
        backend = self._ctx.get_backend()
        if X is None:
            _, X, _, _ = self._ctx.get_split_data()
            scope = "test"
        else:
            scope = "external"
        preds = np.asarray(backend.predict(model=model, X=X))
        self._ctx.set_predictions(preds, scope=scope)
        return preds
