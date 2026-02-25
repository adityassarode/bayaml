from __future__ import annotations

from typing import List, Callable
from enum import Enum

from baya.context import Context
from baya.orchestration.dag import DAG
from baya.tracking.tracker import Tracker
from baya.reproducibility.config_freeze import freeze_config


class Phase(str, Enum):
    """
    Explicit execution phases.

    Prevents lifecycle drift and enforces ordering.
    """

    PREPARE = "prepare"
    SPLIT = "split"
    TRAIN = "train"
    PREDICT = "predict"
    EVALUATE = "evaluate"
    FINALIZE = "finalize"


class Executor:
    """
    Deterministic orchestration engine.

    Responsibilities:
    - Enforce strict phase ordering
    - Prevent double training
    - Enforce predict-before-evaluate
    - Freeze configuration before training
    - Integrate tracking lifecycle
    - Maintain deterministic DAG execution
    """

    def __init__(self, context: Context) -> None:
        self._context: Context = context
        self._train_executed: bool = False
        self._predict_executed: bool = False

    # =====================================================
    # Public Entry Point
    # =====================================================

    def execute(self, dag: DAG) -> None:
        """
        Execute DAG in deterministic topological order.
        """

        Tracker.start_run(self._context)

        order: List[str] = dag.topological_sort()

        for node_name in order:
            phase: Phase = dag.get_phase(node_name)
            step: Callable[[Context], None] = dag.get_callable(node_name)

            self._validate_phase_transition(phase)

            # Freeze reproducibility at training boundary
            if phase == Phase.TRAIN:
                self._freeze_configuration()

            # Execute node
            step(self._context)

            self._mark_phase_complete(phase)

        Tracker.end_run(self._context)

    # =====================================================
    # Phase Validation
    # =====================================================

    def _validate_phase_transition(self, phase: Phase) -> None:
        """
        Enforce strict lifecycle ordering.
        """

        if phase == Phase.TRAIN:
            if self._train_executed:
                raise RuntimeError("Training phase already executed.")

            if not self._context.is_split:
                raise RuntimeError(
                    "Dataset must be split before training."
                )

        if phase == Phase.PREDICT:
            if not self._context.is_fitted:
                raise RuntimeError(
                    "Model must be trained before prediction."
                )

        if phase == Phase.EVALUATE:
            if not self._predict_executed:
                raise RuntimeError(
                    "Prediction must be executed before evaluation."
                )

    # =====================================================
    # Phase State Tracking
    # =====================================================

    def _mark_phase_complete(self, phase: Phase) -> None:
        """
        Update internal execution state.
        """

        if phase == Phase.TRAIN:
            self._train_executed = True

        if phase == Phase.PREDICT:
            self._predict_executed = True

    # =====================================================
    # Reproducibility Freeze
    # =====================================================

    def _freeze_configuration(self) -> None:
        """
        Freeze configuration prior to training.

        Ensures deterministic run identity without mutating metrics.
        """

        config = {
            "seed": self._context.get_seed(),
            "target": self._context.get_target(),
        }

        # Freeze only — do not mutate Context metrics
        freeze_config(config)