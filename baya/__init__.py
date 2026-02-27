"""Baya - Structured ML Orchestration Framework."""

from __future__ import annotations

from .project import Project

from .simple import Baya, quick_train


from .version import __version__

__author__ = "Aditya Sarode"
__license__ = "MIT"
__website__ = "https://baya-ml.dev"
__buy_me_a_coffee__ = "https://buymeacoffee.com/adityasarode"


def info(open_website: bool = False) -> None:
    import webbrowser

    print("Baya ML Framework")
    print(f"Version : {__version__}")
    print(f"Author  : {__author__}")
    print(f"Website : {__website__}")
    print(f"Support : {__buy_me_a_coffee__}")
    if open_website:
        webbrowser.open(__website__)



__all__ = ["Project", "Baya", "quick_train", "__version__", "info"]

__all__ = ["Project", "__version__", "info"]

