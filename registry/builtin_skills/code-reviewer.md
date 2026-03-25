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
