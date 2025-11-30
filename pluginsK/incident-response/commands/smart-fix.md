# Intelligent 이슈 해결 와 함께 Multi-에이전트 오케스트레이션

[확장된 thinking: This 워크플로우 구현합니다 a 정교한 디버깅 및 해결 파이프라인 것 leverages AI-지원된 디버깅 tools 및 observability 플랫폼 에 systematically diagnose 및 resolve production 이슈. The intelligent 디버깅 전략 결합합니다 자동화된 근 cause 분석 와 함께 human expertise, 사용하여 현대적인 2024/2025 관행 포함하여 AI 코드 assistants (GitHub Copilot, Claude 코드), observability 플랫폼 (Sentry, DataDog, OpenTelemetry), git bisect 자동화 위한 regression 추적, 및 production-safe 디버깅 techniques 같은 분산 추적 및 구조화된 로깅. The 프로세스 따릅니다 a rigorous four-단계 접근법: (1) 이슈 분석 단계 - 오류-detective 및 디버거 에이전트 analyze 오류 추적합니다, 로깅합니다, reproduction steps, 및 observability 데이터 에 understand the 전체 컨텍스트 of the 실패 포함하여 업스트림/다운스트림 impacts, (2) 근 Cause Investigation 단계 - 디버거 및 코드-리뷰어 에이전트 perform deep 코드 분석, 자동화된 git bisect 에 identify introducing 커밋, 종속성 compatibility 확인합니다, 및 상태 검사 에 isolate the exact 실패 메커니즘, (3) Fix 구현 단계 - 도메인-특정 에이전트 (python-pro, typescript-pro, rust-전문가, etc.) implement 최소 수정합니다 와 함께 포괄적인 test coverage 포함하여 단위, 통합, 및 엣지 case 테스트합니다 동안 다음 production-safe 관행, (4) 확인 단계 - test-automator 및 성능-엔지니어 에이전트 run regression suites, 성능 benchmarks, security scans, 및 verify 아니요 새로운 이슈 are introduced. 복잡한 이슈 spanning 여러 시스템 require 오케스트레이션된 조정 사이 전문가 에이전트 (데이터베이스-최적화기 → 성능-엔지니어 → devops-troubleshooter) 와 함께 명시적인 컨텍스트 passing 및 상태 sharing. The 워크플로우 강조합니다 understanding 근 causes over treating symptoms, implementing lasting architectural improvements, automating 감지 통해 향상된 모니터링 및 경고, 및 preventing 미래 occurrences 통해 유형 시스템 enhancements, 정적 분석 규칙, 및 개선된 오류 처리 패턴. Success is 측정된 not 방금 에 의해 이슈 해결 그러나 에 의해 감소된 평균 시간 에 복구 (MTTR), 방지 of similar 이슈, 및 개선된 시스템 복원력.]

## 단계 1: 이슈 분석 - 오류 감지 및 컨텍스트 수집

Use 작업 tool 와 함께 subagent_type="오류-디버깅::오류-detective" 따르는 에 의해 subagent_type="오류-디버깅::디버거":

**첫 번째: 오류-Detective 분석**

**Prompt:**
```
Analyze error traces, logs, and observability data for: $ARGUMENTS

Deliverables:
1. Error signature analysis: exception type, message patterns, frequency, first occurrence
2. Stack trace deep dive: failure location, call chain, involved components
3. Reproduction steps: minimal test case, environment requirements, data fixtures needed
4. Observability context:
   - Sentry/DataDog error groups and trends
   - Distributed traces showing request flow (OpenTelemetry/Jaeger)
   - Structured logs (JSON logs with correlation IDs)
   - APM metrics: latency spikes, error rates, resource usage
5. User impact assessment: affected user segments, error rate, business metrics impact
6. Timeline analysis: when did it start, correlation with deployments/config changes
7. Related symptoms: similar errors, cascading failures, upstream/downstream impacts

Modern debugging techniques to employ:
- AI-assisted log analysis (pattern detection, anomaly identification)
- Distributed trace correlation across microservices
- Production-safe debugging (no code changes, use observability data)
- Error fingerprinting for deduplication and tracking
```

**예상되는 출력:**
```
ERROR_SIGNATURE: {exception type + key message pattern}
FREQUENCY: {count, rate, trend}
FIRST_SEEN: {timestamp or git commit}
STACK_TRACE: {formatted trace with key frames highlighted}
REPRODUCTION: {minimal steps + sample data}
OBSERVABILITY_LINKS: [Sentry URL, DataDog dashboard, trace IDs]
USER_IMPACT: {affected users, severity, business impact}
TIMELINE: {when started, correlation with changes}
RELATED_ISSUES: [similar errors, cascading failures]
```

**Second: 디버거 근 Cause 식별**

**Prompt:**
```
Perform root cause investigation using error-detective output:

Context from Error-Detective:
- Error signature: {ERROR_SIGNATURE}
- Stack trace: {STACK_TRACE}
- Reproduction: {REPRODUCTION}
- Observability: {OBSERVABILITY_LINKS}

Deliverables:
1. Root cause hypothesis with supporting evidence
2. Code-level analysis: variable states, control flow, timing issues
3. Git bisect analysis: identify introducing commit (automate with git bisect run)
4. Dependency analysis: version conflicts, API changes, configuration drift
5. State inspection: database state, cache state, external API responses
6. Failure mechanism: why does the code fail under these specific conditions
7. Fix strategy options with tradeoffs (quick fix vs proper fix)

Context needed for next phase:
- Exact file paths and line numbers requiring changes
- Data structures or API contracts affected
- Dependencies that may need updates
- Test scenarios to verify the fix
- Performance characteristics to maintain
```

**예상되는 출력:**
```
ROOT_CAUSE: {technical explanation with evidence}
INTRODUCING_COMMIT: {git SHA + summary if found via bisect}
AFFECTED_FILES: [file paths with specific line numbers]
FAILURE_MECHANISM: {why it fails - race condition, null check, type mismatch, etc}
DEPENDENCIES: [related systems, libraries, external APIs]
FIX_STRATEGY: {recommended approach with reasoning}
QUICK_FIX_OPTION: {temporary mitigation if applicable}
PROPER_FIX_OPTION: {long-term solution}
TESTING_REQUIREMENTS: [scenarios that must be covered]
```

## 단계 2: 근 Cause Investigation - Deep 코드 분석

Use 작업 tool 와 함께 subagent_type="오류-디버깅::디버거" 및 subagent_type="포괄적인-review::코드-리뷰어" 위한 systematic investigation:

**첫 번째: 디버거 코드 분석**

**Prompt:**
```
Perform deep code analysis and bisect investigation:

Context from Phase 1:
- Root cause: {ROOT_CAUSE}
- Affected files: {AFFECTED_FILES}
- Failure mechanism: {FAILURE_MECHANISM}
- Introducing commit: {INTRODUCING_COMMIT}

Deliverables:
1. Code path analysis: trace execution from entry point to failure
2. Variable state tracking: values at key decision points
3. Control flow analysis: branches taken, loops, async operations
4. Git bisect automation: create bisect script to identify exact breaking commit
   ```bash
   git bisect start HEAD v1.2.3
   git bisect run ./test_reproduction.sh
   ```
5. Dependency compatibility matrix: version combinations that work/fail
6. Configuration analysis: environment variables, feature flags, deployment configs
7. Timing and race condition analysis: async operations, event ordering, locks
8. Memory and resource analysis: leaks, exhaustion, contention

Modern investigation techniques:
- AI-assisted code explanation (Claude/Copilot to understand complex logic)
- Automated git bisect with reproduction test
- Dependency graph analysis (npm ls, go mod graph, pip show)
- Configuration drift detection (compare staging vs production)
- Time-travel debugging using production traces
```

**예상되는 출력:**
```
CODE_PATH: {entry → ... → failure location with key variables}
STATE_AT_FAILURE: {variable values, object states, database state}
BISECT_RESULT: {exact commit that introduced bug + diff}
DEPENDENCY_ISSUES: [version conflicts, breaking changes, CVEs]
CONFIGURATION_DRIFT: {differences between environments}
RACE_CONDITIONS: {async issues, event ordering problems}
ISOLATION_VERIFICATION: {confirmed single root cause vs multiple issues}
```

**Second: 코드-리뷰어 Deep Dive**

**Prompt:**
```
Review code logic and identify design issues:

Context from Debugger:
- Code path: {CODE_PATH}
- State at failure: {STATE_AT_FAILURE}
- Bisect result: {BISECT_RESULT}

Deliverables:
1. Logic flaw analysis: incorrect assumptions, missing edge cases, wrong algorithms
2. Type safety gaps: where stronger types could prevent the issue
3. Error handling review: missing try-catch, unhandled promises, panic scenarios
4. Contract validation: input validation gaps, output guarantees not met
5. Architectural issues: tight coupling, missing abstractions, layering violations
6. Similar patterns: other code locations with same vulnerability
7. Fix design: minimal change vs refactoring vs architectural improvement

Review checklist:
- Are null/undefined values handled correctly?
- Are async operations properly awaited/chained?
- Are error cases explicitly handled?
- Are type assertions safe?
- Are API contracts respected?
- Are side effects isolated?
```

**예상되는 출력:**
```
LOGIC_FLAWS: [specific incorrect assumptions or algorithms]
TYPE_SAFETY_GAPS: [where types could prevent issues]
ERROR_HANDLING_GAPS: [unhandled error paths]
SIMILAR_VULNERABILITIES: [other code with same pattern]
FIX_DESIGN: {minimal change approach}
REFACTORING_OPPORTUNITIES: {if larger improvements warranted}
ARCHITECTURAL_CONCERNS: {if systemic issues exist}
```

## 단계 3: Fix 구현 - 도메인-특정 에이전트 실행

Based 에 단계 2 출력, 라우트 에 적절한 도메인 에이전트 사용하여 작업 tool:

**라우팅 Logic:**
- Python 이슈 → subagent_type="python-개발::python-pro"
- TypeScript/JavaScript → subagent_type="javascript-typescript::typescript-pro"
- Go → subagent_type="시스템-programming::golang-pro"
- Rust → subagent_type="시스템-programming::rust-pro"
- SQL/데이터베이스 → subagent_type="데이터베이스-cloud-최적화::데이터베이스-최적화기"
- 성능 → subagent_type="애플리케이션-성능::성능-엔지니어"
- Security → subagent_type="security-scanning::security-감사자"

**Prompt 템플릿 (adapt 위한 language):**
```
Implement production-safe fix with comprehensive test coverage:

Context from Phase 2:
- Root cause: {ROOT_CAUSE}
- Logic flaws: {LOGIC_FLAWS}
- Fix design: {FIX_DESIGN}
- Type safety gaps: {TYPE_SAFETY_GAPS}
- Similar vulnerabilities: {SIMILAR_VULNERABILITIES}

Deliverables:
1. Minimal fix implementation addressing root cause (not symptoms)
2. Unit tests:
   - Specific failure case reproduction
   - Edge cases (boundary values, null/empty, overflow)
   - Error path coverage
3. Integration tests:
   - End-to-end scenarios with real dependencies
   - External API mocking where appropriate
   - Database state verification
4. Regression tests:
   - Tests for similar vulnerabilities
   - Tests covering related code paths
5. Performance validation:
   - Benchmarks showing no degradation
   - Load tests if applicable
6. Production-safe practices:
   - Feature flags for gradual rollout
   - Graceful degradation if fix fails
   - Monitoring hooks for fix verification
   - Structured logging for debugging

Modern implementation techniques (2024/2025):
- AI pair programming (GitHub Copilot, Claude Code) for test generation
- Type-driven development (leverage TypeScript, mypy, clippy)
- Contract-first APIs (OpenAPI, gRPC schemas)
- Observability-first (structured logs, metrics, traces)
- Defensive programming (explicit error handling, validation)

Implementation requirements:
- Follow existing code patterns and conventions
- Add strategic debug logging (JSON structured logs)
- Include comprehensive type annotations
- Update error messages to be actionable (include context, suggestions)
- Maintain backward compatibility (version APIs if breaking)
- Add OpenTelemetry spans for distributed tracing
- Include metric counters for monitoring (success/failure rates)
```

**예상되는 출력:**
```
FIX_SUMMARY: {what changed and why - root cause vs symptom}
CHANGED_FILES: [
  {path: "...", changes: "...", reasoning: "..."}
]
NEW_FILES: [{path: "...", purpose: "..."}]
TEST_COVERAGE: {
  unit: "X scenarios",
  integration: "Y scenarios",
  edge_cases: "Z scenarios",
  regression: "W scenarios"
}
TEST_RESULTS: {all_passed: true/false, details: "..."}
BREAKING_CHANGES: {none | API changes with migration path}
OBSERVABILITY_ADDITIONS: [
  {type: "log", location: "...", purpose: "..."},
  {type: "metric", name: "...", purpose: "..."},
  {type: "trace", span: "...", purpose: "..."}
]
FEATURE_FLAGS: [{flag: "...", rollout_strategy: "..."}]
BACKWARD_COMPATIBILITY: {maintained | breaking with mitigation}
```

## 단계 4: 확인 - 자동화된 테스트 및 성능 검증

Use 작업 tool 와 함께 subagent_type="단위-테스트::test-automator" 및 subagent_type="애플리케이션-성능::성능-엔지니어":

**첫 번째: Test-Automator Regression Suite**

**Prompt:**
```
Run comprehensive regression testing and verify fix quality:

Context from Phase 3:
- Fix summary: {FIX_SUMMARY}
- Changed files: {CHANGED_FILES}
- Test coverage: {TEST_COVERAGE}
- Test results: {TEST_RESULTS}

Deliverables:
1. Full test suite execution:
   - Unit tests (all existing + new)
   - Integration tests
   - End-to-end tests
   - Contract tests (if microservices)
2. Regression detection:
   - Compare test results before/after fix
   - Identify any new failures
   - Verify all edge cases covered
3. Test quality assessment:
   - Code coverage metrics (line, branch, condition)
   - Mutation testing if applicable
   - Test determinism (run multiple times)
4. Cross-environment testing:
   - Test in staging/QA environments
   - Test with production-like data volumes
   - Test with realistic network conditions
5. Security testing:
   - Authentication/authorization checks
   - Input validation testing
   - SQL injection, XSS prevention
   - Dependency vulnerability scan
6. Automated regression test generation:
   - Use AI to generate additional edge case tests
   - Property-based testing for complex logic
   - Fuzzing for input validation

Modern testing practices (2024/2025):
- AI-generated test cases (GitHub Copilot, Claude Code)
- Snapshot testing for UI/API contracts
- Visual regression testing for frontend
- Chaos engineering for resilience testing
- Production traffic replay for load testing
```

**예상되는 출력:**
```
TEST_RESULTS: {
  total: N,
  passed: X,
  failed: Y,
  skipped: Z,
  new_failures: [list if any],
  flaky_tests: [list if any]
}
CODE_COVERAGE: {
  line: "X%",
  branch: "Y%",
  function: "Z%",
  delta: "+/-W%"
}
REGRESSION_DETECTED: {yes/no + details if yes}
CROSS_ENV_RESULTS: {staging: "...", qa: "..."}
SECURITY_SCAN: {
  vulnerabilities: [list or "none"],
  static_analysis: "...",
  dependency_audit: "..."
}
TEST_QUALITY: {deterministic: true/false, coverage_adequate: true/false}
```

**Second: 성능-엔지니어 검증**

**Prompt:**
```
Measure performance impact and validate no regressions:

Context from Test-Automator:
- Test results: {TEST_RESULTS}
- Code coverage: {CODE_COVERAGE}
- Fix summary: {FIX_SUMMARY}

Deliverables:
1. Performance benchmarks:
   - Response time (p50, p95, p99)
   - Throughput (requests/second)
   - Resource utilization (CPU, memory, I/O)
   - Database query performance
2. Comparison with baseline:
   - Before/after metrics
   - Acceptable degradation thresholds
   - Performance improvement opportunities
3. Load testing:
   - Stress test under peak load
   - Soak test for memory leaks
   - Spike test for burst handling
4. APM analysis:
   - Distributed trace analysis
   - Slow query detection
   - N+1 query patterns
5. Resource profiling:
   - CPU flame graphs
   - Memory allocation tracking
   - Goroutine/thread leaks
6. Production readiness:
   - Capacity planning impact
   - Scaling characteristics
   - Cost implications (cloud resources)

Modern performance practices:
- OpenTelemetry instrumentation
- Continuous profiling (Pyroscope, pprof)
- Real User Monitoring (RUM)
- Synthetic monitoring
```

**예상되는 출력:**
```
PERFORMANCE_BASELINE: {
  response_time_p95: "Xms",
  throughput: "Y req/s",
  cpu_usage: "Z%",
  memory_usage: "W MB"
}
PERFORMANCE_AFTER_FIX: {
  response_time_p95: "Xms (delta)",
  throughput: "Y req/s (delta)",
  cpu_usage: "Z% (delta)",
  memory_usage: "W MB (delta)"
}
PERFORMANCE_IMPACT: {
  verdict: "improved|neutral|degraded",
  acceptable: true/false,
  reasoning: "..."
}
LOAD_TEST_RESULTS: {
  max_throughput: "...",
  breaking_point: "...",
  memory_leaks: "none|detected"
}
APM_INSIGHTS: [slow queries, N+1 patterns, bottlenecks]
PRODUCTION_READY: {yes/no + blockers if no}
```

**Third: 코드-리뷰어 최종 Approval**

**Prompt:**
```
Perform final code review and approve for deployment:

Context from Testing:
- Test results: {TEST_RESULTS}
- Regression detected: {REGRESSION_DETECTED}
- Performance impact: {PERFORMANCE_IMPACT}
- Security scan: {SECURITY_SCAN}

Deliverables:
1. Code quality review:
   - Follows project conventions
   - No code smells or anti-patterns
   - Proper error handling
   - Adequate logging and observability
2. Architecture review:
   - Maintains system boundaries
   - No tight coupling introduced
   - Scalability considerations
3. Security review:
   - No security vulnerabilities
   - Proper input validation
   - Authentication/authorization correct
4. Documentation review:
   - Code comments where needed
   - API documentation updated
   - Runbook updated if operational impact
5. Deployment readiness:
   - Rollback plan documented
   - Feature flag strategy defined
   - Monitoring/alerting configured
6. Risk assessment:
   - Blast radius estimation
   - Rollout strategy recommendation
   - Success metrics defined

Review checklist:
- All tests pass
- No performance regressions
- Security vulnerabilities addressed
- Breaking changes documented
- Backward compatibility maintained
- Observability adequate
- Deployment plan clear
```

**예상되는 출력:**
```
REVIEW_STATUS: {APPROVED|NEEDS_REVISION|BLOCKED}
CODE_QUALITY: {score/assessment}
ARCHITECTURE_CONCERNS: [list or "none"]
SECURITY_CONCERNS: [list or "none"]
DEPLOYMENT_RISK: {low|medium|high}
ROLLBACK_PLAN: {
  steps: ["..."],
  estimated_time: "X minutes",
  data_recovery: "..."
}
ROLLOUT_STRATEGY: {
  approach: "canary|blue-green|rolling|big-bang",
  phases: ["..."],
  success_metrics: ["..."],
  abort_criteria: ["..."]
}
MONITORING_REQUIREMENTS: [
  {metric: "...", threshold: "...", action: "..."}
]
FINAL_VERDICT: {
  approved: true/false,
  blockers: [list if not approved],
  recommendations: ["..."]
}
```

## 단계 5: 문서화 및 방지 - Long-term 복원력

Use 작업 tool 와 함께 subagent_type="포괄적인-review::코드-리뷰어" 위한 방지 strategies:

**Prompt:**
```
Document fix and implement prevention strategies to avoid recurrence:

Context from Phase 4:
- Final verdict: {FINAL_VERDICT}
- Review status: {REVIEW_STATUS}
- Root cause: {ROOT_CAUSE}
- Rollback plan: {ROLLBACK_PLAN}
- Monitoring requirements: {MONITORING_REQUIREMENTS}

Deliverables:
1. Code documentation:
   - Inline comments for non-obvious logic (minimal)
   - Function/class documentation updates
   - API contract documentation
2. Operational documentation:
   - CHANGELOG entry with fix description and version
   - Release notes for stakeholders
   - Runbook entry for on-call engineers
   - Postmortem document (if high-severity incident)
3. Prevention through static analysis:
   - Add linting rules (eslint, ruff, golangci-lint)
   - Configure stricter compiler/type checker settings
   - Add custom lint rules for domain-specific patterns
   - Update pre-commit hooks
4. Type system enhancements:
   - Add exhaustiveness checking
   - Use discriminated unions/sum types
   - Add const/readonly modifiers
   - Leverage branded types for validation
5. Monitoring and alerting:
   - Create error rate alerts (Sentry, DataDog)
   - Add custom metrics for business logic
   - Set up synthetic monitors (Pingdom, Checkly)
   - Configure SLO/SLI dashboards
6. Architectural improvements:
   - Identify similar vulnerability patterns
   - Propose refactoring for better isolation
   - Document design decisions
   - Update architecture diagrams if needed
7. Testing improvements:
   - Add property-based tests
   - Expand integration test scenarios
   - Add chaos engineering tests
   - Document testing strategy gaps

Modern prevention practices (2024/2025):
- AI-assisted code review rules (GitHub Copilot, Claude Code)
- Continuous security scanning (Snyk, Dependabot)
- Infrastructure as Code validation (Terraform validate, CloudFormation Linter)
- Contract testing for APIs (Pact, OpenAPI validation)
- Observability-driven development (instrument before deploying)
```

**예상되는 출력:**
```
DOCUMENTATION_UPDATES: [
  {file: "CHANGELOG.md", summary: "..."},
  {file: "docs/runbook.md", summary: "..."},
  {file: "docs/architecture.md", summary: "..."}
]
PREVENTION_MEASURES: {
  static_analysis: [
    {tool: "eslint", rule: "...", reason: "..."},
    {tool: "ruff", rule: "...", reason: "..."}
  ],
  type_system: [
    {enhancement: "...", location: "...", benefit: "..."}
  ],
  pre_commit_hooks: [
    {hook: "...", purpose: "..."}
  ]
}
MONITORING_ADDED: {
  alerts: [
    {name: "...", threshold: "...", channel: "..."}
  ],
  dashboards: [
    {name: "...", metrics: [...], url: "..."}
  ],
  slos: [
    {service: "...", sli: "...", target: "...", window: "..."}
  ]
}
ARCHITECTURAL_IMPROVEMENTS: [
  {improvement: "...", reasoning: "...", effort: "small|medium|large"}
]
SIMILAR_VULNERABILITIES: {
  found: N,
  locations: [...],
  remediation_plan: "..."
}
FOLLOW_UP_TASKS: [
  {task: "...", priority: "high|medium|low", owner: "..."}
]
POSTMORTEM: {
  created: true/false,
  location: "...",
  incident_severity: "SEV1|SEV2|SEV3|SEV4"
}
KNOWLEDGE_BASE_UPDATES: [
  {article: "...", summary: "..."}
]
```

## Multi-도메인 조정 위한 복잡한 이슈

위한 이슈 spanning 여러 domains, orchestrate specialized 에이전트 순차적으로 와 함께 명시적인 컨텍스트 passing:

**예제 1: 데이터베이스 성능 이슈 Causing 애플리케이션 Timeouts**

**시퀀스:**
1. **단계 1-2**: 오류-detective + 디버거 identify slow 데이터베이스 쿼리
2. **단계 3a**: 작업(subagent_type="데이터베이스-cloud-최적화::데이터베이스-최적화기")
   - Optimize 쿼리 와 함께 적절한 인덱스
   - 컨텍스트: "쿼리 실행 taking 5s, missing 인덱스 에 user_id 열, N+1 쿼리 패턴 감지된"
3. **단계 3b**: 작업(subagent_type="애플리케이션-성능::성능-엔지니어")
   - Add 캐싱 레이어 위한 자주 accessed 데이터
   - 컨텍스트: "데이터베이스 쿼리 최적화된 에서 5s 에 50ms 에 의해 adding 인덱스 에 user_id 열. 애플리케이션 여전히 experiencing 2s 응답 times due 에 N+1 쿼리 패턴 로드 100+ 사용자 레코드 per 요청. Add Redis 캐싱 와 함께 5-minute TTL 위한 사용자 프로필."
4. **단계 3c**: 작업(subagent_type="인시던트-응답::devops-troubleshooter")
   - Configure 모니터링 위한 쿼리 성능 및 캐시 hit 평가합니다
   - 컨텍스트: "캐시 레이어 added 와 함께 Redis. Need 모니터링 위한: 쿼리 p95 지연 시간 (threshold: 100ms), 캐시 hit rate (threshold: >80%), 캐시 메모리 usage (경고 에서 80%)."

**예제 2: Frontend JavaScript 오류 에서 Production**

**시퀀스:**
1. **단계 1**: 오류-detective 분석합니다 Sentry 오류 보고서
   - 컨텍스트: "TypeError: Cannot 읽은 속성 '맵' of undefined, 500+ occurrences 에서 마지막 hour, affects Safari 사용자 에 iOS 14"
2. **단계 2**: 디버거 + 코드-리뷰어 investigate
   - 컨텍스트: "API 응답 때때로 returns null instead of 빈 배열 때 아니요 results. Frontend assumes 배열."
3. **단계 3a**: 작업(subagent_type="javascript-typescript::typescript-pro")
   - Fix frontend 와 함께 적절한 null 확인합니다
   - Add 유형 guards
   - 컨텍스트: "Backend API /api/사용자 엔드포인트 returning null instead of [] 때 아니요 results. Fix frontend 에 handle 둘 다. Add TypeScript strict null 확인합니다."
4. **단계 3b**: 작업(subagent_type="backend-개발::backend-아키텍트")
   - Fix backend 에 항상 반환 배열
   - 업데이트 API 계약
   - 컨텍스트: "Frontend now 처리합니다 null, 그러나 API should follow 계약 및 반환 [] not null. 업데이트 OpenAPI spec 에 document this."
5. **단계 4**: test-automator 실행합니다 cross-browser 테스트합니다
6. **단계 5**: 코드-리뷰어 문서화합니다 API 계약 변경합니다

**예제 3: Security 취약점 에서 인증**

**시퀀스:**
1. **단계 1**: 오류-detective 검토합니다 security scan 보고서
   - 컨텍스트: "SQL 인젝션 취약점 에서 login 엔드포인트, Snyk severity: HIGH"
2. **단계 2**: 디버거 + security-감사자 investigate
   - 컨텍스트: "사용자 입력 not sanitized 에서 SQL 곳 clause, 허용합니다 인증 bypass"
3. **단계 3**: 작업(subagent_type="security-scanning::security-감사자")
   - Implement parameterized 쿼리
   - Add 입력 검증
   - Add 속도 제한
   - 컨텍스트: "Replace string concatenation 와 함께 준비된 statements. Add 입력 검증 위한 email format. Implement 속도 제한 (5 attempts per 15 min)."
4. **단계 4a**: test-automator adds security 테스트합니다
   - SQL 인젝션 attempts
   - Brute force scenarios
5. **단계 4b**: security-감사자 수행합니다 penetration 테스트
6. **단계 5**: 코드-리뷰어 문서화합니다 security improvements 및 생성합니다 postmortem

**컨텍스트 Passing 템플릿:**
```
Context for {next_agent}:

Completed by {previous_agent}:
- {summary_of_work}
- {key_findings}
- {changes_made}

Remaining work:
- {specific_tasks_for_next_agent}
- {files_to_modify}
- {constraints_to_follow}

Dependencies:
- {systems_or_components_affected}
- {data_needed}
- {integration_points}

Success criteria:
- {measurable_outcomes}
- {verification_steps}
```

## 구성 Options

Customize 워크플로우 behavior 에 의해 setting priorities 에서 호출:

**VERIFICATION_LEVEL**: 제어합니다 depth of 테스트 및 검증
- **최소**: Quick fix 와 함께 기본 테스트합니다, skip 성능 benchmarks
  - Use 위한: Low-위험 버그, cosmetic 이슈, 문서화 수정합니다
  - Phases: 1-2-3 (skip 상세한 단계 4)
  - Timeline: ~30 minutes
- **표준**: 전체 test coverage + 코드 review (default)
  - Use 위한: Most production 버그, 기능 이슈, 데이터 버그
  - Phases: 1-2-3-4 (모든 확인)
  - Timeline: ~2-4 hours
- **포괄적인**: 표준 + security audit + 성능 benchmarks + chaos 테스트
  - Use 위한: Security 이슈, 성능 문제, 데이터 corruption, high-traffic 시스템
  - Phases: 1-2-3-4-5 (포함하여 long-term 방지)
  - Timeline: ~1-2 days

**PREVENTION_FOCUS**: 제어합니다 investment 에서 미래 방지
- **없음**: Fix 오직, 아니요 방지 work
  - Use 위한: One-꺼짐 이슈, 레거시 코드 being 더 이상 사용되지 않음, 외부 라이브러리 버그
  - 출력: 코드 fix + 테스트합니다 오직
- **immediate**: Add 테스트합니다 및 기본 linting (default)
  - Use 위한: 일반적인 버그, recurring 패턴, 팀 codebase
  - 출력: Fix + 테스트합니다 + linting 규칙 + 최소 모니터링
- **포괄적인**: 전체 방지 suite 와 함께 모니터링, 아키텍처 improvements
  - Use 위한: High-severity incidents, systemic 이슈, architectural 문제
  - 출력: Fix + 테스트합니다 + linting + 모니터링 + 아키텍처 docs + postmortem

**ROLLOUT_STRATEGY**: 제어합니다 배포 접근법
- **immediate**: Deploy 직접 에 production (위한 hotfixes, low-위험 변경합니다)
- **canary**: Gradual rollout 에 subset of traffic (default 위한 medium-위험)
- **blue-green**: 전체 환경 switch 와 함께 순간 롤백 역량
- **기능-flag**: Deploy 코드 그러나 control activation 를 통해 기능 flags (high-위험 변경합니다)

**OBSERVABILITY_LEVEL**: 제어합니다 instrumentation depth
- **최소**: 기본 오류 로깅 오직
- **표준**: 구조화된 로깅합니다 + 키 메트릭 (default)
- **포괄적인**: 전체 분산 추적 + 사용자 정의 대시보드 + SLOs

**예제 호출:**
```
Issue: Users experiencing timeout errors on checkout page (500+ errors/hour)

Config:
- VERIFICATION_LEVEL: comprehensive (affects revenue)
- PREVENTION_FOCUS: comprehensive (high business impact)
- ROLLOUT_STRATEGY: canary (test on 5% traffic first)
- OBSERVABILITY_LEVEL: comprehensive (need detailed monitoring)
```

## 현대적인 디버깅 Tools 통합

This 워크플로우 leverages 현대적인 2024/2025 tools:

**Observability 플랫폼:**
- Sentry (오류 추적, 릴리스 추적, 성능 모니터링)
- DataDog (APM, 로깅합니다, 추적합니다, 인프라 모니터링)
- OpenTelemetry (벤더 중립적 분산 추적)
- Honeycomb (observability 위한 복잡한 분산 시스템)
- 새로운 Relic (APM, synthetic 모니터링)

**AI-지원된 디버깅:**
- GitHub Copilot (코드 suggestions, test 세대, 버그 패턴 인식)
- Claude 코드 (포괄적인 코드 분석, 아키텍처 review)
- Sourcegraph Cody (codebase search 및 understanding)
- Tabnine (코드 완료 와 함께 버그 방지)

**Git 및 버전 Control:**
- 자동화된 git bisect 와 함께 reproduction 스크립트
- GitHub Actions 위한 자동화된 테스트 에 bisect commits
- Git blame 분석 위한 identifying 코드 ownership
- 커밋 메시지 분석 위한 understanding 변경합니다

**테스트 프레임워크:**
- Jest/Vitest (JavaScript/TypeScript 단위/통합 테스트합니다)
- pytest (Python 테스트 와 함께 fixtures 및 parametrization)
- Go 테스트 + testify (Go 단위 및 테이블-driven 테스트합니다)
- Playwright/Cypress (end-에-end browser 테스트)
- k6/Locust (load 및 성능 테스트)

**정적 분석:**
- ESLint/Prettier (JavaScript/TypeScript linting 및 형식 지정)
- Ruff/mypy (Python linting 및 유형 확인)
- golangci-lint (Go 포괄적인 linting)
- Clippy (Rust linting 및 최선의 관행)
- SonarQube (엔터프라이즈 코드 품질 및 security)

**성능 Profiling:**
- Chrome DevTools (frontend 성능)
- pprof (Go profiling)
- py-spy (Python profiling)
- Pyroscope (continuous profiling)
- Flame 그래프 위한 CPU/메모리 분석

**Security Scanning:**
- Snyk (종속성 취약점 scanning)
- Dependabot (자동화된 종속성 업데이트합니다)
- OWASP ZAP (security 테스트)
- Semgrep (사용자 정의 security 규칙)
- npm audit / pip-audit / cargo audit

## Success Criteria

A fix is considered 완전한 때 모든 of the 다음 are met:

**근 Cause Understanding:**
- 근 cause is 식별된 와 함께 supporting evidence
- 실패 메커니즘 is 명확하게 문서화된
- Introducing 커밋 식별된 (만약 적용 가능한 를 통해 git bisect)
- Similar 취약점 catalogued

**Fix 품질:**
- Fix 주소 근 cause, not 방금 symptoms
- 최소 코드 변경합니다 (avoid over-engineering)
- 따릅니다 project 규약 및 패턴
- 아니요 코드 smells 또는 anti-패턴 introduced
- 뒤로 compatibility 유지됨 (또는 breaking 변경합니다 문서화된)

**테스트 확인:**
- 모든 기존 테스트합니다 pass (zero regressions)
- 새로운 테스트합니다 cover the 특정 버그 reproduction
- 엣지 cases 및 오류 경로 테스트된
- 통합 테스트합니다 verify end-에-end behavior
- Test coverage 증가된 (또는 유지됨 에서 high 레벨)

**성능 & Security:**
- 아니요 성능 degradation (p95 지연 시간 내에 5% of baseline)
- 아니요 security 취약점 introduced
- 리소스 usage acceptable (메모리, CPU, I/O)
- Load 테스트 통과 위한 high-traffic 변경합니다

**배포 Readiness:**
- 코드 review approved 에 의해 도메인 전문가
- 롤백 plan 문서화된 및 테스트된
- 기능 flags 구성된 (만약 적용 가능한)
- 모니터링 및 경고 구성된
- Runbook 업데이트된 와 함께 문제 해결 steps

**방지 측정합니다:**
- 정적 분석 규칙 added (만약 적용 가능한)
- 유형 시스템 improvements 구현된 (만약 적용 가능한)
- 문서화 업데이트된 (코드, API, runbook)
- Postmortem 생성된 (만약 high-severity 인시던트)
- 지식 밑 article 생성된 (만약 novel 이슈)

**메트릭:**
- 평균 시간 에 복구 (MTTR): < 4 hours 위한 SEV2+
- 버그 recurrence rate: 0% (same 근 cause should not recur)
- Test coverage: 아니요 decrease, 이상적으로 increase
- 배포 success rate: > 95% (롤백 rate < 5%)

이슈 에 resolve: $인수
