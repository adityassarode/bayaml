from __future__ import annotations

from typing import Any, Dict, Optional, Callable

import torch
import torch.nn as nn
import torch.optim as optim

from ..base_backend import BaseBackend


class PyTorchBackend(BaseBackend):
    """
    Baya PyTorch Backend

    Responsibilities:
    - Model creation registry
    - Deterministic training
    - Prediction interface
    - Device safe execution
    """

    # -------------------------------------------------
    # Backend Identity
    # -------------------------------------------------

    @property
    def name(self) -> str:
        return "pytorch"

    # -------------------------------------------------
    # Internal Utilities
    # -------------------------------------------------

    def _set_seed(self, seed: int = 42) -> None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def _to_tensor(self, x: Any) -> torch.Tensor:
        if isinstance(x, torch.Tensor):
            return x.clone().detach()
        return torch.tensor(x, dtype=torch.float32)

    # -------------------------------------------------
    # Model Creation
    # -------------------------------------------------

    def create_model(self, model_type: str, **kwargs) -> nn.Module:
        """
        User supplies builder function OR simple linear model
        """

        if model_type == "linear_regression":
            input_dim = kwargs.get("input_dim")
            if input_dim is None:
                raise ValueError("linear_regression requires input_dim")

            return nn.Linear(input_dim, 1)

        if model_type == "custom":
            builder: Optional[Callable[[], nn.Module]] = kwargs.get("builder")
            if builder is None:
                raise ValueError("custom model requires builder callable")
            return builder()

        raise ValueError(f"Unsupported PyTorch model_type '{model_type}'")

    # -------------------------------------------------
    # Training
    # -------------------------------------------------

    def train(
        self,
        model: nn.Module,
        X_train: Any,
        y_train: Any,
        **kwargs,
    ) -> nn.Module:

        self._set_seed(kwargs.get("seed", 42))

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)

        X = self._to_tensor(X_train).to(device)
        y = self._to_tensor(y_train).view(-1, 1).to(device)

        epochs: int = kwargs.get("epochs", 100)
        lr: float = kwargs.get("lr", 1e-3)

        optimizer = optim.Adam(model.parameters(), lr=lr)
        criterion = nn.MSELoss()

        model.train()

        for _ in range(epochs):
            optimizer.zero_grad()
            pred = model(X)
            loss = criterion(pred, y)
            loss.backward()
            optimizer.step()

        return model

    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------

    def predict(
        self,
        model: nn.Module,
        X: Any,
    ) -> Any:

        device = next(model.parameters()).device
        X_tensor = self._to_tensor(X).to(device)

        model.eval()
        with torch.no_grad():
            preds = model(X_tensor)

        return preds.cpu().numpy()

    # -------------------------------------------------
    # Evaluation (Optional)
    # -------------------------------------------------

    def evaluate(
        self,
        model: nn.Module,
        X_test: Any,
        y_test: Any,
    ) -> Dict[str, Any]:

        import numpy as np

        preds = self.predict(model, X_test)
        y_true = self._to_tensor(y_test).numpy()

        mse = float(np.mean((preds - y_true) ** 2))

        return {"mse": mse}