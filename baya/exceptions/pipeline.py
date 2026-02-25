from __future__ import annotations
from .core import BayaError


class PipelineError(BayaError):
    """General pipeline execution failure."""


class StepExecutionError(PipelineError):
    """Raised when a pipeline step fails."""


class DependencyResolutionError(PipelineError):
    """Raised when DAG resolution fails."""


class GuardrailViolation(PipelineError):
    """Raised when guardrails block execution."""