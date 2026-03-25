"""Auxiliary CLI for Agent Factory utilities."""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from factory import __version__
from factory.registries.loader import RegistryLoader
from factory.schemas.validator import validate_spec


# Resolve the registry that ships with the package.
def _find_builtin_registry() -> Path:
    """Resolve registry — installed package data first, then dev layout."""
    try:
        from importlib.resources import files as _res_files
        candidate = Path(str(_res_files("factory").joinpath("registry")))
        if (candidate / "sources").is_dir():
            return candidate
    except (ModuleNotFoundError, TypeError):
        pass
    return Path(__file__).resolve().parent.parent.parent / "registry"


_BUILTIN_REGISTRY_DIR = _find_builtin_registry()


@click.group()
def cli() -> None:
    """Agent Factory — auxiliary utilities."""


@cli.command()
def version() -> None:
    """Print the Agent Factory version."""
    click.echo(f"agent-factory {__version__}")


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def validate(file: str) -> None:
    """Validate a spec YAML file against the schema."""
    path = Path(file)
    with open(path) as fh:
        data: dict[str, object] = yaml.safe_load(fh)

    errors = validate_spec(data)
    if errors:
        click.echo(f"Validation failed with {len(errors)} error(s):", err=True)
        for error in errors:
            click.echo(f"  - {error}", err=True)
        raise SystemExit(1)
    else:
        click.echo("Valid.")


@cli.command()
def skills() -> None:
    """List available built-in skills."""
    loader = RegistryLoader(_BUILTIN_REGISTRY_DIR)
    items = loader.list_skills()
    click.echo(f"{'ID':<20} {'POLICY':<8} DESCRIPTION")
    click.echo("-" * 72)
    for item in items:
        skill_id: str = item["id"]
        policy: str = item["policy"]
        description: str = item["description"]
        # Truncate long descriptions so the table stays readable.
        short_desc = description[:48] + "…" if len(description) > 48 else description
        click.echo(f"{skill_id:<20} {policy:<8} {short_desc}")


@cli.command()
@click.argument("agent_dir", type=click.Path(exists=True))
@click.option(
    "--preview",
    is_flag=True,
    help="Show what would change without upgrading.",
)
@click.option(
    "--no-backup",
    is_flag=True,
    help="Skip creating a backup.",
)
def upgrade(
    agent_dir: str, preview: bool, no_backup: bool,
) -> None:
    """Check for and apply template upgrades to a generated agent."""
    from factory.core.upgrader import (
        check_upgrade,
        execute_upgrade,
        preview_upgrade,
    )

    agent_path = Path(agent_dir)

    if preview:
        result = preview_upgrade(agent_path)
        click.echo(
            f"Current: {result.current_version}"
            f" → Latest: {result.latest_version}"
        )
        if result.changed_files:
            click.echo("Changes:")
            for f in result.changed_files:
                click.echo(f"  {f}")
        else:
            click.echo("No changes detected.")
        return

    result = check_upgrade(agent_path)
    if not result.needs_upgrade:
        click.echo(
            "Already up to date"
            f" (version {result.current_version})."
        )
        return

    click.echo(
        f"Upgrading {agent_path.name}:"
        f" {result.current_version}"
        f" → {result.latest_version}"
    )
    result = execute_upgrade(
        agent_path, backup=not no_backup,
    )
    if result.backup_path:
        click.echo(f"Backup: {result.backup_path}")
    click.echo("Upgrade complete.")


@cli.command("critique")
@click.argument("file", type=click.Path(exists=True))
def critique_cmd(file: str) -> None:
    """Evaluate an agent spec against best practices."""
    from factory.core.critique import critique

    path = Path(file)
    with open(path) as fh:
        spec: dict[str, object] = yaml.safe_load(fh)

    result = critique(spec)

    if result.warnings:
        click.echo("Warnings:")
        for w in result.warnings:
            click.echo(f"  ! {w}")
        click.echo()
    else:
        click.echo("No warnings -- spec looks good!\n")

    click.echo("Score:")
    for category, score in result.score.items():
        click.echo(f"  {category:<20} {score}/100")
    click.echo(
        f"  {'TOTAL':<20} "
        f"{result.total_score}/100 "
        f"(Grade: {result.grade})"
    )


@cli.command()
def personas() -> None:
    """List available built-in personas."""
    loader = RegistryLoader(_BUILTIN_REGISTRY_DIR)
    items = loader.list_personas()
    click.echo(f"{'ID':<16} {'TONE':<30} DESCRIPTION")
    click.echo("-" * 72)
    for item in items:
        persona_id: str = item["id"]
        tone: str = item["tone"]
        description: str = item["description"]
        short_desc = description[:24] + "…" if len(description) > 24 else description
        click.echo(f"{persona_id:<16} {tone:<30} {short_desc}")
