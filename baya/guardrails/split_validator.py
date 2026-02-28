def validate_split(test_size: float) -> None:
    if not (0.0 < test_size < 1.0):
        raise ValueError("test_size must be between 0 and 1.")
