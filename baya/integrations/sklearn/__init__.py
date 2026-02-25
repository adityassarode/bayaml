"""
Sklearn Integration

Automatically registers:
- SklearnBackend
- Default sklearn models

This makes sklearn models available immediately
when Baya is imported.
"""

from __future__ import annotations

# Import backend
from .sklearn_backend import SklearnBackend

# Import central registry
from ..model_registry import ModelRegistry


# -------------------------------------------------
# Instantiate Backend
# -------------------------------------------------

_backend = SklearnBackend()

# Register backend globally
ModelRegistry.register_backend(_backend)


# -------------------------------------------------
# Register Default Sklearn Models
# -------------------------------------------------

# Classification
ModelRegistry.register_model("logistic_regression", "sklearn")
ModelRegistry.register_model("random_forest", "sklearn")
ModelRegistry.register_model("svm", "sklearn")
ModelRegistry.register_model("gradient_boosting", "sklearn")

# Regression
ModelRegistry.register_model("linear_regression", "sklearn")
ModelRegistry.register_model("ridge", "sklearn")
ModelRegistry.register_model("lasso", "sklearn")
ModelRegistry.register_model("random_forest_regressor", "sklearn")

# Clustering
ModelRegistry.register_model("kmeans", "sklearn")
ModelRegistry.register_model("dbscan", "sklearn")

# -------------------------------------------------
# Public Export
# -------------------------------------------------

__all__ = [
    "SklearnBackend",
]
