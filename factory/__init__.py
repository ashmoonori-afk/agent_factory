"""Agent Factory — Generate AI agent repositories through conversation."""

from __future__ import annotations

from factory.core.generator import ApprovalRequiredError as ApprovalRequiredError
from factory.core.generator import GenerationError as GenerationError
from factory.core.generator import GenerationResult as GenerationResult
from factory.core.generator import SpecValidationError as SpecValidationError
from factory.core.generator import generate as generate
from factory.schemas.validator import validate_spec as validate

__version__ = "1.0.0"

__all__ = [
    "generate",
    "validate",
    "GenerationResult",
    "SpecValidationError",
    "ApprovalRequiredError",
    "GenerationError",
    "__version__",
]
