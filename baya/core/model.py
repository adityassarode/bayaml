from __future__ import annotations
from typing import Any

from ..context import Context
from ..integrations.model_registry import ModelRegistry


class ModelModule:
    """Model lifecycle controller — NO ML logic here."""

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # CREATE (ATTACH ONLY — NO TRAINING)
    # -------------------------------------------------
    def create(self, name: str, *, target: str) -> Any:
        """
        Resolve model and attach to context.
        Deterministic — does NOT train.
        """

        # Guardrail 1 — dataset must exist
        self.context.ensure_dataframe()

        df = self.context.dataframe
        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found")

        # Guardrail 2 — set target BEFORE split
        self.context.target = target

        # Resolve backend
        backend, model_key = ModelRegistry.resolve(name)

        # Instantiate model
        model = backend.create_model(model_key)

        # Attach to context
        self.context.model = model
        self.context.backend = backend

        return model

    def __repr__(self) -> str:
        if self.context.model is None:
            return "<ModelModule model=None>"
        return f"<ModelModule model={self.context.model.__class__.__name__}>"