from __future__ import annotations

from typing import Any

from baya.context import Context
from baya.reproducibility.snapshot import freeze_config
from baya.tracking.tracker import Tracker

from .dag import DAG


class Executor:
    def __init__(self, context: Context) -> None:
        self._context = context

    def execute(self, dag: DAG) -> None:
        Tracker.start_run(self._context)

        order = dag.topological_sort()

        for node_name in order:
            step_callable = dag.get_callable(node_name)

            # Guardrails before training phase
            if node_name == "train":
                freeze_config(self._context)

            step_callable(self._context)

        Tracker.end_run(self._context)