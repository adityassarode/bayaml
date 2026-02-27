from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List


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
    - Must not retain model references internally.
    """

    # =====================================================
    # Identity
    # =====================================================

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique backend identifier."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Backend implementation version.

        Required for reproducibility and registry hashing.
        Must be stable.
        """
        ...

    # =====================================================
    # Capability Declaration
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
        """
        Instantiate model object.

        Must not mutate global state.
        """
        ...

    @abstractmethod
    def train(
        self,
        model: Any,
        X_train: Any,
        y_train: Any,
        *,
        seed: int,
        **kwargs: Any,
    ) -> Any:
        """
        Train model deterministically.

        Requirements:
        - Must respect provided seed.
        - Must NOT mutate global RNG.
        - Must NOT access Context.
        - Must NOT store model internally.
        - Must return trained model.
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
        - Be deterministic given identical inputs
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
    # Representation
    # =====================================================

    def __repr__(self) -> str:
        return f"<BayaBackend name={self.name} version={self.version}>"