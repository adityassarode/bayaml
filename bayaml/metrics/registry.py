from __future__ import annotations

from typing import Any, Callable, Dict

from .classification import accuracy, f1, precision, recall
from .regression import mae, mse, r2

MetricFn = Callable[[Any, Any], float]

_METRICS: Dict[str, MetricFn] = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1": f1,
    "mae": mae,
    "mse": mse,
    "r2": r2,
}


def list_metrics() -> list[str]:
    return sorted(_METRICS)


def get_metric(name: str) -> MetricFn:
    if name not in _METRICS:
        raise KeyError(name)
    return _METRICS[name]


def evaluate_predictions(y_true: Any, y_pred: Any, names: list[str]) -> Dict[str, float]:
    return {name: float(get_metric(name)(y_true, y_pred)) for name in names}
