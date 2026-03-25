"""End-to-end smoke tests for factory.generate().

These tests call the real generate() pipeline (no mocking) and verify that
all expected artefacts are produced correctly for both single-agent and
multi-agent specs.
"""

from __future__ import annotations

import json
import time
import zipfile
from pathlib import Path

import yaml

import factory

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

SINGLE_SPEC: dict[str, object] = {
    "name": "data-analysis-bot",
    "description": "Analyze CSV files and generate summary reports",
    "type": "single",
    "skills": ["sql-executor", "csv-reader"],
    "persona": {"tone": "professional", "language": "en"},
    "policies": {
        "deny": ["send_email", "delete_file", "deploy"],
        "ask": ["execute_sql"],
        "allow": ["*"],
    },
}

MULTI_SPEC: dict[str, object] = {
    "name": "code-review-team",
    "description": "A team of agents that reviews and improves code",
    "type": "multi",
    "agents": [
        {"id": "reviewer", "role": "reviews code for issues", "next": ["fixer"]},
        {"id": "fixer", "role": "applies suggested fixes"},
    ],
    "topology": {"entry": "reviewer", "max_loops": 2},
    "skills": ["code-reviewer", "code-generator"],
    "persona": {"tone": "technical", "language": "en"},
}

VALID_APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "smoke test approval",
}


# ---------------------------------------------------------------------------
# Single-agent smoke tests
# ---------------------------------------------------------------------------


class TestSingleAgentGeneration:
    """Full end-to-end generation of a single-agent repo."""

    def test_generate_succeeds(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        assert isinstance(result, factory.GenerationResult)

    def test_all_expected_files_created(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        out = Path(result.output_path)
        expected = [
            "CLAUDE.md",
            "CODEX.md",
            "README.md",
            "agent_spec.yaml",
            ".env.example",
            "meta.yaml",
            "approval_log.jsonl",
            "policies/policy.yaml",
            "policies/approval_log.jsonl",
            "docs/architecture.md",
            "docs/policy.md",
            "docs/reading_order.md",
            "tests/test-agent.md",
            "tests/test-policy.md",
            "skills/sql-executor.md",
            "skills/csv-reader.md",
            "personas/default.yaml",
        ]
        for fname in expected:
            assert (out / fname).exists(), f"Missing file: {fname}"

    def test_file_count_matches(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        assert result.file_count == len(result.files)
        assert result.file_count >= 17  # standard + shared + skills + persona

    def test_zip_created_and_valid(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        assert result.zip_path is not None
        assert Path(result.zip_path).exists()
        assert zipfile.is_zipfile(result.zip_path)

    def test_zip_contains_all_files(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        assert result.zip_path is not None
        with zipfile.ZipFile(result.zip_path) as zf:
            names = set(zf.namelist())
        assert "CLAUDE.md" in names
        assert "CODEX.md" in names
        assert "meta.yaml" in names
        assert "approval_log.jsonl" in names
        assert "policies/policy.yaml" in names
        assert "docs/architecture.md" in names

    def test_meta_yaml_correct_version(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        meta_path = Path(result.output_path) / "meta.yaml"
        meta = yaml.safe_load(meta_path.read_text())
        assert meta["factory_version"] == "1.0.0"
        assert meta["template_version"] == "1.0.1"
        assert meta["name"] == "data-analysis-bot"
        assert meta["type"] == "single"
        assert "generated_at" in meta
        assert "approval_hash" in meta

    def test_approval_log_has_hash(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        log_path = Path(result.output_path) / "approval_log.jsonl"
        lines = log_path.read_text().strip().splitlines()
        assert len(lines) >= 1
        entry = json.loads(lines[0])
        assert "hash" in entry
        assert len(entry["hash"]) == 64  # SHA-256 hex
        assert entry["decision"] == "APPROVED"

    def test_claude_md_not_empty(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        claude_md = Path(result.output_path) / "CLAUDE.md"
        content = claude_md.read_text()
        assert len(content) > 50  # non-trivial content

    def test_agent_spec_yaml_exists_and_nonempty(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "data-analysis-bot"),
            approval_record=VALID_APPROVAL,
        )
        spec_path = Path(result.output_path) / "agent_spec.yaml"
        content = spec_path.read_text()
        assert len(content) > 20  # non-trivial content
        assert "data-analysis-bot" in content


# ---------------------------------------------------------------------------
# Multi-agent smoke tests
# ---------------------------------------------------------------------------


class TestMultiAgentGeneration:
    """Full end-to-end generation of a multi-agent repo."""

    def test_generate_succeeds(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "code-review-team"),
            approval_record=VALID_APPROVAL,
        )
        assert isinstance(result, factory.GenerationResult)

    def test_all_expected_files_created(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "code-review-team"),
            approval_record=VALID_APPROVAL,
        )
        out = Path(result.output_path)
        expected = [
            "CLAUDE.md",
            "CODEX.md",
            "README.md",
            "agent_spec.yaml",
            "meta.yaml",
            "approval_log.jsonl",
            "orchestrator.md",
            "agents/agent_role.md",
            "architecture/topology.yaml",
            "policies/policy.yaml",
            "policies/approval_log.jsonl",
            "docs/architecture.md",
            "docs/policy.md",
            "docs/reading_order.md",
            "tests/test-agent.md",
            "tests/test-policy.md",
            "skills/code-reviewer.md",
            "skills/code-generator.md",
            "personas/default.yaml",
        ]
        for fname in expected:
            assert (out / fname).exists(), f"Missing file: {fname}"

    def test_file_count_matches(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "code-review-team"),
            approval_record=VALID_APPROVAL,
        )
        assert result.file_count == len(result.files)
        assert result.file_count >= 19  # standard + shared + skills + persona

    def test_zip_created_and_contains_multi_agent_files(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "code-review-team"),
            approval_record=VALID_APPROVAL,
        )
        assert result.zip_path is not None
        with zipfile.ZipFile(result.zip_path) as zf:
            names = set(zf.namelist())
        assert "orchestrator.md" in names
        assert "agents/agent_role.md" in names
        assert "architecture/topology.yaml" in names

    def test_meta_yaml_correct_for_multi(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "code-review-team"),
            approval_record=VALID_APPROVAL,
        )
        meta = yaml.safe_load(
            (Path(result.output_path) / "meta.yaml").read_text()
        )
        assert meta["factory_version"] == "1.0.0"
        assert meta["name"] == "code-review-team"
        assert meta["type"] == "multi"

    def test_approval_log_has_hash(self, tmp_path: Path) -> None:
        result = factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "code-review-team"),
            approval_record=VALID_APPROVAL,
        )
        log_path = Path(result.output_path) / "approval_log.jsonl"
        entry = json.loads(log_path.read_text().strip().splitlines()[0])
        assert "hash" in entry
        assert len(entry["hash"]) == 64


# ---------------------------------------------------------------------------
# Performance test
# ---------------------------------------------------------------------------


class TestGenerationPerformance:
    """Verify generation completes within time budget."""

    def test_single_agent_under_2_seconds(self, tmp_path: Path) -> None:
        start = time.monotonic()
        factory.generate(
            spec=SINGLE_SPEC,
            output=str(tmp_path / "perf-single"),
            approval_record=VALID_APPROVAL,
        )
        elapsed = time.monotonic() - start
        assert elapsed < 2.0, f"Generation took {elapsed:.2f}s (limit: 2s)"

    def test_multi_agent_under_2_seconds(self, tmp_path: Path) -> None:
        start = time.monotonic()
        factory.generate(
            spec=MULTI_SPEC,
            output=str(tmp_path / "perf-multi"),
            approval_record=VALID_APPROVAL,
        )
        elapsed = time.monotonic() - start
        assert elapsed < 2.0, f"Generation took {elapsed:.2f}s (limit: 2s)"
