from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC, SVR

from ..base_backend import BaseBackend


class SklearnBackend(BaseBackend):
    def __init__(self) -> None:
        self._models: Dict[str, Type[Any]] = {
            "linear_regression": LinearRegression,
            "logistic_regression": LogisticRegression,
            "random_forest_classifier": RandomForestClassifier,
            "random_forest_regressor": RandomForestRegressor,
            "svm_classifier": SVC,
            "svm_regressor": SVR,
        }

    @property
    def name(self) -> str:
        return "sklearn"

    @property
    def version(self) -> str:
        return "1"

    def available_models(self) -> List[str]:
        return sorted(self._models.keys())

    def create_model(self, model_type: str, **kwargs: Any) -> Any:
        if model_type not in self._models:
            raise ValueError(f"Unknown model '{model_type}'.")
        return self._models[model_type](**kwargs)

    def train(self, model: Any, X_train: Any, y_train: Any, *, seed: int, **kwargs: Any) -> Any:
        if hasattr(model, "get_params"):
            params = model.get_params()
            if "random_state" in params and params.get("random_state") is None:
                try:
                    model.set_params(random_state=seed)
                except Exception:
                    pass
        model.fit(X_train, y_train, **kwargs)
        return model

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)
