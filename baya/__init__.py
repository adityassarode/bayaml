"""Baya - Structured ML Orchestration Framework."""

from __future__ import annotations

from .automl import baya
from .project import Project
from .registry import list_models, register_model
from .simple import Baya, quick_train
from .version import __version__

__author__ = "Aditya Sarode"
__license__ = "MIT"
__GitHub__ = "https://github.com/adityassarode"
__buy_me_a_coffee__ = "https://buymeacoffee.com/adityassarode"
__Repository__ = "https://github.com/adityassarode/baya"
__Issues__ = "https://github.com/adityassarode/baya/issues"
__Instagram__ = "https://www.instagram.com/adityassarode"
__Ko_fi__ = "https://ko-fi.com/adityassarode"


def info(open_website: bool = False) -> None:
    import webbrowser

    print("Baya ML Framework")
    print(f"Version : {__version__}")
    print(f"Author  : {__author__}")
    print(f"GitHub  : {__GitHub__}")
    print(f"Repository : {__Repository__}")
    print(f"Issues : {__Issues__}")
    print(f"Instagram : {__Instagram__}")
    print(f"Buymeacoffee : {__buy_me_a_coffee__}")
    print(f"Ko-fi : {__Ko_fi__}")
    print("Built with ❤️ by Aditya Sarode")
    if open_website:
        webbrowser.open(__GitHub__)


__all__ = ["Project", "Baya", "quick_train", "baya", "register_model", "list_models", "__version__", "info"]
