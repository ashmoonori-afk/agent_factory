"""Shared fixtures for the eval suite."""
from __future__ import annotations

from pathlib import Path

import yaml

import factory

VALID_APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "eval test",
}


def generate_agent(
    spec: dict[str, object],
    tmp_path: Path,
) -> factory.GenerationResult:
    """Generate an agent and return the result."""
    name = spec.get("name", "eval-agent")
    output = str(tmp_path / str(name))
    return factory.generate(
        spec=spec,
        output=output,
        approval_record=VALID_APPROVAL,
        no_zip=True,
    )


def load_scenarios(scenario_file: str) -> list[dict[str, object]]:
    """Load scenarios from a YAML file in the scenarios/ dir."""
    path = Path(__file__).parent / "scenarios" / scenario_file
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("scenarios", [])
