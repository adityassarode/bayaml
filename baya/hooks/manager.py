from __future__ import annotations

from typing import Callable, Dict, List, Any

from .events import EventType


HookCallback = Callable[..., None]


class HookManager:
    """
    Manages lifecycle hook subscriptions.

    Must be attached to Context.
    No global singleton allowed.
    """

    def __init__(self) -> None:
        self._hooks: Dict[EventType, List[HookCallback]] = {}

    # -------------------------------------------------
    # Registration
    # -------------------------------------------------

    def register(
        self,
        event: EventType,
        callback: HookCallback,
    ) -> None:
        if event not in self._hooks:
            self._hooks[event] = []

        self._hooks[event].append(callback)

    # -------------------------------------------------
    # Emission
    # -------------------------------------------------

    def emit(
        self,
        event: EventType,
        **payload: Any,
    ) -> None:

        callbacks = self._hooks.get(event, [])

        for cb in callbacks:
            cb(**payload)

    # -------------------------------------------------
    # Introspection
    # -------------------------------------------------

    def list_hooks(self) -> Dict[EventType, int]:
        return {
            event: len(callbacks)
            for event, callbacks in self._hooks.items()
        }