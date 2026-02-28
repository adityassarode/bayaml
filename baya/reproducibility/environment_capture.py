import platform


def capture_environment() -> dict:
    return {"python": platform.python_version(), "platform": platform.platform()}
