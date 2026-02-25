from __future__ import annotations
from baya.context import Context


def run_pipeline(context: Context) -> None:
    context.pipeline.run()


def show_models(context: Context) -> None:
    print(context.registry.list_models())