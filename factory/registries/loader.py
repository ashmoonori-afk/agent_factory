"""Registry loader — resolves built-in skills and personas from disk."""

from __future__ import annotations

from pathlib import Path

import yaml


def _find_registry_dir() -> Path:
    """Resolve registry directory — installed package data first, then dev."""
    try:
        from importlib.resources import files as _res_files
        candidate = Path(str(_res_files("factory").joinpath("registry")))
        if (candidate / "sources").is_dir():
            return candidate
    except (ModuleNotFoundError, TypeError):
        pass
    return Path(__file__).resolve().parent.parent.parent / "registry"


_DEFAULT_REGISTRY_DIR = _find_registry_dir()

# Skill frontmatter is parsed from the first H1 and H2 lines of each .md file
# rather than a separate YAML block, keeping skill files self-contained.
_POLICY_TAG = "Level:"


def _parse_skill_frontmatter(skill_id: str, content: str) -> dict[str, str]:
    """Extract id, name, description, and policy from .md content.

    The format expected is:
        # Skill: <Display Name>
        ## When to Use
        <description lines>
        ## Policy
        Level: <DENY|ASK|ALLOW>
    """
    name = skill_id  # fallback
    description = ""
    policy = "ALLOW"  # fallback

    lines = content.splitlines()
    in_when_to_use = False
    desc_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Title line: # Skill: Display Name
        if stripped.startswith("# Skill:"):
            name = stripped[len("# Skill:"):].strip()
            in_when_to_use = False

        # Section headers
        elif stripped.startswith("## When to Use"):
            in_when_to_use = True

        elif stripped.startswith("##"):
            in_when_to_use = False

        # Collect "When to Use" body as description
        elif in_when_to_use and stripped:
            desc_lines.append(stripped)

        # Policy level line
        elif stripped.startswith(_POLICY_TAG):
            policy = stripped[len(_POLICY_TAG):].strip().split()[0].upper()

    description = " ".join(desc_lines)

    return {
        "id": skill_id,
        "name": name,
        "description": description,
        "policy": policy,
    }


class RegistryLoader:
    """Load built-in skills and personas from the registry directory.

    Args:
        registry_dir: Path to the registry root (the directory that contains
            ``sources/registry.yaml``). Defaults to the built-in registry
            shipped with the package.
    """

    def __init__(self, registry_dir: Path | None = None) -> None:
        self._registry_dir = (registry_dir or _DEFAULT_REGISTRY_DIR).resolve()
        manifest_path = self._registry_dir / "sources" / "registry.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Registry manifest not found: {manifest_path}"
            )
        with open(manifest_path) as fh:
            manifest: dict[str, object] = yaml.safe_load(fh)

        skills_cfg = manifest.get("skills", {})
        if not isinstance(skills_cfg, dict):
            raise TypeError(
                f"Registry manifest 'skills' must be a dict, got {type(skills_cfg).__name__}"
            )
        skills_dir_rel = str(skills_cfg.get("builtin_dir", "../builtin_skills"))
        self._skills_dir = (
            self._registry_dir / "sources" / skills_dir_rel
        ).resolve()
        raw_skill_items = skills_cfg.get("items", [])
        if not isinstance(raw_skill_items, list):
            raw_type = type(raw_skill_items).__name__
            raise TypeError(
                f"Registry manifest 'skills.items' must be a list, got {raw_type}"
            )
        self._skill_ids: list[str] = [str(i) for i in raw_skill_items]

        personas_cfg = manifest.get("personas", {})
        if not isinstance(personas_cfg, dict):
            raise TypeError(
                f"Registry manifest 'personas' must be a dict, got {type(personas_cfg).__name__}"
            )
        personas_dir_rel = str(personas_cfg.get("builtin_dir", "../builtin_personas"))
        self._personas_dir = (
            self._registry_dir / "sources" / personas_dir_rel
        ).resolve()
        raw_persona_items = personas_cfg.get("items", [])
        if not isinstance(raw_persona_items, list):
            raw_type = type(raw_persona_items).__name__
            raise TypeError(
                f"Registry manifest 'personas.items' must be a list, got {raw_type}"
            )
        self._persona_ids: list[str] = [str(i) for i in raw_persona_items]

        # Eagerly cache parsed frontmatter so list_* calls are cheap.
        self._skill_meta: dict[str, dict[str, str]] = {}
        self._skill_content: dict[str, str] = {}
        self._persona_meta: dict[str, dict[str, str]] = {}
        self._persona_data: dict[str, dict[str, object]] = {}

        self._load_skills()
        self._load_personas()

    # ------------------------------------------------------------------
    # Private loading helpers
    # ------------------------------------------------------------------

    def _load_skills(self) -> None:
        for skill_id in self._skill_ids:
            path = self._skills_dir / f"{skill_id}.md"
            if not path.exists():
                raise FileNotFoundError(
                    f"Skill file not found for '{skill_id}': {path}"
                )
            content = path.read_text(encoding="utf-8")
            self._skill_content[skill_id] = content
            self._skill_meta[skill_id] = _parse_skill_frontmatter(skill_id, content)

    def _load_personas(self) -> None:
        for persona_id in self._persona_ids:
            path = self._personas_dir / f"{persona_id}.yaml"
            if not path.exists():
                raise FileNotFoundError(
                    f"Persona file not found for '{persona_id}': {path}"
                )
            with open(path) as fh:
                data: dict[str, object] = yaml.safe_load(fh)
            self._persona_data[persona_id] = data
            self._persona_meta[persona_id] = {
                "id": str(data.get("id", persona_id)),
                "tone": str(data.get("tone", "")),
                "description": str(data.get("description", "")),
            }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_skills(self) -> list[dict[str, str]]:
        """Return summary metadata for all registered skills.

        Returns:
            List of dicts with keys: ``id``, ``name``, ``description``, ``policy``.
            Order matches the registry manifest.
        """
        return [self._skill_meta[sid] for sid in self._skill_ids]

    def get_skill(self, skill_id: str) -> str:
        """Return the raw Markdown content for a skill.

        Args:
            skill_id: The skill identifier, e.g. ``"csv-reader"``.

        Returns:
            Full `.md` file contents as a string.

        Raises:
            KeyError: If `skill_id` is not registered.
        """
        if skill_id not in self._skill_content:
            raise KeyError(skill_id)
        return self._skill_content[skill_id]

    def list_personas(self) -> list[dict[str, str]]:
        """Return summary metadata for all registered personas.

        Returns:
            List of dicts with keys: ``id``, ``tone``, ``description``.
            Order matches the registry manifest.
        """
        return [self._persona_meta[pid] for pid in self._persona_ids]

    def get_persona(self, persona_id: str) -> dict[str, object]:
        """Return the full parsed YAML dict for a persona.

        Args:
            persona_id: The persona identifier, e.g. ``"professional"``.

        Returns:
            Parsed YAML dict with keys: ``id``, ``tone``, ``language``,
            ``description``, ``custom_instructions``.

        Raises:
            KeyError: If `persona_id` is not registered.
        """
        if persona_id not in self._persona_data:
            raise KeyError(persona_id)
        return self._persona_data[persona_id]
