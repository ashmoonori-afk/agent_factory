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
