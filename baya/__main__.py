"""
Baya - CLI Entry Point

Allows execution using:

    python -m baya

or

    baya   (if installed via PyPI)
"""

from __future__ import annotations

import sys

from .version import __version__


def main() -> None:
    """
    Entry point for Baya CLI.
    Delegates execution to CLI layer.
    """
    try:
        from .cli.main import main as cli_main
        cli_main()
    except Exception as exc:
        print("Baya CLI failed to start.")
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
