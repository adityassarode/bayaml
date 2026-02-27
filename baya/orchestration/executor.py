from __future__ import annotations

from typing import List, Callable
from enum import Enum
import random
import numpy as np

from baya.context import Context
from baya.orchestration.dag import DAG
from baya.tracking.tracker import Tracker
from baya.reproducibility.config_freeze import freeze_config
from baya.integrations.model_registry import ModelRegistry


class Phase(str, Enum):
    PREPARE = "prepare"
    SPLIT = "split"
    TRAIN = "train"
    PREDICT = "predict"
    EVALUATE = "evaluate"
    FINALIZE = "finalize"


class Executor:
    """
    Deterministic orchestration engine.
    """

    def __init__(self, context: Context) -> None:
        self._context: Context = context
        self._train_executed: bool = False
        self._predict_executed: bool = False
        self._executed: bool = False
        self._tracker: Tracker | None = None

    # =====================================================
    # Public Entry Point
    # =====================================================

    def execute(self, dag: DAG) -> None:

        if self._executed:
            raise RuntimeError("Executor already executed.")

        if not ModelRegistry.is_frozen():
            raise RuntimeError("ModelRegistry must be frozen before execution.")

        self._initialize_rng()

        self._tracker = Tracker.create_from_context(self._context)

        try:
            order: List[str] = dag.topological_sort()

            for node_name in order:
                phase: Phase = dag.get_phase(node_name)
                step: Callable[[Context], None] = dag.get_callable(node_name)

                self._validate_phase_transition(phase)

                if phase == Phase.TRAIN:
                    self._freeze_configuration()

                step(self._context)

                self._mark_phase_complete(phase)

            self._finalize()

        finally:
            if self._tracker is not None:
                self._tracker.finalize()

            self._executed = True

    # =====================================================
    # RNG Control
    # =====================================================

    def _initialize_rng(self) -> None:
        seed = self._context.get_seed()
        random.seed(seed)
        np.random.seed(seed)

    # =====================================================
    # Phase Validation
    # =====================================================

    def _validate_phase_transition(self, phase: Phase) -> None:

        if phase == Phase.TRAIN:
            if self._train_executed:
                raise RuntimeError("Training phase already executed.")

            if not self._context.is_split:
                raise RuntimeError("Dataset must be split before training.")

        if phase == Phase.PREDICT:
            if not self._context.is_fitted:
                raise RuntimeError("Model must be trained before prediction.")

        if phase == Phase.EVALUATE:
            if not self._predict_executed:
                raise RuntimeError("Prediction must be executed before evaluation.")

    # =====================================================
    # Phase State Tracking
    # =====================================================

    def _mark_phase_complete(self, phase: Phase) -> None:

        if phase == Phase.TRAIN:
            self._train_executed = True

        if phase == Phase.PREDICT:
            self._predict_executed = True

    # =====================================================
    # Reproducibility Freeze
    # =====================================================

    def _freeze_configuration(self) -> None:

        ModelRegistry.freeze()

        config = {
            "seed": self._context.get_seed(),
            "target": self._context.get_target(),
            "registry_hash": ModelRegistry.registry_hash(),
        }

        freeze_config(config)

    # =====================================================
    # Finalization
    # =====================================================

    def _finalize(self) -> None:
        pass