from __future__ import annotations


def build_project_report(metrics: dict) -> str:
    return "Baya Project Report\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(metrics.items()))
