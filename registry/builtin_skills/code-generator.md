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
