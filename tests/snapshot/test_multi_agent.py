"""Snapshot tests for multi-agent templates."""

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
    """A fully-populated multi-agent context matching the generator's output."""
    return {
        "spec": {
            "name": "team-bot",
            "description": "A multi-agent team for code review",
            "type": "multi",
            "runtime": {"primary": "claude-code"},
            "policies": {
                "deny": [
                    "send_email",
                    "deploy",
                    "payment",
                    "modify_own_prompt",
                    "modify_policy_file",
                ],
                "ask": ["sql_execute", "delete_file"],
                "allow": ["*"],
            },
            "persona": {"tone": "technical", "language": "en"},
            "skills": ["code-review", "file-reader"],
            "agents": [
                {"id": "planner", "role": "Plans review tasks", "next": ["reviewer"]},
                {"id": "reviewer", "role": "Reviews code changes", "next": ["reporter"]},
                {"id": "reporter", "role": "Writes review reports"},
            ],
            "topology": {
                "entry": "planner",
                "max_loops": 3,
                "exit_condition": "reporter completes report",
            },
        },
        "name": "team-bot",
        "description": "A multi-agent team for code review",
        "type": "multi",
        "skills": ["code-review", "file-reader"],
        "persona": {"tone": "technical", "language": "en"},
        "approval_hash": "sha256-multi-hash-xyz",
        "generated_at": "2026-03-25T15:00:00Z",
    }


@pytest.fixture()
def minimal_multi_context() -> dict[str, object]:
    """Minimal multi-agent context — no agents, no topology."""
    return {
        "spec": {
            "name": "bare-multi",
            "description": "A bare multi-agent",
            "type": "multi",
        },
        "name": "bare-multi",
        "description": "A bare multi-agent",
        "type": "multi",
        "skills": [],
        "persona": {},
        "approval_hash": "sha256-bare",
        "generated_at": "2026-01-01T00:00:00Z",
    }


# ---------------------------------------------------------------------------
# render_all: file set completeness
# ---------------------------------------------------------------------------


def test_multi_agent_renders_all_expected_files(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("multi_agent", full_context)
    expected_files = {
        "CLAUDE.md",
        "CODEX.md",
        "AGENTS.md",
        "orchestrator.md",
        "agents/agent_role.md",
        "architecture/topology.yaml",
        "agent_spec.yaml",
        "README.md",
        "meta.yaml",
    }
    assert expected_files == set(result.keys())


def test_multi_agent_minimal_renders_all_files(
    renderer: TemplateRenderer, minimal_multi_context: dict[str, object]
) -> None:
    result = renderer.render_all("multi_agent", minimal_multi_context)
    assert len(result) == 9  # +AGENTS.md


# ---------------------------------------------------------------------------
# CLAUDE.md (multi)
# ---------------------------------------------------------------------------


def test_multi_claude_md_contains_orchestrator_reference(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CLAUDE.md"]
    assert "orchestrator" in content.lower()
    assert "topology" in content.lower()


def test_multi_claude_md_lists_agents(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CLAUDE.md"]
    assert "planner" in content
    assert "reviewer" in content
    assert "reporter" in content


def test_multi_claude_md_contains_deny_actions(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CLAUDE.md"]
    assert "send_email" in content
    assert "deploy" in content


def test_multi_claude_md_contains_reading_order(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CLAUDE.md"]
    assert "Reading Order" in content
    assert "orchestrator.md" in content
    assert "topology.yaml" in content


def test_multi_claude_md_contains_skills(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CLAUDE.md"]
    assert "code-review" in content
    assert "file-reader" in content


# ---------------------------------------------------------------------------
# CODEX.md (multi)
# ---------------------------------------------------------------------------


def test_multi_codex_md_contains_agent_name(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CODEX.md"]
    assert "team-bot" in content


def test_multi_codex_md_points_to_agents_md(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["CODEX.md"]
    assert "AGENTS.md" in content


def test_multi_agents_md_has_codex_specific_notes(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["AGENTS.md"]
    assert "sandbox" in content.lower()


# ---------------------------------------------------------------------------
# orchestrator.md
# ---------------------------------------------------------------------------


def test_orchestrator_contains_topology(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["orchestrator.md"]
    assert "planner" in content
    assert "Entry point: planner" in content
    assert "Max loops: 3" in content


def test_orchestrator_lists_agents(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["orchestrator.md"]
    assert "planner" in content
    assert "reviewer" in content
    assert "reporter" in content


def test_orchestrator_contains_handoff_rules(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["orchestrator.md"]
    assert "Orchestration Rules" in content


def test_orchestrator_minimal_no_topology(
    renderer: TemplateRenderer, minimal_multi_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", minimal_multi_context)["orchestrator.md"]
    assert "sequentially" in content.lower()


# ---------------------------------------------------------------------------
# agents/agent_role.md
# ---------------------------------------------------------------------------


def test_agent_role_lists_all_agents(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["agents/agent_role.md"]
    assert "planner" in content
    assert "reviewer" in content
    assert "reporter" in content


def test_agent_role_includes_next_links(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["agents/agent_role.md"]
    # planner -> reviewer
    assert "reviewer" in content


# ---------------------------------------------------------------------------
# architecture/topology.yaml
# ---------------------------------------------------------------------------


def test_topology_yaml_contains_entry(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["architecture/topology.yaml"]
    assert "entry: planner" in content


def test_topology_yaml_lists_agents(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["architecture/topology.yaml"]
    assert "planner" in content
    assert "reviewer" in content
    assert "reporter" in content


def test_topology_yaml_contains_max_loops(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["architecture/topology.yaml"]
    assert "max_loops: 3" in content


# ---------------------------------------------------------------------------
# agent_spec.yaml (multi)
# ---------------------------------------------------------------------------


def test_multi_agent_spec_contains_agents(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["agent_spec.yaml"]
    assert "agents:" in content
    assert "planner" in content
    assert "topology:" in content


def test_multi_agent_spec_contains_type_multi(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["agent_spec.yaml"]
    assert "type: multi" in content


# ---------------------------------------------------------------------------
# README.md (multi)
# ---------------------------------------------------------------------------


def test_multi_readme_mentions_multi_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["README.md"]
    assert "Multi-Agent" in content


def test_multi_readme_lists_agents(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["README.md"]
    assert "planner" in content
    assert "reviewer" in content


def test_multi_readme_contains_structure_section(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["README.md"]
    assert "orchestrator.md" in content
    assert "architecture/" in content


# ---------------------------------------------------------------------------
# meta.yaml (multi)
# ---------------------------------------------------------------------------


def test_multi_meta_yaml_contains_name_and_type(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("multi_agent", full_context)["meta.yaml"]
    assert "name: team-bot" in content
    assert "type: multi" in content


# ---------------------------------------------------------------------------
# Shared templates render for multi-agent context
# ---------------------------------------------------------------------------


def test_shared_docs_render_for_multi_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("docs", full_context)
    assert "architecture.md" in result
    content = result["architecture.md"]
    assert "Multi-Agent Topology" in content
    assert "planner" in content


def test_shared_reading_order_for_multi_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("docs", full_context)["reading_order.md"]
    assert "orchestrator.md" in content
    assert "topology.yaml" in content


def test_shared_policies_render_for_multi_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    result = renderer.render_all("policies", full_context)
    content = result["policy.yaml"]
    assert "deny:" in content
    assert "send_email" in content


def test_shared_test_agent_for_multi_agent(
    renderer: TemplateRenderer, full_context: dict[str, object]
) -> None:
    content = renderer.render_all("tests", full_context)["test-agent.md"]
    assert "Multi-agent orchestration" in content
    assert "planner" in content
