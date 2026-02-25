from __future__ import annotations

"""
Deterministic backend bootstrap.

Responsibilities:
- Register built-in backends
- Register supported models
- Freeze ModelRegistry
- Prevent duplicate registration
- No side effects outside registry
"""

from typing import Type

from .base_backend import BaseBackend
from .model_registry import ModelRegistry


# Internal idempotency guard
_BOOTSTRAPPED: bool = False


def _register_backend(
    backend_class: Type[BaseBackend],
) -> None:
    """
    Register backend and its models atomically.
    """

    backend = backend_class()

    # Prevent duplicate registration
    if backend.name in ModelRegistry.list_backends():
        return

    ModelRegistry.register_backend(backend)

    # Enforce strict contract
    model_names = backend.available_models()

    if not isinstance(model_names, list):
        raise TypeError(
            f"available_models() of '{backend.name}' must return list[str]."
        )

    for model_name in model_names:
        ModelRegistry.register_model(
            model_name=model_name,
            backend_name=backend.name,
        )


def bootstrap_backends() -> None:
    """
    Register all built-in backends deterministically.
    Freeze registry after bootstrap.
    """

    global _BOOTSTRAPPED

    if _BOOTSTRAPPED:
        return

    # -------------------------------
    # Built-in backends
    # -------------------------------
    from .sklearn.sklearn_backend import SklearnBackend

    _register_backend(SklearnBackend)

    # -------------------------------
    # Freeze registry after wiring
    # -------------------------------
    ModelRegistry.freeze()

    _BOOTSTRAPPED = True