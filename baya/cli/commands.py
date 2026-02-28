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
