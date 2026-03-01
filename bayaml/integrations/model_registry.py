from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Tuple

from .base_backend import BaseBackend


class ModelRegistry:
    _models: Dict[str, str] = {}
    _backends: Dict[str, BaseBackend] = {}
    _frozen = False

    @classmethod
    def register_backend(cls, backend: BaseBackend) -> None:
        if cls._frozen:
            raise RuntimeError("Registry frozen.")
        if backend.name in cls._backends:
            return
        cls._backends[backend.name] = backend

    @classmethod
    def register_model(cls, model_name: str, backend_name: str) -> None:
        if cls._frozen:
            raise RuntimeError("Registry frozen.")
        if backend_name not in cls._backends:
            raise ValueError(f"Unknown backend: {backend_name}")
        cls._models[model_name] = backend_name

    @classmethod
    def list_backends(cls) -> List[str]:
        return sorted(cls._backends)

    @classmethod
    def list_models(cls) -> List[str]:
        return sorted(cls._models)

    @classmethod
    def resolve(cls, model_name: str) -> Tuple[BaseBackend, str]:
        if model_name not in cls._models:
            raise ValueError(f"Model '{model_name}' not registered.")
        backend_name = cls._models[model_name]
        return cls._backends[backend_name], model_name

    @classmethod
    def freeze(cls) -> None:
        cls._frozen = True

    @classmethod
    def is_frozen(cls) -> bool:
        return cls._frozen

    @classmethod
    def snapshot(cls) -> Dict[str, Any]:
        return {
            "models": cls.list_models(),
            "backends": cls.list_backends(),
            "versions": {k: v.version for k, v in cls._backends.items()},
        }

    @classmethod
    def registry_hash(cls) -> str:
        return hashlib.sha256(json.dumps(cls.snapshot(), sort_keys=True).encode("utf-8")).hexdigest()

    @classmethod
    def clear(cls) -> None:
        cls._models.clear()
        cls._backends.clear()
        cls._frozen = False
