from __future__ import annotations

from typing import Any, Callable, Dict
import json
import pandas as pd
from tabulate import tabulate
import numpy as np
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    explained_variance_score,
    median_absolute_error,
    max_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    confusion_matrix,
    matthews_corrcoef,
    log_loss,
    roc_auc_score,
)

import numpy as np
from ..context import Context
from ..metrics.classification import accuracy, f1, precision, recall
from ..metrics.regression import mae, mse, r2


class EvaluateModule:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def _y(self) -> tuple[Any, Any]:
        if self._ctx.get_predictions() is None:
            raise RuntimeError(
                "No predictions found. Run project.model.predict() before evaluation."
            )
        _, _, _, y_test = self._ctx.get_split_data()
        return y_test, self._ctx.get_predictions()

    def _format_output(self, metrics: dict, mode: str):

        # Keep logic same, just protect numeric operations
        numeric_values = [
            v
            for v in metrics.values()
            if isinstance(v, (int, float, np.integer, np.floating))
        ]

        if mode == "dict":
            return metrics

        if mode == "original":
            print("\n===== Model Evaluation =====")
            if "mse" in metrics:
                print("Mean Squared Error:", metrics.get("mse"))
            if "r2" in metrics:
                print("R2 Score:", metrics.get("r2"))
            if "accuracy" in metrics:
                print("Accuracy:", metrics.get("accuracy"))
            return metrics

        if mode == "pretty":
            print("\n===== Evaluation Report =====")
            for k, v in metrics.items():
                if isinstance(v, (int, float, np.integer, np.floating)):
                    print(f"{k.replace('_', ' ').title():<25}: {v:.6f}")
                else:
                    print(f"{k.replace('_', ' ').title():<25}: {v}")
            return metrics

        if mode == "full":
            print("\n===== FULL METRICS REPORT =====")
            for k, v in metrics.items():
                print(f"{k:<25} -> {v}")
            print("\nTotal Metrics:", len(metrics))

            if numeric_values:
                print("Mean of Metrics:", np.mean(numeric_values))
                print("Std of Metrics:", np.std(numeric_values))
                print(
                    "Max Metric:",
                    max(
                        (
                            k
                            for k in metrics
                            if isinstance(metrics[k], (int, float))
                        ),
                        key=lambda x: metrics[x],
                    ),
                )
                print(
                    "Min Metric:",
                    min(
                        (
                            k
                            for k in metrics
                            if isinstance(metrics[k], (int, float))
                        ),
                        key=lambda x: metrics[x],
                    ),
                )

            return metrics

        if mode == "sklearn":
            print(
                tabulate(
                    metrics.items(),
                    headers=["Metric", "Score"],
                    tablefmt="simple",
                )
            )
            return metrics

        if mode == "table":
            print(
                tabulate(
                    metrics.items(),
                    headers=["Metric", "Value"],
                    tablefmt="grid",
                )
            )
            return metrics

        if mode == "pandas":
            df = pd.DataFrame(
                metrics.items(),
                columns=["Metric", "Value"],
            )
            print(df)
            return df

        if mode == "numpy":
            arr = np.array(numeric_values)
            print("NumPy Metrics Array:")
            print(arr)
            return arr

        if mode == "json":
            print(json.dumps(metrics, indent=4))
            return metrics

        if mode == "markdown":
            print(
                tabulate(
                    metrics.items(),
                    headers=["Metric", "Value"],
                    tablefmt="github",
                )
            )
            return metrics

        if mode == "latex":
            df = pd.DataFrame(
                metrics.items(),
                columns=["Metric", "Value"],
            )
            print(df.to_latex(index=False))
            return metrics

        if mode == "diagnostic":
            print("\n===== Diagnostic Report =====")
            print("Metric Count:", len(metrics))

            if numeric_values:
                print("Metric Mean:", np.mean(numeric_values))
                print("Metric Std:", np.std(numeric_values))
                print("Metric Variance:", np.var(numeric_values))
                print(
                    "Best Metric:",
                    max(
                        (
                            k
                            for k in metrics
                            if isinstance(metrics[k], (int, float))
                        ),
                        key=lambda x: metrics[x],
                    ),
                )
                print(
                    "Worst Metric:",
                    min(
                        (
                            k
                            for k in metrics
                            if isinstance(metrics[k], (int, float))
                        ),
                        key=lambda x: metrics[x],
                    ),
                )

            return metrics

        raise ValueError(f"Unknown mode: {mode}")

    def classification(self, mode="dict"):
        y_true = self._ctx.get_y_test()
        y_pred = self._ctx.get_predictions()

        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(
                y_true, y_pred, average="weighted", zero_division=0
            ),
            "recall": recall_score(
                y_true, y_pred, average="weighted", zero_division=0
            ),
            "f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
            "matthews_corrcoef": matthews_corrcoef(y_true, y_pred),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        }

        try:
            metrics["roc_auc"] = roc_auc_score(y_true, y_pred)
        except Exception:
            pass

        try:
            metrics["log_loss"] = log_loss(y_true, y_pred)
        except Exception:
            pass

        return self._format_output(metrics, mode)

    def regression(self, mode="dict"):
        y_true = self._ctx.get_y_test()
        y_pred = self._ctx.get_predictions()

        residuals = y_true - y_pred

        metrics = {
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
            "mae": mean_absolute_error(y_true, y_pred),
            "median_ae": median_absolute_error(y_true, y_pred),
            "r2": r2_score(y_true, y_pred),
            "explained_variance": explained_variance_score(y_true, y_pred),
            "max_error": max_error(y_true, y_pred),
            "residual_mean": float(np.mean(residuals)),
            "residual_std": float(np.std(residuals)),
            "residual_variance": float(np.var(residuals)),
        }

        return self._format_output(metrics, mode)

    def custom_metric(
        self, fn: Callable[[Any, Any], float], name: str = "custom_metric"
    ) -> float:
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