from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from baya import __author__, __version__, info
from baya.cli.commands import (
    run_automl_from_config,
    run_from_config,
    show_leaderboard,
    visualize_leaderboard,
)
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
    parser = argparse.ArgumentParser(
        prog="baya", description="Baya production-grade ML framework"
    )
    parser.add_argument("--banner", action="store_true", help="Print framework banner")

    sub = parser.add_subparsers(dest="command")

    run_cmd = sub.add_parser("run", help="Run training/evaluation from config")
    run_cmd.add_argument("config", type=str)

    automl_cmd = sub.add_parser("automl", help="Run AutoML from workflow config")
    automl_cmd.add_argument("config", type=str)

    sub.add_parser("leaderboard", help="Print latest leaderboard entries")

    viz_cmd = sub.add_parser("visualize", help="Visualization commands")
    viz_cmd.add_argument("target", choices=["leaderboard"])

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

    if args.command == "automl":
        result = run_automl_from_config(Path(args.config))
        print(
            f"AutoML completed. run_id={result['run_id']} "
            f"best_model={result['best_model']} score={result['best_score']:.4f}"
        )
        return

    if args.command == "leaderboard":
        board = show_leaderboard()
        if not board:
            print("No leaderboard runs found.")
        else:
            latest = board[-1]
            for row in latest.get("leaderboard", []):
                print(f"{row['model']}: {row['score']:.4f}")
        return

    if args.command == "visualize":
        if args.target == "leaderboard":
            visualize_leaderboard()
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
