from __future__ import annotations

from pathlib import Path

from baya.config import load_config, validate_config
from baya.project import Project


def run_from_config(path: Path) -> Project:
    cfg = validate_config(load_config(path))
    project = Project.from_config(cfg)
    project.model.train()
    project.model.predict()
    metrics = project.evaluate.classification() if cfg.task == "classification" else project.evaluate.regression()
    project.tracker.log_metrics(metrics)
    project.tracker.finalize()
    return project
