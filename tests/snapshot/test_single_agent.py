"""Snapshot tests for single-agent templates."""

from __future__ import annotations

import pytest

from factory.core.renderer import TemplateRenderer

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def renderer() -> TemplateRenderer:
    return TemplateRenderer()


@pytest.fixture()
def full_context() -> dict[str, object]:
    """A fully-populated single-agent context matching the generator's output."""
    return {
        "spec": {
            "name": "data-bot",
            "description": "Analyze CSV files and generate summary reports",
            "type": "single",
            "runtime": {"primary": "both"},
            "policies": {
                "deny": [
                    "send_email",
                    "delete_file",
                    "deploy",
                    "payment",
                    "external_share",
                    "modify_meta_agent",
                    "modify_own_prompt",
                    "modify_policy_file",
                ],
                "ask": ["sql_execute"],
                "allow": ["*"],
            },
            "persona": {
                "tone": "professional",
                "language": "en",
                "custom_instructions": "Always cite data sources.",
            },
            "skills": ["sql-executor", "csv-reader"],
            "context": "Background knowledge here",
        },
        "name": "data-bot",
        "description": "Analyze CSV files and generate summary reports",
        "type": "single",
        "skills": ["sql-executor", "csv-reader"],
        "persona": {
            "tone": "professional",
            "language": "en",
            "custom_instructions": "Always cite data sources.",
        },
        "approval_hash": "sha256-test-hash-abc123",
        "generated_at": "2026-03-25T14:30:00Z",
    }


@pytest.fixture()
def minimal_context() -> dict[str, object]:
    """Minimal context — only required fields, no optional extras."""
    return {
        "spec": {
            "name": "minimal-bot",
            "description": "A minimal agent",
            "type": "single",
        },
        "name": "minimal-bot",
        "description": "A minimal agent",
        "type": "single",
        "skills": [],
        "persona": {},
        "approval_hash": "sha256-min",
        "generated_at": "2026-01-01T00:00:00Z",
    }


# ---------------------------------------------------------------------------
# render_all: file set completeness
# ---------------------------------------------------------------------------


def test_single_agent_renders_all_expected_files(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("single_agent", full_context)
    expected_files = {
        "CLAUDE.md",
        "CODEX.md",
        "agent_spec.yaml",
        "README.md",
        "meta.yaml",
        ".env.example",
    }
    assert expected_files == set(result.keys())


def test_single_agent_minimal_renders_all_files(
    renderer: TemplateRenderer, minimal_context: dict[str, object]
) -> None:
    result = renderer.render_all("single_agent", minimal_context)
    assert len(result) == 6


# ---------------------------------------------------------------------------
# CLAUDE.md
# ---------------------------------------------------------------------------


def test_claude_md_contains_agent_name(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("single_agent", full_context)
    assert "data-bot" in result["CLAUDE.md"]


def test_claude_md_contains_identity_section(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "## Identity" in content
    assert "Tone: professional" in content
    assert "Language: en" in content


def test_claude_md_contains_deny_actions(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "send_email" in content
    assert "delete_file" in content
    assert "Forbidden Actions" in content


def test_claude_md_contains_ask_actions(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "sql_execute" in content
    assert "Requiring Approval" in content


def test_claude_md_contains_skills(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "sql-executor" in content
    assert "csv-reader" in content


def test_claude_md_contains_reading_order(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "Reading Order" in content
    assert "CLAUDE.md" in content
    assert "agent_spec.yaml" in content


def test_claude_md_contains_policy_rules_section(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "## Policy Rules" in content
    assert "DENY" in content
    assert "ASK" in content
    assert "ALLOW" in content


def test_claude_md_contains_custom_instructions(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CLAUDE.md"]
    assert "Always cite data sources." in content


def test_claude_md_minimal_has_no_skills_section(
    renderer: TemplateRenderer, minimal_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", minimal_context)["CLAUDE.md"]
    assert "No skills configured" in content


# ---------------------------------------------------------------------------
# CODEX.md
# ---------------------------------------------------------------------------


def test_codex_md_contains_agent_name(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CODEX.md"]
    assert "data-bot" in content


def test_codex_md_has_codex_specific_notes(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CODEX.md"]
    assert "Codex" in content
    assert "sandbox" in content.lower()


def test_codex_md_contains_deny_actions(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["CODEX.md"]
    assert "send_email" in content


# ---------------------------------------------------------------------------
# agent_spec.yaml
# ---------------------------------------------------------------------------


def test_agent_spec_yaml_contains_name_and_type(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["agent_spec.yaml"]
    assert "name: data-bot" in content
    assert "type: single" in content


def test_agent_spec_yaml_contains_policies(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["agent_spec.yaml"]
    assert "deny:" in content
    assert "send_email" in content
    assert "ask:" in content
    assert "sql_execute" in content


def test_agent_spec_yaml_contains_skills(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["agent_spec.yaml"]
    assert "skills:" in content
    assert "csv-reader" in content


def test_agent_spec_yaml_contains_runtime(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["agent_spec.yaml"]
    assert "runtime:" in content
    assert "primary: both" in content


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------


def test_readme_contains_agent_name(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["README.md"]
    assert "# data-bot" in content


def test_readme_contains_quick_start(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["README.md"]
    assert "Quick Start" in content
    assert "Claude Code" in content
    assert "Codex" in content


def test_readme_lists_forbidden_actions(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["README.md"]
    assert "send_email" in content


# ---------------------------------------------------------------------------
# meta.yaml
# ---------------------------------------------------------------------------


def test_meta_yaml_contains_generator_info(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)["meta.yaml"]
    assert "name: data-bot" in content
    assert "factory_version" in content
    assert "generated_at" in content
    assert "approval_hash" in content


# ---------------------------------------------------------------------------
# .env.example
# ---------------------------------------------------------------------------


def test_env_example_contains_placeholders(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("single_agent", full_context)[".env.example"]
    assert "data-bot" in content
    assert "API_KEY" in content


# ---------------------------------------------------------------------------
# Shared templates render for single-agent context
# ---------------------------------------------------------------------------


def test_shared_docs_render_for_single_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("docs", full_context)
    assert "architecture.md" in result
    assert "policy.md" in result
    assert "reading_order.md" in result
    assert "data-bot" in result["architecture.md"]


def test_shared_policies_render_for_single_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("policies", full_context)
    assert "policy.yaml" in result
    assert "approval_log.jsonl" in result
    assert "send_email" in result["policy.yaml"]


def test_shared_tests_render_for_single_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("tests", full_context)
    assert "test-policy.md" in result
    assert "test-agent.md" in result
    assert "send_email" in result["test-policy.md"]


def test_policy_yaml_contains_deny_ask_allow(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("policies", full_context)["policy.yaml"]
    assert "deny:" in content
    assert "ask:" in content
    assert "allow:" in content


def test_reading_order_single_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("docs", full_context)["reading_order.md"]
    assert "CLAUDE.md" in content
    assert "agent_spec.yaml" in content
    assert "policies/policy.yaml" in content
    # Single agent should NOT reference orchestrator
    assert "orchestrator" not in content.lower()
