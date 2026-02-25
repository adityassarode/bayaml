"""
Baya Integrations Package

Handles integration with external ML libraries:

- scikit-learn
- TensorFlow
- PyTorch
- SciPy
- Statsmodels
"""

from __future__ import annotations

from importlib import import_module
from typing import Optional

from .base_backend import BaseBackend
from .model_registry import ModelRegistry


# -----------------------------------------------------
# Safe Backend Registration Helper
# -----------------------------------------------------

def _register_backend(module_path: str, class_name: str) -> None:
    """
    Safely import backend and register it.
    """

    try:
        module = import_module(module_path)
        backend_class = getattr(module, class_name)
        backend_instance: BaseBackend = backend_class()

        ModelRegistry.register_backend(backend_instance)

        # Register all models exposed by backend
        for model_name in backend_instance.available_models():
            ModelRegistry.register_model(
                model_name,
                backend_instance.name(),
            )

    except Exception:
        # Silently skip if dependency not installed
        pass


# -----------------------------------------------------
# Register Built-in Backends
# -----------------------------------------------------

_register_backend(
    "baya.integrations.sklearn.sklearn_backend",
    "SklearnBackend",
)

_register_backend(
    "baya.integrations.tensorflow.tensorflow_backend",
    "TensorFlowBackend",
)

_register_backend(
    "baya.integrations.pytorch.pytorch_backend",
    "PyTorchBackend",
)

_register_backend(
    "baya.integrations.scipy.scipy_backend",
    "ScipyBackend",
)

_register_backend(
    "baya.integrations.statsmodels.stats_backend",
    "StatsBackend",
)


# -----------------------------------------------------
# Public API
# -----------------------------------------------------

__all__ = [
    "BaseBackend",
    "ModelRegistry",
]
