from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from baya import __author__, __version__, info
from baya.cli.commands import run_from_config
from baya.integrations import bootstrap_integrations
from baya.integrations.model_registry import ModelRegistry


def banner() -> str:
    return (
        "Baya ML Framework\n"
        f"Version : {__version__}\n"
        f"Author  : {__author__}\n"
        "Website : https://baya-ml.dev"
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="baya", description="Baya production-grade ML framework")
    parser.add_argument("--banner", action="store_true", help="Print framework banner")

    sub = parser.add_subparsers(dest="command")

    run_cmd = sub.add_parser("run", help="Run training/evaluation from config")
    run_cmd.add_argument("config", type=str)

    reg_cmd = sub.add_parser("registry", help="Registry operations")
    reg_cmd.add_argument("action", choices=["list-models", "list-backends"])

    info_cmd = sub.add_parser("info", help="Show framework metadata")
    info_cmd.add_argument("--open-website", action="store_true")

    args = parser.parse_args()

    if args.banner:
        print(banner())

    if args.command == "run":
        project = run_from_config(Path(args.config))
        print(f"Run completed. Tracker run_id={project.tracker.run_id}")
        return

    if args.command == "registry":
        bootstrap_integrations()
        if args.action == "list-models":
            print("\n".join(ModelRegistry.list_models()))
        else:
            print("\n".join(ModelRegistry.list_backends()))
        return

    if args.command == "info":
        info(open_website=bool(args.open_website))
        if args.open_website:
            webbrowser.open("https://baya-ml.dev")
        return

    if args.command is None:
        parser.print_help()
