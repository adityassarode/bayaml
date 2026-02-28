from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_hash(data: Any) -> str:
    """
    Deterministic SHA256 hash of JSON‑serializable object.

    Used for:
    - config hashing
    - lightweight structural fingerprinting

    Not for dataset file hashing (use reproducibility.dataset_hash instead).
    """

    serialized = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()