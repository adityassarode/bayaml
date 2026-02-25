"""
Baya Project Core
Lifecycle root — no validation during construction.
"""

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


class Project:
    """
    User entry point.
    """

    def __init__(
        self,
        data: Optional[Union[str, Path, pd.DataFrame]] = None,
        *,
        target: Optional[str] = None,
        workspace: Optional[Union[str, Path]] = None,
    ) -> None:

        self.context = Context(workspace=workspace)

        # Declare only (no validation)
        self.context.set_target(target)

        # Modules
        self.data = DataModule(self.context)
        self.clean = CleanModule(self.context)
        self.encode = EncodeModule(self.context)
        self.scale = ScaleModule(self.context)
        self.split = SplitModule(self.context)
        self.model = ModelModule(self.context)
        self.evaluate = EvaluateModule(self.context)
        self.transform = TransformModule(self.context)

        # Optional ingestion
        if data is not None:
            self.data.load(data)

    # ----------------------------------------------

    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        return self.context.get_dataframe()

    @property
    def target(self) -> Optional[str]:
        return self.context.get_target()

    def __repr__(self) -> str:
        df = self.context.get_dataframe()
        rows = len(df) if df is not None else 0
        return f"<Baya Project rows={rows} target={self.target}>"