"""Auxiliary CLI for Agent Factory utilities."""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from factory import __version__
from factory.registries.loader import RegistryLoader
from factory.schemas.validator import validate_spec

# Resolve the registry that ships with the package.
_BUILTIN_REGISTRY_DIR = (
    Path(__file__).resolve().parent.parent.parent / "registry"
)


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
