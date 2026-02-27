from __future__ import annotations

from pathlib import Path

from ..context import Context


class DOCXExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def to_docx(self, path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("Baya DOCX placeholder\n" + str(self._ctx.get_metrics()), encoding="utf-8")
        return out
