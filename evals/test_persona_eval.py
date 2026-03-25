"""Eval tests for persona consistency in generated agents."""
from __future__ import annotations

from pathlib import Path

import pytest

from evals.conftest import generate_agent, load_scenarios

_PERSONA_SCENARIOS = load_scenarios("persona_consistency.yaml")


@pytest.mark.parametrize(
    "scenario",
    _PERSONA_SCENARIOS,
    ids=[s["id"] for s in _PERSONA_SCENARIOS],
)
def test_persona_in_claude_md(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """Persona tone appears in generated CLAUDE.md."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    claude_md = Path(result.output_path) / "CLAUDE.md"
    content = claude_md.read_text()

    for token in check["claude_md_contains"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not in CLAUDE.md"
        )


@pytest.mark.parametrize(
    "scenario",
    _PERSONA_SCENARIOS,
    ids=[s["id"] for s in _PERSONA_SCENARIOS],
)
def test_persona_file_created(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """Persona default.yaml is created with expected content."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    persona_path = Path(result.output_path) / str(
        check["persona_file"]
    )
    assert persona_path.exists(), "personas/default.yaml missing"
    content = persona_path.read_text()

    for token in check["persona_contains"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not in {check['persona_file']}"
        )
