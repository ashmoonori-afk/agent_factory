"""Auxiliary CLI for Agent Factory utilities."""

from __future__ import annotations

from pathlib import Path

import click
import yaml

from factory import __version__
from factory.schemas.validator import validate_spec


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
    with open(path) as f:
        data: dict[str, object] = yaml.safe_load(f)

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
    click.echo("Built-in skills: (not yet loaded — Phase 4)")


@cli.command()
def personas() -> None:
    """List available built-in personas."""
    click.echo("Built-in personas: (not yet loaded — Phase 4)")
