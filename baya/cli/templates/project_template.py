from pathlib import Path


def create_project(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

    (path / "config.yaml").write_text(
        "dataset_path: data.csv\n"
        "target: target\n"
        "task: regression\n"
        "metric: rmse\n"
        "seed: 42\n"
        "test_size: 0.2\n"
    )