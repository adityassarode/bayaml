from __future__ import annotations

from typing import Dict, Tuple, List, Any
import hashlib
import json
import os

from .base_backend import BaseBackend


class ModelRegistry:
    """
    Central deterministic model registry.

    Guarantees:
    - Explicit registration
    - No auto-registration
    - Explicit freeze
    - Deterministic snapshot
    - Reproducibility-safe hashing
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

        name = backend.name

        if name in cls._backend_map:
            raise ValueError(f"Backend '{name}' already registered.")

        cls._backend_map[name] = backend

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

        return cls._backend_map[backend_name], model_name

    # =====================================================
    # Freeze
    # =====================================================

    @classmethod
    def freeze(cls) -> None:
        if cls._is_frozen:
            return

        if not cls._backend_map:
            raise RuntimeError("Cannot freeze empty registry.")

        cls._is_frozen = True

    @classmethod
    def is_frozen(cls) -> bool:
        return cls._is_frozen

    # =====================================================
    # Snapshot / Hash (Reproducibility Safe)
    # =====================================================

    @classmethod
    def snapshot(cls) -> Dict[str, Any]:
        return {
            "models": sorted(cls._model_map.keys()),
            "backends": sorted(cls._backend_map.keys()),
            "backend_versions": {
                name: getattr(cls._backend_map[name], "version", "unknown")
                for name in sorted(cls._backend_map.keys())
            },
        }

    @classmethod
    def registry_hash(cls) -> str:
        if not cls._is_frozen:
            raise RuntimeError("Registry must be frozen before computing hash.")

        encoded = json.dumps(
            cls.snapshot(),
            sort_keys=True,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    # =====================================================
    # Test Reset (Protected)
    # =====================================================

    @classmethod
    def clear(cls) -> None:
        if not os.environ.get("BAYA_TEST_MODE"):
            raise RuntimeError("Registry.clear() allowed only in test mode.")

        cls._model_map.clear()
        cls._backend_map.clear()
        cls._is_frozen = False