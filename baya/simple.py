from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from .project import Project

DataInput = Union[str, Path, pd.DataFrame]


def quick_train(
    data: DataInput,
    target: str,
    model: str,
    test_size: float = 0.2,
    **kwargs: Any,
) -> Dict[str, float]:
    """Train and evaluate a model in a single call using the Project engine."""
    project = Project(data=data, target=target)
    project.split.train_test(test_size=test_size)
    project.model.create(model, **kwargs)
    project.model.train()
    project.model.predict()

    task = project.context.get_task_type()
    if task == "classification":
        return project.evaluate.classification()
    return project.evaluate.regression()


class Baya:
    """Fluent high-level API wrapper around Project for shorter workflows."""

    def __init__(
        self,
        data: DataInput,
        *,
        target: str,
        test_size: float = 0.2,
        workspace: Optional[Union[str, Path]] = None,
        seed: int = 42,
    ) -> None:
        self._project = Project(
            data=data,
            target=target,
            workspace=workspace,
            seed=seed,
        )
        self._project.split.train_test(test_size=test_size)

    def train(self, model: str, **kwargs: Any) -> "Baya":
        self._project.model.create(model, **kwargs)
        self._project.model.train()
        self._project.model.predict()
        return self

    def evaluate(self) -> Dict[str, float]:
        task = self._project.context.get_task_type()
        if task == "classification":
            return self._project.evaluate.classification()
        return self._project.evaluate.regression()

    @property
    def project(self) -> Project:
        return self._project
