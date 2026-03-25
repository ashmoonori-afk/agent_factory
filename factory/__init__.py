"""Agent Factory — Generate AI agent repositories through conversation."""

from __future__ import annotations

from factory.core.critique import CritiqueResult as CritiqueResult
from factory.core.critique import critique as critique
from factory.core.generator import ApprovalRequiredError as ApprovalRequiredError
from factory.core.generator import GenerationError as GenerationError
from factory.core.generator import GenerationResult as GenerationResult
from factory.core.generator import SpecValidationError as SpecValidationError
from factory.core.generator import generate as generate
from factory.schemas.validator import validate_spec as validate

__version__ = "1.0.0"


def get_builtin_skills() -> list[dict[str, str]]:
    """Return metadata for all built-in skills.

    Each dict contains: id, name, description, policy.
    """
    from factory.registries.loader import RegistryLoader

    loader = RegistryLoader()
    return loader.list_skills()


def get_builtin_personas() -> list[dict[str, str]]:
    """Return metadata for all built-in personas.

    Each dict contains: id, tone, description.
    """
    from factory.registries.loader import RegistryLoader

    loader = RegistryLoader()
    return loader.list_personas()


__all__ = [
    "critique",
    "CritiqueResult",
    "generate",
    "validate",
    "get_builtin_skills",
    "get_builtin_personas",
    "GenerationResult",
    "SpecValidationError",
    "ApprovalRequiredError",
    "GenerationError",
    "__version__",
]
