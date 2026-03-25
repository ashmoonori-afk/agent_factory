from __future__ import annotations

from factory.schemas.validator import load_schema, validate_spec


def test_load_agent_spec_schema() -> None:
    schema = load_schema("agent_spec")
    assert schema["title"] == "Agent Spec"
    assert "properties" in schema


def test_validate_valid_minimal_spec() -> None:
    spec = {
        "name": "my-bot",
        "description": "A test bot",
        "type": "single",
    }
    errors = validate_spec(spec)
    assert errors == []


def test_validate_missing_required_field() -> None:
    spec = {
        "name": "my-bot",
        # missing description and type
    }
    errors = validate_spec(spec)
    assert len(errors) > 0
    assert any("description" in e or "type" in e for e in errors)


def test_validate_invalid_type_enum() -> None:
    spec = {
        "name": "my-bot",
        "description": "A test bot",
        "type": "invalid",
    }
    errors = validate_spec(spec)
    assert len(errors) > 0


def test_validate_invalid_name_pattern() -> None:
    spec = {
        "name": "My Bot!",
        "description": "A test bot",
        "type": "single",
    }
    errors = validate_spec(spec)
    assert len(errors) > 0


def test_validate_full_spec_with_optional_fields() -> None:
    spec = {
        "name": "data-analyzer",
        "description": "Analyze CSV and SQL data",
        "type": "single",
        "runtime": {"primary": "both"},
        "policies": {
            "deny": ["send_email", "delete_file"],
            "ask": ["sql_execute"],
            "allow": ["*"],
        },
        "persona": {"tone": "professional", "language": "en"},
        "skills": ["csv-reader", "sql-executor"],
        "context": "Used for financial data analysis",
    }
    errors = validate_spec(spec)
    assert errors == []


def test_validate_multi_agent_spec() -> None:
    spec = {
        "name": "team-bot",
        "description": "A multi-agent team",
        "type": "multi",
        "agents": [
            {"id": "planner", "role": "Plan tasks", "next": ["executor"]},
            {"id": "executor", "role": "Execute tasks", "next": ["reviewer"]},
            {"id": "reviewer", "role": "Review results", "next": ["planner"]},
        ],
        "topology": {
            "entry": "planner",
            "max_loops": 3,
            "exit_condition": "reviewer approves",
        },
    }
    errors = validate_spec(spec)
    assert errors == []
