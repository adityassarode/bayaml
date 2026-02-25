from __future__ import annotations
from typing import Any, Dict


class ModelSummary:
    def summarize(self, model: Any) -> Dict[str, str]:
        summary: Dict[str, str] = {}

        if hasattr(model, "get_params"):
            summary["type"] = type(model).__name__
            summary["params"] = str(model.get_params())

        elif hasattr(model, "summary"):
            summary["type"] = type(model).__name__
            summary["details"] = str(model.summary())

        else:
            summary["type"] = type(model).__name__

        return summary