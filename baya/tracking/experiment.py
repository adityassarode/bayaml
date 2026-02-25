from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import uuid
import random
import numpy as np

from baya.reproducibility import RunManifest
from baya.reproducibility.environment_capture import capture_environment
from baya.reproducibility.config_freeze import freeze_config
from baya.reproducibility.snapshot import project_snapshot_hash

from .tracker import Tracker


class Experiment:
    def __init__(
        self,
        config: Dict[str, Any],
        dataset_hash: str,
        project_root: Path,
        tracking_root: Path,
        seed: int = 42,
    ) -> None:

        random.seed(seed)
        np.random.seed(seed)

        frozen = freeze_config(config)
        env = capture_environment()
        code_hash = project_snapshot_hash(project_root)

        manifest = RunManifest.new(
            run_id=str(uuid.uuid4()),
            dataset_hash=dataset_hash,
            code_hash=code_hash,
            config_hash=frozen["config_hash"],
            environment=env,
            config=frozen["config"],
            seed=seed,
        )

        self.manifest = manifest
        self.tracker = Tracker(manifest, tracking_root)