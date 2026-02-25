# baya/integrations/sklearn_backend.py

from __future__ import annotations
from typing import Any, Dict, Type

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR

from .base_backend import BaseBackend


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

    # identity
    @property
    def name(self) -> str:
        return "sklearn"

    # lifecycle
    def create_model(self, model_name: str, **kwargs: Any) -> Any:
        if model_name not in self._models:
            raise ValueError(f"Model '{model_name}' not supported by sklearn backend")
        return self._models[model_name](**kwargs)

    def train(self, model: Any, X: Any, y: Any, **kwargs: Any) -> Any:
        model.fit(X, y, **kwargs)
        return model

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)