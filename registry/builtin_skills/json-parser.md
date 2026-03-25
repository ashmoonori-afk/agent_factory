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
