from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class Storage:
    def __init__(self, root: Path) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def save_json(self, name: str, payload: Dict[str, Any]) -> Path:
        path = self._root / f"{name}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return path
