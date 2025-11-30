Optimize 애플리케이션 성능 end-에-end 사용하여 specialized 성능 및 최적화 에이전트:

[확장된 thinking: This 워크플로우 오케스트레이션합니다 a 포괄적인 성능 최적화 프로세스 전반에 걸쳐 the entire 애플리케이션 스택. 시작하는 와 함께 deep profiling 및 baseline establishment, the 워크플로우 진행합니다 통해 targeted optimizations 에서 각 시스템 레이어, 검증합니다 improvements 통해 load 테스트, 및 설정합니다 continuous 모니터링 위한 sustained 성능. 각 단계 빌드 에 인사이트 에서 이전 phases, 생성하는 a 데이터 기반 최적화 전략 것 주소 real bottlenecks 오히려 보다 theoretical improvements. The 워크플로우 강조합니다 현대적인 observability 관행, 사용자-centric 성능 메트릭, 및 cost-effective 최적화 strategies.]

## 단계 1: 성능 Profiling & Baseline

### 1. 포괄적인 성능 Profiling
- Use 작업 tool 와 함께 subagent_type="성능-엔지니어"
- Prompt: "프로필 애플리케이션 성능 포괄적으로 위한: $인수. Generate flame 그래프 위한 CPU usage, 힙 dumps 위한 메모리 분석, trace I/O 작업, 및 identify hot 경로. Use APM tools 같은 DataDog 또는 새로운 Relic 만약 사용 가능한. Include 데이터베이스 쿼리 profiling, API 응답 times, 및 frontend 렌더링 메트릭. Establish 성능 baselines 위한 모든 긴급 사용자 journeys."
- 컨텍스트: 초기 성능 investigation
- 출력: 상세한 성능 프로필 와 함께 flame 그래프, 메모리 분석, 병목 식별, baseline 메트릭

### 2. Observability 스택 평가
- Use 작업 tool 와 함께 subagent_type="observability-엔지니어"
- Prompt: "Assess 현재 observability 설정 위한: $인수. Review 기존 모니터링, 분산 추적 와 함께 OpenTelemetry, log 집계, 및 메트릭 컬렉션. Identify gaps 에서 visibility, missing 메트릭, 및 areas needing 더 나은 instrumentation. Recommend APM tool 통합 및 사용자 정의 메트릭 위한 비즈니스-긴급 작업."
- 컨텍스트: 성능 프로필 에서 단계 1
- 출력: Observability 평가 보고서, instrumentation gaps, 모니터링 recommendations

### 3. 사용자 Experience 분석
- Use 작업 tool 와 함께 subagent_type="성능-엔지니어"
- Prompt: "Analyze 사용자 experience 메트릭 위한: $인수. 측정 핵심 Web Vitals (LCP, FID, CLS), 페이지 load times, 시간 에 interactive, 및 perceived 성능. Use Real 사용자 모니터링 (RUM) 데이터 만약 사용 가능한. Identify 사용자 journeys 와 함께 poor 성능 및 their 비즈니스 impact."
- 컨텍스트: 성능 baselines 에서 단계 1
- 출력: UX 성능 보고서, 핵심 Web Vitals 분석, 사용자 impact 평가

## 단계 2: 데이터베이스 & Backend 최적화

### 4. 데이터베이스 성능 최적화
- Use 작업 tool 와 함께 subagent_type="데이터베이스-cloud-최적화::데이터베이스-최적화기"
- Prompt: "Optimize 데이터베이스 성능 위한: $인수 based 에 profiling 데이터: {context_from_phase_1}. Analyze slow 쿼리 로깅합니다, create missing 인덱스, optimize 실행 계획합니다, implement 쿼리 result 캐싱 와 함께 Redis/Memcached. Review 연결 풀링, 준비된 statements, 및 batch 처리 opportunities. Consider 읽은 replicas 및 데이터베이스 샤딩 만약 필요한."
- 컨텍스트: 성능 bottlenecks 에서 단계 1
- 출력: 최적화된 쿼리, 새로운 인덱스, 캐싱 전략, 연결 풀 구성

### 5. Backend 코드 & API 최적화
- Use 작업 tool 와 함께 subagent_type="backend-개발::backend-아키텍트"
- Prompt: "Optimize backend 서비스 위한: $인수 targeting bottlenecks: {context_from_phase_1}. Implement efficient algorithms, add 애플리케이션-레벨 캐싱, optimize N+1 쿼리, use 비동기/await 패턴 effectively. Implement pagination, 응답 압축, GraphQL 쿼리 최적화, 및 batch API 작업. Add 회로 breakers 및 bulkheads 위한 복원력."
- 컨텍스트: 데이터베이스 optimizations 에서 단계 4, profiling 데이터 에서 단계 1
- 출력: 최적화된 backend 코드, 캐싱 구현, API improvements, 복원력 패턴

### 6. Microservices & 분산 시스템 최적화
- Use 작업 tool 와 함께 subagent_type="성능-엔지니어"
- Prompt: "Optimize 분산 시스템 성능 위한: $인수. Analyze 서비스-에-서비스 communication, implement 서비스 메시 optimizations, optimize 메시지 큐 성능 (Kafka/RabbitMQ), reduce 네트워크 hops. Implement 분산 캐싱 strategies 및 optimize 직렬화/역직렬화."
- 컨텍스트: Backend optimizations 에서 단계 5
- 출력: 서비스 communication improvements, 메시지 큐 최적화, 분산 캐싱 설정

## 단계 3: Frontend & CDN 최적화

### 7. Frontend Bundle & 로드 최적화
- Use 작업 tool 와 함께 subagent_type="frontend-개발자"
- Prompt: "Optimize frontend 성능 위한: $인수 targeting 핵심 Web Vitals: {context_from_phase_1}. Implement 코드 분할하는, 트리 shaking, lazy 로드, 및 동적 imports. Optimize bundle sizes 와 함께 webpack/롤업 분석. Implement 리소스 hints (prefetch, preconnect, preload). Optimize 긴급 렌더링 경로 및 eliminate render-차단 리소스."
- 컨텍스트: UX 분석 에서 단계 1, backend optimizations 에서 단계 2
- 출력: 최적화된 번들링합니다, lazy 로드 구현, 개선된 핵심 Web Vitals

### 8. CDN & 엣지 최적화
- Use 작업 tool 와 함께 subagent_type="cloud-인프라::cloud-아키텍트"
- Prompt: "Optimize CDN 및 엣지 성능 위한: $인수. Configure CloudFlare/CloudFront 위한 최적 캐싱, implement 엣지 함수 위한 동적 콘텐츠, 세트 up image 최적화 와 함께 responsive images 및 WebP/AVIF 형식을 지정합니다. Configure HTTP/2 및 HTTP/3, implement Brotli 압축. 세트 up geographic 배포 위한 전역 사용자."
- 컨텍스트: Frontend optimizations 에서 단계 7
- 출력: CDN 구성, 엣지 캐싱 규칙, 압축 설정, geographic 최적화

### 9. Mobile & Progressive Web App 최적화
- Use 작업 tool 와 함께 subagent_type="frontend-mobile-개발::mobile-개발자"
- Prompt: "Optimize mobile experience 위한: $인수. Implement 서비스 workers 위한 offline 기능, optimize 위한 slow networks 와 함께 adaptive 로드. Reduce JavaScript 실행 시간 위한 mobile CPUs. Implement virtual scrolling 위한 long 목록. Optimize touch responsiveness 및 부드러운 animations. Consider React Native/Flutter 특정 optimizations 만약 적용 가능한."
- 컨텍스트: Frontend optimizations 에서 steps 7-8
- 출력: Mobile-최적화된 코드, PWA 구현, offline 기능

## 단계 4: Load 테스트 & 검증

### 10. 포괄적인 Load 테스트
- Use 작업 tool 와 함께 subagent_type="성능-엔지니어"
- Prompt: "Conduct 포괄적인 load 테스트 위한: $인수 사용하여 k6/Gatling/Artillery. 설계 realistic load scenarios based 에 production traffic 패턴. Test 정상 load, peak load, 및 stress scenarios. Include API 테스트, browser-based 테스트, 및 WebSocket 테스트 만약 적용 가능한. 측정 응답 times, 처리량, 오류 평가합니다, 및 리소스 사용률 에서 various load levels."
- 컨텍스트: 모든 optimizations 에서 phases 1-3
- 출력: Load test results, 성능 under load, breaking points, scalability 분석

### 11. 성능 Regression 테스트
- Use 작업 tool 와 함께 subagent_type="성능-테스트-review::test-automator"
- Prompt: "Create 자동화된 성능 regression 테스트합니다 위한: $인수. 세트 up 성능 budgets 위한 키 메트릭, integrate 와 함께 CI/CD 파이프라인 사용하여 GitHub Actions 또는 similar. Create Lighthouse CI 테스트합니다 위한 frontend, API 성능 테스트합니다 와 함께 Artillery, 및 데이터베이스 성능 benchmarks. Implement automatic 롤백 트리거합니다 위한 성능 regressions."
- 컨텍스트: Load test results 에서 단계 10, baseline 메트릭 에서 단계 1
- 출력: 성능 test suite, CI/CD 통합, regression 방지 시스템

## 단계 5: 모니터링 & Continuous 최적화

### 12. Production 모니터링 설정
- Use 작업 tool 와 함께 subagent_type="observability-엔지니어"
- Prompt: "Implement production 성능 모니터링 위한: $인수. 세트 up APM 와 함께 DataDog/새로운 Relic/Dynatrace, configure 분산 추적 와 함께 OpenTelemetry, implement 사용자 정의 비즈니스 메트릭. Create Grafana 대시보드 위한 키 메트릭, 세트 up PagerDuty 경고 위한 성능 degradation. Define SLIs/SLOs 위한 긴급 서비스 와 함께 오류 budgets."
- 컨텍스트: 성능 improvements 에서 모든 이전 phases
- 출력: 모니터링 대시보드, 경고 규칙, SLI/SLO definitions, runbooks

### 13. Continuous 성능 최적화
- Use 작업 tool 와 함께 subagent_type="성능-엔지니어"
- Prompt: "Establish continuous 최적화 프로세스 위한: $인수. Create 성능 budget 추적, implement A/B 테스트 위한 성능 변경합니다, 세트 up continuous profiling 에서 production. Document 최적화 opportunities backlog, create 용량 계획 모델, 및 establish 일반 성능 review 순환합니다."
- 컨텍스트: 모니터링 설정 에서 단계 12, 모든 이전 최적화 work
- 출력: 성능 budget 추적, 최적화 backlog, 용량 계획, review 프로세스

## 구성 Options

- **performance_focus**: "지연 시간" | "처리량" | "cost" | "균형된" (default: "균형된")
- **optimization_depth**: "quick-wins" | "포괄적인" | "엔터프라이즈" (default: "포괄적인")
- **tools_available**: ["datadog", "newrelic", "prometheus", "grafana", "k6", "gatling"]
- **budget_constraints**: 세트 maximum acceptable costs 위한 인프라 변경합니다
- **user_impact_tolerance**: "zero-downtime" | "유지보수-window" | "gradual-rollout"

## Success Criteria

- **응답 시간**: P50 < 200ms, P95 < 1s, P99 < 2s 위한 긴급 엔드포인트
- **핵심 Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1
- **처리량**: 지원 2x 현재 peak load 와 함께 <1% 오류 rate
- **데이터베이스 성능**: 쿼리 P95 < 100ms, 아니요 쿼리 > 1s
- **리소스 사용률**: CPU < 70%, 메모리 < 80% under 정상 load
- **Cost 효율성**: 성능 per dollar 개선된 에 의해 minimum 30%
- **모니터링 Coverage**: 100% of 긴급 경로 instrumented 와 함께 경고

성능 최적화 target: $인수