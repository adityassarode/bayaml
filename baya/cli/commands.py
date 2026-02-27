from __future__ import annotations

from pathlib import Path

from typing import Any, Mapping

from baya.automl import baya as automl_entry
from baya.leaderboard import load_leaderboard
from baya.project import Project
from baya.visualize import plot_leaderboard


def run_from_config(path: Path) -> Project:
    project = Project.from_config(path)
    project.run()
    return project


def run_automl_from_config(path: Path) -> dict[str, Any]:
    cfg_project = Project._coerce_config(path)
    cfg: Mapping[str, Any] = {}
    result = automl_entry(data=cfg_project.data_path, target=cfg_project.target, config=cfg)
    return result


def show_leaderboard() -> list[dict[str, Any]]:
    return load_leaderboard()


def visualize_leaderboard() -> None:
    plot_leaderboard()




from baya.config import load_config, validate_config

from baya.project import Project


def run_from_config(path: Path) -> Project:

    project = Project.from_config(path)
    project.run()

    cfg = validate_config(load_config(path))
    project = Project.from_config(cfg)
    project.model.train()
    project.model.predict()
    metrics = project.evaluate.classification() if cfg.task == "classification" else project.evaluate.regression()
    project.tracker.log_metrics(metrics)
    project.tracker.finalize()

    return project

