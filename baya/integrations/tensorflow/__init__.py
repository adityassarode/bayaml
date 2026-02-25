"""
TensorFlow Backend Adapter for Baya ML.

Public API:
    TensorFlowBackend

No side effects.
No auto-registration.
No global state.
"""

from .tensorflow_backend import TensorFlowBackend

__all__: list[str] = ["TensorFlowBackend"]