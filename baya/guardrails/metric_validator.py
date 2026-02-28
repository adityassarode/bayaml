def validate_metrics(metrics: dict) -> dict:
    out = {}
    for k, v in metrics.items():
        out[str(k)] = float(v) if isinstance(v, (int, float)) else v
    return out
