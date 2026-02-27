from __future__ import annotations

from pathlib import Path


class ImageExporter:
    def save_bytes(self, image_bytes: bytes, path: str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(image_bytes)
        return out
