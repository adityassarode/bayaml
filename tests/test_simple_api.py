from pathlib import Path

import pandas as pd

from baya import Baya, quick_train


def test_quick_train_classification_dataframe() -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [0, 0, 1, 1]})
    metrics = quick_train(data=df, target="y", model="logistic_regression")
    assert "accuracy" in metrics


def test_fluent_baya_regression_csv(tmp_path: Path) -> None:
    csv = tmp_path / "data.csv"
    csv.write_text("x,y\n1,2.0\n2,4.0\n3,6.0\n4,8.0\n", encoding="utf-8")

    metrics = Baya(csv, target="y", test_size=0.25).train("linear_regression").evaluate()
    assert "mse" in metrics
