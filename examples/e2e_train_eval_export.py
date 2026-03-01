import pandas as pd
import bayaml as by


def main() -> None:
    df = pd.DataFrame({
        "x1": [1, 2, 3, 4, 5, 6, 7, 8],
        "x2": [8, 7, 6, 5, 4, 3, 2, 1],
        "label": [0, 0, 0, 1, 1, 1, 1, 0],
    })

    p = by.Project(df, target="label", workspace="./demo_workspace", seed=42)
    p.split.train_test(test_size=0.25)
    p.model.create("random_forest_classifier", n_estimators=10)
    p.model.train()
    p.model.predict()
    metrics = p.evaluate.classification()
    p.tracker.log_metrics(metrics)
    p.tracker.finalize()
    print(metrics)


if __name__ == "__main__":
    main()
