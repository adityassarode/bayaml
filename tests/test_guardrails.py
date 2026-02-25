from __future__ import annotations

import pytest
import pandas as pd
import numpy as np

from baya.project import Project
from baya.integrations.model_registry import ModelRegistry
from baya.integrations.sklearn.sklearn_backend import SklearnBackend


def _dataset() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    X = rng.normal(size=(100, 2))
    y = (X[:, 0] > 0).astype(int)

    df = pd.DataFrame(X, columns=["a", "b"])
    df["target"] = y
    return df


def _register() -> None:
    ModelRegistry.clear()
    backend = SklearnBackend()
    ModelRegistry.register_backend(backend)
    for m in backend.available_models():
        ModelRegistry.register_model(m, backend.name)


def test_train_before_split_fails() -> None:
    _register()
    df = _dataset()

    project = Project(data=df, target="target")
    project.model.create("logistic_regression", target="target")

    with pytest.raises(RuntimeError):
        project.model.train()


def test_evaluate_before_predict_fails() -> None:
    _register()
    df = _dataset()

    project = Project(data=df, target="target")
    project.split.random(test_size=0.2)
    project.model.create("logistic_regression", target="target")
    project.model.train()

    with pytest.raises(RuntimeError):
        project.evaluate.evaluate_classifier()


def test_schema_mismatch_predict_fails() -> None:
    _register()
    df = _dataset()

    project = Project(data=df, target="target")
    project.split.random(test_size=0.2)
    project.model.create("logistic_regression", target="target")
    project.model.train()

    bad_df = pd.DataFrame({"wrong": [1, 2, 3]})

    with pytest.raises(Exception):
        project.model.predict(bad_df)