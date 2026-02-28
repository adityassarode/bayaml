from __future__ import annotations

from pathlib import Path


class GraphExporter:
    def export(self, figure, path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(figure, "savefig"):
            figure.savefig(out)
        else:
            out.write_text(str(figure), encoding="utf-8")
        return out
