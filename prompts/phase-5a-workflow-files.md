# Phase 5A: CLAUDE.md + CODEX.md Final Versions

> **Depends on**: phase-3b + phase-4a
> **Read first**: `00-overview.md`, `CLAUDE.md`, `CODEX.md`

## Objective

Finalize the Agent Factory's own CLAUDE.md and CODEX.md workflow files. These are the actual runtime instruction files — they must be tested end-to-end.

---

## Task 1: Verify CLAUDE.md

The CLAUDE.md at project root has already been rewritten (Phase 0). Verify it works by checking:

1. Phase 1-4 (Interview → Approve): All questions, defaults, and approval gate text are correct.
2. Phase 5 (Generate): The Python invocation pattern works:
   ```bash
   python3 -c "import factory; result = factory.generate(...)"
   ```
3. Phase 6 (Deliver): Next steps correctly reference opening in Claude Code.
4. Safety rules are complete and match PRD Section 11.
5. Default DENY list matches PRD Section 11.2.
6. No references to old CLI architecture (no `factory create`, no `click.prompt()`, no stdin).

**Execution pattern difference:**
- CLAUDE.md uses `python3 -c "..."` via Bash tool (Claude Code convention).
- CODEX.md uses inline Python execution block (Codex convention).

## Task 2: Verify CODEX.md

Same checks as CLAUDE.md but for Codex:
1. Tool references are Codex-appropriate.
2. Python execution pattern works in Codex context.
3. No Claude Code-specific features referenced.

## Task 3: Manual Test (Claude Code)

Run the full workflow manually:
1. Open the agent-factory folder in Claude Code.
2. Say: "I want to create a data analysis agent."
3. Verify: LLM follows interview → approve → generate workflow.
4. Verify: `factory.generate()` runs and produces correct output.
5. Verify: Generated repo has CLAUDE.md, skills/*.md, policy.yaml.

## Task 4: Manual Test (Codex)

Same test in Codex environment.

---

## Verification

- CLAUDE.md contains no references to: `factory create`, `click`, `stdin`, `main.py`, `requirements.txt`
- CLAUDE.md references `factory.generate()` Python call
- Both files enforce the 6-phase workflow in correct order
- Approval gate text matches PRD Section 11.3
