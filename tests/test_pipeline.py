import pandas as pd

from bayaml.orchestration import Phase
from bayaml.project import Project


def test_pipeline_executes_steps(tmp_path):
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [0, 0, 1, 1]})
    p = Project(df, target="y", workspace=tmp_path)

    p.pipeline.add_step("split", Phase.SPLIT, lambda c: p.split.train_test(0.5))
    p.pipeline.add_step("create", Phase.TRAIN, lambda c: p.model.create("logistic_regression"), depends_on="split")
    p.pipeline.add_step("fit", Phase.TRAIN, lambda c: p.model.train(), depends_on="create")
    p.pipeline.add_step("pred", Phase.PREDICT, lambda c: p.model.predict(), depends_on="fit")
    p.pipeline.add_step("eval", Phase.EVALUATE, lambda c: p.evaluate.classification(), depends_on="pred")
    p.pipeline.run()
    assert p.context.get_metrics()["accuracy"] >= 0.0
