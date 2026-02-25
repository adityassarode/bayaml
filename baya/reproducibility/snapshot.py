from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "build",
    "dist",
}


def _iter_source_files(root: Path) -> Iterable[Path]:
    """
    Deterministically iterate over source files.
    Excludes hidden/system directories.
    """

    for path in sorted(root.rglob("*.py")):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        if path.is_file():
            yield path


def project_snapshot_hash(root: Path) -> str:
    """
    Compute deterministic project snapshot hash.

    Includes:
        - Relative file path
        - File contents (normalized)
    """

    root = root.resolve()
    sha = hashlib.sha256()

    for file in _iter_source_files(root):
        relative_path = file.relative_to(root).as_posix()

        # Include file path in hash
        sha.update(relative_path.encode("utf-8"))

        # Normalize line endings for cross-platform determinism
        content = file.read_text(encoding="utf-8").replace("\r\n", "\n")

        sha.update(content.encode("utf-8"))

    return sha.hexdigest()