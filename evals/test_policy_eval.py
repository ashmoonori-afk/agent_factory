"""Eval tests for DENY / ASK / ALLOW policy generation."""
from __future__ import annotations

from pathlib import Path

import pytest

from evals.conftest import generate_agent, load_scenarios

# ---------------------------------------------------------------
# DENY scenarios (5 tests)
# ---------------------------------------------------------------

_DENY_SCENARIOS = load_scenarios("deny_policies.yaml")


@pytest.mark.parametrize(
    "scenario",
    _DENY_SCENARIOS,
    ids=[s["id"] for s in _DENY_SCENARIOS],
)
def test_deny_policy_in_claude_md(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """DENY actions appear under the DENY section of CLAUDE.md."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    target = Path(result.output_path) / str(check["file"])
    content = target.read_text()

    for token in check["must_contain"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not found in {check['file']}"
        )

    # Verify the token appears after the section header
    section = str(check.get("section", ""))
    if section:
        idx_section = content.find(section)
        assert idx_section != -1, (
            f"Section {section!r} missing from {check['file']}"
        )
        for token in check["must_contain"]:  # type: ignore[union-attr]
            idx_token = content.find(
                str(token), idx_section
            )
            assert idx_token > idx_section, (
                f"{token!r} not under section {section!r}"
            )


@pytest.mark.parametrize(
    "scenario",
    _DENY_SCENARIOS,
    ids=[s["id"] for s in _DENY_SCENARIOS],
)
def test_deny_policy_in_policy_yaml(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """DENY actions also appear in policies/policy.yaml."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    policy = Path(result.output_path) / "policies" / "policy.yaml"
    content = policy.read_text()

    for token in check["must_contain"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not found in policies/policy.yaml"
        )


# ---------------------------------------------------------------
# ASK scenarios (3 tests)
# ---------------------------------------------------------------

_ASK_SCENARIOS = load_scenarios("ask_policies.yaml")


@pytest.mark.parametrize(
    "scenario",
    _ASK_SCENARIOS,
    ids=[s["id"] for s in _ASK_SCENARIOS],
)
def test_ask_policy_in_claude_md(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """ASK actions appear under the ASK section of CLAUDE.md."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    target = Path(result.output_path) / str(check["file"])
    content = target.read_text()

    for token in check["must_contain"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not found in {check['file']}"
        )

    section = str(check.get("section", ""))
    if section:
        idx_section = content.find(section)
        assert idx_section != -1, (
            f"Section {section!r} missing from {check['file']}"
        )
        for token in check["must_contain"]:  # type: ignore[union-attr]
            idx_token = content.find(
                str(token), idx_section
            )
            assert idx_token > idx_section, (
                f"{token!r} not under section {section!r}"
            )


# ---------------------------------------------------------------
# ALLOW scenarios (2 tests)
# ---------------------------------------------------------------

_ALLOW_SCENARIOS = load_scenarios("allow_policies.yaml")


@pytest.mark.parametrize(
    "scenario",
    _ALLOW_SCENARIOS,
    ids=[s["id"] for s in _ALLOW_SCENARIOS],
)
def test_allow_policy_in_policy_yaml(
    scenario: dict[str, object],
    tmp_path: Path,
) -> None:
    """ALLOW actions appear in policies/policy.yaml."""
    spec = scenario["spec"]  # type: ignore[index]
    check = scenario["check"]  # type: ignore[index]

    result = generate_agent(spec, tmp_path)  # type: ignore[arg-type]
    target = Path(result.output_path) / str(check["file"])
    content = target.read_text()

    for token in check["must_contain"]:  # type: ignore[union-attr]
        assert str(token) in content, (
            f"{token!r} not found in {check['file']}"
        )
