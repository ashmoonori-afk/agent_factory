"""Schema validation using jsonschema."""

from __future__ import annotations

from pathlib import Path

import jsonschema
import yaml


def _find_schema_dir() -> Path:
    """Resolve schema directory — installed package data first, then dev layout.

    The schema YAML files live in the top-level ``schemas/`` directory (NOT inside
    ``factory/schemas/``, which is a Python package containing validator.py).
    After ``pip install``, hatchling force-includes them into ``factory/schemas/``
    inside the wheel, so importlib.resources will find them there.  In dev mode
    (editable install or direct checkout) we fall back to the project-root path.
    """
    # Installed wheel: templates are force-included under factory/schemas/
    try:
        from importlib.resources import files as _res_files
        candidate = Path(str(_res_files("factory").joinpath("schemas")))
        # Must contain actual schema files, not just __init__.py
        if any(candidate.glob("*.schema.yaml")):
            return candidate
    except (ModuleNotFoundError, TypeError):
        pass
    # Dev layout: schemas/ sits next to the factory/ package
    return Path(__file__).resolve().parent.parent.parent / "schemas"


_SCHEMA_DIR = _find_schema_dir()


def load_schema(name: str) -> dict[str, object]:
    """Load a YAML schema file by name (without extension).

    Args:
        name: Schema name, e.g. "agent_spec" loads "agent_spec.schema.yaml"

    Returns:
        Parsed schema dict.

    Raises:
        FileNotFoundError: If schema file doesn't exist.
    """
    path = _SCHEMA_DIR / f"{name}.schema.yaml"
    with open(path) as f:
        schema: dict[str, object] = yaml.safe_load(f)
    return schema


def validate_spec(data: dict[str, object], schema_name: str = "agent_spec") -> list[str]:
    """Validate data against a named schema.

    Args:
        data: The data dict to validate.
        schema_name: Schema to validate against (default: "agent_spec").

    Returns:
        List of error messages. Empty list means valid.
    """
    schema = load_schema(schema_name)
    validator = jsonschema.Draft7Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path)
        prefix = f"{path}: " if path else ""
        errors.append(f"{prefix}{error.message}")
    return errors
