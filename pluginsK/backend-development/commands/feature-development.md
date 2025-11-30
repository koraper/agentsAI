Orchestrate end-에-end 기능 개발 에서 요구사항 에 production 배포:

[확장된 thinking: This 워크플로우 오케스트레이션합니다 specialized 에이전트 통해 포괄적인 기능 개발 phases - 에서 발견 및 계획 통해 구현, 테스트, 및 배포. 각 단계 빌드 에 이전 출력, 보장하는 일관된 기능 전달. The 워크플로우 지원합니다 여러 개발 methodologies (전통적인, TDD/BDD, DDD), 기능 complexity levels, 및 현대적인 배포 strategies 포함하여 기능 flags, gradual rollouts, 및 observability-첫 번째 개발. 에이전트 receive 상세한 컨텍스트 에서 이전 phases 에 maintain 일관성 및 품질 throughout the 개발 lifecycle.]

## 구성 Options

### 개발 Methodology
- **전통적인**: Sequential 개발 와 함께 테스트 이후 구현
- **tdd**: 테스트 주도 개발 와 함께 red-green-refactor 순환합니다
- **bdd**: 행동 주도 개발 와 함께 시나리오-based 테스트
- **ddd**: 도메인 주도 설계 와 함께 제한된 contexts 및 집계합니다

### 기능 Complexity
- **간단한**: Single 서비스, 최소 통합 (1-2 days)
- **medium**: 여러 서비스, moderate 통합 (3-5 days)
- **복잡한**: Cross-도메인, 광범위한 통합 (1-2 weeks)
- **epic**: 주요 architectural 변경합니다, 여러 teams (2+ weeks)

### 배포 전략
- **직접**: Immediate rollout 에 모든 사용자
- **canary**: Gradual rollout 시작하는 와 함께 5% of traffic
- **기능-flag**: 제어된 activation 를 통해 기능 toggles
- **blue-green**: Zero-downtime 배포 와 함께 순간 롤백
- **a-b-test**: 분할된 traffic 위한 experimentation 및 메트릭

## 단계 1: 발견 & 요구사항 계획

1. **비즈니스 분석 & 요구사항**
   - Use 작업 tool 와 함께 subagent_type="비즈니스-분석::비즈니스-분석가"
   - Prompt: "Analyze 기능 요구사항 위한: $인수. Define 사용자 stories, acceptance criteria, success 메트릭, 및 비즈니스 값. Identify stakeholders, 종속성, 및 위험. Create 기능 사양 document 와 함께 명확한 범위 boundaries."
   - 예상되는 출력: 요구사항 document 와 함께 사용자 stories, success 메트릭, 위험 평가
   - 컨텍스트: 초기 기능 요청 및 비즈니스 컨텍스트

2. **Technical 아키텍처 설계**
   - Use 작업 tool 와 함께 subagent_type="포괄적인-review::아키텍트-review"
   - Prompt: "설계 technical 아키텍처 위한 기능: $인수. 사용하여 요구사항: [include 비즈니스 분석 에서 단계 1]. Define 서비스 boundaries, API 계약, 데이터 모델, 통합 points, 및 technology 스택. Consider scalability, 성능, 및 security 요구사항."
   - 예상되는 출력: Technical 설계 document 와 함께 아키텍처 다이어그램, API 사양, 데이터 모델
   - 컨텍스트: 비즈니스 요구사항, 기존 시스템 아키텍처

3. **Feasibility & 위험 평가**
   - Use 작업 tool 와 함께 subagent_type="security-scanning::security-감사자"
   - Prompt: "Assess security implications 및 위험 위한 기능: $인수. Review 아키텍처: [include technical 설계 에서 단계 2]. Identify security 요구사항, compliance needs, 데이터 privacy concerns, 및 potential 취약점."
   - 예상되는 출력: Security 평가 와 함께 위험 매트릭스, compliance checklist, mitigation strategies
   - 컨텍스트: Technical 설계, regulatory 요구사항

## 단계 2: 구현 & 개발

4. **Backend 서비스 구현**
   - Use 작업 tool 와 함께 subagent_type="backend-아키텍트"
   - Prompt: "Implement backend 서비스 위한: $인수. Follow technical 설계: [include 아키텍처 에서 단계 2]. 빌드 RESTful/GraphQL APIs, implement 비즈니스 logic, integrate 와 함께 데이터 레이어, add 복원력 패턴 (회로 breakers, 재시도합니다), implement 캐싱 strategies. Include 기능 flags 위한 gradual rollout."
   - 예상되는 출력: Backend 서비스 와 함께 APIs, 비즈니스 logic, 데이터베이스 통합, 기능 flags
   - 컨텍스트: Technical 설계, API 계약, 데이터 모델

5. **Frontend 구현**
   - Use 작업 tool 와 함께 subagent_type="frontend-mobile-개발::frontend-개발자"
   - Prompt: "빌드 frontend 컴포넌트 위한: $인수. Integrate 와 함께 backend APIs: [include API 엔드포인트 에서 단계 4]. Implement responsive UI, 상태 관리, 오류 처리, 로드 states, 및 분석 추적. Add 기능 flag 통합 위한 A/B 테스트 역량."
   - 예상되는 출력: Frontend 컴포넌트 와 함께 API 통합, 상태 관리, 분석
   - 컨텍스트: Backend APIs, UI/UX 설계, 사용자 stories

6. **데이터 파이프라인 & 통합**
   - Use 작업 tool 와 함께 subagent_type="데이터-engineering::데이터-엔지니어"
   - Prompt: "빌드 데이터 파이프라인 위한: $인수. 설계 ETL/ELT 프로세스, implement 데이터 검증, create 분석 이벤트, 세트 up 데이터 품질 모니터링. Integrate 와 함께 product 분석 플랫폼 위한 기능 usage 추적."
   - 예상되는 출력: 데이터 파이프라인, 분석 이벤트, 데이터 품질 확인합니다
   - 컨텍스트: 데이터 요구사항, 분석 needs, 기존 데이터 인프라

## 단계 3: 테스트 & 품질 Assurance

7. **자동화된 Test Suite**
   - Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
   - Prompt: "Create 포괄적인 test suite 위한: $인수. Write 단위 테스트합니다 위한 backend: [에서 단계 4] 및 frontend: [에서 단계 5]. Add 통합 테스트합니다 위한 API 엔드포인트, E2E 테스트합니다 위한 긴급 사용자 journeys, 성능 테스트합니다 위한 scalability 검증. Ensure minimum 80% 코드 coverage."
   - 예상되는 출력: Test suites 와 함께 단위, 통합, E2E, 및 성능 테스트합니다
   - 컨텍스트: 구현 코드, acceptance criteria, test 요구사항

8. **Security 검증**
   - Use 작업 tool 와 함께 subagent_type="security-scanning::security-감사자"
   - Prompt: "Perform security 테스트 위한: $인수. Review 구현: [include backend 및 frontend 에서 steps 4-5]. Run OWASP 확인합니다, penetration 테스트, 종속성 scanning, 및 compliance 검증. Verify 데이터 암호화, 인증, 및 인가."
   - 예상되는 출력: Security test results, 취약점 보고서, remediation actions
   - 컨텍스트: 구현 코드, security 요구사항

9. **성능 최적화**
   - Use 작업 tool 와 함께 subagent_type="애플리케이션-성능::성능-엔지니어"
   - Prompt: "Optimize 성능 위한: $인수. Analyze backend 서비스: [에서 단계 4] 및 frontend: [에서 단계 5]. 프로필 코드, optimize 쿼리, implement 캐싱, reduce bundle sizes, improve load times. 세트 up 성능 budgets 및 모니터링."
   - 예상되는 출력: 성능 improvements, 최적화 보고서, 성능 메트릭
   - 컨텍스트: 구현 코드, 성능 요구사항

## 단계 4: 배포 & 모니터링

10. **배포 전략 & 파이프라인**
    - Use 작업 tool 와 함께 subagent_type="배포-strategies::배포-엔지니어"
    - Prompt: "Prepare 배포 위한: $인수. Create CI/CD 파이프라인 와 함께 자동화된 테스트합니다: [에서 단계 7]. Configure 기능 flags 위한 gradual rollout, implement blue-green 배포, 세트 up 롤백 절차. Create 배포 runbook 및 롤백 plan."
    - 예상되는 출력: CI/CD 파이프라인, 배포 구성, 롤백 절차
    - 컨텍스트: Test suites, 인프라 요구사항, 배포 전략

11. **Observability & 모니터링**
    - Use 작업 tool 와 함께 subagent_type="observability-모니터링::observability-엔지니어"
    - Prompt: "세트 up observability 위한: $인수. Implement 분산 추적, 사용자 정의 메트릭, 오류 추적, 및 경고. Create 대시보드 위한 기능 usage, 성능 메트릭, 오류 평가합니다, 및 비즈니스 KPIs. 세트 up SLOs/SLIs 와 함께 자동화된 경고."
    - 예상되는 출력: 모니터링 대시보드, 경고, SLO definitions, observability 인프라
    - 컨텍스트: 기능 구현, success 메트릭, operational 요구사항

12. **문서화 & 지식 전송**
    - Use 작업 tool 와 함께 subagent_type="문서화-세대::docs-아키텍트"
    - Prompt: "Generate 포괄적인 문서화 위한: $인수. Create API 문서화, 사용자 안내합니다, 배포 안내합니다, 문제 해결 runbooks. Include 아키텍처 다이어그램, 데이터 흐름 다이어그램, 및 통합 안내합니다. Generate 자동화된 changelog 에서 commits."
    - 예상되는 출력: API docs, 사용자 안내합니다, runbooks, 아키텍처 문서화
    - 컨텍스트: 모든 이전 phases' 출력

## 실행 매개변수

### 필수 매개변수
- **--기능**: 기능 name 및 설명
- **--methodology**: 개발 접근법 (전통적인|tdd|bdd|ddd)
- **--complexity**: 기능 complexity 레벨 (간단한|medium|복잡한|epic)

### 선택적 매개변수
- **--배포-전략**: 배포 접근법 (직접|canary|기능-flag|blue-green|a-b-test)
- **--test-coverage-min**: Minimum test coverage threshold (default: 80%)
- **--성능-budget**: 성능 요구사항 (e.g., <200ms 응답 시간)
- **--rollout-백분율**: 초기 rollout 백분율 위한 gradual 배포 (default: 5%)
- **--기능-flag-서비스**: 기능 flag 프로바이더 (launchdarkly|분할된|unleash|사용자 정의)
- **--분석-플랫폼**: 분석 통합 (segment|amplitude|mixpanel|사용자 정의)
- **--모니터링-스택**: Observability tools (datadog|newrelic|grafana|사용자 정의)

## Success Criteria

- 모든 acceptance criteria 에서 비즈니스 요구사항 are met
- Test coverage exceeds minimum threshold (80% default)
- Security scan 표시합니다 아니요 긴급 취약점
- 성능 meets 정의된 budgets 및 SLOs
- 기능 flags 구성된 위한 제어된 rollout
- 모니터링 및 경고 완전히 operational
- 문서화 완전한 및 approved
- 성공한 배포 에 production 와 함께 롤백 역량
- Product 분석 추적 기능 usage
- A/B test 메트릭 구성된 (만약 적용 가능한)

## 롤백 전략

만약 이슈 arise 동안 또는 이후 배포:
1. Immediate 기능 flag disable (< 1 minute)
2. Blue-green traffic switch (< 5 minutes)
3. 전체 배포 롤백 를 통해 CI/CD (< 15 minutes)
4. 데이터베이스 마이그레이션 롤백 만약 필요한 (좌표 와 함께 데이터 팀)
5. 인시던트 post-mortem 및 수정합니다 이전 re-배포

기능 설명: $인수