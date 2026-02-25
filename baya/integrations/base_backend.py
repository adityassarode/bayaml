from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class BaseBackend(ABC):
    """
    Strict backend execution contract.

    Rules:
    - Must be stateless.
    - Must not access Context.
    - Must not mutate global state.
    - Must operate only on provided data.
    - Must respect seed for deterministic behavior.
    - Must encapsulate framework-specific behavior.
    """

    # =====================================================
    # Identity
    # =====================================================

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique backend identifier."""
        ...

    # =====================================================
    # Capability Declaration (Required)
    # =====================================================

    @abstractmethod
    def available_models(self) -> List[str]:
        """
        Return supported model names.

        Must be:
        - Deterministic
        - Stable ordering
        - No dynamic mutation
        """
        ...

    # =====================================================
    # Model Lifecycle
    # =====================================================

    @abstractmethod
    def create_model(
        self,
        model_type: str,
        **kwargs: Any,
    ) -> Any:
        """Instantiate model object."""
        ...

    @abstractmethod
    def train(
        self,
        model: Any,
        X_train: Any,
        y_train: Any,
        *,
        seed: Optional[int] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Train model deterministically.

        Requirements:
        - Respect seed if provided
        - Must NOT mutate global RNG
        - Must NOT access Context
        - Must return trained model
        """
        ...

    @abstractmethod
    def predict(
        self,
        model: Any,
        X: Any,
    ) -> Any:
        """
        Generate predictions.

        Must:
        - Not mutate model
        - Not access Context
        """
        ...

    # =====================================================
    # Probability Support (Optional)
    # =====================================================

    def supports_proba(self, model: Any) -> bool:
        """
        Indicates whether probability prediction is supported.

        Must be deterministic.
        """
        return False

    def predict_proba(
        self,
        model: Any,
        X: Any,
    ) -> Any:
        """
        Probability prediction.

        Must be overridden if supported.
        """
        raise NotImplementedError(
            f"Backend '{self.name}' does not support probability prediction."
        )

    # =====================================================
    # Optional Extensions
    # =====================================================

    def evaluate(
        self,
        model: Any,
        X_test: Any,
        y_test: Any,
    ) -> Dict[str, Any]:
        return {}

    def tune(
        self,
        model: Any,
        X_train: Any,
        y_train: Any,
        param_grid: Optional[Dict[str, Any]] = None,
        *,
        seed: Optional[int] = None,
    ) -> Any:
        return model

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:
        return f"<BayaBackend name={self.name}>"