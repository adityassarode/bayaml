from __future__ import annotations

from typing import Any, Dict

from .schema import ConfigSchema


def validate_config(data: Dict[str, Any]) -> ConfigSchema:
    required = ["data_path", "target", "model"]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")
    return ConfigSchema(
        data_path=str(data["data_path"]),
        target=str(data["target"]),
        model=str(data["model"]),
        task=str(data.get("task", "classification")),
        test_size=float(data.get("test_size", 0.2)),
        seed=int(data.get("seed", 42)),
    )
