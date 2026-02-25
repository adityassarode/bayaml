from baya.integrations.model_registry import ModelRegistry
from baya.integrations.sklearn.sklearn_backend import SklearnBackend

import pytest


def test_duplicate_backend_registration_fails() -> None:
    ModelRegistry.clear()

    backend = SklearnBackend()
    ModelRegistry.register_backend(backend)

    with pytest.raises(ValueError):
        ModelRegistry.register_backend(backend)


def test_model_without_backend_fails() -> None:
    ModelRegistry.clear()

    with pytest.raises(ValueError):
        ModelRegistry.register_model("fake_model", "fake_backend")