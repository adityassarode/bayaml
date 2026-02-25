"""
Baya Model Registry

Single source of truth mapping:
model_alias -> (backend_name, backend_model_key)

NO backend imports outside this layer.
"""

from __future__ import annotations
from typing import Dict, Tuple

from .base_backend import BaseBackend


class ModelRegistry:
    """Central deterministic model resolution."""

    # backend_name -> backend instance
    _backends: Dict[str, BaseBackend] = {}

    # public alias -> (backend_name, backend_model_key)
    _models: Dict[str, Tuple[str, str]] = {}

    # -------------------------------
    # Backend registration
    # -------------------------------
    @classmethod
    def register_backend(cls, backend: BaseBackend) -> None:
        name = backend.name
        if name in cls._backends:
            raise RuntimeError(f"Backend '{name}' already registered")
        cls._backends[name] = backend

    # -------------------------------
    # Model registration
    # -------------------------------
    @classmethod
    def register_model(
        cls,
        alias: str,
        backend_name: str,
        backend_model_key: str,
    ) -> None:
        if backend_name not in cls._backends:
            raise RuntimeError(f"Backend '{backend_name}' not registered")

        cls._models[alias] = (backend_name, backend_model_key)

    # -------------------------------
    # Resolution (CRITICAL)
    # -------------------------------
    @classmethod
    def resolve(cls, alias: str) -> tuple[BaseBackend, str]:
        if alias not in cls._models:
            raise ValueError(f"Model '{alias}' not registered")

        backend_name, model_key = cls._models[alias]
        backend = cls._backends[backend_name]
        return backend, model_key

    # -------------------------------
    # Determinism helpers
    # -------------------------------
    @classmethod
    def list_models(cls) -> list[str]:
        return sorted(cls._models.keys())

    @classmethod
    def clear(cls) -> None:
        cls._models.clear()
        cls._backends.clear()