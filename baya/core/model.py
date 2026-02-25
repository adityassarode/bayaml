"""
Baya Model Module

Handles:
- Training classifiers
- Training regressors
- Neural network training
- Custom model injection
- Custom training loops
- Prediction
- Hyperparameter tuning
- Backend registry integration
"""

from __future__ import annotations

from typing import Any, Optional, Callable

import numpy as np
from sklearn.model_selection import GridSearchCV

from ..context import Context
from ..integrations.model_registry import ModelRegistry


class ModelModule:
    """
    Model training and prediction module.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------

    def _ensure_split(self) -> None:
        if self.context.X_train is None or self.context.y_train is None:
            raise RuntimeError(
                "Data not split. Call p.split.splitData() before training."
            )

    def _resolve_model(self, model: Any) -> Any:
        """
        If model is string → use ModelRegistry
        If model is object → return directly
        """
        if isinstance(model, str):
            backend = ModelRegistry.get_backend_for_model(model)
            return backend.build_model(model)

        return model

    # -------------------------------------------------
    # Train Classifier
    # -------------------------------------------------

    def trainClassifier(
        self,
        model: Any,
    ) -> "ModelModule":
        """
        Train classification model.

        model:
            - string name (uses registry)
            - sklearn-like model object
        """

        self._ensure_split()

        model = self._resolve_model(model)

        model.fit(self.context.X_train, self.context.y_train)

        self.context.model = model
        self.context.model_type = "classification"
        self.context.mark_fitted()

        return self

    # -------------------------------------------------
    # Train Regressor
    # -------------------------------------------------

    def trainRegressor(
        self,
        model: Any,
    ) -> "ModelModule":
        """
        Train regression model.

        model:
            - string name (uses registry)
            - sklearn-like model object
        """

        self._ensure_split()

        model = self._resolve_model(model)

        model.fit(self.context.X_train, self.context.y_train)

        self.context.model = model
        self.context.model_type = "regression"
        self.context.mark_fitted()

        return self

    # -------------------------------------------------
    # Train Neural Network
    # -------------------------------------------------

    def trainNeural(
        self,
        model: Any,
        epochs: int = 10,
        batch_size: int = 32,
        **kwargs: Any,
    ) -> "ModelModule":
        """
        Train deep learning model (TensorFlow / PyTorch compatible).
        """

        self._ensure_split()

        model = self._resolve_model(model)

        # TensorFlow-style API
        if hasattr(model, "fit"):
            model.fit(
                self.context.X_train,
                self.context.y_train,
                epochs=epochs,
                batch_size=batch_size,
                **kwargs,
            )

        # PyTorch-style custom callable loop
        elif callable(model):
            model(
                self.context.X_train,
                self.context.y_train,
                epochs=epochs,
                batch_size=batch_size,
                **kwargs,
            )

        else:
            raise ValueError("Unsupported neural model type.")

        self.context.model = model
        self.context.model_type = "neural"
        self.context.mark_fitted()

        return self

    # -------------------------------------------------
    # Custom Training Loop
    # -------------------------------------------------

    def trainCustom(
        self,
        training_function: Callable[[Any, Any], Any],
    ) -> "ModelModule":
        """
        Inject custom training loop.
        """

        self._ensure_split()

        trained_model = training_function(
            self.context.X_train,
            self.context.y_train,
        )

        self.context.model = trained_model
        self.context.model_type = "custom"
        self.context.mark_fitted()

        return self

    # -------------------------------------------------
    # Predict
    # -------------------------------------------------

    def predict(
        self,
        X: Optional[Any] = None,
    ) -> np.ndarray:
        """
        Make predictions.
        """

        if self.context.model is None:
            raise RuntimeError("No trained model found.")

        if not hasattr(self.context.model, "predict"):
            raise RuntimeError("Model does not support predict().")

        if X is None:
            if self.context.X_test is None:
                raise RuntimeError("No test data available.")
            X = self.context.X_test

        preds = self.context.model.predict(X)

        self.context.predictions = preds

        return preds

    # -------------------------------------------------
    # Hyperparameter Tuning
    # -------------------------------------------------

    def tuneHyperparameters(
        self,
        model: Any,
        param_grid: dict,
        cv: int = 5,
        scoring: Optional[str] = None,
    ) -> "ModelModule":
        """
        Perform grid search hyperparameter tuning.
        """

        self._ensure_split()

        model = self._resolve_model(model)

        grid = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=cv,
            scoring=scoring,
        )

        grid.fit(self.context.X_train, self.context.y_train)

        self.context.model = grid.best_estimator_
        self.context.model_type = "tuned"
        self.context.best_params = grid.best_params_
        self.context.mark_fitted()

        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        model = self.context.model
        if model is None:
            return "<ModelModule model=None>"

        return f"<ModelModule model={model.__class__.__name__}>"
