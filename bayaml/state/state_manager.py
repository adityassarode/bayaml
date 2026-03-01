from __future__ import annotations

from typing import Any, Dict, Optional


class StateManager:
    """
    Scoped runtime state container.

    Attached to Context.
    Never global.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    # ---------------------------------

    def set(self, key: str, value: Any) -> None:
        if key in self._store:
            raise KeyError(f"State key already set: {key}")

        self._store[key] = value

    # ---------------------------------

    def get(self, key: str) -> Any:
        if key not in self._store:
            raise KeyError(f"State key not found: {key}")

        return self._store[key]

    # ---------------------------------

    def get_optional(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    # ---------------------------------

    def has(self, key: str) -> bool:
        return key in self._store

    # ---------------------------------

    def clear(self) -> None:
        """
        Used only by tests.
        """
        self._store.clear()