from __future__ import annotations

from pathlib import Path

from ..context import Context


class JSONExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def to_json(self, path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        self._ctx.ensure_dataframe().to_json(out, orient="records")
        return out
