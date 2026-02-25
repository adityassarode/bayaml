from __future__ import annotations
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:
    yaml = None


def load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError(
            "PyYAML is required for YAML config support."
        )

    return yaml.safe_load(path.read_text())