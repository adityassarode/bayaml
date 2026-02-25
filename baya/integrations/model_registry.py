"""
Baya Model Registry

Central registry mapping:

model_name  →  backend instance

Supports:
- Built-in backends
- Custom injected backends
- Plugin-registered backends
"""

from __future__ import annotations

from typing import Dict

from .base_backend import BaseBackend


class ModelRegistry:
    """
    Central model-to-backend registry.
    """

    # model_name → backend instance
    _model_map: Dict[str, BaseBackend] = {}

    # backend_name → backend instance
    _backend_map: Dict[str, BaseBackend] = {}

    # -------------------------------------------------
    # Backend Registration
    # -------------------------------------------------

    @classmethod
    def register_backend(cls, backend: BaseBackend) -> None:
        """
        Register a backend instance.

        Example:
            ModelRegistry.register_backend(SklearnBackend())
        """

        backend_name = backend.name()

        cls._backend_map[backend_name] = backend

    # -------------------------------------------------
    # Model Registration
    # -------------------------------------------------

    @classmethod
    def register_model(
        cls,
        model_name: str,
        backend_name: str,
    ) -> None:
        """
        Map model name to backend.
        """

        if backend_name not in cls._backend_map:
            raise ValueError(
                f"Backend '{backend_name}' not registered."
            )

        cls._model_map[model_name] = cls._backend_map[backend_name]

    # -------------------------------------------------
    # Backend Lookup
    # -------------------------------------------------

    @classmethod
    def get_backend_for_model(
        cls,
        model_name: str,
    ) -> BaseBackend:
        """
        Get backend responsible for model.
        """

        if model_name not in cls._model_map:
            raise ValueError(
                f"Model '{model_name}' not registered in ModelRegistry."
            )

        return cls._model_map[model_name]

    # -------------------------------------------------
    # Direct Backend Access
    # -------------------------------------------------

    @classmethod
    def get_backend(
        cls,
        backend_name: str,
    ) -> BaseBackend:
        if backend_name not in cls._backend_map:
            raise ValueError(
                f"Backend '{backend_name}' not registered."
            )

        return cls._backend_map[backend_name]

    # -------------------------------------------------
    # Introspection
    # -------------------------------------------------

    @classmethod
    def list_models(cls) -> list[str]:
        return list(cls._model_map.keys())

    @classmethod
    def list_backends(cls) -> list[str]:
        return list(cls._backend_map.keys())

    # -------------------------------------------------
    # Reset (for testing)
    # -------------------------------------------------

    @classmethod
    def clear(cls) -> None:
        cls._model_map.clear()
        cls._backend_map.clear()

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<ModelRegistry "
            f"models={len(self._model_map)} "
            f"backends={len(self._backend_map)}>"
        )
