from __future__ import annotations

from typing import Callable

from bayaml.context import Context

from .dag import DAG, Phase
from .executor import Executor


class Pipeline:
    def __init__(self, context: Context) -> None:
        self._context = context
        self._dag = DAG()

    def add_step(self, name: str, phase: Phase, func: Callable[[Context], None], depends_on: str | None = None) -> "Pipeline":
        self._dag.add_node(name, phase, func)
        if depends_on:
            self._dag.add_dependency(name, depends_on)
        return self

    def depends_on(self, node: str, dependency: str) -> "Pipeline":
        self._dag.add_dependency(node, dependency)
        return self

    def run(self) -> None:
        Executor(self._context).execute(self._dag)
