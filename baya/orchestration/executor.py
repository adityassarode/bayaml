from __future__ import annotations

import random

import numpy as np

from baya.context import Context
from baya.hooks.events import EventType
from baya.hooks.manager import HookManager
from baya.integrations.model_registry import ModelRegistry
from baya.orchestration.dag import DAG, Phase


class Executor:
    def __init__(self, context: Context) -> None:
        self._context = context

    def execute(self, dag: DAG) -> None:
        if not ModelRegistry.is_frozen():
            ModelRegistry.freeze()
        seed = self._context.get_seed()
        random.seed(seed)
        np.random.seed(seed)

        for node in dag.topological_sort():
            HookManager.emit(EventType.BEFORE_STEP, {"step": node.name, "phase": node.phase.value})
            if node.phase == Phase.TRAIN and not self._context.is_split:
                raise RuntimeError("SPLIT phase must run before TRAIN.")
            if node.phase == Phase.EVALUATE and self._context.get_predictions() is None:
                raise RuntimeError("PREDICT phase must run before EVALUATE.")
            node.func(self._context)
            HookManager.emit(EventType.AFTER_STEP, {"step": node.name, "phase": node.phase.value})
        self._context.lock()
