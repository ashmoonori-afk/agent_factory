"""Unit tests for RegistryLoader."""

from __future__ import annotations

from pathlib import Path

import pytest

from factory.registries.loader import RegistryLoader

# Resolve the registry directory relative to the project root.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_REGISTRY_DIR = _PROJECT_ROOT / "registry"


@pytest.fixture()
def loader() -> RegistryLoader:
    return RegistryLoader(_REGISTRY_DIR)


# ---------------------------------------------------------------------------
# list_skills
# ---------------------------------------------------------------------------


def test_list_skills_returns_expected_count(loader: RegistryLoader) -> None:
    skills = loader.list_skills()
    # 10 original + 125 from everything-claude-code + 7 from ui-ux-pro-max + 23 from awesome-claude-code
    assert len(skills) >= 10  # at least the original 10 built-in skills


def test_list_skills_items_have_required_keys(loader: RegistryLoader) -> None:
    for skill in loader.list_skills():
        assert "id" in skill, f"Missing 'id' in {skill}"
        assert "name" in skill, f"Missing 'name' in {skill}"
        assert "description" in skill, f"Missing 'description' in {skill}"
        assert "policy" in skill, f"Missing 'policy' in {skill}"


def test_list_skills_policies_are_valid(loader: RegistryLoader) -> None:
    valid_policies = {"DENY", "ASK", "ALLOW"}
    for skill in loader.list_skills():
        assert skill["policy"] in valid_policies, (
            f"Skill {skill['id']} has invalid policy {skill['policy']!r}"
        )


def test_list_skills_contains_expected_ids(loader: RegistryLoader) -> None:
    ids = {s["id"] for s in loader.list_skills()}
    # Original 10 skills must always be present
    original_10 = {
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
    }
    assert original_10.issubset(ids), f"Missing original skills: {original_10 - ids}"


def test_list_skills_shell_executor_is_deny(loader: RegistryLoader) -> None:
    skills_by_id = {s["id"]: s for s in loader.list_skills()}
    assert skills_by_id["shell-executor"]["policy"] == "DENY"


def test_list_skills_csv_reader_is_allow(loader: RegistryLoader) -> None:
    skills_by_id = {s["id"] for s in loader.list_skills() if s["policy"] == "ALLOW"}
    assert "csv-reader" in skills_by_id


# ---------------------------------------------------------------------------
# get_skill
# ---------------------------------------------------------------------------


def test_get_skill_returns_string(loader: RegistryLoader) -> None:
    content = loader.get_skill("csv-reader")
    assert isinstance(content, str)
    assert len(content) > 0


def test_get_skill_returns_markdown_content(loader: RegistryLoader) -> None:
    content = loader.get_skill("sql-executor")
    assert "# Skill:" in content
    assert "## Policy" in content
    assert "## Instructions" in content


def test_get_skill_returns_correct_skill(loader: RegistryLoader) -> None:
    content = loader.get_skill("shell-executor")
    assert "shell" in content.lower() or "Shell" in content


def test_get_skill_raises_for_unknown_id(loader: RegistryLoader) -> None:
    with pytest.raises(KeyError, match="unknown-skill"):
        loader.get_skill("unknown-skill")


def test_get_skill_all_ten_are_readable(loader: RegistryLoader) -> None:
    for skill in loader.list_skills():
        content = loader.get_skill(skill["id"])
        assert len(content) > 100, (
            f"Skill {skill['id']} content is too short ({len(content)} chars)"
        )


# ---------------------------------------------------------------------------
# list_personas
# ---------------------------------------------------------------------------


def test_list_personas_returns_four_items(loader: RegistryLoader) -> None:
    personas = loader.list_personas()
    assert len(personas) == 4


def test_list_personas_items_have_required_keys(loader: RegistryLoader) -> None:
    for persona in loader.list_personas():
        assert "id" in persona, f"Missing 'id' in {persona}"
        assert "tone" in persona, f"Missing 'tone' in {persona}"
        assert "description" in persona, f"Missing 'description' in {persona}"


def test_list_personas_contains_expected_ids(loader: RegistryLoader) -> None:
    ids = {p["id"] for p in loader.list_personas()}
    assert ids == {"professional", "friendly", "technical", "minimal"}


# ---------------------------------------------------------------------------
# get_persona
# ---------------------------------------------------------------------------


def test_get_persona_returns_dict(loader: RegistryLoader) -> None:
    persona = loader.get_persona("professional")
    assert isinstance(persona, dict)


def test_get_persona_has_required_fields(loader: RegistryLoader) -> None:
    persona = loader.get_persona("professional")
    assert "id" in persona
    assert "tone" in persona
    assert "language" in persona
    assert "description" in persona
    assert "custom_instructions" in persona


def test_get_persona_raises_for_unknown_id(loader: RegistryLoader) -> None:
    with pytest.raises(KeyError, match="nonexistent"):
        loader.get_persona("nonexistent")


def test_get_persona_all_four_are_readable(loader: RegistryLoader) -> None:
    for persona in loader.list_personas():
        data = loader.get_persona(persona["id"])
        assert data["id"] == persona["id"]
        assert data["custom_instructions"], (
            f"Persona {persona['id']} has empty custom_instructions"
        )


# ---------------------------------------------------------------------------
# Default registry_dir resolution
# ---------------------------------------------------------------------------


def test_loader_default_registry_dir_resolves() -> None:
    """RegistryLoader with no args should find the built-in registry."""
    loader = RegistryLoader()
    skills = loader.list_skills()
    assert len(skills) >= 10  # at least the original 10 built-in skills
