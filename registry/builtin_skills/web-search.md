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
