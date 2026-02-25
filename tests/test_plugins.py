import baya


def test_baya_end_to_end(tmp_path):
    # create project
    project = baya.Project(workspace=tmp_path)

    # load dataset
    df = project.data.from_dict({
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 6, 8, 10],
    })

    # train model
    model = project.model.create("linear_regression", target="y")
    model.train()

    # predict
    preds = model.predict(df[["x"]])

    assert len(preds) == 5