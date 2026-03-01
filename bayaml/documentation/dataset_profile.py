def dataset_profile(df) -> dict:
    return {"rows": int(len(df)), "columns": int(len(df.columns))}
