# baya/project.py

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd

from .context import Context

from .core.data import DataModule
from .core.clean import CleanModule
from .core.encode import EncodeModule
from .core.scale import ScaleModule
from .core.split import SplitModule
from .core.model import ModelModule
from .core.evaluate import EvaluateModule
from .core.transform import TransformModule

from .integrations import bootstrap_integrations


class Project:
    """
    User entry point.
    Thin orchestration layer.
    """

    def __init__(
        self,
        data: Optional[Union[str, Path, pd.DataFrame]] = None,
        *,
        target: Optional[str] = None,
        workspace: Optional[Union[str, Path]] = None,
        seed: int = 42,
    ) -> None:

        # -------------------------------------------------
        # Deterministic Backend Registration (Idempotent)
        # -------------------------------------------------
        bootstrap_integrations()

        # -------------------------------------------------
        # Workspace normalization
        # -------------------------------------------------
        workspace_path: Optional[Path] = None
        if workspace is not None:
            workspace_path = Path(workspace).resolve()
            workspace_path.mkdir(parents=True, exist_ok=True)

        # -------------------------------------------------
        # Context initialization
        # -------------------------------------------------
        self.context = Context(
            workspace=workspace_path,
            seed=seed,
        )

        # -------------------------------------------------
        # Module wiring
        # -------------------------------------------------
        self.data = DataModule(self.context)
        self.clean = CleanModule(self.context)
        self.encode = EncodeModule(self.context)
        self.scale = ScaleModule(self.context)
        self.split = SplitModule(self.context)
        self.model = ModelModule(self.context)
        self.evaluate = EvaluateModule(self.context)
        self.transform = TransformModule(self.context)

        # -------------------------------------------------
        # Optional ingestion
        # -------------------------------------------------
        if data is not None:
            self.data.load(data)

        # -------------------------------------------------
        # Optional target declaration
        # -------------------------------------------------
        if target is not None and self.context.get_dataframe() is not None:
            self.context.set_target(target)

    # =====================================================
    # Read-only accessors
    # =====================================================

    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        return self.context.get_dataframe()

    @property
    def target(self) -> Optional[str]:
        return self.context.get_target()

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:
        df = self.context.get_dataframe()
        rows = len(df) if df is not None else 0
        return f"<Baya Project rows={rows} target={self.target}>"