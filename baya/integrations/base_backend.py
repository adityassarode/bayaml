# baya/integrations/base_backend.py

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseBackend(ABC):
    """Abstract ML backend interface"""

    # ---------------------------
    # Identity
    # ---------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique backend name"""
        raise NotImplementedError

    # ---------------------------
    # Model lifecycle
    # ---------------------------

    @abstractmethod
    def create_model(self, model_name: str, **kwargs: Any) -> Any:
        """Instantiate model (NOT train)"""
        raise NotImplementedError

    @abstractmethod
    def train(self, model: Any, X: Any, y: Any, **kwargs: Any) -> Any:
        """Fit model"""
        raise NotImplementedError

    @abstractmethod
    def predict(self, model: Any, X: Any) -> Any:
        """Generate predictions"""
        raise NotImplementedError

    # ---------------------------
    # Optional
    # ---------------------------

    def evaluate(self, model: Any, X: Any, y: Any) -> Dict[str, Any]:
        return {}

    def tune(self, model: Any, X: Any, y: Any, param_grid: Optional[Dict[str, Any]] = None) -> Any:
        return model

    def __repr__(self) -> str:
        return f"<BayaBackend name={self.name}>"