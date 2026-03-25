"""Eval tests for skill activation in generated agents."""
from __future__ import annotations

from pathlib import Path

import pytest

from evals.conftest import generate_agent, load_scenarios

_SKILL_SCENARIOS = load_scenarios("skill_activation.yaml")


@pytest.mark.parametrize(
    "scenario",
    [s for s in _SKILL_SCENARIOS if s["id"] != "skill-unknown-graceful"],
    ids=[
        s["id"]
        for s in _SKILL_SCENARIOS
        if s["id"] != "skill-unknown-graceful"
    ],
)
def test_skill_file_exists(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """Known skill produces a non-empty .md file in skills/."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    skill_path = Path(result.output_path) / str(
        check["skill_file"]
    )
    assert skill_path.exists(), (
        f"Skill file {check['skill_file']} not found"
    )
    assert skill_path.stat().st_size > 0, (
        f"Skill file {check['skill_file']} is empty"
    )


@pytest.mark.parametrize(
    "scenario",
    [s for s in _SKILL_SCENARIOS if s["id"] != "skill-unknown-graceful"],
    ids=[
        s["id"]
        for s in _SKILL_SCENARIOS
        if s["id"] != "skill-unknown-graceful"
    ],
)
def test_skill_listed_in_claude_md(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """Skill name appears in CLAUDE.md Available Skills section."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    claude_md = Path(result.output_path) / "CLAUDE.md"
    content = claude_md.read_text()

    for token in check["claude_md_contains"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not in CLAUDE.md"
        )


def test_unknown_skill_no_crash(tmp_path: Path) -> None:
    """Unknown skill ID does not crash generation."""
    scenario = next(
        s for s in _SKILL_SCENARIOS
        if s["id"] == "skill-unknown-graceful"
    )
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    assert result.file_count > 0

    claude_md = Path(result.output_path) / "CLAUDE.md"
    content = claude_md.read_text()
    for token in check["claude_md_contains"]:  # type: ignore[union-attr]
        assert str(token) in content
