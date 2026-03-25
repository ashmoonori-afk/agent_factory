# Agent Factory

AI 에이전트 저장소를 대화를 통해 생성하는 LLM-native 메타 에이전트 + Python 라이브러리.

Claude Code 또는 Codex에서 이 폴더를 열면, LLM이 인터뷰를 진행하고, 아키텍처를 제안하고, 승인을 받은 뒤, `factory.generate()`를 호출하여 완성된 에이전트 저장소를 생성합니다.

```
사용자 ↔ LLM (인터뷰) → factory.generate() → 완성된 에이전트 저장소
```

## 빠른 시작

### 런처로 실행 (권장)

| OS | Claude Code | Codex |
|----|-------------|-------|
| macOS | `launch-claude.command` 더블클릭 | `launch-codex.command` 더블클릭 |
| Windows | `launch-claude.bat` 더블클릭 | `launch-codex.bat` 더블클릭 |
| Linux | `./launch-claude.sh` | `./launch-codex.sh` |

### 직접 실행

```bash
# Claude Code
cd agent-factory && claude

# Codex
cd agent-factory && codex
```

- Claude Code는 `CLAUDE.md`를 자동으로 읽습니다.
- Codex는 `AGENTS.md`를 자동으로 읽습니다.

LLM이 아래 6단계 워크플로우를 자동으로 진행합니다:

1. **Interview** — 에이전트 이름, 목적, 스킬, 정책 등을 질문
2. **Normalize** — 답변을 spec dict로 변환
3. **Architecture** — 아키텍처 제안서 표시
4. **Approve** — 사용자가 YES 입력 (필수)
5. **Generate** — `factory.generate()` 호출, 전체 저장소 생성
6. **Deliver** — 결과 보고 및 사용법 안내

## 설치

```bash
git clone <repo-url> && cd agent-factory
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Python 라이브러리로 사용

```python
import factory

spec = {
    "name": "my-bot",
    "description": "데이터를 분석하고 리포트를 생성하는 에이전트",
    "type": "single",
    "skills": ["csv-reader", "sql-executor"],
    "persona": {"tone": "professional", "language": "ko"},
    "policies": {
        "deny": ["send_email", "delete_file", "deploy"],
        "ask": ["execute_sql"],
        "allow": ["*"],
    },
    "launchers": True,  # 더블클릭 런처 파일 포함
}

approval = {
    "decision": "APPROVED",
    "timestamp": "2026-03-25T12:00:00Z",
    "user_input": "YES",
    "action_type": "architecture_approval",
    "detail": "my-bot single-agent approved",
}

result = factory.generate(
    spec=spec,
    output="./my-bot",
    approval_record=approval,
)
print(f"Generated {result.file_count} files at {result.output_path}")
```

## CLI

```bash
python -m factory validate spec.yaml   # 스펙 검증
python -m factory skills               # 스킬 목록 (165개)
python -m factory personas             # 페르소나 목록 (4개)
python -m factory critique spec.yaml   # 아키텍처 비평 + 점수
python -m factory upgrade ./my-agent   # 에이전트 업그레이드
python -m factory version              # 버전 출력
```

## 생성 결과물

생성된 에이전트 저장소 구조:

```
my-agent/
├── CLAUDE.md                  # Claude Code용 시스템 프롬프트
├── AGENTS.md                  # Codex용 시스템 프롬프트
├── CODEX.md                   # → AGENTS.md 포인터
├── agent_spec.yaml            # 에이전트 사양 (기계 판독용)
├── meta.yaml                  # 생성 메타데이터
├── README.md                  # 사용 가이드
├── .env.example               # API 키 템플릿
├── personas/default.yaml      # 페르소나 정의
├── policies/
│   ├── policy.yaml            # DENY/ASK/ALLOW 정책
│   └── approval_log.jsonl     # 승인 감사 로그
├── skills/
│   ├── index.yaml             # 스킬 매니페스트
│   └── *.md                   # 스킬 인스트럭션 파일
├── docs/
│   ├── architecture.md
│   ├── policy.md
│   └── reading_order.md
├── tests/
│   ├── test-agent.md          # 동작 검증 프롬프트
│   └── test-policy.md         # 정책 검증 프롬프트
├── launch-claude.command      # macOS 런처 (Claude Code)
├── launch-codex.command       # macOS 런처 (Codex)
├── launch-claude.bat          # Windows 런처
├── launch-codex.bat           # Windows 런처
├── launch-claude.sh           # Linux 런처
└── launch-codex.sh            # Linux 런처
```

멀티에이전트 사양 시 추가:
```
├── orchestrator.md            # 오케스트레이션 규칙
├── agents/agent_role.md       # 에이전트별 역할 정의
└── architecture/topology.yaml # 토폴로지 그래프
```

## 스킬 레지스트리 (165개)

3개 소스에서 수집:

| 소스 | 수량 | 범위 |
|------|------|------|
| 기본 빌트인 | 10 | sql-executor, csv-reader, file-reader, file-writer, web-search, json-parser, text-summarizer, code-reviewer, code-generator, shell-executor |
| [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 125 | api-design, tdd-workflow, python-patterns, rust-patterns, django-tdd, security-review, docker-patterns, autonomous-loops 등 |
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 7 | uiux-design, uiux-brand, uiux-slides, uiux-ui-styling, uiux-ui-ux-pro-max 등 |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 23 | cmd-commit, cmd-create-pr, cmd-pr-review, cmd-release, cmd-todo 등 |

정책 분포: ALLOW 130 / ASK 23 / DENY 12

## 페르소나 (4개)

| ID | 톤 | 설명 |
|----|------|------|
| professional | 격식, 정확 | 기본 비즈니스 페르소나 |
| friendly | 캐주얼, 친근 | 소비자 대면용 |
| technical | 디테일, 전문 용어 OK | 개발자 대면용 |
| minimal | 간결, 필러 없음 | 효율 중심 |

## 정책 모델

| 레벨 | 의미 | 동작 |
|------|------|------|
| `DENY` | 절대 금지 | 실행 불가. 예외 없음. |
| `ASK` | 허가 필요 | 사용자 확인 후 실행. |
| `ALLOW` | 자유 실행 | 확인 없이 실행. |

기본 DENY 목록: `send_email`, `delete_file`, `deploy`, `payment`, `external_share`, `modify_meta_agent`, `modify_own_prompt`, `modify_policy_file`

## 예시 에이전트

| 에이전트 | 유형 | 스킬 |
|----------|------|------|
| `examples/data-analysis-bot/` | 싱글 | sql-executor, csv-reader |
| `examples/code-assistant/` | 싱글 | code-reviewer, code-generator |
| `sql-bot/` | 싱글 | sql-executor, csv-reader |
| `unicode0bot/` | 싱글 | file-reader |
| `uiux-design-helper/` | 멀티 (4노드 허브) | web-search, file-reader, file-writer, text-summarizer, json-parser |

## 프로젝트 구조

```
agent-factory/
├── CLAUDE.md / AGENTS.md      # 메타 에이전트 워크플로우 인스트럭션
├── factory/                   # Python 라이브러리 (~1,500 LOC)
│   ├── core/                  # generator, renderer, repo_builder, packager, critique, upgrader
│   ├── approval/              # 승인 레코드 + SHA-256 해시
│   ├── schemas/               # jsonschema 검증
│   ├── registries/            # 스킬/페르소나 로더
│   └── cli/                   # 보조 CLI (validate, skills, personas, critique, upgrade)
├── templates/                 # Jinja2 템플릿 (29개)
│   ├── single_agent/          # 싱글 에이전트 템플릿
│   ├── multi_agent/           # 멀티 에이전트 템플릿
│   ├── launchers/             # OS별 런처 템플릿
│   ├── policies/, docs/, tests/  # 공유 템플릿
├── registry/                  # 165 스킬 + 4 페르소나
│   ├── builtin_skills/        # .md 스킬 파일
│   ├── builtin_personas/      # .yaml 페르소나 파일
│   └── sources/registry.yaml  # 매니페스트
├── schemas/                   # JSON Schema (agent_spec, persona, policy, skill)
├── tests/                     # 232 테스트 (unit, snapshot, smoke)
├── evals/                     # 런타임 동작 평가 시나리오
└── examples/                  # 예시 스펙 + 생성 결과물
```

## 테스트

```bash
pytest tests/ -v               # 232 테스트
ruff check factory/ tests/     # 린트
mypy factory/ --strict         # 타입 체크
```

## 기술 스택

| 항목 | 기술 |
|------|------|
| 언어 | Python 3.10+ |
| 템플릿 | Jinja2 |
| 스키마 | jsonschema + PyYAML |
| CLI | click |
| 패키징 | zipfile (built-in) |
| 빌드 | pyproject.toml + hatchling |
| 테스트 | pytest |
| 린트 | ruff |
| 타입 | mypy (strict) |

프로덕션 의존성: **4개** (click, jinja2, pyyaml, jsonschema)

## 라이선스

MIT
