"""
Baya Project Core

This is the main orchestration entry point for users.

Usage:

    import baya as by

    p = by.Project("data.csv", target="price")
    p.data.preview()
    p.clean.fillMissing("Age", "mean")
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Any

import pandas as pd

from .context import Context

# Core modules
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
    Main user-facing Baya Project class.

    Holds dataset, configuration, and module access.
    """

    def __init__(
        self,
        data: Optional[str | Path | pd.DataFrame] = None,
        *,
        target: Optional[str] = None,
    ) -> None:
        """
        Initialize a Baya Project.

        Parameters
        ----------
        data : str | Path | DataFrame | None
            Path to CSV/Excel/JSON or existing DataFrame.
        target : str | None
            Target column for modeling.
        """

        self.context = Context()

        self.context.target = target

        if isinstance(data, (str, Path)):
            self._load_file(data)
        elif isinstance(data, pd.DataFrame):
            self.context.dataframe = data.copy()
        elif data is None:
            self.context.dataframe = None
        else:
            raise TypeError("Unsupported data type for Project initialization.")

        # Expose modules
        self.data = DataModule(self.context)
        self.clean = CleanModule(self.context)
        self.encode = EncodeModule(self.context)
        self.scale = ScaleModule(self.context)
        self.split = SplitModule(self.context)
        self.model = ModelModule(self.context)
        self.evaluate = EvaluateModule(self.context)
        self.transform = TransformModule(self.context)

    # -------------------------------------------------
    # Internal helpers
    # -------------------------------------------------

    def _load_file(self, path: str | Path) -> None:
        """
        Load file automatically based on extension.
        """

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = path.suffix.lower()

        if suffix == ".csv":
            self.context.dataframe = pd.read_csv(path)
        elif suffix in (".xlsx", ".xls"):
            self.context.dataframe = pd.read_excel(path)
        elif suffix == ".json":
            self.context.dataframe = pd.read_json(path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    # -------------------------------------------------
    # Public properties
    # -------------------------------------------------

    @property
    def dataframe(self) -> Optional[pd.DataFrame]:
        """
        Direct access to underlying DataFrame.
        """
        return self.context.dataframe

    @property
    def target(self) -> Optional[str]:
        """
        Get target column.
        """
        return self.context.target

    # -------------------------------------------------
    # User Extensions
    # -------------------------------------------------

    def injectModel(self, model: Any) -> None:
        """
        Inject custom model instance.
        """
        self.context.model = model

    def setDataFrame(self, df: pd.DataFrame) -> None:
        """
        Replace current DataFrame.
        """
        self.context.dataframe = df.copy()

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<Baya Project "
            f"rows={len(self.context.dataframe) if self.context.dataframe is not None else 0} "
            f"target={self.context.target}>"
        )
