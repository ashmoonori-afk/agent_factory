"""Agent upgrade logic -- compare and update generated agents."""

from __future__ import annotations

import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

from factory.core.generator import generate
from factory.core.renderer import TemplateRenderer


class UpgradeResult:
    """Result of an upgrade check or execution."""

    def __init__(
        self,
        current_version: str,
        latest_version: str,
        needs_upgrade: bool,
        changed_files: list[str] | None = None,
        backup_path: str | None = None,
    ) -> None:
        self.current_version = current_version
        self.latest_version = latest_version
        self.needs_upgrade = needs_upgrade
        self.changed_files = changed_files or []
        self.backup_path = backup_path


def _read_latest_version() -> str:
    """Read the latest template version from the VERSION file."""
    renderer = TemplateRenderer()
    version_file = renderer.template_dir / "VERSION"
    if version_file.is_file():
        return version_file.read_text().strip()
    return "unknown"


def check_upgrade(agent_dir: Path) -> UpgradeResult:
    """Check if an agent needs upgrading.

    Reads meta.yaml from the agent directory and compares
    template_version against the current templates/VERSION.
    """
    meta_path = agent_dir / "meta.yaml"
    if not meta_path.exists():
        raise FileNotFoundError(
            f"No meta.yaml found in {agent_dir}"
        )

    meta = yaml.safe_load(meta_path.read_text())
    current_version = str(
        meta.get("template_version", "unknown")
    )
    latest_version = _read_latest_version()
    needs_upgrade = current_version != latest_version

    return UpgradeResult(
        current_version=current_version,
        latest_version=latest_version,
        needs_upgrade=needs_upgrade,
    )


def _make_approval(
    current: str, latest: str, action: str,
) -> dict[str, str]:
    """Build an approval record for upgrade operations."""
    return {
        "decision": "APPROVED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_input": "YES",
        "action_type": action,
        "detail": f"upgrade from {current} to {latest}",
    }


def preview_upgrade(agent_dir: Path) -> UpgradeResult:
    """Preview what files would change during an upgrade.

    Generates a temporary new version and compares file-by-file.
    """
    result = check_upgrade(agent_dir)

    spec_path = agent_dir / "agent_spec.yaml"
    if not spec_path.exists():
        raise FileNotFoundError(
            f"No agent_spec.yaml found in {agent_dir}"
        )

    spec: dict[str, object] = yaml.safe_load(
        spec_path.read_text()
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp).resolve() / "preview"
        approval = _make_approval(
            result.current_version,
            result.latest_version,
            "upgrade_preview",
        )
        gen_result = generate(
            spec=spec,
            output=str(tmp_path),
            approval_record=approval,
            no_zip=True,
        )

        changed: list[str] = []
        for file_path in gen_result.files:
            abs_path = Path(file_path).resolve()
            rel = abs_path.relative_to(tmp_path)
            existing = agent_dir / rel
            if not existing.exists():
                changed.append(f"+ {rel} (new)")
            elif existing.read_text() != abs_path.read_text():
                changed.append(f"~ {rel} (modified)")

        skip = {".DS_Store"}
        for existing_file in agent_dir.rglob("*"):
            if not existing_file.is_file():
                continue
            if existing_file.name in skip:
                continue
            rel = existing_file.relative_to(agent_dir)
            new_file = tmp_path / rel
            if not new_file.exists():
                changed.append(f"- {rel} (removed)")

    result.changed_files = changed
    return result


def execute_upgrade(
    agent_dir: Path, *, backup: bool = True,
) -> UpgradeResult:
    """Execute an upgrade: backup then regenerate.

    Args:
        agent_dir: Path to the agent directory.
        backup: If True, create a backup before upgrading.
    """
    result = check_upgrade(agent_dir)
    if not result.needs_upgrade:
        return result

    spec_path = agent_dir / "agent_spec.yaml"
    spec: dict[str, object] = yaml.safe_load(
        spec_path.read_text()
    )

    backup_path_str: str | None = None
    if backup:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_dir = (
            agent_dir.parent / f"{agent_dir.name}.backup_{ts}"
        )
        shutil.copytree(agent_dir, backup_dir)
        backup_path_str = str(backup_dir)

    shutil.rmtree(agent_dir)

    approval = _make_approval(
        result.current_version,
        result.latest_version,
        "upgrade",
    )
    try:
        generate(
            spec=spec,
            output=str(agent_dir),
            approval_record=approval,
            no_zip=True,
        )
    except Exception:
        # Regeneration failed — restore from backup if available
        if backup_path_str and Path(backup_path_str).exists():
            if agent_dir.exists():
                shutil.rmtree(agent_dir)
            shutil.copytree(Path(backup_path_str), agent_dir)
        raise

    result.backup_path = backup_path_str
    return result
