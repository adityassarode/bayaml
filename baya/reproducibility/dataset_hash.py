from __future__ import annotations

import hashlib
from pathlib import Path


CHUNK_SIZE = 1024 * 1024


def hash_file(path: Path) -> str:
    sha = hashlib.sha256()

    with path.open("rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            sha.update(chunk)

    return sha.hexdigest()


def hash_dataframe_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()