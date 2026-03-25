"""Jinja2 template renderer for Agent Factory."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateRenderer:
    """Loads Jinja2 templates from a directory and renders them with a context dict.

    Args:
        template_dir: Root directory containing template sets (e.g. ``templates/``).
                      If ``None``, the default ``templates/`` directory adjacent to the
                      ``factory`` package is used. Pass an explicit path in tests.
    """

    def __init__(self, template_dir: Path | None = None) -> None:
        if template_dir is None:
            template_dir = Path(__file__).resolve().parent.parent.parent / "templates"
        self._template_dir = template_dir

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render_template(self, template_path: str, context: dict[str, object]) -> str:
        """Render a single template file and return the result as a string.

        Args:
            template_path: Path relative to *template_dir*, e.g.
                           ``"single_agent/CLAUDE.md.j2"``.
            context: Variables available inside the template.

        Returns:
            Rendered string content.

        Raises:
            jinja2.TemplateNotFound: If *template_path* does not exist.
            jinja2.UndefinedError: If the template references an undefined variable.
        """
        env = self._make_env(self._template_dir)
        template = env.get_template(template_path)
        return template.render(**context)

    def render_all(self, template_set: str, context: dict[str, object]) -> dict[str, str]:
        """Render every template inside a named template set directory.

        Args:
            template_set: Sub-directory name inside *template_dir*,
                          e.g. ``"single_agent"`` or ``"multi_agent"``.
            context: Variables available inside all templates.

        Returns:
            Dict mapping rendered output paths (relative, ``.j2`` suffix stripped)
            to rendered content strings.  Returns an empty dict if the template
            set directory does not exist or contains no templates.
        """
        set_dir = self._template_dir / template_set
        if not set_dir.is_dir():
            return {}

        env = self._make_env(self._template_dir)
        result: dict[str, str] = {}

        for template_file in sorted(set_dir.rglob("*")):
            if not template_file.is_file():
                continue

            # Build the path relative to template_dir so Jinja can load it.
            rel_from_root = template_file.relative_to(self._template_dir)
            # Build the output path relative to set_dir (no leading set name).
            rel_from_set = template_file.relative_to(set_dir)
            output_key = str(rel_from_set)

            # Strip .j2 suffix from output filename.
            if output_key.endswith(".j2"):
                output_key = output_key[:-3]

            template = env.get_template(str(rel_from_root))
            result[output_key] = template.render(**context)

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _make_env(template_dir: Path) -> Environment:
        """Return a Jinja2 Environment configured with StrictUndefined."""
        return Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
            autoescape=False,
        )
