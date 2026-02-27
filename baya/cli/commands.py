from __future__ import annotations

from pathlib import Path

from baya.project import Project


def run_from_config(path: Path) -> Project:
    project = Project.from_config(path)
    project.run()
    return project
