"""Tests for the architecture critique engine."""

from __future__ import annotations

from factory.core.critique import critique


def _perfect_spec() -> dict[str, object]:
    """Return a well-defined spec that should produce no warnings."""
    return {
        "name": "my-agent",
        "description": "A helpful assistant for data tasks.",
        "type": "single",
        "policies": {
            "deny": [
                "delete_file",
                "send_email",
                "deploy",
                "payment",
            ],
            "ask": ["execute_sql"],
            "allow": ["*"],
        },
        "persona": {"tone": "professional", "language": "en"},
        "skills": ["csv-reader", "sql-executor"],
    }


# --- Safety tests ---


def test_critique_no_deny_policies_warns() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {"deny": [], "ask": ["something"]},
        "persona": {"tone": "friendly"},
        "skills": ["csv-reader"],
    }
    result = critique(spec)
    deny_warnings = [
        w for w in result.warnings if "No DENY policies" in w
    ]
    assert len(deny_warnings) == 1


def test_critique_missing_critical_denies() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {
            "deny": ["delete_file"],
            "ask": [],
        },
        "persona": {"tone": "friendly"},
        "skills": ["csv-reader"],
    }
    result = critique(spec)
    missing_warnings = [
        w
        for w in result.warnings
        if "Missing recommended DENY" in w
    ]
    assert len(missing_warnings) == 1
    # Should mention deploy, payment, send_email
    w = missing_warnings[0]
    assert "deploy" in w
    assert "payment" in w
    assert "send_email" in w


def test_critique_no_ask_no_deny_unrestricted() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {"deny": [], "ask": []},
        "persona": {"tone": "friendly"},
        "skills": ["csv-reader"],
    }
    result = critique(spec)
    unrestricted = [
        w for w in result.warnings if "unrestricted" in w
    ]
    assert len(unrestricted) == 1


# --- Completeness tests ---


def test_critique_no_description_warns() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "policies": {
            "deny": [
                "delete_file",
                "send_email",
                "deploy",
                "payment",
            ],
        },
        "persona": {"tone": "friendly"},
        "skills": ["csv-reader"],
    }
    result = critique(spec)
    desc_warnings = [
        w for w in result.warnings if "No description" in w
    ]
    assert len(desc_warnings) == 1


def test_critique_no_skills_warns() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {
            "deny": [
                "delete_file",
                "send_email",
                "deploy",
                "payment",
            ],
        },
        "persona": {"tone": "friendly"},
        "skills": [],
    }
    result = critique(spec)
    skill_warnings = [
        w for w in result.warnings if "No skills defined" in w
    ]
    assert len(skill_warnings) == 1


def test_critique_no_persona_warns() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {
            "deny": [
                "delete_file",
                "send_email",
                "deploy",
                "payment",
            ],
        },
        "skills": ["csv-reader"],
    }
    result = critique(spec)
    persona_warnings = [
        w for w in result.warnings if "No persona defined" in w
    ]
    assert len(persona_warnings) == 1


# --- Maintainability tests ---


def test_critique_too_many_skills_warns() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {
            "deny": [
                "delete_file",
                "send_email",
                "deploy",
                "payment",
            ],
        },
        "persona": {"tone": "friendly"},
        "skills": ["a", "b", "c", "d", "e", "f", "g"],
    }
    result = critique(spec)
    skill_warnings = [
        w for w in result.warnings if "7 skills defined" in w
    ]
    assert len(skill_warnings) == 1


def test_critique_too_many_agents_warns() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {
            "deny": [
                "delete_file",
                "send_email",
                "deploy",
                "payment",
            ],
        },
        "persona": {"tone": "friendly"},
        "skills": ["csv-reader"],
        "agents": [
            {"name": f"agent-{i}"} for i in range(6)
        ],
    }
    result = critique(spec)
    agent_warnings = [
        w for w in result.warnings if "6 agents" in w
    ]
    assert len(agent_warnings) == 1


# --- Scoring / grading tests ---


def test_critique_perfect_spec_no_warnings() -> None:
    result = critique(_perfect_spec())
    assert result.warnings == []
    assert result.score["safety"] == 100
    assert result.score["completeness"] == 100
    assert result.score["maintainability"] == 100


def test_critique_score_ranges() -> None:
    spec: dict[str, object] = {
        "name": "bot",
        "description": "test",
        "policies": {"deny": ["delete_file"], "ask": []},
        "persona": {"tone": "friendly"},
        "skills": ["csv-reader"],
    }
    result = critique(spec)
    for val in result.score.values():
        assert 0 <= val <= 100
    # Verify weighted calculation
    s = result.score["safety"]
    c = result.score["completeness"]
    m = result.score["maintainability"]
    expected = int(s * 0.5 + c * 0.3 + m * 0.2)
    assert result.total_score == expected


def test_critique_grade_a_for_good_spec() -> None:
    result = critique(_perfect_spec())
    assert result.grade == "A"
    assert result.total_score >= 90


def test_critique_grade_f_for_empty_spec() -> None:
    spec: dict[str, object] = {}
    result = critique(spec)
    assert result.grade == "F"
    assert result.total_score < 60
