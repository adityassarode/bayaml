"""
Baya Evaluate Module

Handles:
- Classification metrics
- Regression metrics
- Confusion matrix
- ROC AUC
- Probability-based metrics
"""

from __future__ import annotations

from typing import Optional, Dict, Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    confusion_matrix,
    classification_report,
    roc_auc_score,
)

from ..context import Context


class EvaluateModule:
    """
    Model evaluation operations.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Internal Checks
    # -------------------------------------------------

    def _ensure_model(self) -> None:
        if self.context.model is None:
            raise RuntimeError("No trained model found.")

        if self.context.X_test is None or self.context.y_test is None:
            raise RuntimeError("No test data available. Run splitData().")

    def _predict(self) -> np.ndarray:
        return self.context.model.predict(self.context.X_test)

    # -------------------------------------------------
    # Classification Evaluation
    # -------------------------------------------------

    def evaluateClassifier(
        self,
        average: str = "weighted",
    ) -> Dict[str, float]:
        """
        Compute classification metrics.
        """

        self._ensure_model()

        y_pred = self._predict()
        y_true = self.context.y_test

        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average=average, zero_division=0),
            "recall": recall_score(y_true, y_pred, average=average, zero_division=0),
            "f1": f1_score(y_true, y_pred, average=average, zero_division=0),
        }

        self.context.metrics = metrics
        return metrics

    # -------------------------------------------------
    # Regression Evaluation
    # -------------------------------------------------

    def evaluateRegressor(self) -> Dict[str, float]:
        """
        Compute regression metrics.
        """

        self._ensure_model()

        y_pred = self._predict()
        y_true = self.context.y_test

        metrics = {
            "r2": r2_score(y_true, y_pred),
            "mse": mean_squared_error(y_true, y_pred),
            "mae": mean_absolute_error(y_true, y_pred),
        }

        self.context.metrics = metrics
        return metrics

    # -------------------------------------------------
    # Classification Report
    # -------------------------------------------------

    def classificationReport(self) -> str:
        """
        Generate classification report.
        """

        self._ensure_model()

        y_pred = self._predict()
        y_true = self.context.y_test

        report = classification_report(y_true, y_pred)
        self.context.metrics = {"report": report}

        return report

    # -------------------------------------------------
    # Confusion Matrix
    # -------------------------------------------------

    def confusionMatrix(self) -> np.ndarray:
        """
        Compute confusion matrix.
        """

        self._ensure_model()

        y_pred = self._predict()
        y_true = self.context.y_test

        cm = confusion_matrix(y_true, y_pred)

        self.context.metrics = {"confusion_matrix": cm}
        return cm

    # -------------------------------------------------
    # ROC AUC
    # -------------------------------------------------

    def rocAuc(self) -> float:
        """
        Compute ROC AUC score.

        Works only if model supports predict_proba.
        """

        self._ensure_model()

        model = self.context.model

        if not hasattr(model, "predict_proba"):
            raise RuntimeError("Model does not support probability predictions.")

        y_true = self.context.y_test
        y_prob = model.predict_proba(self.context.X_test)

        # Binary classification assumed
        if y_prob.shape[1] == 2:
            score = roc_auc_score(y_true, y_prob[:, 1])
        else:
            score = roc_auc_score(y_true, y_prob, multi_class="ovr")

        self.context.metrics = {"roc_auc": score}
        return score

    # -------------------------------------------------
    # Custom Metric
    # -------------------------------------------------

    def customMetric(
        self,
        metric_function: Any,
    ) -> float:
        """
        Apply custom metric function.
        """

        self._ensure_model()

        y_pred = self._predict()
        y_true = self.context.y_test

        value = metric_function(y_true, y_pred)

        self.context.metrics = {"custom_metric": value}
        return value

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        if self.context.metrics is None:
            return "<EvaluateModule metrics=None>"
        return f"<EvaluateModule metrics={list(self.context.metrics.keys())}>"
