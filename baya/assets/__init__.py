from __future__ import annotations

from importlib.resources import files
from pathlib import Path


def get_default_config_path() -> Path:
    return Path(str(files(__package__).joinpath("default_config.yaml")))


def get_default_logging_path() -> Path:
    return Path(str(files(__package__).joinpath("default_logging.yaml")))
