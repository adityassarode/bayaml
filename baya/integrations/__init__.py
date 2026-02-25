from __future__ import annotations

from importlib import import_module
from typing import Type, List

from .base_backend import BaseBackend
from .model_registry import ModelRegistry


# =====================================================
# Backend Bootstrap
# =====================================================

def register_backend(
    module_path: str,
    class_name: str,
) -> None:
    """
    Deterministic backend registration.

    No silent failures.
    No import-time side effects.
    Must be called explicitly during system bootstrap.
    """

    if ModelRegistry.list_backends():
    # Already bootstrapped — do nothing
        return

    module = import_module(module_path)

    backend_class: Type[BaseBackend] = getattr(module, class_name)

    backend = backend_class()

    backend_name: str = backend.name

    # Validate contract strictly
    if not hasattr(backend, "available_models"):
        raise TypeError(
            f"Backend '{backend_name}' must implement available_models()."
        )

    model_names: List[str] = backend.available_models()

    if not isinstance(model_names, list):
        raise TypeError(
            f"available_models() of '{backend_name}' must return list[str]."
        )

    # -------- Atomic registration block --------
    # Validate first
    for model_name in model_names:
        if not isinstance(model_name, str):
            raise TypeError(
                f"Invalid model name '{model_name}' in backend '{backend_name}'."
            )

    # Register backend
    ModelRegistry.register_backend(backend)

    # Register models
    for model_name in model_names:
        ModelRegistry.register_model(
            model_name=model_name,
            backend_name=backend_name,
        )


# =====================================================
# Explicit Bootstrap
# =====================================================

def bootstrap_integrations() -> None:
    """
    Explicit integration bootstrap.
    Must be called once during application startup.
    """

    register_backend(
        "baya.integrations.sklearn.sklearn_backend",
        "SklearnBackend",
    )


__all__ = [
    "BaseBackend",
    "ModelRegistry",
    "bootstrap_integrations",
]