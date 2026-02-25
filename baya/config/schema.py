from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


TaskType = Literal["classification", "regression"]


@dataclass(frozen=True)
class ConfigSchema:
    dataset_path: str
    target: str
    task: TaskType
    metric: str
    seed: int
    test_size: float