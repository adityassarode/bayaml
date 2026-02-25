from __future__ import annotations

from typing import Any, Dict, Callable, Tuple
import numpy as np

from ..base_backend import BaseBackend


class ScipyBackend(BaseBackend):
    """
    Scipy statistical / optimization backend.

    Provides lightweight mathematical models.
    No preprocessing, scaling, encoding, or splitting.
    """

    # -------------------------------------------------
    # Identity
    # -------------------------------------------------

    @property
    def name(self) -> str:
        return "scipy"

    # -------------------------------------------------
    # Model Creation
    # -------------------------------------------------

    def create_model(self, model_type: str, **kwargs) -> Dict[str, Any]:
        """
        Create a scipy model descriptor (not fitted yet).
        """

        if model_type == "linear_regression":
            return {"type": "linear_regression", "coef": None}

        if model_type == "curve_fit":
            if "function" not in kwargs:
                raise ValueError("curve_fit requires 'function' argument")
            return {"type": "curve_fit", "function": kwargs["function"], "params": None}

        raise ValueError(f"Unsupported scipy model '{model_type}'")

    # -------------------------------------------------
    # Training
    # -------------------------------------------------

    def train(
        self,
        model: Dict[str, Any],
        X_train: Any,
        y_train: Any,
        **kwargs,
    ) -> Dict[str, Any]:

        X = np.asarray(X_train, dtype=float)
        y = np.asarray(y_train, dtype=float)

        if model["type"] == "linear_regression":
            # add bias column
            X_aug = np.c_[np.ones(len(X)), X]

            coef, *_ = np.linalg.lstsq(X_aug, y, rcond=None)
            model["coef"] = coef
            return model

        if model["type"] == "curve_fit":
            from scipy.optimize import curve_fit

            func: Callable = model["function"]

            params, _ = curve_fit(func, X, y, **kwargs)
            model["params"] = params
            return model

        raise ValueError("Unknown scipy model")

    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------

    def predict(
        self,
        model: Dict[str, Any],
        X: Any,
    ) -> Any:

        X_arr = np.asarray(X, dtype=float)

        if model["type"] == "linear_regression":
            if model["coef"] is None:
                raise RuntimeError("Model not trained")

            X_aug = np.c_[np.ones(len(X_arr)), X_arr]
            return X_aug @ model["coef"]

        if model["type"] == "curve_fit":
            if model["params"] is None:
                raise RuntimeError("Model not trained")

            func: Callable = model["function"]
            return func(X_arr, *model["params"])

        raise ValueError("Unknown scipy model")

    # -------------------------------------------------
    # Evaluation (optional but useful)
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