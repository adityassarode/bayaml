from __future__ import annotations

import argparse
from pathlib import Path

from baya.config import load_config, validate_config
from baya.context import Context
from baya.orchestration.pipeline import Pipeline


def app() -> None:
    parser = argparse.ArgumentParser(prog="baya")
    parser.add_argument("config", type=str, help="Path to config file")

    args = parser.parse_args()

    config_path = Path(args.config)

    raw = load_config(config_path)
    validated = validate_config(raw)

    context = Context(config=validated)

    pipeline = Pipeline(context)
    pipeline.run()