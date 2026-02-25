from __future__ import annotations

from typing import Dict, Any, Callable
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    confusion_matrix as sk_confusion_matrix,
    classification_report as sk_classification_report,
    roc_auc_score,
)

from ..context import Context


class EvaluateModule:
    """
    Model evaluation operations.
    Pure computation layer.

    Rules:
    - Requires fitted model
    - Requires dataset split
    - Requires test-set predictions
    - Must not mutate model
    - Must write metrics via Context API only
    - Must respect task type
    """

    def __init__(self, context: Context) -> None:
        self._ctx: Context = context

    # =====================================================
    # Internal Guards
    # =====================================================

    def _ensure_ready(self) -> None:
        if not self._ctx.is_fitted:
            raise RuntimeError("Model not trained.")

        if not self._ctx.is_split:
            raise RuntimeError("Dataset not split.")

        if self._ctx.get_predictions() is None:
            raise RuntimeError(
                "No predictions found. Call model.predict() first."
            )

        if self._ctx.get_prediction_scope() != "test":
            raise RuntimeError(
                "Evaluation requires test-set predictions."
            )

    def _get_test_data(self) -> tuple[Any, Any]:
        _, X_test, _, y_test = self._ctx.get_split_data()
        return X_test, y_test

    def _get_predictions(self) -> np.ndarray:
        preds = self._ctx.get_predictions()
        if preds is None:
            raise RuntimeError("Predictions missing.")
        return preds

    # =====================================================
    # Classification Metrics
    # =====================================================

    def evaluate_classifier(
        self,
        *,
        average: str = "weighted",
    ) -> Dict[str, float]:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError(
                "Classifier metrics used on non-classification task."
            )

        y_pred = self._get_predictions()
        _, y_true = self._get_test_data()

        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(
                y_true, y_pred, average=average, zero_division=0
            ),
            "recall": recall_score(
                y_true, y_pred, average=average, zero_division=0
            ),
            "f1": f1_score(
                y_true, y_pred, average=average, zero_division=0
            ),
        }

        self._ctx.set_metrics(metrics)
        return metrics

    # =====================================================
    # Regression Metrics
    # =====================================================

    def evaluate_regressor(self) -> Dict[str, float]:

        self._ensure_ready()

        if self._ctx.get_task_type() != "regression":
            raise RuntimeError(
                "Regressor metrics used on non-regression task."
            )

        y_pred = self._get_predictions()
        _, y_true = self._get_test_data()

        metrics = {
            "r2": r2_score(y_true, y_pred),
            "mse": mean_squared_error(y_true, y_pred),
            "mae": mean_absolute_error(y_true, y_pred),
        }

        self._ctx.set_metrics(metrics)
        return metrics

    # =====================================================
    # Confusion Matrix
    # =====================================================

    def get_confusion_matrix(self) -> np.ndarray:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError(
                "Confusion matrix only valid for classification."
            )

        y_pred = self._get_predictions()
        _, y_true = self._get_test_data()

        cm = sk_confusion_matrix(y_true, y_pred)

        self._ctx.set_metrics({"confusion_matrix": cm})
        return cm

    # =====================================================
    # Classification Report
    # =====================================================

    def get_classification_report(self) -> str:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError(
                "Classification report only valid for classification."
            )

        y_pred = self._get_predictions()
        _, y_true = self._get_test_data()

        report = sk_classification_report(y_true, y_pred)

        self._ctx.set_metrics({"classification_report": report})
        return report

    # =====================================================
    # ROC AUC
    # =====================================================

    def roc_auc(self) -> float:

        self._ensure_ready()

        if self._ctx.get_task_type() != "classification":
            raise RuntimeError("ROC AUC only valid for classification.")

        model = self._ctx.get_model()
        backend = self._ctx.get_backend()

        if model is None or backend is None:
            raise RuntimeError("Model state invalid.")

        X_test, y_true = self._get_test_data()

        y_prob = backend.predict_proba(model=model, X=X_test)

        if y_prob.shape[1] == 2:
            score = roc_auc_score(y_true, y_prob[:, 1])
        else:
            score = roc_auc_score(y_true, y_prob, multi_class="ovr")

        self._ctx.set_metrics({"roc_auc": score})
        return score

    # =====================================================
    # Custom Metric
    # =====================================================

    def custom_metric(
        self,
        metric_function: Callable[[Any, Any], float],
    ) -> float:

        self._ensure_ready()

        y_pred = self._get_predictions()
        _, y_true = self._get_test_data()

        value = metric_function(y_true, y_pred)

        self._ctx.set_metrics({"custom_metric": value})
        return value

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:
        metrics = self._ctx.get_metrics()
        if not metrics:
            return "<EvaluateModule metrics=None>"
        return f"<EvaluateModule metrics={list(metrics.keys())}>"