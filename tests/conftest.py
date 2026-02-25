"""
Global pytest configuration for Baya.

Ensures:
- Deterministic random behavior
- Clean model registry per test
- No cross‑test state leakage
"""

from __future__ import annotations

import random
import numpy as np
import pytest

# If ModelRegistry has global state, import it
from baya.integrations.model_registry import ModelRegistry


# --------------------------------------------------
# Deterministic seed
# --------------------------------------------------

@pytest.fixture(autouse=True)
def _set_seed():
    random.seed(42)
    np.random.seed(42)
    yield


# --------------------------------------------------
# Reset registry between tests
# --------------------------------------------------

@pytest.fixture(autouse=True)
def _reset_registry():
    if hasattr(ModelRegistry, "clear"):
        ModelRegistry.clear()
    yield