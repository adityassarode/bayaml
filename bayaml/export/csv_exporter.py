from __future__ import annotations

from pathlib import Path

from ..context import Context


class CSVExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def to_csv(self, path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        self._ctx.ensure_dataframe().to_csv(out, index=False)
        return out
