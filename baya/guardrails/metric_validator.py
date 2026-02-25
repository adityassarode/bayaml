from __future__ import annotations


class MetricError(Exception):
    pass


REGRESSION = {"rmse", "mae", "r2"}
CLASSIFICATION = {"accuracy", "f1", "precision", "recall", "auc"}


def validate_metrics(task_type: str, metric: str) -> None:
    metric = metric.lower()

    if task_type == "regression" and metric not in REGRESSION:
        raise MetricError(f"{metric} invalid for regression")

    if task_type == "classification" and metric not in CLASSIFICATION:
        raise MetricError(f"{metric} invalid for classification")