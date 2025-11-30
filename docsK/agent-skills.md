# Agent Skills (에이전트 스킬)

Agent Skills는 Anthropic의 [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)을 따르는 모듈화된 패키지로, Claude의 기능을 전문적인 도메인 지식으로 확장합니다. 이 플러그인 생태계는 15개의 플러그인에 걸쳐 **57개의 전문화된 스킬**을 포함하여 점진적 공개와 효율적인 토큰 사용을 가능하게 합니다.

## 개요

스킬은 Claude에게 미리 모든 것을 컨텍스트에 로드하지 않고도 특정 도메인에서 깊은 전문성을 제공합니다. 각 스킬에는 다음이 포함됩니다:

- **YAML Frontmatter**: 이름과 활성화 기준
- **점진적 공개**: 메타데이터 → 지침 → 리소스
- **활성화 트리거**: 자동 호출을 위한 명확한 "사용 시점" 조항

## 플러그인별 스킬

### Kubernetes 작업 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **k8s-manifest-generator** | 배포, 서비스, ConfigMaps, Secrets을 위한 프로덕션급 Kubernetes manifest 생성 |
| **helm-chart-scaffolding** | Helm 차트 설계, 구성 및 관리 |
| **gitops-workflow** | ArgoCD 및 Flux를 사용한 GitOps 워크플로우 구현 |
| **k8s-security-policies** | NetworkPolicy, PodSecurityPolicy 및 RBAC를 포함한 Kubernetes 보안 정책 구현 |

### LLM 애플리케이션 개발 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **langchain-architecture** | 에이전트, 메모리 및 도구 통합이 포함된 LangChain 프레임워크를 사용한 LLM 애플리케이션 설계 |
| **prompt-engineering-patterns** | LLM 성능 및 안정성을 위한 고급 프롬프트 엔지니어링 기법 마스터 |
| **rag-implementation** | 벡터 데이터베이스 및 의미 검색을 사용한 RAG(Retrieval-Augmented Generation) 시스템 구축 |
| **llm-evaluation** | 자동화된 메트릭 및 벤치마킹을 통한 포괄적인 평가 전략 구현 |

### 백엔드 개발 (5개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **api-design-principles** | 직관적이고 확장 가능하며 유지 가능한 API를 위한 REST 및 GraphQL API 설계 마스터 |
| **architecture-patterns** | Clean Architecture, Hexagonal Architecture 및 Domain-Driven Design 구현 |
| **microservices-patterns** | 서비스 경계, 이벤트 기반 통신 및 탄력성을 갖춘 마이크로서비스 설계 |
| **workflow-orchestration-patterns** | 분산 시스템, saga 패턴 및 상태 관리를 위한 Temporal을 사용한 내구성 있는 워크플로우 설계 |
| **temporal-python-testing** | pytest, 시간 건너뛰기 및 mocking 전략을 사용한 Temporal 워크플로우 테스트 |

### 개발자 필수 (8개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **git-advanced-workflows** | rebase, cherry-picking, bisect, worktrees 및 reflog를 포함한 고급 Git 워크플로우 마스터 |
| **sql-optimization-patterns** | SQL 쿼리 최적화, 인덱싱 전략 및 EXPLAIN 분석으로 데이터베이스 성능 향상 |
| **error-handling-patterns** | 예외, Result 타입 및 우아한 성능 저하를 통한 견고한 오류 처리 구현 |
| **code-review-excellence** | 건설적인 피드백 및 체계적인 분석을 통한 효과적인 코드 리뷰 제공 |
| **e2e-testing-patterns** | Playwright 및 Cypress를 사용한 신뢰할 수 있는 E2E 테스트 스위트 구축 |
| **auth-implementation-patterns** | JWT, OAuth2, 세션 및 RBAC를 사용한 인증 및 권한 부여 구현 |
| **debugging-strategies** | 체계적인 디버깅 기법, 프로파일링 도구 및 근본 원인 분석 마스터 |
| **monorepo-management** | 확장 가능한 다중 패키지 프로젝트를 위해 Turborepo, Nx 및 pnpm 워크스페이스로 모노레포 관리 |

### 블록체인 & Web3 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **defi-protocol-templates** | staking, AMM, governance 및 lending용 템플릿을 사용한 DeFi 프로토콜 구현 |
| **nft-standards** | 메타데이터 및 마켓플레이스 통합이 포함된 NFT 표준(ERC-721, ERC-1155) 구현 |
| **solidity-security** | 취약점 방지 및 안전한 패턴 구현을 위한 스마트 계약 보안 마스터 |
| **web3-testing** | Hardhat 및 Foundry를 사용한 스마트 계약 테스트 및 메인넷 포킹 |

### CI/CD 자동화 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **deployment-pipeline-design** | 승인 게이트 및 보안 확인이 있는 다단계 CI/CD 파이프라인 설계 |
| **github-actions-templates** | 테스트, 빌드 및 배포를 위한 프로덕션급 GitHub Actions 워크플로우 생성 |
| **gitlab-ci-patterns** | 다단계 워크플로우 및 분산 러너가 있는 GitLab CI/CD 파이프라인 구축 |
| **secrets-management** | Vault, AWS Secrets Manager 또는 기본 솔루션을 사용한 보안 시크릿 관리 구현 |

### 클라우드 인프라 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **terraform-module-library** | AWS, Azure 및 GCP 인프라를 위한 재사용 가능한 Terraform 모듈 구축 |
| **multi-cloud-architecture** | 공급업체 종속을 피하는 다중 클라우드 아키텍처 설계 |
| **hybrid-cloud-networking** | 온프레미스와 클라우드 플랫폼 간의 안전한 연결 구성 |
| **cost-optimization** | 우측 크기 조정, 태깅 및 예약 인스턴스를 통한 클라우드 비용 최적화 |

### 프레임워크 마이그레이션 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **react-modernization** | React 앱 업그레이드, hooks로 마이그레이션 및 동시 기능 채택 |
| **angular-migration** | Hybrid 모드 및 증분 재작성을 사용하여 AngularJS에서 Angular로 마이그레이션 |
| **database-migration** | 다운타임 없는 마이그레이션 전략 및 변환을 사용한 데이터베이스 마이그레이션 실행 |
| **dependency-upgrade** | 호환성 분석 및 테스트를 통한 주요 종속성 업그레이드 관리 |

### 관찰성 및 모니터링 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **prometheus-configuration** | 포괄적인 메트릭 수집 및 모니터링을 위한 Prometheus 설정 |
| **grafana-dashboards** | 실시간 시스템 시각화를 위한 프로덕션 Grafana 대시보드 생성 |
| **distributed-tracing** | Jaeger 및 Tempo를 사용한 분산 추적 구현으로 요청 추적 |
| **slo-implementation** | 오류 예산 및 경고를 통한 SLI 및 SLO 정의 |

### 결제 처리 (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **stripe-integration** | 체크아웃, 구독 및 웹훅에 대한 Stripe 결제 처리 구현 |
| **paypal-integration** | 익스프레스 체크아웃 및 구독이 포함된 PayPal 결제 처리 통합 |
| **pci-compliance** | 안전한 결제 카드 데이터 처리를 위한 PCI DSS 규정 준수 구현 |
| **billing-automation** | 정기적인 결제 및 인보이싱을 위한 자동화된 청구 시스템 구축 |

### Python 개발 (5개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **async-python-patterns** | Python asyncio, 동시 프로그래밍 및 async/await 패턴 마스터 |
| **python-testing-patterns** | pytest, fixture 및 mocking을 통한 포괄적인 테스트 구현 |
| **python-packaging** | 적절한 구조 및 PyPI 출판이 있는 배포 가능한 Python 패키지 생성 |
| **python-performance-optimization** | cProfile 및 성능 모범 사례를 사용한 Python 코드 프로파일 및 최적화 |
| **uv-package-manager** | 빠른 종속성 관리 및 가상 환경을 위한 uv 패키지 매니저 마스터 |

### JavaScript/TypeScript (4개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **typescript-advanced-types** | 제네릭 및 조건부 타입을 포함한 TypeScript의 고급 타입 시스템 마스터 |
| **nodejs-backend-patterns** | Express/Fastify 및 모범 사례를 사용한 프로덕션급 Node.js 서비스 구축 |
| **javascript-testing-patterns** | Jest, Vitest 및 Testing Library를 사용한 포괄적인 테스트 구현 |
| **modern-javascript-patterns** | async/await, 구조 분해 및 함수형 프로그래밍을 포함한 ES6+ 기능 마스터 |

### API 스캐폴딩 (1개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **fastapi-templates** | async 패턴 및 오류 처리를 사용한 프로덕션급 FastAPI 프로젝트 생성 |

### 머신 러닝 작업 (1개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **ml-pipeline-workflow** | 데이터 준비에서 배포까지 엔드-투-엔드 MLOps 파이프라인 구축 |

### 보안 스캔 (1개 스킬)

| 스킬 | 설명 |
|-------|-------------|
| **sast-configuration** | 취약점 감지를 위한 SAST(정적 애플리케이션 보안 테스트) 도구 구성 |

## 스킬 작동 방식

### 활성화

Claude가 요청에서 일치하는 패턴을 감지할 때 스킬이 자동으로 활성화됩니다:

```
User: "Set up Kubernetes deployment with Helm chart"
→ Activates: helm-chart-scaffolding, k8s-manifest-generator

User: "Build a RAG system for document Q&A"
→ Activates: rag-implementation, prompt-engineering-patterns

User: "Optimize Python async performance"
→ Activates: async-python-patterns, python-performance-optimization
```

### 점진적 공개

스킬은 토큰 효율을 위해 3단계 아키텍처를 사용합니다:

1. **메타데이터** (Frontmatter): 이름 및 활성화 기준 (항상 로드됨)
2. **지침**: 핵심 지침 및 패턴 (활성화될 때 로드됨)
3. **리소스**: 예제 및 템플릿 (요청 시 로드됨)

### 에이전트와의 통합

스킬은 에이전트와 함께 깊은 도메인 전문성을 제공합니다:

- **에이전트**: 상위 수준의 추론 및 조정
- **스킬**: 전문화된 지식 및 구현 패턴

예시 워크플로우:
```
backend-architect agent → API 아키텍처 계획
  ↓
api-design-principles skill → REST/GraphQL 모범 사례 제공
  ↓
fastapi-templates skill → 프로덕션급 템플릿 제공
```

## 규격 준수

모든 55개의 스킬은 [Agent Skills Specification](https://github.com/anthropics/skills/blob/main/agent_skills_spec.md)을 따릅니다:

- ✓ 필수 `name` 필드 (하이픈 케이스)
- ✓ "사용 시점" 조항이 있는 필수 `description` 필드
- ✓ 1024자 이하의 설명
- ✓ 완전하고 자르지 않은 설명
- ✓ 적절한 YAML frontmatter 형식

## 새 스킬 생성

플러그인에 스킬을 추가하려면:

1. `plugins/{plugin-name}/skills/{skill-name}/SKILL.md` 생성
2. YAML frontmatter 추가:
   ```yaml
   ---
   name: skill-name
   description: 스킬의 기능. 사용 시점 [활성화 트리거].
   ---
   ```
3. 점진적 공개를 사용하여 포괄적인 스킬 콘텐츠 작성
4. `marketplace.json`에 스킬 경로 추가:
   ```json
   {
     "name": "plugin-name",
     "skills": ["./skills/skill-name"]
   }
   ```

### 스킬 구조

```
plugins/{plugin-name}/
└── skills/
    └── {skill-name}/
        └── SKILL.md        # Frontmatter + 콘텐츠
```

## 이점

- **토큰 효율**: 필요할 때만 관련 지식 로드
- **전문화된 전문성**: 팽창 없이 깊은 도메인 지식
- **명확한 활성화**: 명시적 트리거가 원치 않는 호출 방지
- **구성 가능성**: 워크플로우 간 스킬 믹스 및 매치
- **유지 보수 가능성**: 격리된 업데이트가 다른 스킬에 영향을 주지 않음

## 리소스

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Agent Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
