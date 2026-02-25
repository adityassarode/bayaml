from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .handlers import create_console_handler, create_file_handler


def create_logger(
    name: str,
    *,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    propagate: bool = False,
) -> logging.Logger:
    """
    Create an isolated deterministic logger.

    This function NEVER returns a global shared logger.
    Each call produces an independently configured logger.
    """

    logger = logging.getLogger(name)

    # prevent duplicate handlers if recreated in same process
    logger.handlers.clear()

    logger.setLevel(level)
    logger.propagate = propagate

    # console handler
    logger.addHandler(create_console_handler(level))

    # optional file handler
    if log_file is not None:
        logger.addHandler(create_file_handler(log_file, level))

    return logger