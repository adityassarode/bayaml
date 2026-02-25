from __future__ import annotations

from typing import Any, Dict, Optional

import tensorflow as tf
import numpy as np
import random

from baya.integrations.base_backend import BaseBackend
from baya.context import Context
from baya.guardrails.split_validator import validate_split
from baya.reproducibility.snapshot import freeze_config


class TensorFlowBackend(BaseBackend):
    """
    TensorFlow execution backend.

    Responsibilities:
    - Model instantiation
    - Deterministic training
    - Prediction
    """

    # -----------------------------
    # Required Property
    # -----------------------------

    @property
    def name(self) -> str:
        return "tensorflow"

    # -----------------------------
    # Model Creation
    # -----------------------------

    def create_model(
        self,
        model_type: str,
        **kwargs,
    ) -> Any:
        """
        Create TensorFlow model instance.
        """

        if model_type == "sequential":
            return tf.keras.Sequential(**kwargs)

        raise ValueError(
            f"Unsupported TensorFlow model_type '{model_type}'."
        )

    # -----------------------------
    # Training
    # -----------------------------

    def train(
        self,
        context: Context,
        model: Any,
        X_train: Any,
        y_train: Any,
        **kwargs,
    ) -> Any:
        """
        Train TensorFlow model deterministically.
        """

        # -----------------------------
        # Guardrails
        # -----------------------------
        validate_split(context)

        # -----------------------------
        # Reproducibility
        # -----------------------------
        seed: int = context.reproducibility.seed

        tf.random.set_seed(seed)
        np.random.seed(seed)
        random.seed(seed)

        # Freeze configuration snapshot
        freeze_config(context)

        # -----------------------------
        # Train
        # -----------------------------
        model.fit(
            X_train,
            y_train,
            **kwargs,
        )

        return model

    # -----------------------------
    # Prediction
    # -----------------------------

    def predict(
        self,
        context: Context,
        model: Any,
        X: Any,
    ) -> Any:
        """
        Generate predictions.
        """

        return model.predict(X)