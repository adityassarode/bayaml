from __future__ import annotations

from enum import Enum


class EventType(str, Enum):
    """
    Lifecycle events emitted by orchestration layer.
    """

    PIPELINE_START = "pipeline_start"
    PIPELINE_END = "pipeline_end"

    STEP_START = "step_start"
    STEP_END = "step_end"

    TRAIN_START = "train_start"
    TRAIN_END = "train_end"

    EVALUATE_START = "evaluate_start"
    EVALUATE_END = "evaluate_end"

    DEPLOY_START = "deploy_start"
    DEPLOY_END = "deploy_end"