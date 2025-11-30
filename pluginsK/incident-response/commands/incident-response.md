Orchestrate multi-에이전트 인시던트 응답 와 함께 현대적인 SRE 관행 위한 rapid 해결 및 learning:

[확장된 thinking: This 워크플로우 구현합니다 a 포괄적인 인시던트 명령 시스템 (ICS) 다음 현대적인 SRE 원칙. 여러 specialized 에이전트 collaborate 통해 정의된 phases: 감지/triage, investigation/mitigation, communication/조정, 및 해결/postmortem. The 워크플로우 강조합니다 속도 없이 sacrificing 정확성, 유지합니다 명확한 communication channels, 및 보장합니다 모든 인시던트 becomes a learning opportunity 통해 blameless postmortems 및 systematic improvements.]

## 구성

### Severity Levels
- **P0/SEV-1**: 완전한 outage, security 침해, 데이터 loss - immediate 모든-hands 응답
- **P1/SEV-2**: 주요 degradation, 중요한 사용자 impact - rapid 응답 필수
- **P2/SEV-3**: 부수적 degradation, 제한된 impact - 표준 응답
- **P3/SEV-4**: Cosmetic 이슈, 아니요 사용자 impact - 예약됨 해결

### 인시던트 유형
- 성능 degradation
- 서비스 outage
- Security 인시던트
- 데이터 무결성 이슈
- 인프라 실패
- Third-party 서비스 disruption

## 단계 1: 감지 & Triage

### 1. 인시던트 감지 및 분류
- Use 작업 tool 와 함께 subagent_type="인시던트-responder"
- Prompt: "긴급: Detect 및 classify 인시던트: $인수. Analyze 경고 에서 PagerDuty/Opsgenie/모니터링. Determine: 1) 인시던트 severity (P0-P3), 2) Affected 서비스 및 종속성, 3) 사용자 impact 및 비즈니스 위험, 4) 초기 인시던트 명령 구조 필요한. Check 오류 budgets 및 SLO 위반."
- 출력: Severity 분류, impact 평가, 인시던트 명령 assignments, SLO 상태
- 컨텍스트: 초기 경고, 모니터링 대시보드, 최근 변경합니다

### 2. Observability 분석
- Use 작업 tool 와 함께 subagent_type="observability-모니터링::observability-엔지니어"
- Prompt: "Perform rapid observability sweep 위한 인시던트: $인수. 쿼리: 1) 분산 추적 (OpenTelemetry/Jaeger), 2) 메트릭 correlation (Prometheus/Grafana/DataDog), 3) Log 집계 (ELK/Splunk), 4) APM 데이터, 5) Real 사용자 모니터링. Identify anomalies, 오류 패턴, 및 서비스 degradation points."
- 출력: Observability findings, anomaly 감지, 서비스 health 매트릭스, trace 분석
- 컨텍스트: Severity 레벨 에서 단계 1, affected 서비스

### 3. 초기 Mitigation
- Use 작업 tool 와 함께 subagent_type="인시던트-responder"
- Prompt: "Implement immediate mitigation 위한 P$SEVERITY 인시던트: $인수. Actions: 1) Traffic 제한/rerouting 만약 필요한, 2) 기능 flag disabling 위한 affected 기능, 3) 회로 breaker activation, 4) 롤백 평가 위한 최근 deployments, 5) Scale 리소스 만약 용량-관련됨. Prioritize 사용자 experience 복원."
- 출력: Mitigation actions taken, 임시 수정합니다 applied, 롤백 decisions
- 컨텍스트: Observability findings, severity 분류

## 단계 2: Investigation & 근 Cause 분석

### 4. Deep 시스템 디버깅
- Use 작업 tool 와 함께 subagent_type="오류-디버깅::디버거"
- Prompt: "Conduct deep 디버깅 위한 인시던트: $인수 사용하여 observability 데이터. Investigate: 1) 스택 추적합니다 및 오류 로깅합니다, 2) 데이터베이스 쿼리 성능 및 locks, 3) 네트워크 지연 시간 및 timeouts, 4) 메모리 leaks 및 CPU spikes, 5) 종속성 실패 및 계단식 전파 오류. Apply Five Whys 분석."
- 출력: 근 cause 식별, contributing factors, 종속성 impact 맵
- 컨텍스트: Observability 분석, mitigation 상태

### 5. Security 평가
- Use 작업 tool 와 함께 subagent_type="security-scanning::security-감사자"
- Prompt: "Assess security implications of 인시던트: $인수. Check: 1) DDoS 공격 indicators, 2) 인증/인가 실패, 3) 데이터 exposure 위험, 4) Certificate 이슈, 5) Suspicious access 패턴. Review WAF 로깅합니다, security 그룹화합니다, 및 audit trails."
- 출력: Security 평가, 침해 분석, 취약점 식별
- 컨텍스트: 근 cause findings, 시스템 로깅합니다

### 6. 성능 Engineering 분석
- Use 작업 tool 와 함께 subagent_type="애플리케이션-성능::성능-엔지니어"
- Prompt: "Analyze 성능 aspects of 인시던트: $인수. Examine: 1) 리소스 사용률 패턴, 2) 쿼리 최적화 opportunities, 3) 캐싱 효과성, 4) Load balancer health, 5) CDN 성능, 6) Autoscaling 트리거합니다. Identify bottlenecks 및 용량 이슈."
- 출력: 성능 bottlenecks, 리소스 recommendations, 최적화 opportunities
- 컨텍스트: Debug findings, 현재 mitigation 상태

## 단계 3: 해결 & 복구

### 7. Fix 구현
- Use 작업 tool 와 함께 subagent_type="backend-개발::backend-아키텍트"
- Prompt: "설계 및 implement production fix 위한 인시던트: $인수 based 에 근 cause. 요구사항: 1) 최소 viable fix 위한 rapid 배포, 2) 위험 평가 및 롤백 역량, 3) Staged rollout plan 와 함께 모니터링, 4) 검증 criteria 및 health 확인합니다. Consider 둘 다 immediate fix 및 long-term solution."
- 출력: Fix 구현, 배포 전략, 검증 plan, 롤백 절차
- 컨텍스트: 근 cause 분석, 성능 findings, security 평가

### 8. 배포 및 검증
- Use 작업 tool 와 함께 subagent_type="배포-strategies::배포-엔지니어"
- Prompt: "Execute emergency 배포 위한 인시던트 fix: $인수. 프로세스: 1) Blue-green 또는 canary 배포, 2) Progressive rollout 와 함께 모니터링, 3) Health check 검증 에서 각 단계, 4) 롤백 트리거합니다 구성된, 5) Real-시간 모니터링 동안 배포. 좌표 와 함께 인시던트 명령."
- 출력: 배포 상태, 검증 results, 모니터링 대시보드, 롤백 readiness
- 컨텍스트: Fix 구현, 현재 시스템 상태

## 단계 4: Communication & 조정

### 9. 이해관계자 Communication
- Use 작업 tool 와 함께 subagent_type="콘텐츠-marketing::콘텐츠-marketer"
- Prompt: "Manage 인시던트 communication 위한: $인수. Create: 1) 상태 페이지 업데이트합니다 (공개-facing), 2) 내부 engineering 업데이트합니다 (technical details), 3) Executive summary (비즈니스 impact/ETA), 4) 고객 지원 briefing (talking points), 5) Timeline 문서화 와 함께 키 decisions. 업데이트 모든 15-30 minutes based 에 severity."
- 출력: Communication 아티팩트, 상태 업데이트합니다, 이해관계자 briefings, timeline log
- 컨텍스트: 모든 이전 phases, 현재 해결 상태

### 10. 고객 Impact 평가
- Use 작업 tool 와 함께 subagent_type="인시던트-responder"
- Prompt: "Assess 및 document 고객 impact 위한 인시던트: $인수. Analyze: 1) Affected 사용자 세그먼트합니다 및 지리, 2) 실패 transactions 또는 데이터 loss, 3) SLA 위반 및 contractual implications, 4) 고객 지원 ticket 볼륨, 5) Revenue impact estimation. Prepare proactive 고객 outreach 목록."
- 출력: 고객 impact 보고서, SLA 분석, outreach recommendations
- 컨텍스트: 해결 진행, communication 상태

## 단계 5: Postmortem & 방지

### 11. Blameless Postmortem
- Use 작업 tool 와 함께 subagent_type="문서화-세대::docs-아키텍트"
- Prompt: "Conduct blameless postmortem 위한 인시던트: $인수. Document: 1) 완전한 인시던트 timeline 와 함께 decisions, 2) 근 cause 및 contributing factors (시스템 focus), 3) 무엇 went well 에서 응답, 4) 무엇 could improve, 5) Action items 와 함께 owners 및 deadlines, 6) Lessons learned 위한 팀 education. Follow SRE postmortem 최선의 관행."
- 출력: Postmortem document, action items 목록, 프로세스 improvements, training needs
- 컨텍스트: 완전한 인시던트 history, 모든 에이전트 출력

### 12. 모니터링 및 경고 향상
- Use 작업 tool 와 함께 subagent_type="observability-모니터링::observability-엔지니어"
- Prompt: "Enhance 모니터링 에 prevent recurrence of: $인수. Implement: 1) 새로운 경고 위한 early 감지, 2) SLI/SLO adjustments 만약 필요한, 3) 대시보드 improvements 위한 visibility, 4) Runbook 자동화 opportunities, 5) Chaos engineering scenarios 위한 테스트. Ensure 경고 are actionable 및 reduce noise."
- 출력: 새로운 모니터링 구성, 경고 규칙, 대시보드 업데이트합니다, runbook 자동화
- 컨텍스트: Postmortem findings, 근 cause 분석

### 13. 시스템 강화
- Use 작업 tool 와 함께 subagent_type="backend-개발::backend-아키텍트"
- Prompt: "설계 시스템 improvements 에 prevent 인시던트: $인수. Propose: 1) 아키텍처 변경합니다 위한 복원력 (회로 breakers, bulkheads), 2) Graceful degradation strategies, 3) 용량 계획 adjustments, 4) Technical debt 우선순위 지정, 5) 종속성 감소 opportunities. Create 구현 roadmap."
- 출력: 아키텍처 improvements, 복원력 패턴, technical debt items, roadmap
- 컨텍스트: Postmortem action items, 성능 분석

## Success Criteria

### Immediate Success (동안 인시던트)
- 서비스 복원 내에 SLA targets
- Accurate severity 분류 내에 5 minutes
- 이해관계자 communication 모든 15-30 minutes
- 아니요 계단식 전파 실패 또는 인시던트 escalation
- 명확한 인시던트 명령 구조 유지됨

### Long-term Success (Post-인시던트)
- 포괄적인 postmortem 내에 48 hours
- 모든 action items assigned 와 함께 deadlines
- 모니터링 improvements 배포된 내에 1 week
- Runbook 업데이트합니다 완료됨
- 팀 training conducted 에 lessons learned
- 오류 budget impact 평가된 및 communicated

## 조정 프로토콜

### 인시던트 명령 구조
- **인시던트 Commander**: 결정 authority, 조정
- **Technical 리드**: Technical investigation 및 해결
- **Communications 리드**: 이해관계자 업데이트합니다
- **Subject Matter Experts**: 특정 시스템 expertise

### Communication Channels
- War room (Slack/Teams 채널 또는 Zoom)
- 상태 페이지 업데이트합니다 (StatusPage, Statusly)
- PagerDuty/Opsgenie 위한 경고
- Confluence/개념 위한 문서화

### Handoff 요구사항
- 각 단계 제공합니다 명확한 컨텍스트 에 the 다음
- 모든 findings 문서화된 에서 shared 인시던트 doc
- 결정 rationale 기록된 위한 postmortem
- 타임스탬프 모든 중요한 이벤트

Production 인시던트 requiring immediate 응답: $인수