def validate_schema(reference, new) -> None:
    ref_cols = list(reference.columns)
    new_cols = list(new.columns)
    if ref_cols != new_cols:
        raise ValueError("Schema mismatch.")
