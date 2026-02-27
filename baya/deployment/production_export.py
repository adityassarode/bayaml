from __future__ import annotations

from pathlib import Path


def export_production_bundle(output_dir: str) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "README.txt").write_text("Baya deployment bundle", encoding="utf-8")
    return out
