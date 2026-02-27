from __future__ import annotations

from pathlib import Path

from ..context import Context


class PDFExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def to_pdf(self, path: str) -> Path:
        # Minimal implementation: write a simple text report as .pdf-like content.
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        metrics = self._ctx.get_metrics()
        out.write_text("Baya Report\n" + str(metrics), encoding="utf-8")
        return out
