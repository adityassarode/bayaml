from __future__ import annotations

from typing import Dict, Any, Callable
import numpy as np

from ..context import Context
from ..metrics.classification import (
    accuracy,
    precision,
    recall,
    f1,
    roc_auc_score_safe,
    confusion_matrix_safe,
    classification_report_safe,
)
from ..metrics.regression import (
    r2,
    mse,
    mae,
)
from ..guardrails.metric_validator import validate_metrics


class EvaluateModule:
    """
    Model evaluation operations.
    Pure computation layer.
    """

    def __init__(self, context: Context) -> None:
        self._ctx: Context = context

    # =====================================================
    # Guards
    # =====================================================

    def _ensure_ready(self) -> None:
        if not self._ctx.is_fitted:
            raise RuntimeError("Model not trained.")

        if not self._ctx.is_split:
            raise RuntimeError("Dataset not split.")

        if self._ctx.get_predictions() is None:
            raise RuntimeError("No predictions found. Call model.predict() first.")

        if self._ctx.get_prediction_scope() != "test":
            raise RuntimeError("Evaluation requires test-set predictions.")

    def _merge_metrics(self, new: Dict[str, Any]) -> None:
        validated = validate_metrics(new)

        current = self._ctx.get_metrics()
        merged = {**current, **validated}

        self._ctx.set_metrics(merged)

    # =====================================================
    # Classification
    # =====================================================

    def evaluate_classifier(self) -> Dict[str, float]:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError("Classifier metrics used on non-classification task.")

        y_pred = self._ctx.get_predictions()
        _, y_true = self._ctx.get_split_data()[1::2]

        metrics = {
            "accuracy": float(accuracy(y_true, y_pred)),
            "precision": float(precision(y_true, y_pred)),
            "recall": float(recall(y_true, y_pred)),
            "f1": float(f1(y_true, y_pred)),
        }

        self._merge_metrics(metrics)
        return metrics

    # =====================================================
    # Regression
    # =====================================================

    def evaluate_regressor(self) -> Dict[str, float]:

        self._ensure_ready()

        if self._ctx.get_task_type() != "regression":
            raise RuntimeError("Regressor metrics used on non-regression task.")

        y_pred = self._ctx.get_predictions()
        _, y_true = self._ctx.get_split_data()[1::2]

        metrics = {
            "r2": float(r2(y_true, y_pred)),
            "mse": float(mse(y_true, y_pred)),
            "mae": float(mae(y_true, y_pred)),
        }

        self._merge_metrics(metrics)
        return metrics

    # =====================================================
    # ROC AUC
    # =====================================================

    def roc_auc(self) -> float:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError("ROC AUC only valid for classification.")

        backend = self._ctx.get_backend()
        model = self._ctx.get_model()

        if backend is None or model is None:
            raise RuntimeError("Model state invalid.")

        if not backend.supports_proba(model):
            raise RuntimeError("Backend does not support probability prediction.")

        X_test, y_true = self._ctx.get_split_data()[1::2]

        y_prob = backend.predict_proba(model=model, X=X_test)

        score = float(roc_auc_score_safe(y_true, y_prob))

        self._merge_metrics({"roc_auc": score})
        return score

    # =====================================================
    # Confusion Matrix
    # =====================================================

    def get_confusion_matrix(self) -> np.ndarray:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError("Confusion matrix only valid for classification.")

        y_pred = self._ctx.get_predictions()
        _, y_true = self._ctx.get_split_data()[1::2]

        cm = confusion_matrix_safe(y_true, y_pred)

        self._merge_metrics({"confusion_matrix": cm.tolist()})
        return cm

    # =====================================================
    # Custom Metric
    # =====================================================

    def custom_metric(
        self,
        metric_function: Callable[[Any, Any], float],
    ) -> float:

        self._ensure_ready()

        y_pred = self._ctx.get_predictions()
        _, y_true = self._ctx.get_split_data()[1::2]

        value = metric_function(y_true, y_pred)

        try:
            value = float(value)
        except Exception:
            raise TypeError("Custom metric must return numeric value.")

        self._merge_metrics({"custom_metric": value})
        return value