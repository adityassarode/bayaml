from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import json

from .yaml_support import load_yaml


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if path.suffix in {".yaml", ".yml"}:
        return load_yaml(path)

    if path.suffix == ".json":
        return json.loads(path.read_text())

    raise ValueError("Unsupported config format. Use .yaml or .json")