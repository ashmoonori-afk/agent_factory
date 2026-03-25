# Agent Behavior Verification — uiux-design-helper

## Test: Agent identity

- Prompt: "Who are you?"
- Expected: Agent identifies as uiux-design-helper and describes its purpose.

## Test: Agent description

- Prompt: "What do you do?"
- Expected: Agent responds with: UI/UX 디자인 전문 에이전트 팀. 목업 디자인 파일 제공, 디자인 기획안 작성, 기존 디자인 수정 제안 등을 사람처럼 수행한다.

## Test: Reading order

- Prompt: "What files did you read?"
- Expected: Agent confirms it read CLAUDE.md (or CODEX.md), agent_spec.yaml,
  and policies/policy.yaml at minimum.


## Test: Multi-agent orchestration

- Prompt: "How do you coordinate agents?"
- Expected: Agent describes the topology and orchestrator rules.

## Test: Agent roster

- Verify agent knows about planner (기획자 (Hub) — 디자인 기획안 작성, 요구사항 정의, 다른 에이전트에게 작업 분배. 팀의 중심 조율자.).
- Verify agent knows about researcher (리서처 — 사용자 리서치, UX 트렌드 분석, 경쟁사 조사를 수행하고 결과를 기획자에게 전달.).
- Verify agent knows about designer (디자이너 — 목업 제작, 와이어프레임 설계, 비주얼 디자인을 수행.).
- Verify agent knows about reviewer (리뷰어 — 디자인 검수, 사용성 평가, 접근성 평가를 수행하고 개선점을 제안.).

## Test: Skill awareness

- Prompt: "Can you use web-search?"
- Expected: Agent confirms the skill is available.

- Prompt: "Can you use file-reader?"
- Expected: Agent confirms the skill is available.

- Prompt: "Can you use file-writer?"
- Expected: Agent confirms the skill is available.

- Prompt: "Can you use text-summarizer?"
- Expected: Agent confirms the skill is available.

- Prompt: "Can you use json-parser?"
- Expected: Agent confirms the skill is available.

