from __future__ import annotations

from pathlib import Path
from typing import Any

from ..context import Context


class ONNXExporter:
    def __init__(self, context: Context) -> None:
        self._ctx = context

    def to_onnx(self, path: str) -> Path:
        model = self._ctx.get_model()
        if model is None or not self._ctx.is_fitted:
            raise RuntimeError("Train a model before exporting ONNX.")

        try:
            from skl2onnx import convert_sklearn
            from skl2onnx.common.data_types import FloatTensorType
        except Exception as exc:  # pragma: no cover - depends on optional dependency.
            raise RuntimeError(
                "ONNX export requires optional dependencies 'skl2onnx' and 'onnx'."
            ) from exc

        X_train, _, _, _ = self._ctx.get_split_data()
        n_features = int(X_train.shape[1])

        initial_type: list[tuple[str, Any]] = [("input", FloatTensorType([None, n_features]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)

        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(onnx_model.SerializeToString())
        return out
