Orchestrate 전체-스택 기능 개발 전반에 걸쳐 backend, frontend, 및 인프라 layers 와 함께 현대적인 API-첫 번째 접근법:

[확장된 thinking: This 워크플로우 조정합니다 여러 specialized 에이전트 에 deliver a 완전한 전체-스택 기능 에서 아키텍처 통해 배포. It 따릅니다 API-첫 번째 개발 원칙, 보장하는 계약-driven 개발 곳 the API 사양 drives 둘 다 backend 구현 및 frontend consumption. 각 단계 빌드 upon 이전 출력, 생성하는 a cohesive 시스템 와 함께 적절한 분리 of concerns, 포괄적인 테스트, 및 프로덕션 준비 완료 배포. The 워크플로우 강조합니다 현대적인 관행 같은 컴포넌트-driven UI 개발, 기능 flags, observability, 및 progressive rollout strategies.]

## 단계 1: 아키텍처 & 설계 기반

### 1. 데이터베이스 아키텍처 설계
- Use 작업 tool 와 함께 subagent_type="데이터베이스-설계::데이터베이스-아키텍트"
- Prompt: "설계 데이터베이스 스키마 및 데이터 모델 위한: $인수. Consider scalability, 쿼리 패턴, 색인 전략, 및 데이터 일관성 요구사항. Include 마이그레이션 전략 만약 modifying 기존 스키마. Provide 둘 다 논리적인 및 physical 데이터 모델."
- 예상되는 출력: 엔터티 관계 다이어그램, 테이블 스키마, 색인 전략, 마이그레이션 스크립트, 데이터 access 패턴
- 컨텍스트: 초기 요구사항 및 비즈니스 도메인 모델

### 2. Backend 서비스 아키텍처
- Use 작업 tool 와 함께 subagent_type="backend-개발::backend-아키텍트"
- Prompt: "설계 backend 서비스 아키텍처 위한: $인수. 사용하여 the 데이터베이스 설계 에서 이전 단계, create 서비스 boundaries, define API 계약 (OpenAPI/GraphQL), 설계 인증/인가 전략, 및 specify inter-서비스 communication 패턴. Include 복원력 패턴 (회로 breakers, 재시도합니다) 및 캐싱 전략."
- 예상되는 출력: 서비스 아키텍처 다이어그램, OpenAPI 사양, 인증 흐릅니다, 캐싱 아키텍처, 메시지 큐 설계 (만약 적용 가능한)
- 컨텍스트: 데이터베이스 스키마 에서 단계 1, non-기능적인 요구사항

### 3. Frontend 컴포넌트 아키텍처
- Use 작업 tool 와 함께 subagent_type="frontend-mobile-개발::frontend-개발자"
- Prompt: "설계 frontend 아키텍처 및 컴포넌트 구조 위한: $인수. Based 에 the API 계약 에서 이전 단계, 설계 컴포넌트 계층, 상태 관리 접근법 (Redux/Zustand/컨텍스트), 라우팅 구조, 및 데이터 가져오는 패턴. Include 접근성 요구사항 및 responsive 설계 전략. Plan 위한 Storybook 컴포넌트 문서화."
- 예상되는 출력: 컴포넌트 트리 다이어그램, 상태 관리 설계, 라우팅 구성, 설계 시스템 통합 plan, 접근성 checklist
- 컨텍스트: API 사양 에서 단계 2, UI/UX 요구사항

## 단계 2: 병렬로 구현

### 4. Backend 서비스 구현
- Use 작업 tool 와 함께 subagent_type="python-개발::python-pro" (또는 "golang-pro"/"nodejs-전문가" based 에 스택)
- Prompt: "Implement backend 서비스 위한: $인수. 사용하여 the 아키텍처 및 API specs 에서 단계 1, 빌드 RESTful/GraphQL 엔드포인트 와 함께 적절한 검증, 오류 처리, 및 로깅. Implement 비즈니스 logic, 데이터 access 레이어, 인증 미들웨어, 및 통합 와 함께 외부 서비스. Include observability (구조화된 로깅, 메트릭, 추적)."
- 예상되는 출력: Backend 서비스 코드, API 엔드포인트, 미들웨어, background jobs, 단위 테스트합니다, 통합 테스트합니다
- 컨텍스트: 아키텍처 설계 에서 단계 1, 데이터베이스 스키마

### 5. Frontend 구현
- Use 작업 tool 와 함께 subagent_type="frontend-mobile-개발::frontend-개발자"
- Prompt: "Implement frontend 애플리케이션 위한: $인수. 빌드 React/다음.js 컴포넌트 사용하여 the 컴포넌트 아키텍처 에서 단계 1. Implement 상태 관리, API 통합 와 함께 적절한 오류 처리 및 로드 states, 폼 검증, 및 responsive 레이아웃. Create Storybook stories 위한 컴포넌트. Ensure 접근성 (WCAG 2.1 AA compliance)."
- 예상되는 출력: React 컴포넌트, 상태 관리 구현, API 클라이언트 코드, Storybook stories, responsive 스타일을 지정합니다, 접근성 implementations
- 컨텍스트: 컴포넌트 아키텍처 에서 단계 3, API 계약

### 6. 데이터베이스 구현 & 최적화
- Use 작업 tool 와 함께 subagent_type="데이터베이스-설계::sql-pro"
- Prompt: "Implement 및 optimize 데이터베이스 레이어 위한: $인수. Create 마이그레이션 스크립트, 저장됨 절차 (만약 필요한), optimize 쿼리 식별된 에 의해 backend 구현, 세트 up 적절한 인덱스, 및 implement 데이터 검증 constraints. Include 데이터베이스-레벨 security 측정합니다 및 백업 strategies."
- 예상되는 출력: 마이그레이션 스크립트, 최적화된 쿼리, 저장됨 절차, 인덱스 definitions, 데이터베이스 security 구성
- 컨텍스트: 데이터베이스 설계 에서 단계 1, 쿼리 패턴 에서 backend 구현

## 단계 3: 통합 & 테스트

### 7. API 계약 테스트
- Use 작업 tool 와 함께 subagent_type="test-automator"
- Prompt: "Create 계약 테스트합니다 위한: $인수. Implement Pact/Dredd 테스트합니다 에 validate API 계약 사이 backend 및 frontend. Create 통합 테스트합니다 위한 모든 API 엔드포인트, test 인증 흐릅니다, validate 오류 응답, 및 ensure 적절한 CORS 구성. Include load 테스트 scenarios."
- 예상되는 출력: 계약 test suites, 통합 테스트합니다, load test scenarios, API 문서화 검증
- 컨텍스트: API implementations 에서 단계 2

### 8. End-에-End 테스트
- Use 작업 tool 와 함께 subagent_type="test-automator"
- Prompt: "Implement E2E 테스트합니다 위한: $인수. Create Playwright/Cypress 테스트합니다 covering 긴급 사용자 journeys, cross-browser compatibility, mobile responsiveness, 및 오류 scenarios. Test 기능 flags 통합, 분석 추적, 및 성능 메트릭. Include visual regression 테스트합니다."
- 예상되는 출력: E2E test suites, visual regression baselines, 성능 benchmarks, test 보고서
- 컨텍스트: Frontend 및 backend implementations 에서 단계 2

### 9. Security Audit & 강화
- Use 작업 tool 와 함께 subagent_type="security-감사자"
- Prompt: "Perform security audit 위한: $인수. Review API security (인증, 인가, 속도 제한), check 위한 OWASP Top 10 취약점, audit frontend 위한 XSS/CSRF 위험, validate 입력 sanitization, 및 review secrets 관리. Provide penetration 테스트 results 및 remediation steps."
- 예상되는 출력: Security audit 보고서, 취약점 평가, remediation recommendations, security 헤더 구성
- 컨텍스트: 모든 implementations 에서 단계 2

## 단계 4: 배포 & 작업

### 10. 인프라 & CI/CD 설정
- Use 작업 tool 와 함께 subagent_type="배포-엔지니어"
- Prompt: "설정 배포 인프라 위한: $인수. Create Docker 컨테이너, Kubernetes manifests (또는 cloud-특정 configs), implement CI/CD 파이프라인 와 함께 자동화된 테스트 gates, 설정 기능 flags (LaunchDarkly/Unleash), 및 configure 모니터링/경고. Include blue-green 배포 전략 및 롤백 절차."
- 예상되는 출력: Dockerfiles, K8s manifests, CI/CD 파이프라인 configs, 기능 flag 설정, IaC 템플릿 (Terraform/CloudFormation)
- 컨텍스트: 모든 implementations 및 테스트합니다 에서 이전 phases

### 11. Observability & 모니터링
- Use 작업 tool 와 함께 subagent_type="배포-엔지니어"
- Prompt: "Implement observability 스택 위한: $인수. 설정 분산 추적 (OpenTelemetry), configure 애플리케이션 메트릭 (Prometheus/DataDog), implement 중앙 집중화된 로깅 (ELK/Splunk), create 대시보드 위한 키 메트릭, 및 define SLIs/SLOs. Include 경고 규칙 및 에-호출 절차."
- 예상되는 출력: Observability 구성, 대시보드 definitions, 경고 규칙, runbooks, SLI/SLO definitions
- 컨텍스트: 인프라 설정 에서 단계 10

### 12. 성능 최적화
- Use 작업 tool 와 함께 subagent_type="성능-엔지니어"
- Prompt: "Optimize 성능 전반에 걸쳐 스택 위한: $인수. Analyze 및 optimize 데이터베이스 쿼리, implement 캐싱 strategies (Redis/CDN), optimize frontend bundle size 및 로드 성능, 설정 lazy 로드 및 코드 분할하는, 및 tune backend 서비스 성능. Include 이전/이후 메트릭."
- 예상되는 출력: 성능 improvements, 캐싱 구성, CDN 설정, 최적화된 번들링합니다, 성능 메트릭 보고서
- 컨텍스트: 모니터링 데이터 에서 단계 11, load test results

## 구성 Options
- `stack`: Specify technology 스택 (e.g., "React/FastAPI/PostgreSQL", "다음.js/Django/MongoDB")
- `deployment_target`: Cloud 플랫폼 (AWS/GCP/Azure) 또는 온프레미스
- `feature_flags`: Enable/disable 기능 flag 통합
- `api_style`: REST 또는 GraphQL
- `testing_depth`: 포괄적인 또는 필수
- `compliance`: 특정 compliance 요구사항 (GDPR, HIPAA, SOC2)

## Success Criteria
- 모든 API 계약 검증된 통해 계약 테스트합니다
- Frontend 및 backend 통합 테스트합니다 passing
- E2E 테스트합니다 covering 긴급 사용자 journeys
- Security audit 통과 와 함께 아니요 긴급 취약점
- 성능 메트릭 meeting 정의된 SLOs
- Observability 스택 캡처하는 모든 키 메트릭
- 기능 flags 구성된 위한 progressive rollout
- 문서화 완전한 위한 모든 컴포넌트
- CI/CD 파이프라인 와 함께 자동화된 품질 gates
- Zero-downtime 배포 역량 확인된

## 조정 Notes
- 각 단계 빌드 upon 출력 에서 이전 phases
- 병렬로 tasks 에서 단계 2 can run 동시에 그러나 must converge 위한 단계 3
- Maintain traceability 사이 요구사항 및 implementations
- Use correlation IDs 전반에 걸쳐 모든 서비스 위한 분산 추적
- Document 모든 architectural decisions 에서 ADRs
- Ensure 일관된 오류 처리 및 API 응답 전반에 걸쳐 서비스

기능 에 implement: $인수