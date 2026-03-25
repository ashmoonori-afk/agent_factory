from __future__ import annotations

from click.testing import CliRunner

from factory.cli.main import cli


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


def test_skills_placeholder() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0


def test_personas_placeholder() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
