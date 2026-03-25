# Reading Order — uiux-design-helper

## For LLMs

When this agent is loaded, the LLM should read files in this order:


1. `CLAUDE.md` or `CODEX.md` (depending on runtime)
2. `orchestrator.md`
3. `architecture/topology.yaml`
4. `agent_spec.yaml`
5. `policies/policy.yaml`
6. `agents/*.md`
7. `skills/index.yaml` then `skills/*.md`
8. `context/knowledge.md`
9. `docs/*` (as needed)

## For Humans

Start with `README.md` for an overview, then review `docs/architecture.md`
and `docs/policy.md` for details.
