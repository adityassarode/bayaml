from __future__ import annotations

from typing import Any, List

from ..base_backend import BaseBackend


class PyTorchBackend(BaseBackend):
    @property
    def name(self) -> str:
        return "pytorch"

    @property
    def version(self) -> str:
        return "stub"

    def available_models(self) -> List[str]:
        return []

    def create_model(self, model_type: str, **kwargs: Any) -> Any:
        raise NotImplementedError("PyTorch backend is a minimal v1 stub.")

    def train(self, model: Any, X_train: Any, y_train: Any, *, seed: int, **kwargs: Any) -> Any:
        raise NotImplementedError("PyTorch backend is a minimal v1 stub.")

    def predict(self, model: Any, X: Any) -> Any:
        raise NotImplementedError("PyTorch backend is a minimal v1 stub.")
