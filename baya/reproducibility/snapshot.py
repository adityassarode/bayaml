from __future__ import annotations

import hashlib
from pathlib import Path


def project_snapshot_hash(root: Path) -> str:
    sha = hashlib.sha256()

    for file in sorted(root.rglob("*.py")):
        sha.update(file.read_bytes())

    return sha.hexdigest()