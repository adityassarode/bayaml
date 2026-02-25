"""
Static validation layer.

Used before pipeline execution.
"""

from .data_validator import validate_dataframe
from .schema_validator import validate_column_types

__all__ = [
    "validate_dataframe",
    "validate_column_types",
]