"""Regenerate golden-file fixtures. Run manually when templates change intentionally."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Allow running from project root: python tests/fixtures/regenerate_fixtures.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import factory  # noqa: E402

FIXTURE_DIR = Path(__file__).parent

SINGLE_SPEC: dict[str, object] = {
    "name": "fixture-single-agent",
    "description": "Golden file fixture for single agent",
    "type": "single",
    "skills": ["csv-reader"],
    "persona": {"tone": "professional", "language": "en"},
    "policies": {
        "deny": ["delete_file", "send_email"],
        "ask": ["execute_sql"],
        "allow": ["*"],
    },
}

MULTI_SPEC: dict[str, object] = {
    "name": "fixture-multi-agent",
    "description": "Golden file fixture for multi agent",
    "type": "multi",
    "agents": [
        {"id": "reviewer", "role": "reviews code", "next": ["fixer"]},
        {"id": "fixer", "role": "fixes issues"},
    ],
    "topology": {"entry": "reviewer", "max_loops": 2},
    "skills": ["code-reviewer"],
    "persona": {"tone": "technical", "language": "en"},
}

APPROVAL: dict[str, str] = {
    "decision": "APPROVED",
    "timestamp": "2026-01-01T00:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "fixture generation",
}

# Files (relative to the output directory) that contain non-deterministic data
# (timestamps, etc.) — excluded from fixtures so golden comparison stays stable.
NON_DETERMINISTIC = [
    "meta.yaml",
    "approval_log.jsonl",
    "policies/approval_log.jsonl",
]


def main() -> None:
    for name, spec, subdir in [
        ("single", SINGLE_SPEC, "single_agent"),
        ("multi", MULTI_SPEC, "multi_agent"),
    ]:
        out = FIXTURE_DIR / subdir
        if out.exists():
            shutil.rmtree(out)
        result = factory.generate(
            spec=spec, output=str(out), approval_record=APPROVAL, no_zip=True
        )
        # Remove non-deterministic files so golden comparison stays stable
        for rel in NON_DETERMINISTIC:
            p = out / rel
            if p.exists():
                p.unlink()
        print(f"Regenerated {name}: {result.file_count} files at {out}")


if __name__ == "__main__":
    main()
