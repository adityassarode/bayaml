from __future__ import annotations

import pandas as pd
import pytest

from bayaml.project import Project


def test_plan_hash_deterministic_preview() -> None:
    df = pd.DataFrame({"a": [1, 2, 3, 4], "y": [0, 0, 1, 1]})
    p = Project(df, target="y", seed=7)
    p1 = p.auto("train classification model using logistic regression", preview=True)
    p2 = p.auto("train classification model using logistic regression", preview=True)
    assert p1.plan_hash == p2.plan_hash


def test_auto_multistep_instruction_with_matrix(tmp_path) -> None:
    p = Project(workspace=tmp_path)
    result = p.auto(
        "this is the matrix [[1,2,0],[2,3,1],[3,4,0],[4,5,1],[5,6,0],[6,7,1]] "
        "treat last column as target train classification model using random forest "
        "show confusion matrix plot histogram of col_0 export report.pdf"
    )
    assert "train" in result["steps_executed"]
    assert result["model_used"] == "random_forest_classifier"
    assert any(path.endswith("report.pdf") for path in result["exports_generated"])


def test_auto_dataset_csv_parsing_and_cleaning(tmp_path) -> None:
    csv_path = tmp_path / "dataset.csv"
    pd.DataFrame(
        {
            "Age": [10, None, 12, 13, 14, 15, 16, 17],
            "x": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            "y": [0, 1, 0, 1, 0, 1, 0, 1],
        }
    ).to_csv(csv_path, index=False)

    p = Project(workspace=tmp_path)
    result = p.auto(
        f"use {csv_path} remove null values fill Age with mean drop duplicates "
        "train classification model using logistic regression evaluate model"
    )
    assert "evaluate" in result["steps_executed"]
    assert p.context.get_dataframe().isna().sum().sum() == 0


def test_auto_export_and_deploy_parse(tmp_path) -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [0, 0, 0, 1, 1, 1]})
    p = Project(df, target="y", workspace=tmp_path)
    result = p.auto(
        "train classification model using random forest export results.csv deploy model"
    )
    assert any(str(x).endswith("results.csv") for x in result["exports_generated"])
    assert result["deployment_status"]


def test_auto_deploy_cpp_maps_to_onnx(tmp_path) -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [0, 0, 0, 1, 1, 1]})
    p = Project(df, target="y", workspace=tmp_path)
    # preview avoids optional ONNX dependency hard requirement during parse test
    plan = p.auto("train classification model using random forest deploy in c++", preview=True)
    deploy_steps = [s for s in plan.steps if s.name == "deploy"]
    assert deploy_steps and deploy_steps[0].params["mode"] == "onnx"


def test_guardian_imbalance_warning(tmp_path) -> None:
    df = pd.DataFrame({"x": list(range(20)), "y": [1] * 18 + [0, 0]})
    p = Project(df, target="y", workspace=tmp_path)
    p.split.train_test(0.2)
    p.model.create("logistic_regression")
    p.model.train()
    report = p.guardian()
    assert report["warnings"]
    assert any("Imbalance" in msg for msg in report["warnings"])


def test_stability_deterministic(tmp_path) -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6, 7, 8], "y": [0, 0, 0, 1, 1, 1, 1, 1]})

    p1 = Project(df, target="y", seed=42, workspace=tmp_path / "a")
    p1.split.train_test(0.25)
    p1.model.create("logistic_regression")
    p1.model.train()

    p2 = Project(df, target="y", seed=42, workspace=tmp_path / "b")
    p2.split.train_test(0.25)
    p2.model.create("logistic_regression")
    p2.model.train()

    assert p1.stability(n_runs=5) == p2.stability(n_runs=5)


def test_matrix_validation_rejects_invalid() -> None:
    p = Project()
    with pytest.raises(ValueError):
        p.auto("this is the matrix [[1,2],[3,4,5]] train regression model")
