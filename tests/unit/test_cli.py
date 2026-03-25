"""CLI tests for Agent Factory auxiliary commands."""

from __future__ import annotations

from pathlib import Path

import yaml
from click.testing import CliRunner

from factory.cli.main import cli
from factory.core.generator import generate


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_validate_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--help"])
    assert result.exit_code == 0
    assert "Validate" in result.output or "validate" in result.output


# ---------------------------------------------------------------------------
# skills command
# ---------------------------------------------------------------------------


def test_skills_exits_zero() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0, result.output


def test_skills_lists_ten_skills() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0
    # Each skill occupies at least one output line with its ID.
    expected_ids = [
        "sql-executor",
        "csv-reader",
        "file-reader",
        "file-writer",
        "web-search",
        "json-parser",
        "text-summarizer",
        "code-reviewer",
        "code-generator",
        "shell-executor",
    ]
    for skill_id in expected_ids:
        assert skill_id in result.output, (
            f"Expected skill '{skill_id}' not found in output:\n{result.output}"
        )


def test_skills_shows_policy() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0
    # At least one of the policy levels should appear.
    assert any(policy in result.output for policy in ("DENY", "ASK", "ALLOW")), (
        f"No policy level found in skills output:\n{result.output}"
    )


def test_skills_shows_shell_executor_as_deny() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0
    # shell-executor must appear alongside DENY on the same line or nearby.
    lines = result.output.splitlines()
    shell_lines = [line for line in lines if "shell-executor" in line]
    assert shell_lines, "shell-executor not found in skills output"
    assert any("DENY" in line for line in shell_lines), (
        f"shell-executor line does not show DENY:\n{shell_lines}"
    )


# ---------------------------------------------------------------------------
# personas command
# ---------------------------------------------------------------------------


def test_personas_exits_zero() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0, result.output


def test_personas_lists_four_personas() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
    expected_ids = ["professional", "friendly", "technical", "minimal"]
    for persona_id in expected_ids:
        assert persona_id in result.output, (
            f"Expected persona '{persona_id}' not found in output:\n{result.output}"
        )


def test_personas_shows_tone() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
    # At least one of the known tone descriptors should be present.
    tone_keywords = ["Formal", "Casual", "Detailed", "Brief"]
    assert any(kw in result.output for kw in tone_keywords), (
        f"No tone descriptor found in personas output:\n{result.output}"
    )


# -------------------------------------------------------------------
# upgrade command
# -------------------------------------------------------------------

_UPGRADE_SPEC: dict[str, object] = {
    "name": "upgrade-bot",
    "description": "Agent for upgrade CLI tests",
    "type": "single",
}

_UPGRADE_APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "upgrade-bot single-agent",
}


def _gen_agent(tmp_path: Path) -> Path:
    out = tmp_path / "upgrade-bot"
    generate(
        spec=_UPGRADE_SPEC,
        output=str(out),
        approval_record=_UPGRADE_APPROVAL,
        no_zip=True,
    )
    return out


def test_upgrade_already_current(tmp_path: Path) -> None:
    agent_dir = _gen_agent(tmp_path)
    runner = CliRunner()
    result = runner.invoke(cli, ["upgrade", str(agent_dir)])
    assert result.exit_code == 0
    assert "Already up to date" in result.output


def test_upgrade_preview_flag(tmp_path: Path) -> None:
    agent_dir = _gen_agent(tmp_path)
    # Make version outdated
    meta_path = agent_dir / "meta.yaml"
    meta = yaml.safe_load(meta_path.read_text())
    meta["template_version"] = "0.0.1"
    meta_path.write_text(
        yaml.dump(meta, default_flow_style=False)
    )
    runner = CliRunner()
    result = runner.invoke(
        cli, ["upgrade", str(agent_dir), "--preview"],
    )
    assert result.exit_code == 0
    assert "Current: 0.0.1" in result.output
    assert "Latest: 1.0.1" in result.output
