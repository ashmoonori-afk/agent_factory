# Phase 4: Registry — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the built-in registry of skills and personas, implement the `RegistryLoader`, populate 10 skill `.md` files and 4 persona `.yaml` files, and wire `factory skills` / `factory personas` CLI commands to serve live data.

**Architecture:** Registry files live under `registry/` at the project root, organised into `builtin_skills/` (`.md`) and `builtin_personas/` (`.yaml`) subdirectories, with a `sources/registry.yaml` manifest that points the loader at those directories. `RegistryLoader` reads the manifest on init and exposes four public methods; the CLI imports the loader and replaces its Phase 1 placeholders. Everything is resolved relative to the registry manifest so the package stays relocatable.

**Tech Stack:** Python 3.10+, PyYAML (already a dependency), click (already a dependency), pytest, ruff, mypy

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `factory/registries/loader.py` | `RegistryLoader` class — list/get skills and personas |
| Create | `registry/sources/registry.yaml` | Manifest pointing to builtin dirs |
| Create | `registry/builtin_skills/sql-executor.md` | ASK — Execute SQL queries |
| Create | `registry/builtin_skills/csv-reader.md` | ALLOW — Read and analyze CSV files |
| Create | `registry/builtin_skills/file-reader.md` | ALLOW — Read local text files |
| Create | `registry/builtin_skills/file-writer.md` | ASK — Write local text files |
| Create | `registry/builtin_skills/web-search.md` | ASK — Search the web |
| Create | `registry/builtin_skills/json-parser.md` | ALLOW — Parse and query JSON |
| Create | `registry/builtin_skills/text-summarizer.md` | ALLOW — Summarize text |
| Create | `registry/builtin_skills/code-reviewer.md` | ALLOW — Review code |
| Create | `registry/builtin_skills/code-generator.md` | ASK — Generate code |
| Create | `registry/builtin_skills/shell-executor.md` | DENY — Execute shell commands |
| Create | `registry/builtin_personas/professional.yaml` | Formal, precise |
| Create | `registry/builtin_personas/friendly.yaml` | Casual, approachable |
| Create | `registry/builtin_personas/technical.yaml` | Detailed, jargon-ok |
| Create | `registry/builtin_personas/minimal.yaml` | Brief, no filler |
| Modify | `factory/cli/main.py` | Wire skills + personas commands to RegistryLoader |
| Create | `tests/unit/test_registry.py` | Registry loader unit tests |

---

## Task 1: Registry Loader (TDD)

**Files:**
- Create: `factory/registries/loader.py`
- Test: `tests/unit/test_registry.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/unit/test_registry.py`:

```python
"""Unit tests for RegistryLoader."""

from __future__ import annotations

from pathlib import Path

import pytest

from factory.registries.loader import RegistryLoader

# Resolve the registry directory relative to the project root.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_REGISTRY_DIR = _PROJECT_ROOT / "registry"


@pytest.fixture()
def loader() -> RegistryLoader:
    return RegistryLoader(_REGISTRY_DIR)


# ---------------------------------------------------------------------------
# list_skills
# ---------------------------------------------------------------------------


def test_list_skills_returns_ten_items(loader: RegistryLoader) -> None:
    skills = loader.list_skills()
    assert len(skills) == 10


def test_list_skills_items_have_required_keys(loader: RegistryLoader) -> None:
    for skill in loader.list_skills():
        assert "id" in skill, f"Missing 'id' in {skill}"
        assert "name" in skill, f"Missing 'name' in {skill}"
        assert "description" in skill, f"Missing 'description' in {skill}"
        assert "policy" in skill, f"Missing 'policy' in {skill}"


def test_list_skills_policies_are_valid(loader: RegistryLoader) -> None:
    valid_policies = {"DENY", "ASK", "ALLOW"}
    for skill in loader.list_skills():
        assert skill["policy"] in valid_policies, (
            f"Skill {skill['id']} has invalid policy {skill['policy']!r}"
        )


def test_list_skills_contains_expected_ids(loader: RegistryLoader) -> None:
    ids = {s["id"] for s in loader.list_skills()}
    expected = {
        "sql-executor",
        "csv-reader",
        "file-reader",
        "file-writer",
        "web-search",
        "json-parser",
        "text-summarizer",
        "code-reviewer",
        "code-generator",
        "shell-executor",
    }
    assert ids == expected


def test_list_skills_shell_executor_is_deny(loader: RegistryLoader) -> None:
    skills_by_id = {s["id"]: s for s in loader.list_skills()}
    assert skills_by_id["shell-executor"]["policy"] == "DENY"


def test_list_skills_csv_reader_is_allow(loader: RegistryLoader) -> None:
    skills_by_id = {s["id"] for s in loader.list_skills() if s["policy"] == "ALLOW"}
    assert "csv-reader" in skills_by_id


# ---------------------------------------------------------------------------
# get_skill
# ---------------------------------------------------------------------------


def test_get_skill_returns_string(loader: RegistryLoader) -> None:
    content = loader.get_skill("csv-reader")
    assert isinstance(content, str)
    assert len(content) > 0


def test_get_skill_returns_markdown_content(loader: RegistryLoader) -> None:
    content = loader.get_skill("sql-executor")
    assert "# Skill:" in content
    assert "## Policy" in content
    assert "## Instructions" in content


def test_get_skill_returns_correct_skill(loader: RegistryLoader) -> None:
    content = loader.get_skill("shell-executor")
    assert "shell" in content.lower() or "Shell" in content


def test_get_skill_raises_for_unknown_id(loader: RegistryLoader) -> None:
    with pytest.raises(KeyError, match="unknown-skill"):
        loader.get_skill("unknown-skill")


def test_get_skill_all_ten_are_readable(loader: RegistryLoader) -> None:
    for skill in loader.list_skills():
        content = loader.get_skill(skill["id"])
        assert len(content) > 100, (
            f"Skill {skill['id']} content is too short ({len(content)} chars)"
        )


# ---------------------------------------------------------------------------
# list_personas
# ---------------------------------------------------------------------------


def test_list_personas_returns_four_items(loader: RegistryLoader) -> None:
    personas = loader.list_personas()
    assert len(personas) == 4


def test_list_personas_items_have_required_keys(loader: RegistryLoader) -> None:
    for persona in loader.list_personas():
        assert "id" in persona, f"Missing 'id' in {persona}"
        assert "tone" in persona, f"Missing 'tone' in {persona}"
        assert "description" in persona, f"Missing 'description' in {persona}"


def test_list_personas_contains_expected_ids(loader: RegistryLoader) -> None:
    ids = {p["id"] for p in loader.list_personas()}
    assert ids == {"professional", "friendly", "technical", "minimal"}


# ---------------------------------------------------------------------------
# get_persona
# ---------------------------------------------------------------------------


def test_get_persona_returns_dict(loader: RegistryLoader) -> None:
    persona = loader.get_persona("professional")
    assert isinstance(persona, dict)


def test_get_persona_has_required_fields(loader: RegistryLoader) -> None:
    persona = loader.get_persona("professional")
    assert "id" in persona
    assert "tone" in persona
    assert "language" in persona
    assert "description" in persona
    assert "custom_instructions" in persona


def test_get_persona_raises_for_unknown_id(loader: RegistryLoader) -> None:
    with pytest.raises(KeyError, match="nonexistent"):
        loader.get_persona("nonexistent")


def test_get_persona_all_four_are_readable(loader: RegistryLoader) -> None:
    for persona in loader.list_personas():
        data = loader.get_persona(persona["id"])
        assert data["id"] == persona["id"]
        assert data["custom_instructions"], (
            f"Persona {persona['id']} has empty custom_instructions"
        )


# ---------------------------------------------------------------------------
# Default registry_dir resolution
# ---------------------------------------------------------------------------


def test_loader_default_registry_dir_resolves() -> None:
    """RegistryLoader with no args should find the built-in registry."""
    loader = RegistryLoader()
    skills = loader.list_skills()
    assert len(skills) == 10
```

- [ ] **Step 2: Run tests — confirm they fail**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/unit/test_registry.py -v 2>&1 | head -40
```

Expected: `ModuleNotFoundError` or `ImportError` for `factory.registries.loader`.

- [ ] **Step 3: Create the registry manifest and directory skeleton**

```bash
mkdir -p /Users/MoonGwanghoon/hoops/agent-factory/registry/builtin_skills
mkdir -p /Users/MoonGwanghoon/hoops/agent-factory/registry/builtin_personas
mkdir -p /Users/MoonGwanghoon/hoops/agent-factory/registry/sources
```

Create `registry/sources/registry.yaml`:

```yaml
version: "1.0"
skills:
  builtin_dir: "../builtin_skills"
  items:
    - sql-executor
    - csv-reader
    - file-reader
    - file-writer
    - web-search
    - json-parser
    - text-summarizer
    - code-reviewer
    - code-generator
    - shell-executor
personas:
  builtin_dir: "../builtin_personas"
  items:
    - professional
    - friendly
    - technical
    - minimal
```

- [ ] **Step 4: Implement `factory/registries/loader.py`**

```python
"""Registry loader — resolves built-in skills and personas from disk."""

from __future__ import annotations

from pathlib import Path

import yaml

# Default: registry/ sits next to the factory/ package at the project root.
_DEFAULT_REGISTRY_DIR = Path(__file__).resolve().parent.parent.parent / "registry"

# Skill frontmatter is parsed from the first H1 and H2 lines of each .md file
# rather than a separate YAML block, keeping skill files self-contained.
_POLICY_TAG = "Level:"


def _parse_skill_frontmatter(skill_id: str, content: str) -> dict[str, str]:
    """Extract id, name, description, and policy from .md content.

    The format expected is:
        # Skill: <Display Name>
        ## When to Use
        <description lines>
        ## Policy
        Level: <DENY|ASK|ALLOW>
    """
    name = skill_id  # fallback
    description = ""
    policy = "ALLOW"  # fallback

    lines = content.splitlines()
    in_when_to_use = False
    desc_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Title line: # Skill: Display Name
        if stripped.startswith("# Skill:"):
            name = stripped[len("# Skill:"):].strip()
            in_when_to_use = False

        # Section headers
        elif stripped.startswith("## When to Use"):
            in_when_to_use = True

        elif stripped.startswith("##"):
            in_when_to_use = False

        # Collect "When to Use" body as description
        elif in_when_to_use and stripped:
            desc_lines.append(stripped)

        # Policy level line
        elif stripped.startswith(_POLICY_TAG):
            policy = stripped[len(_POLICY_TAG):].strip().split()[0].upper()

    description = " ".join(desc_lines)

    return {
        "id": skill_id,
        "name": name,
        "description": description,
        "policy": policy,
    }


class RegistryLoader:
    """Load built-in skills and personas from the registry directory.

    Args:
        registry_dir: Path to the registry root (the directory that contains
            ``sources/registry.yaml``). Defaults to the built-in registry
            shipped with the package.
    """

    def __init__(self, registry_dir: Path | None = None) -> None:
        self._registry_dir = (registry_dir or _DEFAULT_REGISTRY_DIR).resolve()
        manifest_path = self._registry_dir / "sources" / "registry.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Registry manifest not found: {manifest_path}"
            )
        with open(manifest_path) as fh:
            manifest: dict[str, object] = yaml.safe_load(fh)

        skills_cfg = manifest.get("skills", {})
        assert isinstance(skills_cfg, dict)
        skills_dir_rel: str = skills_cfg.get("builtin_dir", "../builtin_skills")  # type: ignore[assignment]
        self._skills_dir = (
            self._registry_dir / "sources" / skills_dir_rel
        ).resolve()
        self._skill_ids: list[str] = list(skills_cfg.get("items", []))  # type: ignore[arg-type]

        personas_cfg = manifest.get("personas", {})
        assert isinstance(personas_cfg, dict)
        personas_dir_rel: str = personas_cfg.get("builtin_dir", "../builtin_personas")  # type: ignore[assignment]
        self._personas_dir = (
            self._registry_dir / "sources" / personas_dir_rel
        ).resolve()
        self._persona_ids: list[str] = list(personas_cfg.get("items", []))  # type: ignore[arg-type]

        # Eagerly cache parsed frontmatter so list_* calls are cheap.
        self._skill_meta: dict[str, dict[str, str]] = {}
        self._skill_content: dict[str, str] = {}
        self._persona_meta: dict[str, dict[str, str]] = {}
        self._persona_data: dict[str, dict[str, object]] = {}

        self._load_skills()
        self._load_personas()

    # ------------------------------------------------------------------
    # Private loading helpers
    # ------------------------------------------------------------------

    def _load_skills(self) -> None:
        for skill_id in self._skill_ids:
            path = self._skills_dir / f"{skill_id}.md"
            if not path.exists():
                raise FileNotFoundError(
                    f"Skill file not found for '{skill_id}': {path}"
                )
            content = path.read_text(encoding="utf-8")
            self._skill_content[skill_id] = content
            self._skill_meta[skill_id] = _parse_skill_frontmatter(skill_id, content)

    def _load_personas(self) -> None:
        for persona_id in self._persona_ids:
            path = self._personas_dir / f"{persona_id}.yaml"
            if not path.exists():
                raise FileNotFoundError(
                    f"Persona file not found for '{persona_id}': {path}"
                )
            with open(path) as fh:
                data: dict[str, object] = yaml.safe_load(fh)
            self._persona_data[persona_id] = data
            self._persona_meta[persona_id] = {
                "id": str(data.get("id", persona_id)),
                "tone": str(data.get("tone", "")),
                "description": str(data.get("description", "")),
            }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_skills(self) -> list[dict[str, str]]:
        """Return summary metadata for all registered skills.

        Returns:
            List of dicts with keys: ``id``, ``name``, ``description``, ``policy``.
            Order matches the registry manifest.
        """
        return [self._skill_meta[sid] for sid in self._skill_ids]

    def get_skill(self, skill_id: str) -> str:
        """Return the raw Markdown content for a skill.

        Args:
            skill_id: The skill identifier, e.g. ``"csv-reader"``.

        Returns:
            Full `.md` file contents as a string.

        Raises:
            KeyError: If `skill_id` is not registered.
        """
        if skill_id not in self._skill_content:
            raise KeyError(skill_id)
        return self._skill_content[skill_id]

    def list_personas(self) -> list[dict[str, str]]:
        """Return summary metadata for all registered personas.

        Returns:
            List of dicts with keys: ``id``, ``tone``, ``description``.
            Order matches the registry manifest.
        """
        return [self._persona_meta[pid] for pid in self._persona_ids]

    def get_persona(self, persona_id: str) -> dict[str, object]:
        """Return the full parsed YAML dict for a persona.

        Args:
            persona_id: The persona identifier, e.g. ``"professional"``.

        Returns:
            Parsed YAML dict with keys: ``id``, ``tone``, ``language``,
            ``description``, ``custom_instructions``.

        Raises:
            KeyError: If `persona_id` is not registered.
        """
        if persona_id not in self._persona_data:
            raise KeyError(persona_id)
        return self._persona_data[persona_id]
```

- [ ] **Step 5: Run tests — confirm they still fail (no skill/persona files yet)**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/unit/test_registry.py -v 2>&1 | head -30
```

Expected: `FileNotFoundError` — skill and persona files are not created yet. The loader itself imports cleanly.

- [ ] **Step 6: Run ruff and mypy on the loader only**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m ruff check factory/registries/loader.py
.venv/bin/python -m mypy factory/registries/loader.py --strict
```

Expected: No errors.

- [ ] **Step 7: Commit loader + manifest skeleton**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/registries/loader.py registry/sources/registry.yaml tests/unit/test_registry.py
git commit -m "$(cat <<'EOF'
feat(registry): implement RegistryLoader and add failing tests

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Built-in Skills (10 .md files)

**Files:**
- Create: `registry/builtin_skills/sql-executor.md`
- Create: `registry/builtin_skills/csv-reader.md`
- Create: `registry/builtin_skills/file-reader.md`
- Create: `registry/builtin_skills/file-writer.md`
- Create: `registry/builtin_skills/web-search.md`
- Create: `registry/builtin_skills/json-parser.md`
- Create: `registry/builtin_skills/text-summarizer.md`
- Create: `registry/builtin_skills/code-reviewer.md`
- Create: `registry/builtin_skills/code-generator.md`
- Create: `registry/builtin_skills/shell-executor.md`

- [ ] **Step 1: Create `registry/builtin_skills/sql-executor.md`**

```markdown
# Skill: SQL Executor

## When to Use
Use this skill when the user needs to run a SELECT, INSERT, UPDATE, DELETE, or DDL statement against a database. Applies to SQLite, PostgreSQL, MySQL, and compatible engines.

## Policy
Level: ASK
Always ask the user for explicit permission before executing any SQL statement. Show the exact SQL that will be run and the target database before proceeding.

## Instructions
1. Identify the target database connection string or file path from the user's request or environment.
2. Parse the requested operation to determine whether it is read-only (SELECT) or mutating (INSERT, UPDATE, DELETE, DDL).
3. Present the exact SQL statement and the target database to the user and request confirmation.
4. Upon approval, execute the statement using the appropriate database driver.
5. Return the full result set (for SELECT) or affected row count (for mutations) to the user.
6. If execution raises an error, display the full error message and offer to debug.

## Constraints
- Never execute a SQL statement without showing it to the user first.
- Never run DROP DATABASE or DROP SCHEMA without an additional explicit confirmation step.
- Never include credentials (passwords, API tokens) in logged output.
- Limit SELECT result sets to 500 rows by default; paginate or summarize beyond that.
- Do not infer connection details from environment variables without telling the user which variable is being read.

## Examples
User: "Run SELECT * FROM orders WHERE status = 'pending' on orders.db"
Agent: "I will execute the following on orders.db — please confirm:
  SELECT * FROM orders WHERE status = 'pending';
Approve? (yes/no)"
User: "yes"
Agent: [returns result table]

User: "Delete all rows from the sessions table"
Agent: "I will execute: DELETE FROM sessions; on [database]. This will permanently remove all rows. Approve? (yes/no)"
```

- [ ] **Step 2: Create `registry/builtin_skills/csv-reader.md`**

```markdown
# Skill: CSV Reader

## When to Use
Use this skill when the user wants to load, inspect, filter, aggregate, or summarize data stored in a CSV or TSV file. No database connection is required.

## Policy
Level: ALLOW
Reading CSV files is a safe, non-destructive operation and does not require user confirmation.

## Instructions
1. Receive the file path (or URL) from the user's request.
2. Detect the delimiter automatically (comma, tab, semicolon) by inspecting the first line.
3. Load the file into an in-memory data structure. For files larger than 50 MB, read in chunks and warn the user.
4. Report the number of rows, columns, column names, and inferred data types.
5. Perform the requested operation: filter rows, compute aggregates, produce a summary, or return sample rows.
6. Present results in a clear tabular or bullet-point format.
7. If the file is malformed (encoding errors, mismatched columns), report the first problematic line and offer to skip bad rows.

## Constraints
- Never write to or overwrite the source file.
- Limit preview output to 20 rows unless the user requests more.
- Handle UTF-8 and Latin-1 encodings; raise a clear error for unsupported encodings.
- Do not load files from remote URLs without telling the user the exact URL being fetched.

## Examples
User: "Show me the first 5 rows of sales.csv"
Agent: [reads file, prints header + 5 rows as a table]

User: "What is the average revenue per region in sales.csv?"
Agent: [loads file, groups by region column, computes mean, returns table]
```

- [ ] **Step 3: Create `registry/builtin_skills/file-reader.md`**

```markdown
# Skill: File Reader

## When to Use
Use this skill when the user needs to read the content of a local text-based file — source code, configuration files, Markdown, JSON, YAML, log files, or plain text. Does not apply to binary formats (images, PDFs, Office documents).

## Policy
Level: ALLOW
Reading files is non-destructive. No confirmation is required, but the agent must state which file it is reading.

## Instructions
1. Resolve the file path relative to the current working directory if not absolute.
2. Confirm the file exists; if not, report the missing path clearly.
3. Detect the file's encoding (default UTF-8). Warn if a BOM or non-UTF-8 encoding is detected.
4. Read the file contents and return them to the user, labelling the output with the filename.
5. For files larger than 1 MB, summarize rather than returning the full content, and offer to return sections on request.
6. Apply syntax highlighting hints in fenced code blocks when the file extension is recognizable.

## Constraints
- Never read files outside the project root without user confirmation.
- Do not read files whose extensions suggest binary content (.exe, .bin, .png, .jpg, .pdf, .zip).
- Never display credentials found in files without masking them (e.g., replace actual secrets with `***`).
- Return at most 500 lines by default; offer pagination for larger files.

## Examples
User: "Read config/settings.yaml"
Agent: [reads file, returns contents in a YAML fenced block]

User: "What does src/main.py contain?"
Agent: [reads file, returns contents in a Python fenced block, reports line count]
```

- [ ] **Step 4: Create `registry/builtin_skills/file-writer.md`**

```markdown
# Skill: File Writer

## When to Use
Use this skill when the user needs to create a new file, overwrite an existing file, or append content to a file on the local filesystem.

## Policy
Level: ASK
Writing to disk is a mutating operation. Always show the user the target path, the operation type (create/overwrite/append), and the first 20 lines of content before proceeding.

## Instructions
1. Determine the target file path and operation type (create, overwrite, append) from the user's request.
2. Check whether the file already exists.
   - If it exists and the operation is overwrite, warn the user that existing content will be replaced.
   - If it exists and the operation is append, confirm the append position.
3. Present the target path, operation, and a preview of the content to the user and request confirmation.
4. Upon approval, perform the write operation using UTF-8 encoding.
5. Report the number of bytes and lines written, and confirm success.
6. If the write fails (permission denied, disk full), report the exact OS error.

## Constraints
- Never write to system directories (/etc, /usr, /bin, /sbin, /System, C:\Windows) without explicit user instruction.
- Never overwrite .env files that contain credentials without a second confirmation.
- Always create parent directories if they do not exist, and inform the user.
- Do not write more than 10 MB in a single operation without confirmation.

## Examples
User: "Write the following Python code to utils/helper.py: ..."
Agent: "I will create utils/helper.py with the following content (first 20 lines shown):
  [preview]
Approve? (yes/no)"
User: "yes"
Agent: "Written 42 lines (1,204 bytes) to utils/helper.py."

User: "Append a newline and '# END' to README.md"
Agent: "I will append to README.md. Approve? (yes/no)"
```

- [ ] **Step 5: Create `registry/builtin_skills/web-search.md`**

```markdown
# Skill: Web Search

## When to Use
Use this skill when the user needs current information from the internet — news, documentation, pricing, product details, or any fact that may have changed after the model's training cutoff.

## Policy
Level: ASK
Web search sends a query to an external service. Confirm the exact query string with the user before executing, especially if the query contains personal or sensitive terms.

## Instructions
1. Extract the search intent from the user's message and formulate a concise, specific query string.
2. Present the query to the user and ask for confirmation before sending it to the search API.
3. Execute the search using the configured search provider (e.g., Brave Search, SerpAPI, or a browser tool).
4. Return the top 5 results: title, URL, and a one-sentence snippet.
5. If the user wants to read a specific result, use the File Reader or an HTTP fetch skill to retrieve the page content.
6. Cite all sources clearly — never paraphrase search results as original knowledge.

## Constraints
- Never issue more than 10 search requests per user turn without explicit approval.
- Do not send queries containing passwords, API keys, or personal identifiable information (PII).
- Always attribute content to its source URL.
- If no results are found, say so clearly rather than fabricating information.
- Respect robots.txt when fetching full page content after a search.

## Examples
User: "What is the latest version of Python?"
Agent: "I will search for: 'latest Python version release 2025' — approve? (yes/no)"
User: "yes"
Agent: [returns top 5 results with titles, URLs, snippets]

User: "Search for 'FastAPI vs Flask performance 2025'"
Agent: "Confirm search: 'FastAPI vs Flask performance 2025'? (yes/no)"
```

- [ ] **Step 6: Create `registry/builtin_skills/json-parser.md`**

```markdown
# Skill: JSON Parser

## When to Use
Use this skill when the user provides a JSON string, a JSON file path, or a URL returning JSON, and wants to extract, query, filter, transform, or validate the data.

## Policy
Level: ALLOW
Parsing JSON is a read-only, in-memory operation and does not require user confirmation.

## Instructions
1. Accept JSON input as a string, a file path, or a URL.
   - For strings, parse directly.
   - For file paths, read the file first (see File Reader skill for constraints).
   - For URLs, fetch the response body.
2. Validate that the input is well-formed JSON. Report parse errors with line and column numbers.
3. Apply the user's query:
   - Key lookup: extract a specific field or nested field using dot-notation (e.g., `user.address.city`).
   - Array filter: return elements matching a predicate.
   - Aggregation: count, sum, min, max over a numeric field.
   - Schema inspection: list all top-level keys and their types.
4. Return the result in a formatted JSON fenced block or as a human-readable summary.
5. For large JSON payloads (> 10,000 keys or > 1 MB), summarize structure first and offer to drill down.

## Constraints
- Do not load JSON from URLs without informing the user of the URL being fetched.
- Never mutate the source JSON; all operations are read-only.
- For malformed JSON, show the exact parse error and the offending line rather than guessing.
- Limit array output to 50 items by default; paginate or summarize beyond that.

## Examples
User: "Extract the 'email' field from this JSON: {\"user\": {\"name\": \"Alice\", \"email\": \"alice@example.com\"}}"
Agent: "alice@example.com"

User: "List all keys in response.json"
Agent: [reads file, returns top-level keys and their types]
```

- [ ] **Step 7: Create `registry/builtin_skills/text-summarizer.md`**

```markdown
# Skill: Text Summarizer

## When to Use
Use this skill when the user wants to condense a long piece of text — an article, a document, a conversation transcript, code comments, or a meeting log — into a shorter, accurate summary.

## Policy
Level: ALLOW
Summarization is a purely generative, non-destructive operation. No confirmation is required.

## Instructions
1. Receive the text to summarize. Accept it as a direct paste, a file path, or a URL.
2. Identify the summarization target:
   - **Brief** (1-3 sentences): key point only.
   - **Standard** (1 paragraph): main ideas and supporting points.
   - **Structured** (bullet list): one bullet per major topic.
   - **Executive** (title + bullets + action items): for business documents.
   Default to Standard if the user does not specify.
3. Preserve factual accuracy. Do not introduce information not present in the source.
4. Maintain the original language of the source text unless the user requests translation.
5. If the text exceeds 100,000 tokens, split into sections, summarize each, then produce a meta-summary.
6. Return the summary clearly labelled, followed by the word count reduction (e.g., "Reduced from 2,400 to 180 words").

## Constraints
- Never fabricate facts, statistics, names, or dates that are not in the source text.
- Never omit content that contradicts the user's assumed position — summarize neutrally.
- Do not reproduce more than 150 consecutive words verbatim from copyrighted material.
- Always indicate the summarization mode used (Brief/Standard/Structured/Executive).

## Examples
User: "Summarize this article in 3 bullet points: [article text]"
Agent: [returns 3 concise bullets capturing the main points, labels as Structured]

User: "Give me an executive summary of the Q3 report: [document]"
Agent: [returns title, 4-5 bullet points, and a list of recommended actions]
```

- [ ] **Step 8: Create `registry/builtin_skills/code-reviewer.md`**

```markdown
# Skill: Code Reviewer

## When to Use
Use this skill when the user submits code and wants feedback on correctness, style, performance, security vulnerabilities, test coverage, or adherence to best practices. Applies to any programming language.

## Policy
Level: ALLOW
Code review is a read-only analysis operation. No confirmation is required.

## Instructions
1. Identify the programming language from the file extension, shebang line, or explicit user statement.
2. Parse the code and perform a multi-dimensional review:
   a. **Correctness**: logic errors, off-by-one errors, null/None dereferences, unhandled exceptions.
   b. **Security**: SQL injection, XSS, hardcoded secrets, insecure deserialization, path traversal.
   c. **Performance**: O(n²) loops that could be O(n), unnecessary database queries, memory leaks.
   d. **Style**: naming conventions, line length, missing docstrings, dead code.
   e. **Test coverage**: untested branches, missing edge cases.
3. Structure feedback as:
   - **Critical** (must fix): bugs, security vulnerabilities.
   - **Recommended** (should fix): performance, important style issues.
   - **Optional** (nice to have): minor style, naming.
4. For each finding, provide:
   - The line number(s).
   - A clear explanation of the problem.
   - A concrete suggested fix with corrected code.
5. Conclude with a brief overall assessment (1-2 sentences).

## Constraints
- Never execute or run the code being reviewed.
- Do not rewrite the entire codebase — focus on targeted, actionable feedback.
- Flag hardcoded secrets immediately as Critical findings, even if the rest of the review is Optional.
- Limit the review to 200 lines of feedback; if the code is very large, review the most critical sections first and offer to continue.
- Respect language idioms — do not apply Python conventions to Go code, for example.

## Examples
User: "Review this Python function: [code]"
Agent: [returns categorized findings with line numbers, explanations, and suggested fixes]

User: "Is there a SQL injection vulnerability in this code? [code]"
Agent: [identifies parameterized query issues, shows vulnerable line, provides corrected version]
```

- [ ] **Step 9: Create `registry/builtin_skills/code-generator.md`**

```markdown
# Skill: Code Generator

## When to Use
Use this skill when the user provides requirements and wants working code produced: a function, a class, a module, a script, a configuration file, a test suite, or a complete feature.

## Policy
Level: ASK
Generated code will typically be written to disk. Confirm the target language, output path, and high-level approach with the user before generating substantial code (> 30 lines).

## Instructions
1. Clarify requirements if ambiguous before generating code:
   - Target language and version.
   - Intended output (function, class, script, module).
   - Existing code style or conventions to match (ask for a sample if available).
   - Whether tests should be included.
2. For generation requests > 30 lines, present the plan (function signatures, class layout, data flow) and ask for confirmation before writing the full implementation.
3. Generate clean, idiomatic code:
   - Follow language conventions (PEP 8 for Python, gofmt for Go, Prettier defaults for JS/TS).
   - Include type annotations where the language supports them.
   - Add docstrings/JSDoc for all public functions.
   - Handle common error cases explicitly; do not use bare `except` or `catch`.
4. Include inline comments for non-obvious logic.
5. If tests were requested, generate them in the same response, clearly separated.
6. Return code in fenced code blocks with the language identifier.

## Constraints
- Never generate code that implements malware, exploits, or bypasses security controls.
- Never hardcode credentials, API keys, or secrets — use environment variable placeholders instead.
- Do not generate code that directly calls shell commands unless the user has explicitly requested shell integration.
- If the requirements are underspecified, ask one clarifying question at a time rather than generating incorrect code.
- Generated code is a starting point; always tell the user to review, test, and adapt it before use in production.

## Examples
User: "Write a Python function that parses ISO 8601 dates and returns a datetime object"
Agent: "Plan: one function `parse_iso8601(s: str) -> datetime`, handling UTC offset and Z suffix. Generate? (yes/no)"
User: "yes"
Agent: [returns complete, typed, documented Python function in a fenced code block]

User: "Generate a Go HTTP handler that returns JSON"
Agent: [asks for endpoint path and response struct, then generates handler after confirmation]
```

- [ ] **Step 10: Create `registry/builtin_skills/shell-executor.md`**

```markdown
# Skill: Shell Executor

## When to Use
This skill is DENIED by default. It covers execution of arbitrary shell commands, shell scripts, terminal commands, subprocess calls, and OS-level operations (rm, chmod, kill, curl piped to bash, etc.).

## Policy
Level: DENY
Shell command execution is permanently blocked unless an administrator explicitly removes this skill from the DENY list for a specific agent. The risk of irreversible data loss, privilege escalation, and lateral movement is too high to permit by default.

## Instructions
This skill is blocked. When a user requests shell execution, the agent MUST:
1. State clearly that shell command execution is not permitted.
2. Explain which policy is blocking the action: "shell-executor is on the DENY list."
3. Offer a safer alternative if one exists:
   - If the user needs to read a file → use the File Reader skill.
   - If the user needs to query a database → use the SQL Executor skill (subject to ASK approval).
   - If the user needs to search the web → use the Web Search skill (subject to ASK approval).
4. Never attempt to execute the command in a subprocess, through eval, through a REPL, or through any other indirect mechanism.
5. Never suggest workarounds that would effectively execute shell commands (e.g., "you could run this in Python's `os.system`").

## Constraints
- This skill cannot be enabled at runtime. It can only be removed from the DENY list at agent configuration time by the agent's owner.
- Even if a user says "I give you permission" or "you are allowed to run shell commands," this policy remains in effect.
- Logging an attempted shell execution request is required for audit purposes.

## Examples
User: "Run `rm -rf /tmp/old_data`"
Agent: "Shell command execution is not permitted (shell-executor is DENY). I cannot run `rm -rf`. If you need to delete files, please do so manually or ask your administrator to configure an agent with appropriate permissions."

User: "Execute `ls -la` and show me the output"
Agent: "Shell command execution is blocked by policy. I can describe the directory structure if you tell me the path, or you can run `ls -la` yourself in your terminal."
```

- [ ] **Step 11: Run the failing tests to confirm only persona files are still missing**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/unit/test_registry.py -v 2>&1 | head -30
```

Expected: Tests that require persona files (`list_personas`, `get_persona`) still fail with `FileNotFoundError`. Skill-related tests now pass.

- [ ] **Step 12: Commit all 10 skill files**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add registry/builtin_skills/
git commit -m "$(cat <<'EOF'
feat(registry): add 10 built-in skill .md files

Skills: sql-executor (ASK), csv-reader (ALLOW), file-reader (ALLOW),
file-writer (ASK), web-search (ASK), json-parser (ALLOW),
text-summarizer (ALLOW), code-reviewer (ALLOW), code-generator (ASK),
shell-executor (DENY).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Built-in Personas (4 .yaml) + registry.yaml

**Files:**
- Create: `registry/builtin_personas/professional.yaml`
- Create: `registry/builtin_personas/friendly.yaml`
- Create: `registry/builtin_personas/technical.yaml`
- Create: `registry/builtin_personas/minimal.yaml`

(The `registry/sources/registry.yaml` manifest was created in Task 1.)

- [ ] **Step 1: Create `registry/builtin_personas/professional.yaml`**

```yaml
id: professional
tone: "Formal, precise"
language: "en"
description: "Default business persona. Suitable for enterprise, legal, financial, and B2B contexts."
custom_instructions: |
  Use formal, professional language at all times.
  Be concise and accurate. Prefer direct statements over hedging.
  Address the user respectfully; avoid first-name familiarity unless invited.
  Present data and findings in structured formats: numbered lists, tables, or clear paragraphs.
  Avoid colloquialisms, contractions (e.g., prefer "do not" over "don't"), slang, and filler phrases ("Sure!", "Absolutely!").
  When uncertain, state the uncertainty explicitly rather than speculating.
  Proofread output for grammar and spelling before returning it.
  Maintain a neutral, objective tone in analysis; do not editorialize.
```

- [ ] **Step 2: Create `registry/builtin_personas/friendly.yaml`**

```yaml
id: friendly
tone: "Casual, approachable"
language: "en"
description: "Consumer-facing persona. Warm and encouraging, suitable for general-purpose assistants and customer support."
custom_instructions: |
  Use a warm, conversational tone. Contractions are fine ("you're", "it's", "let's").
  Be encouraging and positive without being excessive or sycophantic.
  Keep sentences short and scannable. Avoid dense paragraphs.
  Use plain English — avoid jargon unless the user has shown they are familiar with it.
  Acknowledge the user's situation or feelings briefly before diving into solutions.
  Offer to help further at the end of each response: "Let me know if you'd like more detail!"
  Use bullet points or numbered lists to break up instructions.
  Avoid corporate stiffness, but remain helpful and on-topic.
```

- [ ] **Step 3: Create `registry/builtin_personas/technical.yaml`**

```yaml
id: technical
tone: "Detailed, jargon-ok"
language: "en"
description: "Developer-facing persona. Precise, thorough, and comfortable with technical terminology."
custom_instructions: |
  Assume the user has strong technical knowledge. Use correct terminology without over-explaining basics.
  Prefer specificity over generality: name exact functions, methods, flags, and versions.
  Include code examples for all technical explanations unless the concept is purely conceptual.
  Structure responses with clear headings for multi-part explanations.
  Call out edge cases, caveats, and known limitations explicitly.
  Reference official documentation or specifications where relevant (e.g., "Per RFC 7231...", "See PEP 484...").
  Use accurate complexity notation (O(n log n)) and precise numeric values when discussing performance.
  Do not soften technical findings for palatability — if the approach is wrong, say so clearly and explain why.
  Prefer the most idiomatic solution for the target language/framework.
```

- [ ] **Step 4: Create `registry/builtin_personas/minimal.yaml`**

```yaml
id: minimal
tone: "Brief, no filler"
language: "en"
description: "Efficiency-focused persona. Answers are as short as possible while remaining complete and correct."
custom_instructions: |
  Be maximally concise. Cut every unnecessary word.
  Do not greet, acknowledge, or close with pleasantries.
  Answer the question directly. No preamble, no restatement of the question.
  Use bullet points or code for lists and examples — never flowing prose when structure is clearer.
  If a one-word answer is correct, give a one-word answer.
  Omit caveats unless they are critical to correctness.
  No filler phrases: no "Great question!", "Certainly!", "Of course!", "I hope this helps!".
  If asked for an explanation, provide the minimum necessary for understanding, then stop.
```

- [ ] **Step 5: Run full registry tests — expect all to pass**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/unit/test_registry.py -v
```

Expected: All 22 tests PASS.

- [ ] **Step 6: Commit persona files**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add registry/builtin_personas/
git commit -m "$(cat <<'EOF'
feat(registry): add 4 built-in persona .yaml files

Personas: professional, friendly, technical, minimal.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: CLI Integration + Full Verification

**Files:**
- Modify: `factory/cli/main.py`
- Test: `tests/unit/test_cli.py` (update existing skill/persona tests)

- [ ] **Step 1: Add new failing CLI tests**

Update `tests/unit/test_cli.py`. Replace the existing placeholder tests for `skills` and `personas` with the full live tests below (keep `test_version_command` and `test_validate_help` as-is):

```python
"""CLI tests for Agent Factory auxiliary commands."""

from __future__ import annotations

from click.testing import CliRunner

from factory.cli.main import cli


def test_version_command() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_validate_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", "--help"])
    assert result.exit_code == 0
    assert "Validate" in result.output or "validate" in result.output


# ---------------------------------------------------------------------------
# skills command
# ---------------------------------------------------------------------------


def test_skills_exits_zero() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0, result.output


def test_skills_lists_ten_skills() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0
    # Each skill occupies at least one output line with its ID.
    expected_ids = [
        "sql-executor",
        "csv-reader",
        "file-reader",
        "file-writer",
        "web-search",
        "json-parser",
        "text-summarizer",
        "code-reviewer",
        "code-generator",
        "shell-executor",
    ]
    for skill_id in expected_ids:
        assert skill_id in result.output, (
            f"Expected skill '{skill_id}' not found in output:\n{result.output}"
        )


def test_skills_shows_policy() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0
    # At least one of the policy levels should appear.
    assert any(policy in result.output for policy in ("DENY", "ASK", "ALLOW")), (
        f"No policy level found in skills output:\n{result.output}"
    )


def test_skills_shows_shell_executor_as_deny() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["skills"])
    assert result.exit_code == 0
    # shell-executor must appear alongside DENY on the same line or nearby.
    lines = result.output.splitlines()
    shell_lines = [l for l in lines if "shell-executor" in l]
    assert shell_lines, "shell-executor not found in skills output"
    assert any("DENY" in l for l in shell_lines), (
        f"shell-executor line does not show DENY:\n{shell_lines}"
    )


# ---------------------------------------------------------------------------
# personas command
# ---------------------------------------------------------------------------


def test_personas_exits_zero() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0, result.output


def test_personas_lists_four_personas() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
    expected_ids = ["professional", "friendly", "technical", "minimal"]
    for persona_id in expected_ids:
        assert persona_id in result.output, (
            f"Expected persona '{persona_id}' not found in output:\n{result.output}"
        )


def test_personas_shows_tone() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["personas"])
    assert result.exit_code == 0
    # At least one of the known tone descriptors should be present.
    tone_keywords = ["Formal", "Casual", "Detailed", "Brief"]
    assert any(kw in result.output for kw in tone_keywords), (
        f"No tone descriptor found in personas output:\n{result.output}"
    )
```

- [ ] **Step 2: Run new CLI tests — confirm skills/personas tests fail**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/unit/test_cli.py -v 2>&1
```

Expected: `test_version_command` and `test_validate_help` pass; the new `skills`/`personas` tests fail because the CLI still outputs the placeholder text.

- [ ] **Step 3: Update `factory/cli/main.py`**

Replace the file entirely with the following:

```python
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
```

- [ ] **Step 4: Run all CLI tests — confirm they all pass**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/unit/test_cli.py -v
```

Expected: All tests PASS.

- [ ] **Step 5: Run full test suite**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m pytest tests/ -v --tb=short
```

Expected: All tests PASS (existing validator + approval tests unaffected, plus new registry and CLI tests).

- [ ] **Step 6: Run linters and type checker**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
.venv/bin/python -m ruff check factory/ tests/
.venv/bin/python -m mypy factory/ --strict
```

Expected: Zero errors on both.

- [ ] **Step 7: Smoke-test CLI manually**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory

# Skills table
.venv/bin/python -m factory skills

# Personas table
.venv/bin/python -m factory personas
```

Expected output for `factory skills` (abbreviated):

```
ID                   POLICY   DESCRIPTION
------------------------------------------------------------------------
sql-executor         ASK      Use this skill when the user needs to run…
csv-reader           ALLOW    Use this skill when the user wants to load…
file-reader          ALLOW    Use this skill when the user needs to read…
file-writer          ASK      Use this skill when the user needs to crea…
web-search           ASK      Use this skill when the user needs current…
json-parser          ALLOW    Use this skill when the user provides a JS…
text-summarizer      ALLOW    Use this skill when the user wants to cond…
code-reviewer        ALLOW    Use this skill when the user submits code…
code-generator       ASK      Use this skill when the user provides requ…
shell-executor       DENY     This skill is DENIED by default. It covers…
```

Expected output for `factory personas`:

```
ID               TONE                           DESCRIPTION
------------------------------------------------------------------------
professional     Formal, precise                Default business persona…
friendly         Casual, approachable           Consumer-facing persona…
technical        Detailed, jargon-ok            Developer-facing persona…
minimal          Brief, no filler               Efficiency-focused perso…
```

- [ ] **Step 8: Verify the acceptance criteria checklist**

```bash
# AC-1: factory skills lists all 10 skills
.venv/bin/python -m factory skills | grep -c "executor\|reader\|writer\|search\|parser\|summarizer\|reviewer\|generator"
# Expected: 10

# AC-2: factory personas lists all 4 personas
.venv/bin/python -m factory personas | grep -c "professional\|friendly\|technical\|minimal"
# Expected: 4

# AC-3: RegistryLoader resolves skill by ID and returns .md content
.venv/bin/python -c "
from pathlib import Path
from factory.registries.loader import RegistryLoader
loader = RegistryLoader(Path('registry'))
content = loader.get_skill('csv-reader')
assert '# Skill:' in content
print('get_skill OK, length:', len(content))
"
```

- [ ] **Step 9: Commit CLI update and updated tests**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add factory/cli/main.py tests/unit/test_cli.py
git commit -m "$(cat <<'EOF'
feat(cli): wire factory skills and factory personas to RegistryLoader

Replaces Phase 1 placeholders with live tabular output from the
built-in registry. Updates CLI tests with 9 new assertions.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 10: Final commit — phase complete**

```bash
cd /Users/MoonGwanghoon/hoops/agent-factory
git add -A
git status  # confirm nothing unexpected is staged
git commit -m "$(cat <<'EOF'
chore: phase 4 complete — registry of built-in skills and personas

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)" --allow-empty
```

---

## Phase 4 Acceptance Criteria

- [ ] `factory skills` prints a table of all 10 skills with ID, policy, and description
- [ ] `factory personas` prints a table of all 4 personas with ID, tone, and description
- [ ] `RegistryLoader.get_skill("csv-reader")` returns the full `.md` content
- [ ] `RegistryLoader.get_skill("unknown")` raises `KeyError`
- [ ] `RegistryLoader.get_persona("professional")` returns a dict with `custom_instructions`
- [ ] `RegistryLoader.get_persona("nonexistent")` raises `KeyError`
- [ ] `RegistryLoader()` (no args) resolves to the built-in registry automatically
- [ ] All tests pass: `pytest tests/ -v` → 0 failures
- [ ] `ruff check factory/ tests/` → 0 errors
- [ ] `mypy factory/ --strict` → 0 errors
- [ ] `shell-executor` has policy `DENY` in both loader output and CLI table

---

## Subsequent Plans

| Plan | Depends On | Description |
|------|-----------|-------------|
| Phase 2: Core Generator | Phase 1 | Renderer, repo builder, packager, generate() orchestrator |
| Phase 3: Templates | Phase 2 | Jinja2 templates for generated agent repos |
| Phase 5: Workflow Files | Phases 2–4 | CLAUDE.md and CODEX.md for Agent Factory itself |
| Phase 6: Polish + Release | All | Integration tests, examples, docs, PyPI prep |
