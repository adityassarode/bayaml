"""Baya - Structured ML Orchestration Framework."""

from __future__ import annotations

from .automl import bayaml
from .project import Project
from .registry import list_models, register_model
from .simple import Bayaml, quick_train
from .version import __version__

__author__ = "Aditya Sarode"
__license__ = "MIT"
__GitHub__ = "https://github.com/adityassarode"
__buy_me_a_coffee__ = "https://buymeacoffee.com/adityassarode"
__Repository__ = "https://github.com/adityassarode/bayaml"
__Issues__ = "https://github.com/adityassarode/bayaml/issues"
__Instagram__ = "https://www.instagram.com/adityassarode"
__Ko_fi__ = "https://ko-fi.com/adityassarode"


def info(open_website: bool = False) -> None:
    import webbrowser

    print("""
============================================================
                BAYAML v0.1.5
        ML & AI Orchestration Framework
============================================================

Bayaml is a lightweight ML & AI orchestration framework
designed for structured, reproducible, and deployable
machine learning workflows.

It features a deterministic execution engine and an
intelligent Auto Mode (.auto()) that interprets structured
instructions using rule-based NLP — without external AI
services — ensuring your data remains completely local
and secure.

Auto Mode automatically manages:
  • Data loading
  • Safe preprocessing
  • Task detection (classification/regression)
  • Structured pipeline construction
  • Model training
  • Evaluation
  • Deployment

Built-in AutoML features include:
  • Model comparison
  • Cross-validation
  • Leaderboard tracking
  • Best-model selection

All executed within reproducible, hash-based execution plans.

Structured APIs available:
  • Simple API
  • Fluent API
  • Advanced Orchestration API

Export Options:
  • REST deployment
  • ONNX export

------------------------------------------------------------

""")
    print(f"Version : {__version__}")
    print(f"Author  : {__author__}")
    print(f"GitHub  : {__GitHub__}")
    print(f"Repository : {__Repository__}")
    print(f"Issues : {__Issues__}")
    print(f"Instagram : {__Instagram__}")
    print(f"Buymeacoffee : {__buy_me_a_coffee__}")
    print(f"Ko-fi : {__Ko_fi__}")
    print("""
------------------------------------------------------------

Built with ❤️ by Aditya Sarode
============================================================""")
    if open_website:
        webbrowser.open(__GitHub__)


__all__ = ["Project", "Bayaml", "quick_train", "bayaml", "register_model", "list_models", "__version__", "info"]
