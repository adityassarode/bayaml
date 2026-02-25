from __future__ import annotations

import pandas as pd
import numpy as np

from baya.project import Project
from baya.integrations.model_registry import ModelRegistry
from baya.integrations.sklearn.sklearn_backend import SklearnBackend


def _make_dataset(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    X = rng.normal(size=(200, 3))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)

    df = pd.DataFrame(X, columns=["a", "b", "c"])
    df["target"] = y

    return df


def _register_backend() -> None:
    ModelRegistry.clear()
    backend = SklearnBackend()
    ModelRegistry.register_backend(backend)

    for model_name in backend.available_models():
        ModelRegistry.register_model(model_name, backend.name)


def test_full_pipeline_deterministic() -> None:
    _register_backend()

    df = _make_dataset()

    project = Project(data=df, target="target", seed=123)

    # split
    project.split.random(test_size=0.2)

    # create
    project.model.create("logistic_regression", target="target")

    # train
    project.model.train()

    # predict
    preds_1 = project.model.predict()

    # evaluate
    metrics_1 = project.evaluate.evaluate_classifier()

    # ---- Run again ----
    _register_backend()

    project2 = Project(data=df, target="target", seed=123)
    project2.split.random(test_size=0.2)
    project2.model.create("logistic_regression", target="target")
    project2.model.train()
    preds_2 = project2.model.predict()
    metrics_2 = project2.evaluate.evaluate_classifier()

    assert np.array_equal(preds_1, preds_2)
    assert metrics_1 == metrics_2