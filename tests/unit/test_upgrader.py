"""Unit tests for factory.core.upgrader."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from factory.core.generator import generate
from factory.core.upgrader import (
    UpgradeResult,
    check_upgrade,
    execute_upgrade,
    preview_upgrade,
)

# ---------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------

VALID_SPEC: dict[str, object] = {
    "name": "test-bot",
    "description": "A test agent for upgrade tests",
    "type": "single",
}

VALID_APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "test-bot single-agent",
}


def _generate_agent(tmp_path: Path) -> Path:
    """Generate an agent and return its directory."""
    out = tmp_path / "test-bot"
    generate(
        spec=VALID_SPEC,
        output=str(out),
        approval_record=VALID_APPROVAL,
        no_zip=True,
    )
    return out


def _set_template_version(
    agent_dir: Path, version: str,
) -> None:
    """Overwrite template_version in meta.yaml."""
    meta_path = agent_dir / "meta.yaml"
    meta = yaml.safe_load(meta_path.read_text())
    meta["template_version"] = version
    meta_path.write_text(
        yaml.dump(meta, default_flow_style=False)
    )


# ---------------------------------------------------------------
# UpgradeResult
# ---------------------------------------------------------------


def test_upgrade_result_defaults() -> None:
    r = UpgradeResult(
        current_version="1.0.0",
        latest_version="1.1.0",
        needs_upgrade=True,
    )
    assert r.changed_files == []
    assert r.backup_path is None


# ---------------------------------------------------------------
# check_upgrade
# ---------------------------------------------------------------


def test_check_upgrade_detects_version_mismatch(
    tmp_path: Path,
) -> None:
    agent_dir = _generate_agent(tmp_path)
    _set_template_version(agent_dir, "0.9.0")
    result = check_upgrade(agent_dir)
    assert result.needs_upgrade is True
    assert result.current_version == "0.9.0"


def test_check_upgrade_current_returns_no_upgrade(
    tmp_path: Path,
) -> None:
    agent_dir = _generate_agent(tmp_path)
    result = check_upgrade(agent_dir)
    assert result.needs_upgrade is False
    assert result.current_version == result.latest_version


def test_check_upgrade_missing_meta_raises(
    tmp_path: Path,
) -> None:
    empty = tmp_path / "empty-agent"
    empty.mkdir()
    with pytest.raises(FileNotFoundError, match="meta.yaml"):
        check_upgrade(empty)


# ---------------------------------------------------------------
# preview_upgrade
# ---------------------------------------------------------------


def test_preview_upgrade_lists_changes(
    tmp_path: Path,
) -> None:
    agent_dir = _generate_agent(tmp_path)
    _set_template_version(agent_dir, "0.9.0")
    result = preview_upgrade(agent_dir)
    assert result.needs_upgrade is True
    assert len(result.changed_files) > 0


# ---------------------------------------------------------------
# execute_upgrade
# ---------------------------------------------------------------


def test_execute_upgrade_creates_backup(
    tmp_path: Path,
) -> None:
    agent_dir = _generate_agent(tmp_path)
    _set_template_version(agent_dir, "0.9.0")
    result = execute_upgrade(agent_dir, backup=True)
    assert result.backup_path is not None
    assert Path(result.backup_path).exists()


def test_execute_upgrade_updates_version(
    tmp_path: Path,
) -> None:
    agent_dir = _generate_agent(tmp_path)
    _set_template_version(agent_dir, "0.9.0")
    execute_upgrade(agent_dir, backup=False)
    meta = yaml.safe_load(
        (agent_dir / "meta.yaml").read_text()
    )
    assert meta["template_version"] == "1.0.1"
