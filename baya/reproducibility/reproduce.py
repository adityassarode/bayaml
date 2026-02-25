from __future__ import annotations

from pathlib import Path
from .run_manifest import RunManifest


def reproduce_run(manifest_path: Path) -> RunManifest:
    """
    Loads a run manifest and prepares reproduction.
    Orchestration layer will use this to rebuild pipeline.
    """
    manifest = RunManifest.load(manifest_path)
    return manifest