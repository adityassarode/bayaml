"""
Baya Context

Central state container for a Project.

Stores:
- Data
- Model
- Metrics
- Pipeline state
- Configuration
- Hooks
- Plugins
- Visualization state
"""

from __future__ import annotations

from typing import Optional, Any, Dict

import pandas as pd


class Context:
    """
    Central runtime state for Baya Project.

    This object is shared across all modules.
    """

    def __init__(self) -> None:
        # ----------------------------
        # Core Data
        # ----------------------------
        self.dataframe: Optional[pd.DataFrame] = None
        self.target: Optional[str] = None

        # ----------------------------
        # Modeling State
        # ----------------------------
        self.model: Optional[Any] = None
        self.X_train: Optional[Any] = None
        self.X_test: Optional[Any] = None
        self.y_train: Optional[Any] = None
        self.y_test: Optional[Any] = None
        self.predictions: Optional[Any] = None

        # ----------------------------
        # Metrics
        # ----------------------------
        self.metrics: Dict[str, Any] = {}

        # ----------------------------
        # Pipeline & Execution
        # ----------------------------
        self.pipeline_nodes: Dict[str, Any] = {}
        self.pipeline_edges: Dict[str, list[str]] = {}

        # ----------------------------
        # Hooks & Middleware
        # ----------------------------
        self.hooks: Dict[str, list[Any]] = {}
        self.middleware: list[Any] = []

        # ----------------------------
        # Tracking
        # ----------------------------
        self.tracker: Optional[Any] = None
        self.experiment_name: Optional[str] = None

        # ----------------------------
        # Config & Plugins
        # ----------------------------
        self.config: Dict[str, Any] = {}
        self.plugins: Dict[str, Any] = {}

        # ----------------------------
        # Visualization State
        # ----------------------------
        self._last_figure: Optional[Any] = None

        # ----------------------------
        # Internal Flags
        # ----------------------------
        self._is_fitted: bool = False

    # -------------------------------------------------
    # Validation Helpers
    # -------------------------------------------------

    def ensure_dataframe(self) -> None:
        if self.dataframe is None:
            raise ValueError("No DataFrame loaded in Project.")

    def ensure_target(self) -> None:
        if self.target is None:
            raise ValueError("Target column not defined.")

    def ensure_model(self) -> None:
        if self.model is None:
            raise ValueError("No model trained or injected.")

    # -------------------------------------------------
    # Visualization Methods
    # -------------------------------------------------

    def set_last_figure(self, figure: Any) -> None:
        """
        Store last generated visualization.
        """
        self._last_figure = figure

    def get_last_figure(self) -> Optional[Any]:
        """
        Retrieve last generated visualization.
        """
        return self._last_figure

    # -------------------------------------------------
    # Reset Methods
    # -------------------------------------------------

    def reset_model_state(self) -> None:
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions = None
        self.metrics.clear()
        self._is_fitted = False

    def reset_pipeline(self) -> None:
        self.pipeline_nodes.clear()
        self.pipeline_edges.clear()

    # -------------------------------------------------
    # Status Properties
    # -------------------------------------------------

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    def mark_fitted(self) -> None:
        self._is_fitted = True

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows = len(self.dataframe) if self.dataframe is not None else 0
        return f"<BayaContext rows={rows} target={self.target}>"
