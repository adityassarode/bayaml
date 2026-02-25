from __future__ import annotations
from typing import Any, Dict, List, Union

JSONPrimitive = Union[str, int, float, bool, None]
JSONType = Union[
    JSONPrimitive,
    Dict[str, "JSONType"],
    List["JSONType"],
]