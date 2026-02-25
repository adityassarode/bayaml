from __future__ import annotations
import pandas as pd
from .split_validator import validate_split
from .schema_guard import validate_schema
from .leakage_detector import detect_leakage


def enforce_best_practices(
    train: pd.DataFrame,
    test: pd.DataFrame,
    target: str,
    reference_schema: pd.DataFrame | None = None
) -> None:
    validate_split(train, test, target)
    detect_leakage(train, target)

    if reference_schema is not None:
        validate_schema(reference_schema, test)