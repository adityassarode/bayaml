from __future__ import annotations

import logging
from pathlib import Path

from .formatters import StructuredFormatter


def create_console_handler(level: int) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(StructuredFormatter())
    return handler


def create_file_handler(path: Path, level: int) -> logging.Handler:
    path.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(StructuredFormatter())
    return handler