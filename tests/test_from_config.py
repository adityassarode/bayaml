import json
from pathlib import Path

from baya.config import ConfigSchema
from baya.project import Project


def _write_data(tmp_path: Path) -> Path:
    data = tmp_path / "data.csv"
    data.write_text("x,y\n1,0\n2,0\n3,1\n4,1\n", encoding="utf-8")
    return data


def test_from_config_with_dict(tmp_path: Path):
    data = _write_data(tmp_path)
    cfg = {
        "data_path": str(data),
        "target": "y",
        "model": "logistic_regression",
        "task": "classification",
    }
    project = Project.from_config(cfg)
    metrics = project.run()
    assert "accuracy" in metrics


def test_from_config_with_path_and_schema(tmp_path: Path):
    data = _write_data(tmp_path)
    cfg_path = tmp_path / "workflow.json"
    cfg_path.write_text(
        json.dumps(
            {
                "data_path": str(data),
                "target": "y",
                "model": "logistic_regression",
                "task": "classification",
            }
        ),
        encoding="utf-8",
    )
    from_path = Project.from_config(str(cfg_path))
    assert from_path.target == "y"

    schema = ConfigSchema(
        data_path=str(data),
        target="y",
        model="logistic_regression",
        task="classification",
    )
    from_schema = Project.from_config(schema)
    assert from_schema.target == "y"
