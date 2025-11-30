# 데이터 기반 기능 개발

빌드 기능 안내된 에 의해 데이터 인사이트, A/B 테스트, 및 continuous 측정 사용하여 specialized 에이전트 위한 분석, 구현, 및 experimentation.

[확장된 thinking: This 워크플로우 오케스트레이션합니다 a 포괄적인 데이터 기반 개발 프로세스 에서 초기 데이터 분석 및 가설 formulation 통해 기능 구현 와 함께 통합된 분석, A/B 테스트 인프라, 및 post-launch 분석. 각 단계 leverages specialized 에이전트 에 ensure 기능 are 구축된 based 에 데이터 인사이트, 적절하게 instrumented 위한 측정, 및 검증된 통해 제어된 experiments. The 워크플로우 강조합니다 현대적인 product 분석 관행, statistical rigor 에서 테스트, 및 continuous learning 에서 사용자 behavior.]

## 단계 1: 데이터 분석 및 가설 Formation

### 1. Exploratory 데이터 분석
- Use 작업 tool 와 함께 subagent_type="machine-learning-ops::데이터-과학자"
- Prompt: "Perform exploratory 데이터 분석 위한 기능: $인수. Analyze 기존 사용자 behavior 데이터, identify 패턴 및 opportunities, segment 사용자 에 의해 behavior, 및 calculate baseline 메트릭. Use 현대적인 분석 tools (Amplitude, Mixpanel, Segment) 에 understand 현재 사용자 journeys, 변환 funnels, 및 engagement 패턴."
- 출력: EDA 보고서 와 함께 시각화, 사용자 세그먼트합니다, behavioral 패턴, baseline 메트릭

### 2. 비즈니스 가설 개발
- Use 작업 tool 와 함께 subagent_type="비즈니스-분석::비즈니스-분석가"
- 컨텍스트: 데이터 과학자's EDA findings 및 behavioral 패턴
- Prompt: "Formulate 비즈니스 가설 위한 기능: $인수 based 에 데이터 분석. Define 명확한 success 메트릭, 예상되는 impact 에 키 비즈니스 KPIs, target 사용자 세그먼트합니다, 및 minimum detectable effects. Create measurable 가설 사용하여 프레임워크 같은 ICE 점수 매기기 또는 RICE 우선순위 지정."
- 출력: 가설 document, success 메트릭 정의, 예상되는 ROI calculations

### 3. Statistical Experiment 설계
- Use 작업 tool 와 함께 subagent_type="machine-learning-ops::데이터-과학자"
- 컨텍스트: 비즈니스 가설 및 success 메트릭
- Prompt: "설계 statistical experiment 위한 기능: $인수. Calculate 필수 샘플 size 위한 statistical 거듭제곱, define control 및 treatment 그룹화합니다, specify randomization 전략, 및 plan 위한 여러 테스트 corrections. Consider Bayesian A/B 테스트 approaches 위한 faster 결정 making. 설계 위한 둘 다 primary 및 guardrail 메트릭."
- 출력: Experiment 설계 document, 거듭제곱 분석, statistical test plan

## 단계 2: 기능 아키텍처 및 분석 설계

### 4. 기능 아키텍처 계획
- Use 작업 tool 와 함께 subagent_type="데이터-engineering::backend-아키텍트"
- 컨텍스트: 비즈니스 요구사항 및 experiment 설계
- Prompt: "설계 기능 아키텍처 위한: $인수 와 함께 A/B 테스트 역량. Include 기능 flag 통합 (LaunchDarkly, 분할된.io, 또는 Optimizely), gradual rollout 전략, 회로 breakers 위한 safety, 및 clean 분리 사이 control 및 treatment logic. Ensure 아키텍처 지원합니다 real-시간 구성 업데이트합니다."
- 출력: 아키텍처 다이어그램, 기능 flag 스키마, rollout 전략

### 5. 분석 Instrumentation 설계
- Use 작업 tool 와 함께 subagent_type="데이터-engineering::데이터-엔지니어"
- 컨텍스트: 기능 아키텍처 및 success 메트릭
- Prompt: "설계 포괄적인 분석 instrumentation 위한: $인수. Define 이벤트 스키마 위한 사용자 interactions, specify 속성 위한 세그먼테이션 및 분석, 설계 funnel 추적 및 변환 이벤트, plan cohort 분석 역량. Implement 사용하여 현대적인 SDKs (Segment, Amplitude, Mixpanel) 와 함께 적절한 이벤트 분류법."
- 출력: 이벤트 추적 plan, 분석 스키마, instrumentation 가이드

### 6. 데이터 파이프라인 아키텍처
- Use 작업 tool 와 함께 subagent_type="데이터-engineering::데이터-엔지니어"
- 컨텍스트: 분석 요구사항 및 기존 데이터 인프라
- Prompt: "설계 데이터 파이프라인 위한 기능: $인수. Include real-시간 스트리밍 위한 live 메트릭 (Kafka, Kinesis), batch 처리 위한 상세한 분석, 데이터 웨어하우스 통합 (Snowflake, BigQuery), 및 기능 store 위한 ML 만약 적용 가능한. Ensure 적절한 데이터 governance 및 GDPR compliance."
- 출력: 파이프라인 아키텍처, ETL/ELT 사양, 데이터 흐름 다이어그램

## 단계 3: 구현 와 함께 Instrumentation

### 7. Backend 구현
- Use 작업 tool 와 함께 subagent_type="backend-개발::backend-아키텍트"
- 컨텍스트: 아키텍처 설계 및 기능 요구사항
- Prompt: "Implement backend 위한 기능: $인수 와 함께 전체 instrumentation. Include 기능 flag 확인합니다 에서 결정 points, 포괄적인 이벤트 추적 위한 모든 사용자 actions, 성능 메트릭 컬렉션, 오류 추적 및 모니터링. Implement 적절한 로깅 위한 experiment 분석."
- 출력: Backend 코드 와 함께 분석, 기능 flag 통합, 모니터링 설정

### 8. Frontend 구현
- Use 작업 tool 와 함께 subagent_type="frontend-mobile-개발::frontend-개발자"
- 컨텍스트: Backend APIs 및 분석 요구사항
- Prompt: "빌드 frontend 위한 기능: $인수 와 함께 분석 추적. Implement 이벤트 추적 위한 모든 사용자 interactions, 세션 기록 통합 만약 적용 가능한, 성능 메트릭 (핵심 Web Vitals), 및 적절한 오류 boundaries. Ensure 일관된 experience 사이 control 및 treatment 그룹화합니다."
- 출력: Frontend 코드 와 함께 분석, A/B test variants, 성능 모니터링

### 9. ML 모델 통합 (만약 적용 가능한)
- Use 작업 tool 와 함께 subagent_type="machine-learning-ops::ml-엔지니어"
- 컨텍스트: 기능 요구사항 및 데이터 파이프라인
- Prompt: "Integrate ML 모델 위한 기능: $인수 만약 필요한. Implement online inference 와 함께 low 지연 시간, A/B 테스트 사이 모델 버전, 모델 성능 추적, 및 automatic fallback mechanisms. 세트 up 모델 모니터링 위한 drift 감지."
- 출력: ML 파이프라인, 모델 serving 인프라, 모니터링 설정

## 단계 4: Pre-Launch 검증

### 10. 분석 검증
- Use 작업 tool 와 함께 subagent_type="데이터-engineering::데이터-엔지니어"
- 컨텍스트: 구현된 추적 및 이벤트 스키마
- Prompt: "Validate 분석 구현 위한: $인수. Test 모든 이벤트 추적 에서 staging, verify 데이터 품질 및 완전성, validate funnel definitions, ensure 적절한 사용자 식별 및 세션 추적. Run end-에-end 테스트합니다 위한 데이터 파이프라인."
- 출력: 검증 보고서, 데이터 품질 메트릭, 추적 coverage 분석

### 11. Experiment 설정
- Use 작업 tool 와 함께 subagent_type="cloud-인프라::배포-엔지니어"
- 컨텍스트: 기능 flags 및 experiment 설계
- Prompt: "Configure experiment 인프라 위한: $인수. 세트 up 기능 flags 와 함께 적절한 targeting 규칙, configure traffic allocation (start 와 함께 5-10%), implement kill switches, 세트 up 모니터링 경고 위한 키 메트릭. Test randomization 및 할당 logic."
- 출력: Experiment 구성, 모니터링 대시보드, rollout plan

## 단계 5: Launch 및 Experimentation

### 12. Gradual Rollout
- Use 작업 tool 와 함께 subagent_type="cloud-인프라::배포-엔지니어"
- 컨텍스트: Experiment 구성 및 모니터링 설정
- Prompt: "Execute gradual rollout 위한 기능: $인수. Start 와 함께 내부 dogfooding, then 베타 사용자 (1-5%), 점진적으로 increase 에 target traffic. 모니터 오류 평가합니다, 성능 메트릭, 및 early indicators. Implement 자동화된 롤백 에 anomalies."
- 출력: Rollout 실행, 모니터링 경고, health 메트릭

### 13. Real-시간 모니터링
- Use 작업 tool 와 함께 subagent_type="observability-모니터링::observability-엔지니어"
- 컨텍스트: 배포된 기능 및 success 메트릭
- Prompt: "세트 up 포괄적인 모니터링 위한: $인수. Create real-시간 대시보드 위한 experiment 메트릭, configure 경고 위한 statistical significance, 모니터 guardrail 메트릭 위한 부정 impacts, track 시스템 성능 및 오류 평가합니다. Use tools 같은 Datadog, 새로운 Relic, 또는 사용자 정의 대시보드."
- 출력: 모니터링 대시보드, 경고 configurations, SLO definitions

## 단계 6: 분석 및 결정 Making

### 14. Statistical 분석
- Use 작업 tool 와 함께 subagent_type="machine-learning-ops::데이터-과학자"
- 컨텍스트: Experiment 데이터 및 original 가설
- Prompt: "Analyze A/B test results 위한: $인수. Calculate statistical significance 와 함께 confidence intervals, check 위한 segment-레벨 effects, analyze secondary 메트릭 impact, investigate 어떤 unexpected 패턴. Use 둘 다 frequentist 및 Bayesian approaches. 계정 위한 여러 테스트 만약 적용 가능한."
- 출력: Statistical 분석 보고서, significance 테스트합니다, segment 분석

### 15. 비즈니스 Impact 평가
- Use 작업 tool 와 함께 subagent_type="비즈니스-분석::비즈니스-분석가"
- 컨텍스트: Statistical 분석 및 비즈니스 메트릭
- Prompt: "Assess 비즈니스 impact of 기능: $인수. Calculate actual vs 예상되는 ROI, analyze impact 에 키 비즈니스 메트릭, evaluate cost-benefit 포함하여 operational overhead, project long-term 값. Make 권장사항 에 전체 rollout, 반복, 또는 롤백."
- 출력: 비즈니스 impact 보고서, ROI 분석, 권장사항 document

### 16. Post-Launch 최적화
- Use 작업 tool 와 함께 subagent_type="machine-learning-ops::데이터-과학자"
- 컨텍스트: Launch results 및 사용자 feedback
- Prompt: "Identify 최적화 opportunities 위한: $인수 based 에 데이터. Analyze 사용자 behavior 패턴 에서 treatment 그룹, identify friction points 에서 사용자 journey, suggest improvements based 에 데이터, plan follow-up experiments. Use cohort 분석 위한 long-term impact."
- 출력: 최적화 recommendations, follow-up experiment 계획합니다

## 구성 Options

```yaml
experiment_config:
  min_sample_size: 10000
  confidence_level: 0.95
  runtime_days: 14
  traffic_allocation: "gradual"  # gradual, fixed, or adaptive

analytics_platforms:
  - amplitude
  - segment
  - mixpanel

feature_flags:
  provider: "launchdarkly"  # launchdarkly, split, optimizely, unleash

statistical_methods:
  - frequentist
  - bayesian

monitoring:
  - real_time_metrics: true
  - anomaly_detection: true
  - automatic_rollback: true
```

## Success Criteria

- **데이터 Coverage**: 100% of 사용자 interactions 추적된 와 함께 적절한 이벤트 스키마
- **Experiment 유효성**: 적절한 randomization, 충분한 statistical 거듭제곱, 아니요 샘플 비율 mismatch
- **Statistical Rigor**: 명확한 significance 테스트, 적절한 confidence intervals, 여러 테스트 corrections
- **비즈니스 Impact**: Measurable improvement 에서 target 메트릭 없이 degrading guardrail 메트릭
- **Technical 성능**: 아니요 degradation 에서 p95 지연 시간, 오류 평가합니다 below 0.1%
- **결정 속도**: 명확한 go/아니요-go 결정 내에 계획된 experiment 런타임
- **Learning Outcomes**: 문서화된 인사이트 위한 미래 기능 개발

## 조정 Notes

- 데이터 scientists 및 비즈니스 analysts collaborate 에 가설 formation
- Engineers implement 와 함께 분석 처럼 첫 번째-클래스 요구사항, not afterthought
- 기능 flags enable safe experimentation 없이 전체 deployments
- Real-시간 모니터링 허용합니다 위한 quick 반복 및 롤백 만약 필요한
- Statistical rigor 균형된 와 함께 비즈니스 practicality 및 속도 에 market
- Continuous learning 루프 feeds back into 다음 기능 개발 사이클

기능 에 develop 와 함께 데이터 기반 접근법: $인수