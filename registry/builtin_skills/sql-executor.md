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
