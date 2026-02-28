from __future__ import annotations

from pathlib import Path

from ..context import Context


class GraphExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def graph(self, path: str) -> Path:
        figure = self._ctx.get_last_figure()
        if figure is None:
            raise RuntimeError("No figure captured.")
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(figure, "savefig"):
            figure.savefig(out)
        elif hasattr(figure, "write_html"):
            figure.write_html(str(out))
        else:
            out.write_text(str(figure), encoding="utf-8")
        return out
