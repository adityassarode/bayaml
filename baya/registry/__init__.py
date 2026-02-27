
from __future__ import annotations

from typing import Any, Callable, Dict

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC, SVR


from .artifact_store import ArtifactStore
from .dataset_registry import DatasetRegistry
from .model_registry import RegistryModelStore
from .versioning import Versioning


ModelConstructor = Callable[..., Any]
MODEL_REGISTRY: Dict[str, ModelConstructor] = {}


def register_model(name: str, constructor: ModelConstructor) -> None:
    MODEL_REGISTRY[name] = constructor


def get_model(name: str) -> ModelConstructor:
    if name not in MODEL_REGISTRY:
        raise KeyError(f"Model '{name}' not found in MODEL_REGISTRY")
    return MODEL_REGISTRY[name]


def list_models() -> list[str]:
    return sorted(MODEL_REGISTRY)


# default built-ins
register_model("linear_regression", LinearRegression)
register_model("logistic_regression", LogisticRegression)
register_model("random_forest_classifier", RandomForestClassifier)
register_model("random_forest_regressor", RandomForestRegressor)
register_model("svm_classifier", SVC)
register_model("svm_regressor", SVR)


__all__ = [
    "MODEL_REGISTRY",
    "register_model",
    "get_model",
    "list_models",
    "RegistryModelStore",
    "DatasetRegistry",
    "ArtifactStore",
    "Versioning",
]

__all__ = ["RegistryModelStore", "DatasetRegistry", "ArtifactStore", "Versioning"]

