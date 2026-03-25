"""Golden-file tests: compare generated output against stored reference fixtures.

These tests detect unintended template changes. If a template is changed
intentionally, run ``tests/fixtures/regenerate_fixtures.py`` to update the
reference files.
"""

from __future__ import annotations

import difflib
import tempfile
from pathlib import Path

import pytest

import factory

from .conftest import FIXTURE_DIR

# ---------------------------------------------------------------------------
# Deterministic spec constants
# ---------------------------------------------------------------------------

SINGLE_SPEC: dict[str, object] = {
    "name": "fixture-single-agent",
    "description": "Golden file fixture for single agent",
    "type": "single",
    "skills": ["csv-reader"],
    "persona": {"tone": "professional", "language": "en"},
    "policies": {
        "deny": ["delete_file", "send_email"],
        "ask": ["execute_sql"],
        "allow": ["*"],
    },
}

MULTI_SPEC: dict[str, object] = {
    "name": "fixture-multi-agent",
    "description": "Golden file fixture for multi agent",
    "type": "multi",
    "agents": [
        {"id": "reviewer", "role": "reviews code", "next": ["fixer"]},
        {"id": "fixer", "role": "fixes issues"},
    ],
    "topology": {"entry": "reviewer", "max_loops": 2},
    "skills": ["code-reviewer"],
    "persona": {"tone": "technical", "language": "en"},
}

APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-01-01T00:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "fixture generation",
}

# Files that are excluded from exact byte-for-byte comparison because they
# contain non-deterministic data (timestamps, etc.).
SKIP_EXACT: frozenset[str] = frozenset(
    {
        "meta.yaml",
        "approval_log.jsonl",
        "policies/approval_log.jsonl",
    }
)

# ---------------------------------------------------------------------------
# Key files to test for each agent type
# ---------------------------------------------------------------------------

SINGLE_EXACT_FILES = [
    "CLAUDE.md",
    "CODEX.md",
    "AGENTS.md",
    "README.md",
    "agent_spec.yaml",
    ".env.example",
    "policies/policy.yaml",
    "docs/architecture.md",
    "docs/policy.md",
    "docs/reading_order.md",
    "skills/csv-reader.md",
    "personas/default.yaml",
]

MULTI_EXACT_FILES = [
    "CLAUDE.md",
    "CODEX.md",
    "AGENTS.md",
    "README.md",
    "agent_spec.yaml",
    "orchestrator.md",
    "agents/agent_role.md",
    "architecture/topology.yaml",
    "policies/policy.yaml",
    "docs/architecture.md",
    "docs/policy.md",
    "docs/reading_order.md",
    "skills/code-reviewer.md",
    "personas/default.yaml",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _assert_files_match(generated_dir: Path, fixture_dir: Path, rel_path: str) -> None:
    """Compare a generated file against the stored fixture reference."""
    generated = generated_dir / rel_path
    fixture = fixture_dir / rel_path

    assert fixture.exists(), (
        f"Fixture file missing: {fixture}. "
        "Run tests/fixtures/regenerate_fixtures.py to create it."
    )
    assert generated.exists(), f"Generated file missing: {generated}"

    generated_text = generated.read_text(encoding="utf-8")
    fixture_text = fixture.read_text(encoding="utf-8")

    if generated_text != fixture_text:
        diff = "".join(
            difflib.unified_diff(
                fixture_text.splitlines(keepends=True),
                generated_text.splitlines(keepends=True),
                fromfile=f"fixture/{rel_path}",
                tofile=f"generated/{rel_path}",
            )
        )
        pytest.fail(
            f"Golden file mismatch for '{rel_path}'.\n"
            "If this change is intentional, run tests/fixtures/regenerate_fixtures.py.\n\n"
            f"Diff (fixture → generated):\n{diff}"
        )


# ---------------------------------------------------------------------------
# Fixtures (pytest)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def single_agent_dir() -> Path:
    """Generate a fresh single-agent output and return its directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "single_agent"
        factory.generate(
            spec=SINGLE_SPEC,
            output=str(out),
            approval_record=APPROVAL,
            no_zip=True,
        )
        yield out


@pytest.fixture(scope="module")
def multi_agent_dir() -> Path:
    """Generate a fresh multi-agent output and return its directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "multi_agent"
        factory.generate(
            spec=MULTI_SPEC,
            output=str(out),
            approval_record=APPROVAL,
            no_zip=True,
        )
        yield out


# ---------------------------------------------------------------------------
# Single-agent golden-file tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rel_path", SINGLE_EXACT_FILES)
def test_single_agent_golden_file(single_agent_dir: Path, rel_path: str) -> None:
    """Each key single-agent file must match the stored fixture exactly."""
    _assert_files_match(single_agent_dir, FIXTURE_DIR / "single_agent", rel_path)


def test_single_agent_timestamp_files_exist(single_agent_dir: Path) -> None:
    """Non-deterministic files should exist but are not compared byte-for-byte."""
    assert (single_agent_dir / "meta.yaml").exists()
    assert (single_agent_dir / "policies" / "approval_log.jsonl").exists()


# ---------------------------------------------------------------------------
# Multi-agent golden-file tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rel_path", MULTI_EXACT_FILES)
def test_multi_agent_golden_file(multi_agent_dir: Path, rel_path: str) -> None:
    """Each key multi-agent file must match the stored fixture exactly."""
    _assert_files_match(multi_agent_dir, FIXTURE_DIR / "multi_agent", rel_path)


def test_multi_agent_timestamp_files_exist(multi_agent_dir: Path) -> None:
    """Non-deterministic files should exist but are not compared byte-for-byte."""
    assert (multi_agent_dir / "meta.yaml").exists()
    assert (multi_agent_dir / "policies" / "approval_log.jsonl").exists()
