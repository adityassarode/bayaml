from .model_registry import ModelRegistry
from .sklearn_backend import SklearnBackend

# default backend
ModelRegistry.register_backend(SklearnBackend())

# register models
for m in [
    "linear_regression",
    "logistic_regression",
    "random_forest_classifier",
    "random_forest_regressor",
    "svm_classifier",
    "svm_regressor",
]:
    ModelRegistry.register_model(m, "sklearn")