Orchestrate 포괄적인 multi-dimensional 코드 review 사용하여 specialized review 에이전트

[확장된 thinking: This 워크플로우 수행합니다 an exhaustive 코드 review 에 의해 orchestrating 여러 specialized 에이전트 에서 sequential phases. 각 단계 빌드 upon 이전 findings 에 create a 포괄적인 review 것 covers 코드 품질, security, 성능, 테스트, 문서화, 및 최선의 관행. The 워크플로우 통합합니다 현대적인 AI-지원된 review tools, 정적 분석, security scanning, 및 자동화된 품질 메트릭. Results are 통합된 into actionable feedback 와 함께 명확한 우선순위 지정 및 remediation guidance. The phased 접근법 보장합니다 thorough coverage 동안 maintaining 효율성 통해 병렬로 에이전트 실행 곳 적절한.]

## Review 구성 Options

- **--security-focus**: Prioritize security 취약점 및 OWASP compliance
- **--성능-긴급**: Emphasize 성능 bottlenecks 및 scalability 이슈
- **--tdd-review**: Include TDD compliance 및 test-첫 번째 확인
- **--ai-지원된**: Enable AI-powered review tools (Copilot, Codium, Bito)
- **--strict-최빈값**: Fail review 에 어떤 긴급 이슈 찾은
- **--메트릭-보고서**: Generate 상세한 품질 메트릭 대시보드
- **--프레임워크 [name]**: Apply 프레임워크-특정 최선의 관행 (React, Spring, Django, etc.)

## 단계 1: 코드 품질 & 아키텍처 Review

Use 작업 tool 에 orchestrate 품질 및 아키텍처 에이전트 에서 병렬로:

### 1A. 코드 품질 분석
- Use 작업 tool 와 함께 subagent_type="코드-리뷰어"
- Prompt: "Perform 포괄적인 코드 품질 review 위한: $인수. Analyze 코드 complexity, 유지보수성 인덱스, technical debt, 코드 duplication, naming 규약, 및 adherence 에 Clean 코드 원칙. Integrate 와 함께 SonarQube, CodeQL, 및 Semgrep 위한 정적 분석. Check 위한 코드 smells, anti-패턴, 및 위반 of 견고한 원칙. Generate cyclomatic complexity 메트릭 및 identify 리팩토링 opportunities."
- 예상되는 출력: 품질 메트릭, 코드 smell 인벤토리, 리팩토링 recommendations
- 컨텍스트: 초기 codebase 분석, 아니요 종속성 에 other phases

### 1B. 아키텍처 & 설계 Review
- Use 작업 tool 와 함께 subagent_type="아키텍트-review"
- Prompt: "Review architectural 설계 패턴 및 structural 무결성 에서: $인수. Evaluate microservices boundaries, API 설계, 데이터베이스 스키마, 종속성 관리, 및 adherence 에 도메인 주도 설계 원칙. Check 위한 circular 종속성, inappropriate 결합, missing abstractions, 및 architectural drift. Verify compliance 와 함께 엔터프라이즈 아키텍처 표준 및 클라우드 네이티브 패턴."
- 예상되는 출력: 아키텍처 평가, 설계 패턴 분석, structural recommendations
- 컨텍스트: 실행합니다 병렬로 와 함께 코드 품질 분석

## 단계 2: Security & 성능 Review

Use 작업 tool 와 함께 security 및 성능 에이전트, incorporating 단계 1 findings:

### 2A. Security 취약점 평가
- Use 작업 tool 와 함께 subagent_type="security-감사자"
- Prompt: "Execute 포괄적인 security audit 에: $인수. Perform OWASP Top 10 분석, 종속성 취약점 scanning 와 함께 Snyk/Trivy, secrets 감지 와 함께 GitLeaks, 입력 검증 review, 인증/인가 평가, 및 cryptographic 구현 review. Include findings 에서 단계 1 아키텍처 review: {phase1_architecture_context}. Check 위한 SQL 인젝션, XSS, CSRF, insecure 역직렬화, 및 구성 security 이슈."
- 예상되는 출력: 취약점 보고서, CVE 목록, security 위험 매트릭스, remediation steps
- 컨텍스트: Incorporates architectural 취약점 식별된 에서 단계 1B

### 2B. 성능 & Scalability 분석
- Use 작업 tool 와 함께 subagent_type="애플리케이션-성능::성능-엔지니어"
- Prompt: "Conduct 성능 분석 및 scalability 평가 위한: $인수. 프로필 코드 위한 CPU/메모리 hotspots, analyze 데이터베이스 쿼리 성능, review 캐싱 strategies, identify N+1 문제, assess 연결 풀링, 및 evaluate asynchronous 처리 패턴. Consider architectural findings 에서 단계 1: {phase1_architecture_context}. Check 위한 메모리 leaks, 리소스 contention, 및 bottlenecks under load."
- 예상되는 출력: 성능 메트릭, 병목 분석, 최적화 recommendations
- 컨텍스트: Uses 아키텍처 인사이트 에 identify systemic 성능 이슈

## 단계 3: 테스트 & 문서화 Review

Use 작업 tool 위한 test 및 문서화 품질 평가:

### 3A. Test Coverage & 품질 분석
- Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
- Prompt: "Evaluate 테스트 전략 및 구현 위한: $인수. Analyze 단위 test coverage, 통합 test 완전성, end-에-end test scenarios, test pyramid adherence, 및 test 유지보수성. Review test 품질 메트릭 포함하여 assertion density, test 격리, mock usage, 및 flakiness. Consider security 및 성능 test 요구사항 에서 단계 2: {phase2_security_context}, {phase2_performance_context}. Verify TDD 관행 만약 --tdd-review flag is 세트."
- 예상되는 출력: Coverage 보고서, test 품질 메트릭, 테스트 간격 분석
- 컨텍스트: Incorporates security 및 성능 테스트 요구사항 에서 단계 2

### 3B. 문서화 & API 사양 Review
- Use 작업 tool 와 함께 subagent_type="코드-문서화::docs-아키텍트"
- Prompt: "Review 문서화 완전성 및 품질 위한: $인수. Assess inline 코드 문서화, API 문서화 (OpenAPI/Swagger), 아키텍처 결정 레코드 (ADRs), README 완전성, 배포 안내합니다, 및 runbooks. Verify 문서화 reflects actual 구현 based 에 모든 이전 단계 findings: {phase1_context}, {phase2_context}. Check 위한 오래됨 문서화, missing 예제, 및 불명확한 explanations."
- 예상되는 출력: 문서화 coverage 보고서, inconsistency 목록, improvement recommendations
- 컨텍스트: Cross-참조 모든 이전 findings 에 ensure 문서화 정확성

## 단계 4: 최선의 관행 & 표준 Compliance

Use 작업 tool 에 verify 프레임워크-특정 및 산업 최선의 관행:

### 4A. 프레임워크 & Language 최선의 관행
- Use 작업 tool 와 함께 subagent_type="프레임워크-마이그레이션::레거시-modernizer"
- Prompt: "Verify adherence 에 프레임워크 및 language 최선의 관행 위한: $인수. Check 현대적인 JavaScript/TypeScript 패턴, React hooks 최선의 관행, Python PEP compliance, Java 엔터프라이즈 패턴, Go idiomatic 코드, 또는 프레임워크-특정 규약 (based 에 --프레임워크 flag). Review 패키지 관리, 빌드 구성, 환경 처리, 및 배포 관행. Include 모든 품질 이슈 에서 이전 phases: {all_previous_contexts}."
- 예상되는 출력: 최선의 관행 compliance 보고서, modernization recommendations
- 컨텍스트: Synthesizes 모든 이전 findings 위한 프레임워크-특정 guidance

### 4B. CI/CD & DevOps 관행 Review
- Use 작업 tool 와 함께 subagent_type="cicd-자동화::배포-엔지니어"
- Prompt: "Review CI/CD 파이프라인 및 DevOps 관행 위한: $인수. Evaluate 빌드 자동화, test 자동화 통합, 배포 strategies (blue-green, canary), 인프라 처럼 코드, 모니터링/observability 설정, 및 인시던트 응답 절차. Assess 파이프라인 security, 아티팩트 관리, 및 롤백 역량. Consider 모든 이슈 식별된 에서 이전 phases 것 impact 배포: {all_critical_issues}."
- 예상되는 출력: 파이프라인 평가, DevOps maturity 평가, 자동화 recommendations
- 컨텍스트: Focuses 에 operationalizing 수정합니다 위한 모든 식별된 이슈

## 통합된 보고서 세대

Compile 모든 단계 출력 into 포괄적인 review 보고서:

### 긴급 이슈 (P0 - Must Fix 즉시)
- Security 취약점 와 함께 CVSS > 7.0
- 데이터 loss 또는 corruption 위험
- 인증/인가 bypasses
- Production 안정성 위협
- Compliance 위반 (GDPR, PCI DSS, SOC2)

### High Priority (P1 - Fix 이전 다음 릴리스)
- 성능 bottlenecks impacting 사용자 experience
- Missing 긴급 test coverage
- Architectural anti-패턴 causing technical debt
- 오래됨 종속성 와 함께 known 취약점
- 코드 품질 이슈 affecting 유지보수성

### Medium Priority (P2 - Plan 위한 다음 Sprint)
- Non-긴급 성능 optimizations
- 문서화 gaps 및 inconsistencies
- 코드 리팩토링 opportunities
- Test 품질 improvements
- DevOps 자동화 enhancements

### Low Priority (P3 - Track 에서 Backlog)
- 스타일 가이드 위반
- 부수적 코드 smell 이슈
- Nice-에-have 문서화 업데이트합니다
- Cosmetic improvements

## Success Criteria

Review is considered 성공한 때:
- 모든 긴급 security 취약점 are 식별된 및 문서화된
- 성능 bottlenecks are profiled 와 함께 remediation 경로
- Test coverage gaps are mapped 와 함께 priority recommendations
- 아키텍처 위험 are 평가된 와 함께 mitigation strategies
- 문서화 reflects actual 구현 상태
- 프레임워크 최선의 관행 compliance is 확인된
- CI/CD 파이프라인 지원합니다 safe 배포 of 검토된 코드
- 명확한, actionable feedback is 제공된 위한 모든 findings
- 메트릭 대시보드 표시합니다 improvement trends
- 팀 has 명확한 우선순위가 지정됨 action plan 위한 remediation

Target: $인수