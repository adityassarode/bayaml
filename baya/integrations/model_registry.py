from __future__ import annotations

from typing import Dict, Tuple, List

from .base_backend import BaseBackend


class ModelRegistry:
    """
    Central deterministic model registry.

    Rules:
    - No auto-registration
    - No import-time side effects
    - Explicit backend registration
    - Explicit model registration
    - Explicit freeze
    - Deterministic resolution
    """

    _model_map: Dict[str, str] = {}
    _backend_map: Dict[str, BaseBackend] = {}
    _is_frozen: bool = False

    # =====================================================
    # Backend Registration
    # =====================================================

    @classmethod
    def register_backend(cls, backend: BaseBackend) -> None:
        if cls._is_frozen:
            raise RuntimeError("Registry is frozen. Cannot register backends.")

        backend_name: str = backend.name

        if backend_name in cls._backend_map:
            raise ValueError(f"Backend '{backend_name}' already registered.")

        cls._backend_map[backend_name] = backend

    # =====================================================
    # Model Registration
    # =====================================================

    @classmethod
    def register_model(cls, model_name: str, backend_name: str) -> None:
        if cls._is_frozen:
            raise RuntimeError("Registry is frozen. Cannot register models.")

        if model_name in cls._model_map:
            raise ValueError(f"Model '{model_name}' already registered.")

        if backend_name not in cls._backend_map:
            raise ValueError(f"Backend '{backend_name}' not registered.")

        backend = cls._backend_map[backend_name]

        if model_name not in backend.available_models():
            raise ValueError(
                f"Model '{model_name}' not supported by backend '{backend_name}'."
            )

        cls._model_map[model_name] = backend_name

    # =====================================================
    # Resolve
    # =====================================================

    @classmethod
    def resolve(cls, model_name: str) -> Tuple[BaseBackend, str]:
        if model_name not in cls._model_map:
            raise ValueError(f"Model '{model_name}' not registered.")

        backend_name = cls._model_map[model_name]

        if backend_name not in cls._backend_map:
            raise RuntimeError(f"Backend '{backend_name}' not registered.")

        backend = cls._backend_map[backend_name]

        return backend, model_name

    # =====================================================
    # Explicit Freeze
    # =====================================================

    @classmethod
    def freeze(cls) -> None:
        cls._is_frozen = True

    # =====================================================
    # Introspection
    # =====================================================

    @classmethod
    def list_models(cls) -> List[str]:
        return sorted(cls._model_map.keys())

    @classmethod
    def list_backends(cls) -> List[str]:
        return sorted(cls._backend_map.keys())

    # =====================================================
    # Testing Reset (Controlled)
    # =====================================================

    @classmethod
    def clear(cls) -> None:
        """
        Deterministic registry reset.
        Test-only use.
        """
        cls._model_map.clear()
        cls._backend_map.clear()
        cls._is_frozen = False