"""
Sklearn Backend for Baya

Provides model factory for sklearn-based models.
"""

from __future__ import annotations

from typing import Any, Dict, Type

from ..base_backend import BaseBackend

# Import sklearn models
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
)
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor


class SklearnBackend(BaseBackend):
    """
    Backend responsible for building sklearn models.
    """

    def __init__(self) -> None:
        self._model_map: Dict[str, Type[Any]] = {
            # Classification
            "logistic_regression": LogisticRegression,
            "random_forest_classifier": RandomForestClassifier,
            "svm_classifier": SVC,
            "gradient_boosting_classifier": GradientBoostingClassifier,
            "knn_classifier": KNeighborsClassifier,

            # Regression
            "linear_regression": LinearRegression,
            "random_forest_regressor": RandomForestRegressor,
            "svm_regressor": SVR,
            "gradient_boosting_regressor": GradientBoostingRegressor,
            "knn_regressor": KNeighborsRegressor,
        }

    # -------------------------------------------------
    # Backend Identity
    # -------------------------------------------------

    def name(self) -> str:
        return "sklearn"

    # -------------------------------------------------
    # Build Model
    # -------------------------------------------------

    def build_model(
        self,
        model_name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Build sklearn model from name.
        """

        if model_name not in self._model_map:
            raise ValueError(
                f"Model '{model_name}' not supported in SklearnBackend."
            )

        model_class = self._model_map[model_name]
        return model_class(**kwargs)

    # -------------------------------------------------
    # List Available Models
    # -------------------------------------------------

    def available_models(self) -> list[str]:
        return list(self._model_map.keys())
