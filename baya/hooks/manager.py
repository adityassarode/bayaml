from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, List

from .events import EventType


class HookManager:
    _hooks: DefaultDict[EventType, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)

    @classmethod
    def register(cls, event: EventType, callback: Callable[[Dict[str, Any]], None]) -> None:
        cls._hooks[event].append(callback)

    @classmethod
    def emit(cls, event: EventType, payload: Dict[str, Any]) -> None:
        for callback in list(cls._hooks[event]):
            callback(payload)

    @classmethod
    def clear(cls) -> None:
        cls._hooks.clear()
