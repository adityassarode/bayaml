import os
from pathlib import Path

import pandas as pd

from baya import baya, list_models, register_model
from baya.leaderboard import load_leaderboard


def test_baya_automl_runs_and_persists(tmp_path: Path) -> None:
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [0, 0, 0, 1, 1, 1]})

    cwd = Path.cwd()
    try:
        # isolate default persistence location
        os.chdir(tmp_path)
        result = baya(df, target="y", config={"folds": 3})
        assert result["best_model"]
        assert isinstance(result["best_score"], float)

        board = load_leaderboard()
        assert len(board) >= 1
        assert board[-1]["run_id"] == result["run_id"]
    finally:
        os.chdir(cwd)


def test_registry_custom_model_registration() -> None:
    from sklearn.tree import DecisionTreeClassifier

    register_model("decision_tree_classifier", DecisionTreeClassifier)
    assert "decision_tree_classifier" in list_models()
