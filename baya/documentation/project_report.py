from __future__ import annotations
from baya.context import Context
from typing import Dict, Any


class ProjectReport:
    def generate(self, context: Context) -> Dict[str, Any]:
        return {
            "run_id": context.experiment.manifest.run_id,
            "dataset_hash": context.experiment.manifest.dataset_hash,
            "code_hash": context.experiment.manifest.code_hash,
            "config": context.experiment.manifest.config,
            "metrics": context.tracker.get_all_metrics(),
        }