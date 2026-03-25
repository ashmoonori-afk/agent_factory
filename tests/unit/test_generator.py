"""Unit tests for the generate() orchestrator."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from factory.core.generator import (
    ApprovalRequiredError,
    GenerationError,
    GenerationResult,
    SpecValidationError,
    generate,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

VALID_SPEC: dict[str, object] = {
    "name": "test-bot",
    "description": "A test agent for unit tests",
    "type": "single",
}

VALID_APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "test-bot single-agent",
}


def _run(tmp_path: Path, **overrides: object) -> GenerationResult:
    """Call generate() with sensible defaults; overrides replace individual kwargs."""
    kwargs: dict[str, object] = {
        "spec": VALID_SPEC,
        "output": str(tmp_path / "test-bot"),
        "approval_record": VALID_APPROVAL,
    }
    kwargs.update(overrides)
    return generate(**kwargs)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# GenerationResult dataclass
# ---------------------------------------------------------------------------

def test_generation_result_fields() -> None:
    r = GenerationResult(
        output_path="/tmp/x",
        zip_path="/tmp/x.zip",
        file_count=3,
        files=["/tmp/x/a", "/tmp/x/b", "/tmp/x/c"],
    )
    assert r.output_path == "/tmp/x"
    assert r.zip_path == "/tmp/x.zip"
    assert r.file_count == 3
    assert len(r.files) == 3


# ---------------------------------------------------------------------------
# SpecValidationError
# ---------------------------------------------------------------------------

def test_invalid_spec_raises_spec_validation_error(tmp_path: Path) -> None:
    bad_spec: dict[str, object] = {"name": "My Bot!"}  # missing description, type; bad name
    with pytest.raises(SpecValidationError):
        _run(tmp_path, spec=bad_spec)


def test_spec_validation_error_is_exception() -> None:
    assert issubclass(SpecValidationError, Exception)


# ---------------------------------------------------------------------------
# ApprovalRequiredError
# ---------------------------------------------------------------------------

def test_missing_approval_raises_approval_required_error(tmp_path: Path) -> None:
    bad_approval = {**VALID_APPROVAL, "decision": "REJECTED"}
    with pytest.raises(ApprovalRequiredError):
        _run(tmp_path, approval_record=bad_approval)


def test_empty_approval_dict_raises_approval_required_error(tmp_path: Path) -> None:
    with pytest.raises((ApprovalRequiredError, KeyError)):
        _run(tmp_path, approval_record={})


def test_approval_required_error_is_exception() -> None:
    assert issubclass(ApprovalRequiredError, Exception)


# ---------------------------------------------------------------------------
# Successful generation
# ---------------------------------------------------------------------------

def test_generate_returns_generation_result(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert isinstance(result, GenerationResult)


def test_generate_creates_output_directory(tmp_path: Path) -> None:
    out = tmp_path / "test-bot"
    _run(tmp_path, output=str(out))
    assert out.is_dir()


def test_generate_result_output_path_exists(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert Path(result.output_path).is_dir()


def test_generate_writes_meta_yaml(tmp_path: Path) -> None:
    result = _run(tmp_path)
    meta = Path(result.output_path) / "meta.yaml"
    assert meta.exists()


def test_generate_meta_yaml_contains_name(tmp_path: Path) -> None:
    import yaml

    result = _run(tmp_path)
    meta = Path(result.output_path) / "meta.yaml"
    data = yaml.safe_load(meta.read_text())
    assert data["name"] == "test-bot"


def test_generate_writes_approval_log(tmp_path: Path) -> None:
    result = _run(tmp_path)
    log = Path(result.output_path) / "approval_log.jsonl"
    assert log.exists()


def test_generate_approval_log_is_valid_jsonl(tmp_path: Path) -> None:
    result = _run(tmp_path)
    log = Path(result.output_path) / "approval_log.jsonl"
    for line in log.read_text().splitlines():
        parsed = json.loads(line)
        assert "decision" in parsed
        assert "hash" in parsed


def test_generate_file_count_matches_files_list(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.file_count == len(result.files)


# ---------------------------------------------------------------------------
# ZIP behaviour
# ---------------------------------------------------------------------------

def test_generate_creates_zip_by_default(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.zip_path is not None
    assert Path(result.zip_path).exists()


def test_generate_no_zip_flag_skips_zip(tmp_path: Path) -> None:
    result = _run(tmp_path, no_zip=True)
    assert result.zip_path is None


def test_generate_zip_is_valid_archive(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.zip_path is not None
    assert zipfile.is_zipfile(result.zip_path)


def test_generate_zip_contains_meta_yaml(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert result.zip_path is not None
    with zipfile.ZipFile(result.zip_path) as zf:
        names = zf.namelist()
    assert "meta.yaml" in names


# ---------------------------------------------------------------------------
# Template set selection
# ---------------------------------------------------------------------------

def test_generate_single_agent_uses_single_agent_template_set(tmp_path: Path) -> None:
    """No error when type=single (template dir may be empty in test env)."""
    result = _run(tmp_path, spec={**VALID_SPEC, "type": "single"})
    assert isinstance(result, GenerationResult)


def test_generate_multi_agent_uses_multi_agent_template_set(tmp_path: Path) -> None:
    """No error when type=multi (template dir may be empty in test env)."""
    multi_spec: dict[str, object] = {
        "name": "team-bot",
        "description": "A multi-agent team",
        "type": "multi",
    }
    result = _run(tmp_path, spec=multi_spec)
    assert isinstance(result, GenerationResult)


# ---------------------------------------------------------------------------
# GenerationError
# ---------------------------------------------------------------------------

def test_generation_error_is_exception() -> None:
    assert issubclass(GenerationError, Exception)
