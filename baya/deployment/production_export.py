from __future__ import annotations

import pickle
from pathlib import Path

from ..context import Context
from .fastapi_generator import generate_fastapi_app


def export_production_bundle(context: Context, output_dir: str) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    model = context.get_model()
    if model is None or not context.is_fitted:
        raise RuntimeError("Train a model before exporting a deployment bundle.")

    model_path = out / "model.pkl"
    with model_path.open("wb") as handle:
        pickle.dump(model, handle)

    app_path = out / "app.py"
    app_path.write_text(generate_fastapi_app("model.pkl"), encoding="utf-8")

    requirements = "\n".join(["fastapi", "uvicorn", "numpy", "scikit-learn"]) + "\n"
    (out / "requirements.txt").write_text(requirements, encoding="utf-8")

    readme = """Baya deployment bundle\n\nRun:\n  pip install -r requirements.txt\n  uvicorn app:app --host 0.0.0.0 --port 8000\n"""
    (out / "README.txt").write_text(readme, encoding="utf-8")
    return out
