from pathlib import Path
import pickle
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Baya Model Service")
MODEL_PATH = Path(r"model.pkl")


class PredictRequest(BaseModel):
    features: list[list[float]]


def _load_model() -> Any:
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model artifact not found: {MODEL_PATH}")
    with MODEL_PATH.open("rb") as f:
        return pickle.load(f)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: PredictRequest) -> dict[str, list[float]]:
    try:
        model = _load_model()
        data = np.asarray(payload.features, dtype=float)
        preds = model.predict(data)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"predictions": np.asarray(preds).tolist()}
