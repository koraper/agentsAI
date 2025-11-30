# 아키텍처 & 설계 원칙

이 마켓플레이스는 세분화, 구성 가능성 및 최소 토큰 사용에 중점을 두고 업계 모범 사례를 따릅니다.

## 핵심 철학

### 단일 책임 원칙

- 각 플러그인이 **한 가지를 잘함** (Unix 철학)
- 명확하고 집중된 목표 (5-10단어로 설명 가능)
- 평균 플러그인 크기: **3.4개 컴포넌트** (Anthropic의 2-8 패턴 준수)
- **팽창한 플러그인 없음** - 모든 플러그인이 집중적이고 목적에 맞음

### 번들링보다는 구성 가능성

- 필요에 따라 플러그인 혼합 및 일치
- 워크플로우 오케스트레이터가 집중된 플러그인 구성
- 강제 기능 번들링 없음
- 플러그인 간 명확한 경계

### 컨텍스트 효율성

- 더 작은 도구 = 더 빠른 처리
- LLM 컨텍스트 윈도우에 더 잘 맞음
- 더 정확하고 집중된 응답
- 필요한 것만 설치

### 유지 보수 가능성

- 단일 목표 = 더 쉬운 업데이트
- 명확한 경계 = 격리된 변경
- 덜한 중복 = 더 간단한 유지 보수
- 격리된 종속성

## 세분화된 플러그인 아키텍처

### 플러그인 분포

- **63개의 집중된 플러그인** 특정 사용 사례에 최적화됨
- **23개의 명확한 카테고리** 각 카테고리 1-6개의 플러그인으로 쉬운 검색
- 도메인별로 구성:
  - **개발**: 4개 플러그인 (디버깅, 백엔드, 프론트엔드, 다중 플랫폼)
  - **보안**: 4개 플러그인 (스캔, 규정 준수, 백엔드-API, 프론트엔드-모바일)
  - **작업**: 4개 플러그인 (사고, 진단, 분산, 관찰성)
  - **언어**: 7개 플러그인 (Python, JS/TS, 시스템, JVM, 스크립팅, 함수형, 임베디드)
  - **인프라**: 5개 플러그인 (배포, 검증, K8s, 클라우드, CI/CD)
  - 그리고 18개의 더 전문화된 카테고리

### 컴포넌트 분해

**85개의 전문화된 에이전트**
- 깊은 지식을 가진 도메인 전문가
- 아키텍처, 언어, 인프라, 품질, 데이터/AI, 문서, 비즈니스 및 SEO 전체에 걸쳐 구성
- 모델 최적화 (47개 Haiku, 97개 Sonnet) 성능 및 비용을 위해

**15개의 워크플로우 오케스트레이터**
- 다중 에이전트 조정 시스템
- 풀스택 개발, 보안 강화, ML 파이프라인, 사고 대응 같은 복잡한 작업
- 미리 구성된 에이전트 워크플로우

**44개의 개발 도구**
- 최적화된 유틸리티 포함:
  - 프로젝트 스캐폴딩 (Python, TypeScript, Rust)
  - 보안 스캔 (SAST, 종속성 감시, XSS)
  - 테스트 생성 (pytest, Jest)
  - 컴포넌트 스캐폴딩 (React, React Native)
  - 인프라 설정 (Terraform, Kubernetes)

**47개의 에이전트 스킬**
- 모듈화된 지식 패키지
- 점진적 공개 아키텍처
- 14개 플러그인에 걸친 도메인 특화 전문성
- 사양 준수 (Anthropic Agent Skills Specification)

## 저장소 구조

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # 마켓플레이스 카탈로그 (63개 플러그인)
├── plugins/                       # 격리된 플러그인 디렉토리
│   ├── python-development/
│   │   ├── agents/               # Python 언어 에이전트
│   │   │   ├── python-pro.md
│   │   │   ├── django-pro.md
│   │   │   └── fastapi-pro.md
│   │   ├── commands/             # Python 도구
│   │   │   └── python-scaffold.md
│   │   └── skills/               # Python 스킬 (5개 총)
│   │       ├── async-python-patterns/
│   │       ├── python-testing-patterns/
│   │       ├── python-packaging/
│   │       ├── python-performance-optimization/
│   │       └── uv-package-manager/
│   ├── backend-development/
│   │   ├── agents/
│   │   │   ├── backend-architect.md
│   │   │   ├── graphql-architect.md
│   │   │   └── tdd-orchestrator.md
│   │   ├── commands/
│   │   │   └── feature-development.md
│   │   └── skills/               # 백엔드 스킬 (3개 총)
│   │       ├── api-design-principles/
│   │       ├── architecture-patterns/
│   │       └── microservices-patterns/
│   ├── security-scanning/
│   │   ├── agents/
│   │   │   └── security-auditor.md
│   │   ├── commands/
│   │   │   ├── security-hardening.md
│   │   │   ├── security-sast.md
│   │   │   └── security-dependencies.md
│   │   └── skills/               # 보안 스킬 (1개 총)
│   │       └── sast-configuration/
│   └── ... (60개의 더 많은 격리된 플러그인)
├── docs/                          # 문서
│   ├── agent-skills.md           # Agent Skills 가이드
│   ├── agents.md                 # 에이전트 참고자료
│   ├── plugins.md                # 플러그인 카탈로그
│   ├── usage.md                  # 사용 가이드
│   └── architecture.md           # 이 파일
└── README.md                      # 빠른 시작
```

## 플러그인 구조

각 플러그인 포함:

- **agents/** - 그 도메인에 대한 전문화된 에이전트 (선택 사항)
- **commands/** - 해당 플러그인에 대한 도구 및 워크플로우 (선택 사항)
- **skills/** - 점진적 공개가 있는 모듈화된 지식 패키지 (선택 사항)

### 최소 요구 사항

- 최소 하나의 에이전트 또는 하나의 명령
- 명확하고 집중된 목표
- 모든 파일에서 적절한 frontmatter
- marketplace.json의 항목

### 예시 플러그인

```
plugins/kubernetes-operations/
├── agents/
│   └── kubernetes-architect.md   # K8s 아키텍처 및 설계
├── commands/
│   └── k8s-deploy.md            # 배포 자동화
└── skills/
    ├── k8s-manifest-generator/   # Manifest 생성 스킬
    ├── helm-chart-scaffolding/   # Helm 차트 스킬
    ├── gitops-workflow/          # GitOps 자동화 스킬
    └── k8s-security-policies/    # 보안 정책 스킬
```

## 에이전트 스킬 아키텍처

### 점진적 공개

스킬은 토큰 효율을 위해 3단계 아키텍처를 사용합니다:

1. **메타데이터** (Frontmatter): 이름 및 활성화 기준 (항상 로드됨)
2. **지침**: 핵심 지침 및 패턴 (활성화될 때 로드됨)
3. **리소스**: 예제 및 템플릿 (요청 시 로드됨)

### 규격 준수

모든 스킬은 [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)을 따릅니다:

```yaml
---
name: skill-name                  # 필수: 하이픈-케이스
description: 스킬의 기능. 사용 시점 [트리거]. # 필수: < 1024자
---

# 점진적 공개가 있는 스킬 콘텐츠
```

### 이점

- **토큰 효율**: 필요할 때만 관련 지식 로드
- **전문화된 전문성**: 팽창 없이 깊은 도메인 지식
- **명확한 활성화**: 명시적 트리거가 원치 않는 호출 방지
- **구성 가능성**: 워크플로우 간 스킬 혼합 및 일치
- **유지 보수 가능성**: 격리된 업데이트가 다른 스킬에 영향을 주지 않음

자세한 내용은 [에이전트 스킬](./agent-skills.md)를 참조하세요.

## 모델 구성 전략

### 2단계 아키텍처

시스템은 Claude Opus 및 Sonnet 모델을 전략적으로 사용합니다:

| 모델 | 개수 | 사용 사례 |
|-------|-------|----------|
| Haiku | 47개 에이전트 | 빠른 실행, 결정론적 작업 |
| Sonnet | 97개 에이전트 | 복잡한 추론, 아키텍처 결정 |

### 선택 기준

**Haiku - 빠른 실행 & 결정론적 작업**
- 명확한 사양에서 코드 생성
- 확립된 패턴에 따른 테스트 생성
- 명확한 템플릿이 있는 문서 작성
- 인프라 작업 실행
- 데이터베이스 쿼리 최적화 수행
- 고객 지원 응답 처리
- SEO 최적화 작업 처리
- 배포 파이프라인 관리

**Sonnet - 복잡한 추론 & 아키텍처**
- 시스템 아키텍처 설계
- 기술 선택 결정 수행
- 보안 감사 수행
- 아키텍처 패턴의 코드 검토
- 복잡한 AI/ML 파이프라인 생성
- 언어별 전문 지식 제공
- 다중 에이전트 워크플로우 조정
- 비즈니스 중요 법률/HR 문제 처리

### 하이브리드 오케스트레이션

최적의 성능과 비용을 위해 모델 결합:

```
계획 단계 (Sonnet) → 실행 단계 (Haiku) → 검토 단계 (Sonnet)

예:
backend-architect (Sonnet) API 설계
  ↓
엔드포인트 생성 (Haiku) 사양 구현
  ↓
test-automator (Haiku) 테스트 생성
  ↓
code-reviewer (Sonnet) 아키텍처 검증
```

## 성능 & 품질

### 최적화된 토큰 사용

- **격리된 플러그인** 필요한 것만 로드
- **세분화된 아키텍처** 불필요한 컨텍스트 감소
- **점진적 공개** (스킬) 요청 시 지식 로드
- **명확한 경계** 컨텍스트 오염 방지

### 컴포넌트 범위

- **100% 에이전트 범위** - 모든 플러그인이 최소 하나의 에이전트 포함
- **100% 컴포넌트 가용성** - 모든 85개 에이전트가 플러그인 전체에서 접근 가능
- **효율적인 분포** - 플러그인당 평균 3.4개 컴포넌트

### 검색 가능성

- **명확한 플러그인 이름** 목적을 즉시 전달
- **논리적 분류** 23개의 명확하게 정의된 카테고리
- **검색 가능한 문서** 교차 참조 포함
- **찾기 쉬움** 일의 올바른 도구를 찾기

## 설계 패턴

### 패턴 1: 단일 목적 플러그인

각 플러그인이 하나의 도메인에 집중:

```
python-development/
├── agents/           # Python 언어 전문가
├── commands/         # Python 프로젝트 스캐폴딩
└── skills/           # Python 특화 지식
```

**이점:**
- 명확한 책임
- 유지 보수 용이
- 최소 토큰 사용
- 다른 플러그인과 구성 가능

### 패턴 2: 워크플로우 오케스트레이션

오케스트레이터 플러그인이 여러 에이전트를 조정:

```
full-stack-orchestration/
└── commands/
    └── full-stack-feature.md    # 7개 이상의 에이전트 조정
```

**오케스트레이션:**
1. backend-architect (API 설계)
2. database-architect (스키마 설계)
3. frontend-developer (UI 구축)
4. test-automator (테스트 생성)
5. security-auditor (보안 검토)
6. deployment-engineer (CI/CD)
7. observability-engineer (모니터링)

### 패턴 3: 에이전트 + 스킬 통합

에이전트는 추론을 제공하고 스킬은 지식을 제공:

```
User: "Build FastAPI project with async patterns"
  ↓
fastapi-pro agent (조정)
  ↓
fastapi-templates skill (패턴 제공)
  ↓
python-scaffold command (프로젝트 생성)
```

### 패턴 4: 다중 플러그인 구성

복잡한 워크플로우가 여러 플러그인을 사용:

```
기능 개발 워크플로우:
1. backend-development:feature-development
2. security-scanning:security-hardening
3. unit-testing:test-generate
4. code-review-ai:ai-review
5. cicd-automation:workflow-automate
6. observability-monitoring:monitor-setup
```

## 버전 관리 & 업데이트

### 마켓플레이스 업데이트

- `.claude-plugin/marketplace.json`의 마켓플레이스 카탈로그
- 플러그인의 의미 있는 버전 관리
- 유지 보수된 역호환성
- 주요 변경 사항에 대한 명확한 마이그레이션 가이드

### 플러그인 업데이트

- 개별 플러그인 업데이트가 다른 영향 없음
- 스킬을 독립적으로 업데이트 가능
- 에이전트를 워크플로우 손상 없이 추가/제거 가능
- 명령이 안정적인 인터페이스 유지

## 기여 가이드라인

### 플러그인 추가

1. 플러그인 디렉토리 생성: `plugins/{plugin-name}/`
2. 에이전트 및/또는 명령 추가
3. 선택적으로 스킬 추가
4. marketplace.json 업데이트
5. 적절한 카테고리에서 문서화

### 에이전트 추가

1. `plugins/{plugin-name}/agents/{agent-name}.md` 생성
2. frontmatter 추가 (이름, 설명, 모델)
3. 포괄적인 시스템 프롬프트 작성
4. 플러그인 정의 업데이트

### 스킬 추가

1. `plugins/{plugin-name}/skills/{skill-name}/SKILL.md` 생성
2. YAML frontmatter 추가 (이름, "사용 시점"이 있는 설명)
3. 점진적 공개가 있는 스킬 콘텐츠 작성
4. marketplace.json의 플러그인 스킬 배열에 추가

### 품질 표준

- **명확한 명명** - 하이픈-케이스, 설명적
- **집중된 범위** - 단일 책임
- **완전한 문서** - 무엇, 언제, 어떻게
- **테스트된 기능** - 커밋 전 확인
- **사양 준수** - Anthropic 가이드라인 따르기

## 또한 참고하세요

- [에이전트 스킬](./agent-skills.md) - 모듈화된 지식 패키지
- [에이전트 참고자료](./agents.md) - 완전한 에이전트 카탈로그
- [플러그인 참고자료](./plugins.md) - 모든 63개 플러그인
- [사용 가이드](./usage.md) - 명령 및 워크플로우
