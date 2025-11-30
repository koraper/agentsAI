# 레거시 코드 Modernization 워크플로우

Orchestrate a 포괄적인 레거시 시스템 modernization 사용하여 the strangler fig 패턴, 가능하게 하는 gradual replacement of 오래됨 컴포넌트 동안 maintaining continuous 비즈니스 작업 통해 전문가 에이전트 조정.

[확장된 thinking: The strangler fig 패턴, named 이후 the tropical fig 트리 것 점진적으로 envelops 및 대체합니다 its host, represents the gold 표준 위한 위험-관리형 레거시 modernization. This 워크플로우 구현합니다 a systematic 접근법 곳 새로운 기능 점진적으로 대체합니다 레거시 컴포넌트, 허용하는 둘 다 시스템 에 coexist 동안 transition. 에 의해 orchestrating specialized 에이전트 위한 평가, 테스트, security, 및 구현, we ensure 각 마이그레이션 단계 is 검증된 이전 proceeding, minimizing disruption 동안 maximizing modernization velocity.]

## 단계 1: 레거시 평가 및 위험 분석

### 1. 포괄적인 레거시 시스템 분석
- Use 작업 tool 와 함께 subagent_type="레거시-modernizer"
- Prompt: "Analyze the 레거시 codebase 에서 $인수. Document technical debt 인벤토리 포함하여: 오래됨 종속성, 더 이상 사용되지 않음 APIs, security 취약점, 성능 bottlenecks, 및 architectural anti-패턴. Generate a modernization readiness 보고서 와 함께 컴포넌트 complexity 점수를 매깁니다 (1-10), 종속성 매핑, 및 데이터베이스 결합 분석. Identify quick wins vs 복잡한 리팩토링 targets."
- 예상되는 출력: 상세한 평가 보고서 와 함께 위험 매트릭스 및 modernization priorities

### 2. 종속성 및 통합 매핑
- Use 작업 tool 와 함께 subagent_type="아키텍트-review"
- Prompt: "Based 에 the 레거시 평가 보고서, create a 포괄적인 종속성 그래프 표시하는: 내부 모듈 종속성, 외부 서비스 integrations, shared 데이터베이스 스키마, 및 cross-시스템 데이터 흐릅니다. Identify 통합 points 것 will require 파사드 패턴 또는 어댑터 layers 동안 마이그레이션. Highlight circular 종속성 및 tight 결합 것 need 해결."
- 컨텍스트 에서 이전: 레거시 평가 보고서, 컴포넌트 complexity 점수를 매깁니다
- 예상되는 출력: Visual 종속성 맵 및 통합 포인트 카탈로그

### 3. 비즈니스 Impact 및 위험 평가
- Use 작업 tool 와 함께 subagent_type="비즈니스-분석::비즈니스-분석가"
- Prompt: "Evaluate 비즈니스 impact of modernizing 각 컴포넌트 식별된. Create 위험 평가 매트릭스 considering: 비즈니스 criticality (revenue impact), 사용자 traffic 패턴, 데이터 sensitivity, regulatory 요구사항, 및 fallback complexity. Prioritize 컴포넌트 사용하여 a 가중치가 부여된 점수 매기기 시스템: (비즈니스 값 × 0.4) + (Technical 위험 × 0.3) + (Quick Win Potential × 0.3). Define 롤백 strategies 위한 각 컴포넌트."
- 컨텍스트 에서 이전: 컴포넌트 인벤토리, 종속성 매핑
- 예상되는 출력: 우선순위가 지정됨 마이그레이션 roadmap 와 함께 위험 mitigation strategies

## 단계 2: Test Coverage Establishment

### 1. 레거시 코드 Test Coverage 분석
- Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
- Prompt: "Analyze 기존 test coverage 위한 레거시 컴포넌트 에서 $인수. Use coverage tools 에 identify untested 코드 경로, missing 통합 테스트합니다, 및 absent end-에-end scenarios. 위한 컴포넌트 와 함께 <40% coverage, generate characterization 테스트합니다 것 capture 현재 behavior 없이 modifying 기능. Create test harness 위한 safe 리팩토링."
- 예상되는 출력: Test coverage 보고서 및 characterization test suite

### 2. 계약 테스트 구현
- Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator"
- Prompt: "Implement 계약 테스트합니다 위한 모든 통합 points 식별된 에서 종속성 매핑. Create 컨슈머-driven 계약 위한 APIs, 메시지 큐 interactions, 및 데이터베이스 스키마. 세트 up 계약 확인 에서 CI/CD 파이프라인. Generate 성능 baselines 위한 응답 times 및 처리량 에 validate modernized 컴포넌트 maintain SLAs."
- 컨텍스트 에서 이전: 통합 포인트 카탈로그, 기존 test coverage
- 예상되는 출력: 계약 test suite 와 함께 성능 baselines

### 3. Test 데이터 관리 전략
- Use 작업 tool 와 함께 subagent_type="데이터-engineering::데이터-엔지니어"
- Prompt: "설계 test 데이터 관리 전략 위한 병렬로 시스템 연산. Create 데이터 세대 스크립트 위한 엣지 cases, implement 데이터 마스킹 위한 sensitive 정보, 및 establish test 데이터베이스 refresh 절차. 세트 up 모니터링 위한 데이터 일관성 사이 레거시 및 modernized 컴포넌트 동안 마이그레이션."
- 컨텍스트 에서 이전: 데이터베이스 스키마, test 요구사항
- 예상되는 출력: Test 데이터 파이프라인 및 일관성 모니터링

## 단계 3: Incremental 마이그레이션 구현

### 1. Strangler Fig 인프라 설정
- Use 작업 tool 와 함께 subagent_type="backend-개발::backend-아키텍트"
- Prompt: "Implement strangler fig 인프라 와 함께 API 게이트웨이 위한 traffic 라우팅. Configure 기능 flags 위한 gradual rollout 사용하여 환경 변수 또는 기능 관리 서비스. 세트 up 프록시 레이어 와 함께 요청 라우팅 규칙 based 에: URL 패턴, 헤더, 또는 사용자 세그먼트합니다. Implement 회로 breakers 및 fallback mechanisms 위한 복원력. Create observability 대시보드 위한 dual-시스템 모니터링."
- 예상되는 출력: API 게이트웨이 구성, 기능 flag 시스템, 모니터링 대시보드

### 2. 컴포넌트 Modernization - 첫 번째 Wave
- Use 작업 tool 와 함께 subagent_type="python-개발::python-pro" 또는 "golang-pro" (based 에 target 스택)
- Prompt: "Modernize 첫 번째-wave 컴포넌트 (quick wins 식별된 에서 평가). 위한 각 컴포넌트: extract 비즈니스 logic 에서 레거시 코드, implement 사용하여 현대적인 패턴 (종속성 인젝션, 견고한 원칙), ensure 뒤로 compatibility 통해 어댑터 패턴, maintain 데이터 일관성 와 함께 이벤트 sourcing 또는 dual 씁니다. Follow 12-인수 app 원칙. 컴포넌트 에 modernize: [목록 에서 우선순위가 지정됨 roadmap]"
- 컨텍스트 에서 이전: Characterization 테스트합니다, 계약 테스트합니다, 인프라 설정
- 예상되는 출력: Modernized 컴포넌트 와 함께 adapters

### 3. Security 강화
- Use 작업 tool 와 함께 subagent_type="security-scanning::security-감사자"
- Prompt: "Audit modernized 컴포넌트 위한 security 취약점. Implement security improvements 포함하여: OAuth 2.0/JWT 인증, role-based access control, 입력 검증 및 sanitization, SQL 인젝션 방지, XSS 보호, 및 secrets 관리. Verify OWASP top 10 compliance. Configure security 헤더 및 implement 속도 제한."
- 컨텍스트 에서 이전: Modernized 컴포넌트 코드
- 예상되는 출력: Security audit 보고서 및 강화된 컴포넌트

## 단계 4: 성능 검증 및 최적화

### 1. 성능 테스트 및 최적화
- Use 작업 tool 와 함께 subagent_type="애플리케이션-성능::성능-엔지니어"
- Prompt: "Conduct 성능 테스트 comparing 레거시 vs modernized 컴포넌트. Run load 테스트합니다 simulating production traffic 패턴, 측정 응답 times, 처리량, 및 리소스 사용률. Identify 성능 regressions 및 optimize: 데이터베이스 쿼리 와 함께 색인, 캐싱 strategies (Redis/Memcached), 연결 풀링, 및 비동기 처리 곳 적용 가능한. Validate against SLA 요구사항."
- 컨텍스트 에서 이전: 성능 baselines, modernized 컴포넌트
- 예상되는 출력: 성능 test results 및 최적화 recommendations

### 2. Progressive Rollout 및 모니터링
- Use 작업 tool 와 함께 subagent_type="배포-strategies::배포-엔지니어"
- Prompt: "Implement progressive rollout 전략 사용하여 기능 flags. Start 와 함께 5% traffic 에 modernized 컴포넌트, 모니터 오류 평가합니다, 지연 시간, 및 비즈니스 메트릭. Define automatic 롤백 트리거합니다: 오류 rate >1%, 지연 시간 >2x baseline, 또는 비즈니스 metric degradation. Create runbook 위한 traffic shifting: 5% → 25% → 50% → 100% 와 함께 24-hour 관찰 periods."
- 컨텍스트 에서 이전: 기능 flag 구성, 모니터링 대시보드
- 예상되는 출력: Rollout plan 와 함께 자동화된 safeguards

## 단계 5: 마이그레이션 완료 및 문서화

### 1. 레거시 컴포넌트 Decommissioning
- Use 작업 tool 와 함께 subagent_type="레거시-modernizer"
- Prompt: "Plan safe decommissioning of 대체된 레거시 컴포넌트. Verify 아니요 remaining 종속성 통해 traffic 분석 (minimum 30 days 에서 0% traffic). 아카이브 레거시 코드 와 함께 문서화 of original 기능. 업데이트 CI/CD 파이프라인 에 remove 레거시 빌드. Clean up unused 데이터베이스 테이블 및 remove 더 이상 사용되지 않음 API 엔드포인트. Document 어떤 보유됨 레거시 컴포넌트 와 함께 sunset timeline."
- 컨텍스트 에서 이전: Traffic 라우팅 데이터, modernization 상태
- 예상되는 출력: Decommissioning checklist 및 timeline

### 2. 문서화 및 지식 전송
- Use 작업 tool 와 함께 subagent_type="문서화-세대::docs-아키텍트"
- Prompt: "Create 포괄적인 modernization 문서화 포함하여: architectural 다이어그램 (이전/이후), API 문서화 와 함께 마이그레이션 안내합니다, runbooks 위한 dual-시스템 연산, 문제 해결 안내합니다 위한 일반적인 이슈, 및 lessons learned 보고서. Generate 개발자 onboarding 가이드 위한 modernized 시스템. Document technical decisions 및 trade-offs made 동안 마이그레이션."
- 컨텍스트 에서 이전: 모든 마이그레이션 아티팩트 및 decisions
- 예상되는 출력: 완전한 modernization 문서화 패키지

## 구성 Options

- **--병렬로-시스템**: Keep 둘 다 시스템 실행 중 indefinitely (위한 gradual 마이그레이션)
- **--big-bang**: 전체 cutover 이후 검증 (higher 위험, faster 완료)
- **--에 의해-기능**: Migrate 완전한 기능 오히려 보다 technical 컴포넌트
- **--데이터베이스-첫 번째**: Prioritize 데이터베이스 modernization 이전 애플리케이션 레이어
- **--api-첫 번째**: Modernize API 레이어 동안 maintaining 레거시 backend

## Success Criteria

- 모든 high-priority 컴포넌트 modernized 와 함께 >80% test coverage
- Zero unplanned downtime 동안 마이그레이션
- 성능 메트릭 유지됨 또는 개선된 (P95 지연 시간 내에 110% of baseline)
- Security 취약점 감소된 에 의해 >90%
- Technical debt score 개선된 에 의해 >60%
- 성공한 연산 위한 30 days post-마이그레이션 없이 rollbacks
- 완전한 문서화 가능하게 하는 새로운 개발자 onboarding 에서 <1 week

Target: $인수