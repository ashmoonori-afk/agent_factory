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
