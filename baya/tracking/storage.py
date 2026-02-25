from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import tempfile
import os

from .serializers import to_json


class Storage:
    """
    Filesystem persistence boundary.

    Guarantees:
        - Atomic writes
        - Deterministic JSON
        - No path traversal
        - Safe overwrite control
    """

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    # =====================================================
    # Save JSON
    # =====================================================

    def save_json(
        self,
        name: str,
        data: Any,
        *,
        overwrite: bool = False,
    ) -> None:
        safe_name = self._sanitize(name)
        path = self._root / f"{safe_name}.json"

        if path.exists() and not overwrite:
            raise FileExistsError(f"{path} already exists.")

        content = to_json(data)

        self._atomic_write(path, content)

    # =====================================================
    # Load JSON
    # =====================================================

    def load_json(self, name: str) -> Any:
        safe_name = self._sanitize(name)
        path = self._root / f"{safe_name}.json"

        if not path.exists():
            raise FileNotFoundError(path)

        return json.loads(path.read_text())

    # =====================================================
    # Atomic Write
    # =====================================================

    def _atomic_write(self, path: Path, content: str) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=self._root,
            delete=False,
        ) as tmp:
            tmp.write(content)
            temp_path = Path(tmp.name)

        os.replace(temp_path, path)

    # =====================================================
    # Name Sanitization
    # =====================================================

    def _sanitize(self, name: str) -> str:
        if not name.isidentifier():
            raise ValueError(f"Invalid storage name: {name}")
        return name