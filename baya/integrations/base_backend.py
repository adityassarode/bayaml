"""
Baya Base Backend

Defines the abstract interface for all ML backends.

Every integration backend must inherit from BaseBackend
and implement the required methods.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseBackend(ABC):
    """
    Abstract base class for ML backends.

    All ML library integrations must implement this interface.
    """

    # -------------------------------------------------
    # Required Properties
    # -------------------------------------------------

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Backend name (e.g., 'sklearn', 'tensorflow').
        """
        pass

    # -------------------------------------------------
    # Model Lifecycle
    # -------------------------------------------------

    @abstractmethod
    def create_model(self, model_type: str, **kwargs) -> Any:
        """
        Create model instance based on model_type.

        Example:
            model_type="random_forest"
        """
        pass

    @abstractmethod
    def train(
        self,
        model: Any,
        X_train: Any,
        y_train: Any,
        **kwargs,
    ) -> Any:
        """
        Train model and return fitted model.
        """
        pass

    @abstractmethod
    def predict(
        self,
        model: Any,
        X: Any,
    ) -> Any:
        """
        Generate predictions.
        """
        pass

    # -------------------------------------------------
    # Optional Capabilities
    # -------------------------------------------------

    def evaluate(
        self,
        model: Any,
        X_test: Any,
        y_test: Any,
    ) -> Dict[str, Any]:
        """
        Optional backend-specific evaluation.
        Default: empty metrics.
        """
        return {}

    def tune(
        self,
        model: Any,
        X_train: Any,
        y_train: Any,
        param_grid: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Optional hyperparameter tuning.
        Default: return original model.
        """
        return model

    # -------------------------------------------------
    # Custom Training Loop
    # -------------------------------------------------

    def train_custom(
        self,
        training_function,
        *args,
        **kwargs,
    ) -> Any:
        """
        Allow user to inject custom training loop.
        """
        return training_function(*args, **kwargs)

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        return f"<BayaBackend name={self.name}>"
