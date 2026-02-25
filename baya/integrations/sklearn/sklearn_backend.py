from __future__ import annotations

from typing import Any, Dict, Type, Optional, List

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

from ..base_backend import BaseBackend


class SklearnBackend(BaseBackend):
    """
    Sklearn execution backend.

    Guarantees:
    - Stateless
    - Deterministic when seed provided
    - No global RNG mutation
    - No Context access
    """

    def __init__(self) -> None:
        self._models: Dict[str, Type[Any]] = {
            "linear_regression": LinearRegression,
            "logistic_regression": LogisticRegression,
            "random_forest_classifier": RandomForestClassifier,
            "random_forest_regressor": RandomForestRegressor,
            "svm_classifier": SVC,
            "svm_regressor": SVR,
        }

    # =====================================================
    # Identity
    # =====================================================

    @property
    def name(self) -> str:
        return "sklearn"

    # =====================================================
    # Capability Declaration
    # =====================================================

    def available_models(self) -> List[str]:
        # Deterministic ordering
        return sorted(self._models.keys())

    # =====================================================
    # Model Creation
    # =====================================================

    def create_model(
        self,
        model_type: str,
        **kwargs: Any,
    ) -> Any:

        if model_type not in self._models:
            raise ValueError(
                f"Model '{model_type}' not supported by SklearnBackend."
            )

        model_class = self._models[model_type]
        return model_class(**kwargs)

    # =====================================================
    # Training
    # =====================================================

    def train(
        self,
        model: Any,
        X_train: Any,
        y_train: Any,
        *,
        seed: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Deterministic training.

        - Injects seed only if model supports random_state
        - Does NOT mutate global RNG
        - Does NOT override explicitly set random_state
        """

        if seed is not None and hasattr(model, "get_params"):
            params = model.get_params()

            if "random_state" in params:
                if params.get("random_state") is None:
                    try:
                        model.set_params(random_state=seed)
                    except Exception:
                        # Some sklearn models disallow post-init change
                        pass

        model.fit(X_train, y_train, **kwargs)
        return model

    # =====================================================
    # Prediction
    # =====================================================

    def predict(
        self,
        model: Any,
        X: Any,
    ) -> Any:
        return model.predict(X)

    # =====================================================
    # Probability Support
    # =====================================================

    def supports_proba(self, model: Any) -> bool:
        return hasattr(model, "predict_proba")

    def predict_proba(
        self,
        model: Any,
        X: Any,
    ) -> Any:
        if not hasattr(model, "predict_proba"):
            raise RuntimeError(
                f"Model '{type(model).__name__}' does not support probability prediction."
            )

        return model.predict_proba(X)