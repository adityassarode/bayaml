from __future__ import annotations

import json
import hashlib
from typing import Any, Dict


# =====================================================
# Public API
# =====================================================

def freeze_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministically freeze configuration.

    Guarantees:
        - Recursive normalization
        - Deterministic ordering
        - JSON-safe structure
        - Stable hashing
    """

    normalized = _normalize(config)

    serialized = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    config_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    return {
        "config": normalized,
        "config_hash": config_hash,
    }


# =====================================================
# Internal Normalization
# =====================================================

def _normalize(value: Any) -> Any:
    """
    Recursively normalize config into JSON-deterministic structure.
    """

    # Primitive types
    if value is None or isinstance(value, (str, int, bool)):
        return value

    if isinstance(value, float):
        # Normalize float precision
        return float(f"{value:.12g}")

    # Dict
    if isinstance(value, dict):
        return {
            str(k): _normalize(v)
            for k, v in sorted(value.items(), key=lambda x: str(x[0]))
        }

    # List
    if isinstance(value, list):
        return [_normalize(v) for v in value]

    # Tuple → list
    if isinstance(value, tuple):
        return [_normalize(v) for v in value]

    # Set → sorted list
    if isinstance(value, set):
        return sorted(_normalize(v) for v in value)

    # Unsupported type
    raise TypeError(
        f"Unsupported config value type: {type(value).__name__}"
    )