from __future__ import annotations

from typing import Any, Callable, Dict

from ..context import Context
from ..metrics.classification import accuracy, f1, precision, recall
from ..metrics.regression import mae, mse, r2


class EvaluateModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def _y(self) -> tuple[Any, Any]:
        if self._ctx.get_predictions() is None:
            raise RuntimeError("Run prediction first.")
        _, _, _, y_test = self._ctx.get_split_data()
        return y_test, self._ctx.get_predictions()

    def classification(self) -> Dict[str, float]:
        y_true, y_pred = self._y()
        metrics = {
            "accuracy": accuracy(y_true, y_pred),
            "precision": precision(y_true, y_pred),
            "recall": recall(y_true, y_pred),
            "f1": f1(y_true, y_pred),
        }
        self._ctx.set_metrics(metrics)
        return metrics

    def regression(self) -> Dict[str, float]:
        y_true, y_pred = self._y()
        metrics = {"r2": r2(y_true, y_pred), "mse": mse(y_true, y_pred), "mae": mae(y_true, y_pred)}
        self._ctx.set_metrics(metrics)
        return metrics

    def custom_metric(self, fn: Callable[[Any, Any], float], name: str = "custom_metric") -> float:
        y_true, y_pred = self._y()
        value = float(fn(y_true, y_pred))
        current = self._ctx.get_metrics()
        current[name] = value
        self._ctx.set_metrics(current)
        return value

    # compatibility aliases
    def evaluate_classifier(self) -> Dict[str, float]:
        return self.classification()

    def evaluate_regressor(self) -> Dict[str, float]:
        return self.regression()
