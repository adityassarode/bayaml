from __future__ import annotations

from pathlib import Path
from typing import Optional

from .run_manifest import RunManifest
from .snapshot import project_snapshot_hash
from .dataset_hash import hash_dataframe
from .config_freeze import freeze_config


class ReproducibilityError(Exception):
    """Raised when reproduction validation fails."""
    pass


def reproduce_run(
    *,
    manifest_path: Path,
    project_root: Path,
    current_dataset_hash: Optional[str] = None,
    current_config: Optional[dict] = None,
    strict: bool = True,
) -> RunManifest:
    """
    Load and validate a run manifest.

    Verifies:
        - Code snapshot hash
        - Dataset hash (optional)
        - Config hash (optional)

    Does NOT mutate runtime state.
    """

    manifest = RunManifest.load(manifest_path)

    # -------------------------------------------------
    # Code hash validation
    # -------------------------------------------------
    current_code_hash = project_snapshot_hash(project_root)

    if current_code_hash != manifest.code_hash:
        msg = "Code snapshot hash mismatch."

        if strict:
            raise ReproducibilityError(msg)
        else:
            print(f"[WARN] {msg}")

    # -------------------------------------------------
    # Dataset validation (optional)
    # -------------------------------------------------
    if current_dataset_hash is not None:
        if current_dataset_hash != manifest.dataset_hash:
            msg = "Dataset hash mismatch."

            if strict:
                raise ReproducibilityError(msg)
            else:
                print(f"[WARN] {msg}")

    # -------------------------------------------------
    # Config validation (optional)
    # -------------------------------------------------
    if current_config is not None:
        frozen = freeze_config(current_config)

        if frozen["config_hash"] != manifest.config_hash:
            msg = "Config hash mismatch."

            if strict:
                raise ReproducibilityError(msg)
            else:
                print(f"[WARN] {msg}")

    return manifest