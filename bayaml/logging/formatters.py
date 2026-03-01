import logging


def default_formatter() -> logging.Formatter:
    return logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
