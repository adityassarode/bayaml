"""
JSON Exporter

Exports:
- DataFrame to JSON
- Dictionary / metrics to JSON
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from pathlib import Path
import json

import pandas as pd

from ..context import Context


class JSONExporter:
    """
    Handles exporting data to JSON format.
    """

    def __init__(self, context: Context) -> None:
        self.context = context

    # -------------------------------------------------
    # Export DataFrame
    # -------------------------------------------------

    def toJSON(
        self,
        path: str,
        orient: str = "records",
        indent: Optional[int] = 4,
    ) -> "JSONExporter":
        """
        Export current DataFrame to JSON.

        Parameters:
        - path: output file path
        - orient: pandas JSON orientation
            "records", "split", "index", "columns", "values", "table"
        - indent: pretty print indentation
        """
        self.context.ensure_dataframe()

        df: pd.DataFrame = self.context.dataframe

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        json_data = df.to_json(orient=orient)

        # Pretty formatting
        if indent is not None:
            parsed = json.loads(json_data)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=indent)
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_data)

        return self

    # -------------------------------------------------
    # Export Dictionary / Metrics
    # -------------------------------------------------

    def exportDict(
        self,
        data: Dict[str, Any],
        path: str,
        indent: int = 4,
    ) -> "JSONExporter":
        """
        Export dictionary (metrics, config, experiment results).
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)

        return self

    # -------------------------------------------------
    # Representation
    # -------------------------------------------------

    def __repr__(self) -> str:
        rows, cols = (0, 0)
        if self.context.dataframe is not None:
            rows, cols = self.context.dataframe.shape
        return f"<JSONExporter rows={rows} cols={cols}>"
