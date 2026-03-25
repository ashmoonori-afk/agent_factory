# Reading Order — fixture-single-agent

## For LLMs

When this agent is loaded, the LLM should read files in this order:


1. `CLAUDE.md` or `CODEX.md` (depending on runtime)
2. `agent_spec.yaml`
3. `policies/policy.yaml`
4. `skills/index.yaml` then `skills/*.md`
6. `docs/*` (as needed)

## For Humans

Start with `README.md` for an overview, then review `docs/architecture.md`
and `docs/policy.md` for details.
