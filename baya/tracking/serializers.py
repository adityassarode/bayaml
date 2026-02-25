from __future__ import annotations

import json
from typing import Any


def to_json(data: Any) -> str:
    return json.dumps(
        data,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    )