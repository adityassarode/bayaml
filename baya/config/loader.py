from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .yaml_support import load_yaml


def load_config(path: Path) -> Dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix in (".yaml", ".yml"):
        return load_yaml(path)
    if suffix == ".json":
        return dict(json.loads(path.read_text(encoding="utf-8")))
    raise ValueError("Config must be .yaml/.yml/.json")
