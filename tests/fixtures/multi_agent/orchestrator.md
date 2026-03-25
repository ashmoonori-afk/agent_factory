# Orchestrator — fixture-multi-agent

## Overview
This file defines the orchestration rules for the multi-agent system fixture-multi-agent.

## Topology
- Entry point: reviewer
- Max loops: 2
- Exit condition: all agents complete

## Agent Roster

### reviewer
- Role: reviews code
- Passes control to: fixer

### fixer
- Role: fixes issues


## Orchestration Rules
1. Follow the topology graph in `architecture/topology.yaml`.
2. Each agent reads its own file in `agents/` for role-specific instructions.
3. The orchestrator coordinates handoffs between agents.
4. Enforce all policies from `policies/policy.yaml` across every agent.
5. Stop after max_loops iterations or when exit condition is met.
