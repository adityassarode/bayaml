"""
Baya Integrations Bootstrap

Provides controlled, deterministic backend registration.

NO automatic side effects at import time.
Project is responsible for calling bootstrap_integrations().
"""

from __future__ import annotations

from importlib import import_module
from typing import Iterable, Tuple

from .base_backend import BaseBackend
from .model_registry import ModelRegistry

# ---------------------------------------------------------------------
# Backend Definitions (static — deterministic)
# ---------------------------------------------------------------------

_BUILTIN_BACKENDS: Tuple[Tuple[str, str], ...] = (
    ("baya.integrations.sklearn.sklearn_backend", "SklearnBackend"),
    ("baya.integrations.tensorflow.tensorflow_backend", "TensorFlowBackend"),
    ("baya.integrations.pytorch.pytorch_backend", "PyTorchBackend"),
    ("baya.integrations.scipy.scipy_backend", "ScipyBackend"),
    ("baya.integrations.statsmodels.stats_backend", "StatsBackend"),
)

# guard against multiple initialization
_BOOTSTRAPPED: bool = False


# ---------------------------------------------------------------------
# Internal loader
# ---------------------------------------------------------------------

def _safe_load_backend(module_path: str, class_name: str) -> None:
    """
    Load backend safely and deterministically.

    Failure is explicit but non-fatal.
    """
    try:
        module = import_module(module_path)
        backend_cls = getattr(module, class_name)

        backend: BaseBackend = backend_cls()

    except ModuleNotFoundError:
        # dependency missing — acceptable
        return

    except Exception as exc:
        raise RuntimeError(
            f"Backend '{class_name}' failed to initialize: {exc}"
        ) from exc

    # Register backend
    ModelRegistry.register_backend(backend)

    # Register models exposed by backend
    for model_name in backend.available_models():
        ModelRegistry.register_model(model_name, backend.name)


# ---------------------------------------------------------------------
# Public bootstrap
# ---------------------------------------------------------------------

def bootstrap_integrations() -> None:
    """
    Deterministically register all available integrations.

    Idempotent — safe to call multiple times.
    """
    global _BOOTSTRAPPED

    if _BOOTSTRAPPED:
        return

    for module_path, class_name in _BUILTIN_BACKENDS:
        _safe_load_backend(module_path, class_name)

    _BOOTSTRAPPED = True


# ---------------------------------------------------------------------
# Testing utility
# ---------------------------------------------------------------------

def reset_integrations() -> None:
    """
    Reset registry (used in tests only).
    """
    global _BOOTSTRAPPED
    ModelRegistry.clear()
    _BOOTSTRAPPED = False


__all__ = [
    "BaseBackend",
    "ModelRegistry",
    "bootstrap_integrations",
    "reset_integrations",
]