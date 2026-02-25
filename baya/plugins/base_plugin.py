from __future__ import annotations
from typing import Protocol
from baya.context import Context


class BasePlugin(Protocol):
    """
    Plugin contract.

    Must not perform work during import.
    Must register through explicit setup() call.
    """

    name: str

    def setup(self, context: Context) -> None:
        """
        Called after Context initialization,
        before pipeline execution.
        """
        ...