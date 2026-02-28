from __future__ import annotations

from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold

from .project import Project


def _task_type(df: pd.DataFrame, target: str) -> str:
    kind = df[target].dtype.kind
    return "classification" if kind in ("i", "b", "O") else "regression"


def run_cv(
    data: pd.DataFrame,
    target: str,
    model_name: str,
    model_params: Dict[str, Any] | None = None,
    folds: int = 5,
    seed: int = 42,
) -> Dict[str, Any]:
    """Run KFold/StratifiedKFold CV by wrapping Project per fold."""
    df = data.copy()
    params = dict(model_params or {})
    task = _task_type(df, target)

    X = df.drop(columns=[target])
    y = df[target]

    max_folds = len(df)
    if task == "classification":
        min_class = int(y.value_counts().min())
        max_folds = min(max_folds, min_class)
    folds = max(2, min(int(folds), max_folds))

    splitter = (
        StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
        if task == "classification"
        else KFold(n_splits=folds, shuffle=True, random_state=seed)
    )

    fold_metrics: list[Dict[str, float]] = []

    for train_idx, test_idx in splitter.split(X, y):
        fold_df = df.iloc[train_idx.tolist() + test_idx.tolist()].reset_index(drop=True)
        n_train = len(train_idx)

        project = Project(fold_df, target=target, seed=seed)
        X_all = project.context.get_dataframe().drop(columns=[target])
        y_all = project.context.get_dataframe()[target]

        X_train = X_all.iloc[:n_train]
        y_train = y_all.iloc[:n_train]
        X_test = X_all.iloc[n_train:]
        y_test = y_all.iloc[n_train:]

        project.context.set_split_data(X_train, X_test, y_train, y_test)
        project.model.create(model_name, **params)
        project.model.train()

        metrics = (
            project.evaluate.evaluate_classifier()
            if task == "classification"
            else project.evaluate.evaluate_regressor()
        )
        fold_metrics.append({k: float(v) for k, v in metrics.items()})

    keys = sorted(fold_metrics[0].keys()) if fold_metrics else []
    mean_metrics = {k: float(np.mean([m[k] for m in fold_metrics])) for k in keys}
    std_metrics = {k: float(np.std([m[k] for m in fold_metrics])) for k in keys}

    return {
        "task": task,
        "model": model_name,
        "params": params,
        "folds": folds,
        "fold_metrics": fold_metrics,
        "mean_metrics": mean_metrics,
        "std_metrics": std_metrics,
    }
