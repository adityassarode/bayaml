from __future__ import annotations

from .model_registry import ModelRegistry
from .sklearn.sklearn_backend import SklearnBackend


def bootstrap_backends() -> None:
    if ModelRegistry.list_backends():
        return
    backend = SklearnBackend()
    ModelRegistry.register_backend(backend)
    for model_name in backend.available_models():
        ModelRegistry.register_model(model_name, backend.name)
    ModelRegistry.freeze()
