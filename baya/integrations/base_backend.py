from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List


class BaseBackend(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        ...

    @abstractmethod
    def available_models(self) -> List[str]:
        ...

    @abstractmethod
    def create_model(self, model_type: str, **kwargs: Any) -> Any:
        ...

    @abstractmethod
    def train(self, model: Any, X_train: Any, y_train: Any, *, seed: int, **kwargs: Any) -> Any:
        ...

    @abstractmethod
    def predict(self, model: Any, X: Any) -> Any:
        ...

    def supports_proba(self, model: Any) -> bool:
        return hasattr(model, "predict_proba")

    def predict_proba(self, model: Any, X: Any) -> Any:
        if not self.supports_proba(model):
            raise RuntimeError(f"Backend '{self.name}' does not support predict_proba.")
        return model.predict_proba(X)
