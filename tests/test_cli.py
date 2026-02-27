import json
import subprocess
import sys
from pathlib import Path


def test_cli_run(tmp_path: Path):
    data = tmp_path / "data.csv"
    data.write_text("x,y\n1,0\n2,0\n3,1\n4,1\n", encoding="utf-8")
    cfg = tmp_path / "workflow.json"
    cfg.write_text(json.dumps({"data_path": str(data), "target": "y", "model": "logistic_regression", "task": "classification"}), encoding="utf-8")

    cmd = [sys.executable, "-m", "baya", "run", str(cfg)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
