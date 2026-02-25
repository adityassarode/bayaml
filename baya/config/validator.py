from __future__ import annotations
from typing import Dict, Any

from .schema import ConfigSchema


REQUIRED_FIELDS = {
    "dataset_path",
    "target",
    "task",
    "metric",
    "seed",
    "test_size",
}


def validate_config(raw: Dict[str, Any]) -> ConfigSchema:
    missing = REQUIRED_FIELDS - raw.keys()
    if missing:
        raise RuntimeError(f"Missing config fields: {sorted(missing)}")

    return ConfigSchema(
        dataset_path=str(raw["dataset_path"]),
        target=str(raw["target"]),
        task=str(raw["task"]),
        metric=str(raw["metric"]),
        seed=int(raw["seed"]),
        test_size=float(raw["test_size"]),
    )