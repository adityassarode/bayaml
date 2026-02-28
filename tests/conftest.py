import os

import pytest

from baya.hooks import HookManager
from baya.integrations.model_registry import ModelRegistry


@pytest.fixture(autouse=True)
def clean_state():
    ModelRegistry.clear()
    HookManager.clear()
    yield
    ModelRegistry.clear()
    HookManager.clear()
    os.environ["PYTHONHASHSEED"] = "0"
