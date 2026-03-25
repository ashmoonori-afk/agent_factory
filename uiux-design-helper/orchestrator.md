# Orchestrator — uiux-design-helper

## Overview
This file defines the orchestration rules for the multi-agent system uiux-design-helper.

## Topology
- Entry point: planner
- Max loops: 3
- Exit condition: planner가 최종 결과물을 취합하여 사용자에게 전달하면 종료

## Agent Roster

### planner
- Role: 기획자 (Hub) — 디자인 기획안 작성, 요구사항 정의, 다른 에이전트에게 작업 분배. 팀의 중심 조율자.
- Passes control to: researcher, designer, reviewer

### researcher
- Role: 리서처 — 사용자 리서치, UX 트렌드 분석, 경쟁사 조사를 수행하고 결과를 기획자에게 전달.
- Passes control to: planner

### designer
- Role: 디자이너 — 목업 제작, 와이어프레임 설계, 비주얼 디자인을 수행.
- Passes control to: planner

### reviewer
- Role: 리뷰어 — 디자인 검수, 사용성 평가, 접근성 평가를 수행하고 개선점을 제안.
- Passes control to: planner


## Orchestration Rules
1. Follow the topology graph in `architecture/topology.yaml`.
2. Each agent reads its own file in `agents/` for role-specific instructions.
3. The orchestrator coordinates handoffs between agents.
4. Enforce all policies from `policies/policy.yaml` across every agent.
5. Stop after max_loops iterations or when exit condition is met.
