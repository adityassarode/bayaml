from __future__ import annotations

import json
from typing import Any


def to_json(data: Any) -> str:
    """
    Deterministic JSON serializer.

    Guarantees:
        - Stable key ordering
        - Stable separators
        - UTF-8 safe
        - Strict type handling
    """

    normalized = _normalize(data)

    return json.dumps(
        normalized,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
        ensure_ascii=False,
    ) + "\n"


# =====================================================
# Internal Normalization
# =====================================================

def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, bool)):
        return value

    if isinstance(value, float):
        return float(f"{value:.12g}")

    if isinstance(value, dict):
        return {
            str(k): _normalize(v)
            for k, v in sorted(value.items(), key=lambda x: str(x[0]))
        }

    if isinstance(value, list):
        return [_normalize(v) for v in value]

    if isinstance(value, tuple):
        return [_normalize(v) for v in value]

    raise TypeError(
        f"Unsupported type for JSON serialization: {type(value).__name__}"
    )