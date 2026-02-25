"""
Baya Core Modules

This package contains the primary data science operations:

- Data loading & inspection
- Cleaning
- Encoding
- Scaling
- Splitting
- Modeling
- Evaluation
- Transformations

Core modules operate on the shared Context object.
"""

from __future__ import annotations

from .data import DataModule
from .clean import CleanModule
from .encode import EncodeModule
from .scale import ScaleModule
from .split import SplitModule
from .model import ModelModule
from .evaluate import EvaluateModule
from .transform import TransformModule

__all__ = [
    "DataModule",
    "CleanModule",
    "EncodeModule",
    "ScaleModule",
    "SplitModule",
    "ModelModule",
    "EvaluateModule",
    "TransformModule",
]
