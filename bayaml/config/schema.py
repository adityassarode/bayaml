from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class ConfigSchema:
    data_path: str
    target: str
    model: str
    task: Literal["classification", "regression"] = "classification"
    test_size: float = 0.2
    seed: int = 42
