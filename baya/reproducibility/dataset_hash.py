from __future__ import annotations

import hashlib


def dataset_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
