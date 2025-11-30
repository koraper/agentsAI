# 사용 가이드

에이전트, 슬래시 명령 및 다중 에이전트 워크플로우 사용에 대한 완벽한 가이드.

## 개요

플러그인 생태계는 두 가지 주요 인터페이스를 제공합니다:

1. **슬래시 명령** - 도구 및 워크플로우의 직접 호출
2. **자연어** - Claude가 어떤 에이전트를 사용할지 추론

## 슬래시 명령

슬래시 명령은 에이전트 및 워크플로우와 작업하기 위한 주요 인터페이스입니다. 각 플러그인은 직접 실행할 수 있는 네임스페이스된 명령을 제공합니다.

### 명령 형식

```bash
/plugin-name:command-name [arguments]
```

### 명령 발견

설치된 플러그인에서 사용 가능한 모든 슬래시 명령 나열:

```bash
/plugin
```

### 슬래시 명령의 이점

- **직접 호출** - 자연어로 설명할 필요 없음
- **구조화된 인수** - 정밀한 제어를 위해 명시적으로 매개변수 전달
- **구성 가능성** - 복잡한 워크플로우를 위해 명령 체이닝
- **검색 가능성** - `/plugin`을 사용하여 사용 가능한 모든 명령 확인

## 자연어

에이전트는 또한 어떤 전문가를 사용할지 추론해야 할 때 자연어를 통해 호출할 수 있습니다:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

Claude Code는 요청에 따라 적절한 에이전트를 자동으로 선택하고 조정합니다.

## 카테고리별 명령 참고자료

### 개발 & 기능

| 명령 | 설명 |
|---------|-------------|
| `/backend-development:feature-development` | 엔드-투-엔드 백엔드 기능 개발 |
| `/full-stack-orchestration:full-stack-feature` | 완전한 풀스택 기능 구현 |
| `/multi-platform-apps:multi-platform` | 크로스 플랫폼 앱 개발 조정 |

### 테스트 & 품질

| 명령 | 설명 |
|---------|-------------|
| `/unit-testing:test-generate` | 포괄적인 단위 테스트 생성 |
| `/tdd-workflows:tdd-cycle` | 완벽한 TDD red-green-refactor 사이클 |
| `/tdd-workflows:tdd-red` | 먼저 실패하는 테스트 작성 |
| `/tdd-workflows:tdd-green` | 테스트를 통과하도록 코드 구현 |
| `/tdd-workflows:tdd-refactor` | 통과하는 테스트로 리팩토링 |

### 코드 품질 & 검토

| 명령 | 설명 |
|---------|-------------|
| `/code-review-ai:ai-review` | AI 기반 코드 리뷰 |
| `/comprehensive-review:full-review` | 다중 관점 분석 |
| `/comprehensive-review:pr-enhance` | 풀 요청 개선 |

### 디버깅 & 문제 해결

| 명령 | 설명 |
|---------|-------------|
| `/debugging-toolkit:smart-debug` | 대화형 스마트 디버깅 |
| `/incident-response:incident-response` | 프로덕션 사고 관리 |
| `/incident-response:smart-fix` | 자동화된 사고 해결 |
| `/error-debugging:error-analysis` | 심층 오류 분석 |
| `/error-debugging:error-trace` | 스택 추적 디버깅 |
| `/error-diagnostics:smart-debug` | 스마트 진단 디버깅 |
| `/distributed-debugging:debug-trace` | 분산 시스템 추적 |

### 보안

| 명령 | 설명 |
|---------|-------------|
| `/security-scanning:security-hardening` | 포괄적인 보안 강화 |
| `/security-scanning:security-sast` | 정적 애플리케이션 보안 테스트 |
| `/security-scanning:security-dependencies` | 종속성 취약점 스캔 |
| `/security-compliance:compliance-check` | SOC2/HIPAA/GDPR 규정 준수 |
| `/frontend-mobile-security:xss-scan` | XSS 취약점 스캔 |

### 인프라 & 배포

| 명령 | 설명 |
|---------|-------------|
| `/observability-monitoring:monitor-setup` | 모니터링 인프라 설정 |
| `/observability-monitoring:slo-implement` | SLO/SLI 메트릭 구현 |
| `/deployment-validation:config-validate` | 배포 전 검증 |
| `/cicd-automation:workflow-automate` | CI/CD 파이프라인 자동화 |

### 데이터 & ML

| 명령 | 설명 |
|---------|-------------|
| `/machine-learning-ops:ml-pipeline` | ML 훈련 파이프라인 조정 |
| `/data-engineering:data-pipeline` | ETL/ELT 파이프라인 구성 |
| `/data-engineering:data-driven-feature` | 데이터 기반 기능 개발 |

### 문서

| 명령 | 설명 |
|---------|-------------|
| `/code-documentation:doc-generate` | 포괄적인 문서 생성 |
| `/code-documentation:code-explain` | 코드 기능 설명 |
| `/documentation-generation:doc-generate` | OpenAPI 사양, 다이어그램, 튜토리얼 |

### 리팩토링 & 유지 보수

| 명령 | 설명 |
|---------|-------------|
| `/code-refactoring:refactor-clean` | 코드 정리 및 리팩토링 |
| `/code-refactoring:tech-debt` | 기술 부채 관리 |
| `/codebase-cleanup:deps-audit` | 종속성 감시 |
| `/codebase-cleanup:tech-debt` | 기술 부채 감소 |
| `/framework-migration:legacy-modernize` | 레거시 코드 현대화 |
| `/framework-migration:code-migrate` | 프레임워크 마이그레이션 |
| `/framework-migration:deps-upgrade` | 종속성 업그레이드 |

### 데이터베이스

| 명령 | 설명 |
|---------|-------------|
| `/database-migrations:sql-migrations` | SQL 마이그레이션 자동화 |
| `/database-migrations:migration-observability` | 마이그레이션 모니터링 |
| `/database-cloud-optimization:cost-optimize` | 데이터베이스 및 클라우드 최적화 |

### Git & PR 워크플로우

| 명령 | 설명 |
|---------|-------------|
| `/git-pr-workflows:pr-enhance` | 풀 요청 품질 개선 |
| `/git-pr-workflows:onboard` | 팀 온보딩 자동화 |
| `/git-pr-workflows:git-workflow` | Git 워크플로우 자동화 |

### 프로젝트 스캐폴딩

| 명령 | 설명 |
|---------|-------------|
| `/python-development:python-scaffold` | FastAPI/Django 프로젝트 설정 |
| `/javascript-typescript:typescript-scaffold` | Next.js/React + Vite 설정 |
| `/systems-programming:rust-project` | Rust 프로젝트 스캐폴딩 |

### AI & LLM 개발

| 명령 | 설명 |
|---------|-------------|
| `/llm-application-dev:langchain-agent` | LangChain 에이전트 개발 |
| `/llm-application-dev:ai-assistant` | AI 어시스턴트 구현 |
| `/llm-application-dev:prompt-optimize` | 프롬프트 엔지니어링 최적화 |
| `/agent-orchestration:multi-agent-optimize` | 다중 에이전트 최적화 |
| `/agent-orchestration:improve-agent` | 에이전트 개선 워크플로우 |

### 테스트 & 성능

| 명령 | 설명 |
|---------|-------------|
| `/performance-testing-review:ai-review` | 성능 분석 |
| `/application-performance:performance-optimization` | 앱 최적화 |

### 팀 협업

| 명령 | 설명 |
|---------|-------------|
| `/team-collaboration:issue` | 이슈 관리 자동화 |
| `/team-collaboration:standup-notes` | 스탠드업 노트 생성 |

### 접근성

| 명령 | 설명 |
|---------|-------------|
| `/accessibility-compliance:accessibility-audit` | WCAG 규정 준수 감시 |

### API 개발

| 명령 | 설명 |
|---------|-------------|
| `/api-testing-observability:api-mock` | API 모킹 및 테스트 |

### 컨텍스트 관리

| 명령 | 설명 |
|---------|-------------|
| `/context-management:context-save` | 대화 컨텍스트 저장 |
| `/context-management:context-restore` | 이전 컨텍스트 복원 |

## 다중 에이전트 워크플로우 예제

플러그인은 슬래시 명령을 통해 접근할 수 있는 미리 구성된 다중 에이전트 워크플로우를 제공합니다.

### 풀스택 개발

```bash
# 명령 기반 워크플로우 호출
/full-stack-orchestration:full-stack-feature "user dashboard with real-time analytics"

# 자연어 대안
"Implement user dashboard with real-time analytics"
```

**오케스트레이션:** backend-architect → database-architect → frontend-developer → test-automator → security-auditor → deployment-engineer → observability-engineer

**발생하는 일:**

1. 마이그레이션과 함께 데이터베이스 스키마 설계
2. 백엔드 API 구현 (REST/GraphQL)
3. 상태 관리를 사용한 프론트엔드 컴포넌트
4. 포괄적인 테스트 스위트 (단위/통합/E2E)
5. 보안 감시 및 강화
6. 기능 플래그가 있는 CI/CD 파이프라인 설정
7. 관찰성 및 모니터링 구성

### 보안 강화

```bash
# 포괄적인 보안 평가 및 치료
/security-scanning:security-hardening --level comprehensive

# 자연어 대안
"Perform security audit and implement OWASP best practices"
```

**오케스트레이션:** security-auditor → backend-security-coder → frontend-security-coder → mobile-security-coder → test-automator

### 데이터/ML 파이프라인

```bash
# 프로덕션 배포가 있는 ML 기능 개발
/machine-learning-ops:ml-pipeline "customer churn prediction model"

# 자연어 대안
"Build customer churn prediction model with deployment"
```

**오케스트레이션:** data-scientist → data-engineer → ml-engineer → mlops-engineer → performance-engineer

### 사고 대응

```bash
# 근본 원인 분석이 있는 스마트 디버깅
/incident-response:smart-fix "production memory leak in payment service"

# 자연어 대안
"Debug production memory leak and create runbook"
```

**오케스트레이션:** incident-responder → devops-troubleshooter → debugger → error-detective → observability-engineer

## 명령 인수 및 옵션

많은 슬래시 명령은 정밀한 제어를 위한 인수를 지원합니다:

```bash
# 특정 파일에 대한 테스트 생성
/unit-testing:test-generate src/api/users.py

# 방법론 사양이 있는 기능 개발
/backend-development:feature-development OAuth2 integration with social login

# 보안 종속성 스캔
/security-scanning:security-dependencies

# 컴포넌트 스캐폴딩
/frontend-mobile-development:component-scaffold UserProfile component with hooks

# TDD 워크플로우 사이클
/tdd-workflows:tdd-red User can reset password
/tdd-workflows:tdd-green
/tdd-workflows:tdd-refactor

# 스마트 디버깅
/debugging-toolkit:smart-debug memory leak in checkout flow

# Python 프로젝트 스캐폴딩
/python-development:python-scaffold fastapi-microservice
```

## 자연어와 명령 결합

최적의 유연성을 위해 두 가지 접근 방식을 혼합할 수 있습니다:

```
# 구조화된 워크플로우로 시작
/full-stack-orchestration:full-stack-feature "payment processing"

# 그 다음 자연어 지침 제공
"Ensure PCI-DSS compliance and integrate with Stripe"
"Add retry logic for failed transactions"
"Set up fraud detection rules"
```

## 모범 사례

### 슬래시 명령을 사용해야 할 때

- **구조화된 워크플로우** - 명확한 단계가 있는 다단계 프로세스
- **반복되는 작업** - 자주 수행하는 작업
- **정밀한 제어** - 특정 매개변수가 필요한 경우
- **발견** - 사용 가능한 기능 탐색

### 자연어를 사용해야 할 때

- **탐색적 작업** - 어떤 도구를 사용할지 확실하지 않을 때
- **복잡한 추론** - Claude가 여러 에이전트를 조정해야 할 때
- **상황에 맞는 결정** - 올바른 접근 방식이 상황에 따라 다를 때
- **임시 작업** - 명령에 맞지 않는 일회성 작업

### 워크플로우 구성

복잡한 시나리오를 위해 여러 플러그인 구성:

```bash
# 1. 기능 개발로 시작
/backend-development:feature-development payment processing API

# 2. 보안 강화 추가
/security-scanning:security-hardening

# 3. 포괄적인 테스트 생성
/unit-testing:test-generate

# 4. 구현 검토
/code-review-ai:ai-review

# 5. CI/CD 설정
/cicd-automation:workflow-automate

# 6. 모니터링 추가
/observability-monitoring:monitor-setup
```

## 에이전트 스킬 통합

에이전트 스킬은 명령과 함께 깊은 전문성을 제공합니다:

```
User: "Set up FastAPI project with async patterns"
→ Activates: fastapi-templates skill
→ Invokes: /python-development:python-scaffold
→ Result: 모범 사례를 사용한 프로덕션급 FastAPI 프로젝트

User: "Implement Kubernetes deployment with Helm"
→ Activates: helm-chart-scaffolding, k8s-manifest-generator skills
→ Guides: kubernetes-architect agent
→ Result: Helm 차트가 있는 프로덕션급 K8s manifest
```

[에이전트 스킬](./agent-skills.md)에서 47개의 전문화된 스킬 상세 정보를 참고하세요.

## 또한 참고하세요

- [에이전트 스킬](./agent-skills.md) - 전문화된 지식 패키지
- [에이전트 참고자료](./agents.md) - 완벽한 에이전트 카탈로그
- [플러그인 참고자료](./plugins.md) - 모든 63개 플러그인
- [아키텍처](./architecture.md) - 설계 원칙
