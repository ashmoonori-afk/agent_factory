"""CLI entry point for Agent Factory."""

import click


@click.group()
@click.version_option()
def cli() -> None:
    """Agent Factory — Generate AI agent repositories through conversation."""
