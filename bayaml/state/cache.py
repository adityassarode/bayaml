from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class CacheKey:
    step_name: str
    input_hash: str
    config_hash: str


class StepCache:
    def __init__(self) -> None:
        self._cache: Dict[CacheKey, Any] = {}

    def has(self, key: CacheKey) -> bool:
        return key in self._cache

    def load(self, key: CacheKey) -> Any:
        return self._cache[key]

    def store(self, key: CacheKey, value: Any) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()
