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
