from pathlib import Path

from bayaml.tracking import Tracker


def test_tracker_finalize(tmp_path: Path):
    t = Tracker(tmp_path)
    t.log_param("model", "rf")
    t.log_metric("acc", 0.9)
    path = t.finalize()
    assert path.exists()
