from __future__ import annotations


class BayaError(Exception):
    """
    Base exception for entire framework.

    All custom exceptions must inherit from this.
    Enables:
    - structured catching
    - unified logging
    - deterministic failure handling
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message