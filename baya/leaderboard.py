from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def _leaderboard_path(root: Path | None = None) -> Path:
    base = root or Path("baya_runs")
    base.mkdir(parents=True, exist_ok=True)
    return base / "leaderboard.json"


def load_leaderboard(root: Path | None = None) -> List[Dict[str, Any]]:
    path = _leaderboard_path(root)
    if not path.exists():
        return []
    return list(json.loads(path.read_text(encoding="utf-8")))


def append_leaderboard(entry: Dict[str, Any], root: Path | None = None) -> Path:
    records = load_leaderboard(root)
    payload = dict(entry)
    payload.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    records.append(payload)
    path = _leaderboard_path(root)
    path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    return path
