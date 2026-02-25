from typing import List
from baya.context import Context
from .base import BaseMiddleware, Step


class MiddlewareManager:
    def __init__(self) -> None:
        self._middlewares: List[BaseMiddleware] = []

    def add(self, middleware: BaseMiddleware) -> None:
        self._middlewares.append(middleware)

    def wrap(self, step: Step) -> Step:
        wrapped = step
        for mw in reversed(self._middlewares):
            wrapped = mw.wrap(wrapped)
        return wrapped