from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

from .leaderboard import load_leaderboard


def plot_leaderboard(root: Path | None = None) -> None:
    data = load_leaderboard(root)
    if not data:
        raise RuntimeError("No leaderboard runs found.")

    latest = data[-1]
    board = latest.get("leaderboard", [])
    names = [row["model"] for row in board]
    scores = [row["score"] for row in board]

    plt.figure(figsize=(8, 4))
    plt.bar(names, scores)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("score")
    plt.title(f"Baya Leaderboard (run {latest.get('run_id')})")
    plt.tight_layout()
    plt.show()


def plot_metric_history(run_id: str, root: Path | None = None) -> None:
    base = root or Path("baya_runs")
    run_file = base / "tracking" / run_id / "run.json"
    if not run_file.exists():
        raise FileNotFoundError(f"Tracking run file not found: {run_file}")

    payload = json.loads(run_file.read_text(encoding="utf-8"))
    metrics = payload.get("metrics", {})
    if not metrics:
        raise RuntimeError("No metrics found for run.")

    names = list(metrics.keys())
    values = [float(metrics[k]) for k in names]

    plt.figure(figsize=(8, 4))
    plt.plot(names, values, marker="o")
    plt.ylabel("value")
    plt.title(f"Metric History ({run_id})")
    plt.tight_layout()
    plt.show()
