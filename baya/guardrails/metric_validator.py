from __future__ import annotations

from enum import Enum
from typing import Iterable, Set


class MetricError(Exception):
    """Raised when invalid metric is requested for task type."""
    pass


class TaskType(str, Enum):
    REGRESSION = "regression"
    CLASSIFICATION = "classification"


# Must stay synchronized with EvaluateModule
REGRESSION_METRICS: Set[str] = {
    "r2",
    "mse",
    "mae",
}

CLASSIFICATION_METRICS: Set[str] = {
    "accuracy",
    "f1",
    "precision",
    "recall",
    "roc_auc",   # aligned with EvaluateModule.rocAuc()
}


def validate_metrics(
    *,
    task_type: TaskType,
    metrics: Iterable[str],
) -> None:
    """
    Validate metric applicability for given task type.

    Does NOT inspect backend capabilities.
    Only validates domain compatibility.
    """

    if not metrics:
        raise MetricError("At least one metric must be specified.")

    normalized = [m.lower() for m in metrics]

    if task_type == TaskType.REGRESSION:
        allowed = REGRESSION_METRICS
    elif task_type == TaskType.CLASSIFICATION:
        allowed = CLASSIFICATION_METRICS
    else:
        raise MetricError(f"Unknown task type: {task_type}")

    invalid = sorted(set(normalized) - allowed)

    if invalid:
        raise MetricError(
            f"Invalid metrics for {task_type.value}: {invalid} | "
            f"Allowed: {sorted(allowed)}"
        )