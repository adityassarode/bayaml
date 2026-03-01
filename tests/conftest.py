import os

import pytest

from bayaml.hooks import HookManager
from bayaml.integrations.model_registry import ModelRegistry


@pytest.fixture(autouse=True)
def clean_state():
    ModelRegistry.clear()
    HookManager.clear()
    yield
    ModelRegistry.clear()
    HookManager.clear()
    os.environ["PYTHONHASHSEED"] = "0"
