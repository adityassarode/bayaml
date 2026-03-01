import pandas as pd

from bayaml.project import Project


def test_project_train_classification_flow(tmp_path):
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [0, 0, 0, 1, 1, 1]})
    p = Project(df, target="y", workspace=tmp_path)
    p.split.train_test(test_size=0.33)
    p.model.create("random_forest_classifier", n_estimators=8)
    p.model.train()
    preds = p.model.predict()
    assert len(preds) > 0
    metrics = p.evaluate.classification()
    assert "accuracy" in metrics


def test_train_auto_predict_enables_eval(tmp_path):
    import pandas as pd
    from bayaml.project import Project

    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [0, 0, 0, 1, 1, 1]})
    p = Project(df, target="y", workspace=tmp_path)
    p.split.train_test(test_size=0.33)
    p.model.create("logistic_regression")
    p.model.train()
    metrics = p.evaluate.evaluate_classifier()
    assert "accuracy" in metrics
