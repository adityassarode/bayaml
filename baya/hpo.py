from __future__ import annotations

import itertools
import random
from typing import Any, Dict, Iterable, List

import pandas as pd

from .cv import run_cv


def _expand_grid(param_grid: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    if not param_grid:
        return [{}]
    keys = list(param_grid.keys())
    values = [param_grid[k] for k in keys]
    return [dict(zip(keys, combo)) for combo in itertools.product(*values)]


def search(
    data: pd.DataFrame,
    target: str,
    model_name: str,
    param_grid: Dict[str, List[Any]],
    search_type: str = "grid",
    folds: int = 5,
    seed: int = 42,
    max_trials: int = 10,
) -> Dict[str, Any]:
    candidates = _expand_grid(param_grid)
    if search_type == "random" and len(candidates) > max_trials:
        rng = random.Random(seed)
        candidates = rng.sample(candidates, max_trials)

    trials: list[Dict[str, Any]] = []
    best_score = float("-inf")
    best_params: Dict[str, Any] = {}
    best_cv: Dict[str, Any] | None = None

    for params in candidates:
        cv_result = run_cv(
            data=data,
            target=target,
            model_name=model_name,
            model_params=params,
            folds=folds,
            seed=seed,
        )

        task = cv_result["task"]
        score_key = "accuracy" if task == "classification" else "r2"
        score = float(cv_result["mean_metrics"][score_key])

        trials.append({"params": params, "score": score, "cv": cv_result})

        if score > best_score:
            best_score = score
            best_params = params
            best_cv = cv_result

    return {
        "model": model_name,
        "search_type": search_type,
        "best_params": best_params,
        "best_score": best_score,
        "best_cv": best_cv,
        "trials": trials,
    }
