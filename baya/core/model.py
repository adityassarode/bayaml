from __future__ import annotations

from typing import Any, Optional
import numpy as np

from ..context import Context
from ..integrations.model_registry import ModelRegistry
from ..integrations.base_backend import BaseBackend
from ..guardrails.schema_guard import validate_schema


class ModelModule:
    """
    Model lifecycle controller.

    Responsibilities:
    - Model resolution
    - Training boundary enforcement
    - Deterministic seed propagation
    - Strict inference boundary
    """

    def __init__(self, context: Context) -> None:
        self._ctx: Context = context

    # =====================================================
    # Create
    # =====================================================

    def create(self, name: str, *, target: str) -> Any:

        self._ctx.ensure_dataframe()

        current_target = self._ctx.get_target()

        if current_target is None:
            self._ctx.set_target(target)
        elif current_target != target:
            raise RuntimeError(
                "Target already set. Cannot change target after initialization."
            )

        backend, model_name = ModelRegistry.resolve(name)

        if not isinstance(backend, BaseBackend):
            raise TypeError("Resolved backend is invalid.")

        model = backend.create_model(model_name)

        self._ctx.set_model(model, backend)

        self._ctx.set_model(model, backend)
        return self

    # =====================================================
    # Train
    # =====================================================

    def train(self, **kwargs: Any) -> "ModelModule":

        if not self._ctx.is_split:
            raise RuntimeError("Dataset must be split before training.")

        model = self._ctx.get_model()
        backend = self._ctx.get_backend()

        if model is None or backend is None:
            raise RuntimeError("Model not created.")

        X_train, _, y_train, _ = self._ctx.get_split_data()

        seed = self._ctx.get_seed()
        if "seed" not in kwargs:
            kwargs["seed"] = seed

        trained_model = backend.train(
            model=model,
            X_train=X_train,
            y_train=y_train,
            **kwargs,
        )

        self._ctx.set_model(trained_model, backend)
        self._ctx.mark_fitted()

        return self

    # =====================================================
    # Predict (STRICT INFERENCE BOUNDARY)
    # =====================================================

    def predict(self, X: Optional[Any] = None) -> np.ndarray:

        if not self._ctx.is_fitted:
            raise RuntimeError("Model not trained.")

        model = self._ctx.get_model()
        backend = self._ctx.get_backend()

        if model is None or backend is None:
            raise RuntimeError("Model state invalid.")

        # -------------------------------------------------
        # Default: test set prediction
        # -------------------------------------------------
        if X is None:
            if not self._ctx.is_split:
                raise RuntimeError("No split data available.")

            _, X_test, _, _ = self._ctx.get_split_data()
            X = X_test

        # -------------------------------------------------
        # External data: schema validation required
        # -------------------------------------------------
        else:
            reference_df = self._ctx.get_dataframe()

            if reference_df is None:
                raise RuntimeError("Reference dataset unavailable.")

            # Validate strict schema match
            validate_schema(
                reference=reference_df.drop(columns=[self._ctx.get_target()]),
                new=X,
            )

        # -------------------------------------------------
        # Backend inference (no model bypass)
        # -------------------------------------------------
        preds = backend.predict(
            model=model,
            X=X,
        )

        # Explicit overwrite (deterministic)
        self._ctx.set_predictions(preds)

        return preds