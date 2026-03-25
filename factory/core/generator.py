"""Orchestrator: validate → approve → render → build → zip → return result."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from factory.approval.records import ApprovalRecord
from factory.core.packager import create_zip
from factory.core.renderer import TemplateRenderer
from factory.core.repo_builder import RepoBuilder
from factory.schemas.validator import validate_spec

# ---------------------------------------------------------------------------
# Public exceptions
# ---------------------------------------------------------------------------


class SpecValidationError(Exception):
    """Raised when the agent spec fails schema validation."""


class ApprovalRequiredError(Exception):
    """Raised when the approval record is missing, invalid, or not APPROVED."""


class GenerationError(Exception):
    """Raised for unexpected errors during generation."""


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class GenerationResult:
    """Returned by :func:`generate` describing what was created.

    Attributes:
        output_path: Absolute path to the generated directory.
        zip_path: Absolute path to the ZIP archive, or ``None`` if ``no_zip=True``.
        file_count: Number of files written (excludes the ZIP itself).
        files: Sorted list of absolute file paths written to *output_path*.
    """

    output_path: str
    zip_path: str | None
    file_count: int
    files: list[str]


# ---------------------------------------------------------------------------
# Registry stubs (Phase 4 will replace these)
# ---------------------------------------------------------------------------


def _resolve_skills(skill_ids: list[str]) -> list[dict[str, str]]:
    """Stub: return skill ids as minimal dicts until Phase 4 registry is ready."""
    return [{"id": sid} for sid in skill_ids]


def _resolve_persona(persona: dict[str, object]) -> dict[str, object]:
    """Stub: pass persona through unchanged until Phase 4 registry is ready."""
    return persona


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


def generate(
    spec: dict[str, object],
    output: str,
    approval_record: dict[str, str],
    *,
    no_zip: bool = False,
) -> GenerationResult:
    """Generate a complete agent repository from a validated spec.

    Steps (in order):

    1. Validate *spec* against the agent_spec schema.
    2. Construct and validate the :class:`~factory.approval.records.ApprovalRecord`.
    3. Resolve skills and persona from the registry (stub in Phase 2).
    4. Select the Jinja2 template set based on ``spec["type"]``.
    5. Render all templates into a filename→content dict.
    6. Write every file to *output* directory.
    7. Write ``meta.yaml`` into *output*.
    8. Append one JSON line to ``approval_log.jsonl``.
    9. Create a ZIP archive of *output* (unless *no_zip* is ``True``).
    10. Return a :class:`GenerationResult`.

    Args:
        spec: Agent specification dict (must satisfy ``agent_spec`` JSON Schema).
        output: Destination directory path (created if absent).
        approval_record: Approval dict with keys ``decision``, ``timestamp``,
                         ``user_input``, ``action_type``, ``detail``.
        no_zip: If ``True``, skip ZIP creation.

    Returns:
        :class:`GenerationResult` describing generated artefacts.

    Raises:
        SpecValidationError: If *spec* fails schema validation.
        ApprovalRequiredError: If *approval_record* is invalid or not APPROVED.
        GenerationError: For unexpected errors during file creation.
    """
    # ------------------------------------------------------------------
    # Step 1 — Validate spec
    # ------------------------------------------------------------------
    errors = validate_spec(spec)
    if errors:
        raise SpecValidationError(
            f"Spec validation failed with {len(errors)} error(s):\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    # ------------------------------------------------------------------
    # Step 2 — Verify approval record
    # ------------------------------------------------------------------
    try:
        record = ApprovalRecord.from_dict(approval_record)
    except (KeyError, TypeError) as exc:
        raise ApprovalRequiredError(
            f"approval_record is missing required fields: {exc}"
        ) from exc

    approval_errors = record.validate()
    if approval_errors:
        raise ApprovalRequiredError(
            "approval_record is not valid:\n"
            + "\n".join(f"  - {e}" for e in approval_errors)
        )

    # ------------------------------------------------------------------
    # Step 3 — Compute approval hash + resolve registry stubs
    # ------------------------------------------------------------------
    approval_hash = ApprovalRecord.compute_hash(
        record.action_type, record.detail, record.timestamp
    )

    raw_skills = spec.get("skills")
    skill_ids: list[str] = [str(s) for s in (raw_skills if isinstance(raw_skills, list) else [])]
    _resolve_skills(skill_ids)

    raw_persona = spec.get("persona")
    persona_raw: dict[str, object] = raw_persona if isinstance(raw_persona, dict) else {}
    _resolve_persona(persona_raw)

    # ------------------------------------------------------------------
    # Step 4 — Select template set
    # ------------------------------------------------------------------
    agent_type = str(spec.get("type", "single"))
    template_set = "single_agent" if agent_type == "single" else "multi_agent"

    # ------------------------------------------------------------------
    # Step 5 — Render templates
    # ------------------------------------------------------------------
    renderer = TemplateRenderer()
    context: dict[str, object] = {
        "spec": spec,
        "name": spec.get("name", ""),
        "description": spec.get("description", ""),
        "type": agent_type,
        "skills": skill_ids,
        "persona": persona_raw,
        "approval_hash": approval_hash,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    rendered_files = renderer.render_all(template_set, context)

    # ------------------------------------------------------------------
    # Step 6 — Write files to output directory
    # ------------------------------------------------------------------
    output_dir = Path(output)
    try:
        builder = RepoBuilder()
        written = builder.build(rendered_files, output_dir)
    except OSError as exc:
        raise GenerationError(f"Failed to write files to {output_dir}: {exc}") from exc

    # ------------------------------------------------------------------
    # Step 7 — Write meta.yaml
    # ------------------------------------------------------------------
    meta: dict[str, object] = {
        "name": spec.get("name"),
        "description": spec.get("description"),
        "type": agent_type,
        "generated_at": context["generated_at"],
        "approval_hash": approval_hash,
        "factory_version": "1.0.0",
    }
    meta_path = output_dir / "meta.yaml"
    meta_path.write_text(yaml.dump(meta, default_flow_style=False), encoding="utf-8")
    written.append(str(meta_path.resolve()))

    # ------------------------------------------------------------------
    # Step 8 — Append to approval_log.jsonl
    # ------------------------------------------------------------------
    log_entry: dict[str, str] = {
        **record.to_dict(),
        "generated_at": str(context["generated_at"]),
    }
    log_path = output_dir / "approval_log.jsonl"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(log_entry) + "\n")
    written.append(str(log_path.resolve()))

    written_sorted = sorted(set(written))

    # ------------------------------------------------------------------
    # Step 9 — Create ZIP
    # ------------------------------------------------------------------
    zip_result: str | None = None
    if not no_zip:
        zip_path = create_zip(output_dir)
        zip_result = str(zip_path)

    # ------------------------------------------------------------------
    # Step 10 — Return result
    # ------------------------------------------------------------------
    return GenerationResult(
        output_path=str(output_dir.resolve()),
        zip_path=zip_result,
        file_count=len(written_sorted),
        files=written_sorted,
    )
