from typing import Callable, Protocol
from baya.context import Context

Step = Callable[[Context], None]


class BaseMiddleware(Protocol):
    def wrap(self, step: Step) -> Step:
        ...