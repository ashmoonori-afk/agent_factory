# Architecture — uiux-design-helper

## Overview

UI/UX 디자인 전문 에이전트 팀. 목업 디자인 파일 제공, 디자인 기획안 작성, 기존 디자인 수정 제안 등을 사람처럼 수행한다.

**Type:** multi
**Runtime:** both

## Components

### Agent Instructions
- `CLAUDE.md` — Instructions for Claude Code
- `CODEX.md` — Instructions for Codex

### Policies
Policy enforcement is defined in `policies/policy.yaml`.
All actions are classified as DENY, ASK, or ALLOW.

### Skills
This agent uses the following skills:
- web-search
- file-reader
- file-writer
- text-summarizer
- json-parser


## Multi-Agent Topology
- **planner**: 기획자 (Hub) — 디자인 기획안 작성, 요구사항 정의, 다른 에이전트에게 작업 분배. 팀의 중심 조율자.
- **researcher**: 리서처 — 사용자 리서치, UX 트렌드 분석, 경쟁사 조사를 수행하고 결과를 기획자에게 전달.
- **designer**: 디자이너 — 목업 제작, 와이어프레임 설계, 비주얼 디자인을 수행.
- **reviewer**: 리뷰어 — 디자인 검수, 사용성 평가, 접근성 평가를 수행하고 개선점을 제안.


See `architecture/topology.yaml` and `orchestrator.md` for details.
