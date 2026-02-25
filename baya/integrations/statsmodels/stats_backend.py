from __future__ import annotations

from typing import Any, Dict

import numpy as np
import statsmodels.api as sm

from ..base_backend import BaseBackend


class StatsBackend(BaseBackend):
    """
    Statsmodels Backend

    Supports:
    - OLS regression
    - GLM
    """

    # -------------------------------------------------
    # Identity
    # -------------------------------------------------

    @property
    def name(self) -> str:
        return "statsmodels"

    # -------------------------------------------------
    # Model Creation
    # -------------------------------------------------

    def create_model(self, model_type: str, **kwargs: Any) -> Any:
        """
        Returns model descriptor.
        Training attaches fitted result.
        """

        if model_type == "ols":
            return {"type": "ols", "model": None}

        if model_type == "glm":
            family = kwargs.get("family", sm.families.Gaussian())
            return {"type": "glm", "family": family, "model": None}

        raise ValueError(f"Unsupported statsmodels model '{model_type}'")

    # -------------------------------------------------
    # Training
    # -------------------------------------------------

    def train(
        self,
        model: Dict[str, Any],
        X_train: Any,
        y_train: Any,
        **kwargs: Any,
    ) -> Dict[str, Any]:

        X = np.asarray(X_train, dtype=float)
        y = np.asarray(y_train, dtype=float)

        X = sm.add_constant(X)

        if model["type"] == "ols":
            fitted = sm.OLS(y, X).fit()
            model["model"] = fitted
            return model

        if model["type"] == "glm":
            family = model["family"]
            fitted = sm.GLM(y, X, family=family).fit()
            model["model"] = fitted
            return model

        raise ValueError("Unknown statsmodels model")

    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------

    def predict(
        self,
        model: Dict[str, Any],
        X: Any,
    ) -> Any:

        if model["model"] is None:
            raise RuntimeError("Model not trained.")

        X_arr = np.asarray(X, dtype=float)
        X_arr = sm.add_constant(X_arr)

        return model["model"].predict(X_arr)

    # -------------------------------------------------
    # Evaluation
    # -------------------------------------------------

    def evaluate(
        self,
        model: Dict[str, Any],
        X_test: Any,
        y_test: Any,
    ) -> Dict[str, Any]:

        y_pred = self.predict(model, X_test)
        y_true = np.asarray(y_test, dtype=float)

        mse = float(np.mean((y_true - y_pred) ** 2))

        return {"mse": mse}