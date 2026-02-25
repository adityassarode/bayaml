from __future__ import annotations

from typing import Callable

from baya.context import Context
from .dag import DAG
from .executor import Executor


class Pipeline:
    def __init__(self, context: Context) -> None:
        self._context = context
        self._dag = DAG()

    def add_step(
        self,
        name: str,
        func: Callable[[Context], None],
        *,
        depends_on: str | None = None,
    ) -> "Pipeline":
        self._dag.add_node(name, func)
        if depends_on:
            self._dag.add_dependency(name, depends_on)
        return self

    def run(self) -> None:
        executor = Executor(self._context)
        executor.execute(self._dag)