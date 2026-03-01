from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping

import pandas as pd

from .cv import run_cv
from .hpo import search
from .leaderboard import append_leaderboard
from .registry import list_models
from .tracking import Tracker


def _to_df(data: Any) -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data.copy()
    if isinstance(data, (str, Path)):
        path = Path(data)
        if path.suffix.lower() == ".csv":
            return pd.read_csv(path)
        if path.suffix.lower() in (".xlsx", ".xls"):
            return pd.read_excel(path)
        if path.suffix.lower() == ".json":
            return pd.read_json(path)
    raise TypeError("data must be a DataFrame or a supported file path.")


def bayaml(data: Any, target: str, config: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    """Primary AutoML entrypoint wrapping Project-based CV/HPO execution."""
    cfg = dict(config or {})
    df = _to_df(data)

    task = "classification" if df[target].dtype.kind in ("i", "b", "O") else "regression"
    folds = int(cfg.get("folds", 5))
    seed = int(cfg.get("seed", 42))
    search_type = str(cfg.get("search_type", "grid"))
    param_grids = dict(cfg.get("param_grids", {}))

    models = cfg.get("models") or list_models()
    if task == "classification":
        models = [m for m in models if "classifier" in m or "logistic" in m]
    else:
        models = [m for m in models if "regressor" in m or "linear_regression" in m]

    leaderboard: list[Dict[str, Any]] = []
    cv_results: Dict[str, Any] = {}

    for model_name in models:
        grid = param_grids.get(model_name)
        if grid:
            hpo_result = search(
                data=df,
                target=target,
                model_name=model_name,
                param_grid=grid,
                search_type=search_type,
                folds=folds,
                seed=seed,
            )
            cv_result = hpo_result["best_cv"]
            best_params = hpo_result["best_params"]
        else:
            cv_result = run_cv(
                data=df,
                target=target,
                model_name=model_name,
                model_params={},
                folds=folds,
                seed=seed,
            )
            best_params = {}

        score_key = "accuracy" if task == "classification" else "r2"
        score = float(cv_result["mean_metrics"][score_key])

        row = {
            "model": model_name,
            "score": score,
            "params": best_params,
            "mean_metrics": cv_result["mean_metrics"],
            "std_metrics": cv_result["std_metrics"],
        }
        leaderboard.append(row)
        cv_results[model_name] = cv_result

    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    best = leaderboard[0]

    tracker = Tracker(Path("bayaml") / "tracking")
    tracker.log_param("task", task)
    tracker.log_param("models", [row["model"] for row in leaderboard])
    tracker.log_param("best_model", best["model"])
    tracker.log_param("cv_results", cv_results)
    tracker.log_param("hyperparameters", {r["model"]: r["params"] for r in leaderboard})
    tracker.log_metrics(best["mean_metrics"])
    tracker.finalize()

    result = {
        "run_id": tracker.run_id,
        "task": task,
        "best_model": best["model"],
        "best_score": float(best["score"]),
        "leaderboard": leaderboard,
        "cv_results": cv_results,
    }

    append_leaderboard(
        {
            "run_id": tracker.run_id,
            "task": task,
            "models": [row["model"] for row in leaderboard],
            "best_model": best["model"],
            "best_score": float(best["score"]),
            "leaderboard": leaderboard,
        }
    )

    return result
