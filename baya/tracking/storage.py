from __future__ import annotations

from pathlib import Path
from typing import Any
from .serializers import to_json


class Storage:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save_json(self, name: str, data: Any) -> None:
        path = self.root / f"{name}.json"
        path.write_text(to_json(data))