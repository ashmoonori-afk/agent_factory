# tests/unit/test_public_api.py
"""Smoke-tests that the public factory namespace exports are correct."""

from __future__ import annotations


def test_generate_importable_from_factory() -> None:
    from factory import generate  # noqa: F401


def test_validate_importable_from_factory() -> None:
    from factory import validate  # noqa: F401


def test_generation_result_importable_from_factory() -> None:
    from factory import GenerationResult  # noqa: F401


def test_spec_validation_error_importable_from_factory() -> None:
    from factory import SpecValidationError  # noqa: F401


def test_approval_required_error_importable_from_factory() -> None:
    from factory import ApprovalRequiredError  # noqa: F401


def test_generation_error_importable_from_factory() -> None:
    from factory import GenerationError  # noqa: F401


def test_version_present() -> None:
    import factory

    assert factory.__version__ == "1.0.0"


def test_generate_is_callable() -> None:
    import factory

    assert callable(factory.generate)


def test_validate_is_callable() -> None:
    import factory

    assert callable(factory.validate)
