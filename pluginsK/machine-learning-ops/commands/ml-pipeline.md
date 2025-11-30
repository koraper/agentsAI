# Machine Learning 파이프라인 - Multi-에이전트 MLOps 오케스트레이션

설계 및 implement a 완전한 ML 파이프라인 위한: $인수

## Thinking

This 워크플로우 오케스트레이션합니다 여러 specialized 에이전트 에 빌드 a 프로덕션 준비 완료 ML 파이프라인 다음 현대적인 MLOps 최선의 관행. The 접근법 강조합니다:

- **단계-based 조정**: 각 단계 빌드 upon 이전 출력, 와 함께 명확한 handoffs 사이 에이전트
- **현대적인 tooling 통합**: MLflow/W&B 위한 experiments, Feast/Tecton 위한 기능, KServe/Seldon 위한 serving
- **Production-첫 번째 mindset**: 모든 컴포넌트 설계된 위한 scale, 모니터링, 및 신뢰성
- **Reproducibility**: 버전 control 위한 데이터, 모델, 및 인프라
- **Continuous improvement**: 자동화된 retraining, A/B 테스트, 및 drift 감지

The multi-에이전트 접근법 보장합니다 각 측면 is 처리된 에 의해 도메인 experts:
- 데이터 engineers handle ingestion 및 품질
- 데이터 scientists 설계 기능 및 experiments
- ML engineers implement training 파이프라인
- MLOps engineers handle production 배포
- Observability engineers ensure 모니터링

## 단계 1: 데이터 & 요구사항 분석

<작업>
subagent_type: 데이터-엔지니어
prompt: |
  Analyze 및 설계 데이터 파이프라인 위한 ML 시스템 와 함께 요구사항: $인수

  Deliverables:
  1. 데이터 소스 audit 및 ingestion 전략:
     - 소스 시스템 및 연결 패턴
     - 스키마 검증 사용하여 Pydantic/Great Expectations
     - 데이터 versioning 와 함께 DVC 또는 lakeFS
     - Incremental 로드 및 CDC strategies

  2. 데이터 품질 프레임워크:
     - Profiling 및 통계 세대
     - Anomaly 감지 규칙
     - 데이터 lineage 추적
     - 품질 gates 및 SLAs

  3. 스토리지 아키텍처:
     - Raw/처리된/기능 layers
     - 분할 전략
     - Retention 정책
     - Cost 최적화

  Provide 구현 코드 위한 긴급 컴포넌트 및 통합 패턴.
</작업>

<작업>
subagent_type: 데이터-과학자
prompt: |
  설계 기능 engineering 및 모델 요구사항 위한: $인수
  사용하여 데이터 아키텍처 에서: {phase1.데이터-엔지니어.출력}

  Deliverables:
  1. 기능 engineering 파이프라인:
     - 변환 사양
     - 기능 store 스키마 (Feast/Tecton)
     - Statistical 검증 규칙
     - 처리 strategies 위한 missing 데이터/outliers

  2. 모델 요구사항:
     - 알고리즘 선택 rationale
     - 성능 메트릭 및 baselines
     - Training 데이터 요구사항
     - 평가 criteria 및 thresholds

  3. Experiment 설계:
     - 가설 및 success 메트릭
     - A/B 테스트 methodology
     - 샘플 size calculations
     - Bias 감지 접근법

  Include 기능 변환 코드 및 statistical 검증 logic.
</작업>

## 단계 2: 모델 개발 & Training

<작업>
subagent_type: ml-엔지니어
prompt: |
  Implement training 파이프라인 based 에 요구사항: {phase1.데이터-과학자.출력}
  사용하여 데이터 파이프라인: {phase1.데이터-엔지니어.출력}

  빌드 포괄적인 training 시스템:
  1. Training 파이프라인 구현:
     - 모듈식 training 코드 와 함께 명확한 인터페이스
     - Hyperparameter 최적화 (Optuna/Ray Tune)
     - 분산 training 지원 (Horovod/PyTorch DDP)
     - Cross-검증 및 ensemble strategies

  2. Experiment 추적 설정:
     - MLflow/가중치를 부여합니다 & Biases 통합
     - Metric 로깅 및 시각화
     - 아티팩트 관리 (모델, plots, 데이터 샘플)
     - Experiment 비교 및 분석 tools

  3. 모델 레지스트리 통합:
     - 버전 control 및 태깅 전략
     - 모델 메타데이터 및 lineage
     - Promotion 워크플로우 (dev -> staging -> prod)
     - 롤백 절차

  Provide 완전한 training 코드 와 함께 구성 관리.
</작업>

<작업>
subagent_type: python-pro
prompt: |
  Optimize 및 productionize ML 코드 에서: {phase2.ml-엔지니어.출력}

  Focus areas:
  1. 코드 품질 및 구조:
     - Refactor 위한 production 표준
     - Add 포괄적인 오류 처리
     - Implement 적절한 로깅 와 함께 구조화된 형식을 지정합니다
     - Create reusable 컴포넌트 및 utilities

  2. 성능 최적화:
     - 프로필 및 optimize bottlenecks
     - Implement 캐싱 strategies
     - Optimize 데이터 로드 및 preprocessing
     - 메모리 관리 위한 large-scale training

  3. 테스트 프레임워크:
     - 단위 테스트합니다 위한 데이터 transformations
     - 통합 테스트합니다 위한 파이프라인 컴포넌트
     - 모델 품질 테스트합니다 (invariance, directional)
     - 성능 regression 테스트합니다

  Deliver 프로덕션 준비 완료, maintainable 코드 와 함께 전체 test coverage.
</작업>

## 단계 3: Production 배포 & Serving

<작업>
subagent_type: mlops-엔지니어
prompt: |
  설계 production 배포 위한 모델 에서: {phase2.ml-엔지니어.출력}
  와 함께 최적화된 코드 에서: {phase2.python-pro.출력}

  구현 요구사항:
  1. 모델 serving 인프라:
     - REST/gRPC APIs 와 함께 FastAPI/TorchServe
     - Batch prediction 파이프라인 (Airflow/Kubeflow)
     - 스트림 처리 (Kafka/Kinesis 통합)
     - 모델 serving 플랫폼 (KServe/Seldon 핵심)

  2. 배포 strategies:
     - Blue-green deployments 위한 zero downtime
     - Canary 릴리스 와 함께 traffic 분할하는
     - Shadow deployments 위한 검증
     - A/B 테스트 인프라

  3. CI/CD 파이프라인:
     - GitHub Actions/GitLab CI 워크플로우
     - 자동화된 테스트 gates
     - 모델 검증 이전 배포
     - ArgoCD 위한 GitOps 배포

  4. 인프라 처럼 코드:
     - Terraform 모듈 위한 cloud 리소스
     - Helm 차트 위한 Kubernetes deployments
     - Docker multi-단계 빌드 위한 최적화
     - Secret 관리 와 함께 Vault/Secrets Manager

  Provide 완전한 배포 구성 및 자동화 스크립트.
</작업>

<작업>
subagent_type: kubernetes-아키텍트
prompt: |
  설계 Kubernetes 인프라 위한 ML workloads 에서: {phase3.mlops-엔지니어.출력}

  Kubernetes-특정 요구사항:
  1. Workload 오케스트레이션:
     - Training 작업 예약 와 함께 Kubeflow
     - GPU 리소스 allocation 및 sharing
     - 지점/preemptible 인스턴스 통합
     - Priority 클래스 및 리소스 quotas

  2. Serving 인프라:
     - HPA/VPA 위한 autoscaling
     - KEDA 위한 이벤트 기반 확장
     - Istio 서비스 메시 위한 traffic 관리
     - 모델 캐싱 및 warm-up strategies

  3. 스토리지 및 데이터 access:
     - PVC strategies 위한 training 데이터
     - 모델 아티팩트 스토리지 와 함께 CSI drivers
     - 분산 스토리지 위한 기능 저장합니다
     - 캐시 layers 위한 inference 최적화

  Provide Kubernetes manifests 및 Helm 차트 위한 entire ML 플랫폼.
</작업>

## 단계 4: 모니터링 & Continuous Improvement

<작업>
subagent_type: observability-엔지니어
prompt: |
  Implement 포괄적인 모니터링 위한 ML 시스템 배포된 에서: {phase3.mlops-엔지니어.출력}
  사용하여 Kubernetes 인프라: {phase3.kubernetes-아키텍트.출력}

  모니터링 프레임워크:
  1. 모델 성능 모니터링:
     - Prediction 정확성 추적
     - 지연 시간 및 처리량 메트릭
     - 기능 importance shifts
     - 비즈니스 KPI correlation

  2. 데이터 및 모델 drift 감지:
     - Statistical drift 감지 (KS test, PSI)
     - 개념 drift 모니터링
     - 기능 배포 추적
     - 자동화된 drift 경고 및 보고서

  3. 시스템 observability:
     - Prometheus 메트릭 위한 모든 컴포넌트
     - Grafana 대시보드 위한 시각화
     - 분산 추적 와 함께 Jaeger/Zipkin
     - Log 집계 와 함께 ELK/Loki

  4. 경고 및 자동화:
     - PagerDuty/Opsgenie 통합
     - 자동화된 retraining 트리거합니다
     - 성능 degradation 워크플로우
     - 인시던트 응답 runbooks

  5. Cost 추적:
     - 리소스 사용률 메트릭
     - Cost allocation 에 의해 모델/experiment
     - 최적화 recommendations
     - Budget 경고 및 제어합니다

  Deliver 모니터링 구성, 대시보드, 및 경고 규칙.
</작업>

## 구성 Options

- **experiment_tracking**: mlflow | wandb | neptune | clearml
- **feature_store**: feast | tecton | databricks | 사용자 정의
- **serving_platform**: kserve | seldon | torchserve | triton
- **오케스트레이션**: kubeflow | airflow | prefect | dagster
- **cloud_provider**: aws | azure | gcp | 멀티 클라우드
- **deployment_mode**: realtime | batch | 스트리밍 | 하이브리드
- **monitoring_stack**: prometheus | datadog | newrelic | 사용자 정의

## Success Criteria

1. **데이터 파이프라인 Success**:
   - < 0.1% 데이터 품질 이슈 에서 production
   - 자동화된 데이터 검증 passing 99.9% of 시간
   - 완전한 데이터 lineage 추적
   - Sub-second 기능 serving 지연 시간

2. **모델 성능**:
   - Meeting 또는 exceeding baseline 메트릭
   - < 5% 성능 degradation 이전 retraining
   - 성공한 A/B 테스트합니다 와 함께 statistical significance
   - 아니요 undetected 모델 drift > 24 hours

3. **Operational 우수성**:
   - 99.9% uptime 위한 모델 serving
   - < 200ms p99 inference 지연 시간
   - 자동화된 롤백 내에 5 minutes
   - 완전한 observability 와 함께 < 1 minute 경고 시간

4. **개발 Velocity**:
   - < 1 hour 에서 커밋 에 production
   - 병렬로 experiment 실행
   - Reproducible training 실행합니다
   - Self-서비스 모델 배포

5. **Cost 효율성**:
   - < 20% 인프라 waste
   - 최적화된 리소스 allocation
   - Automatic 확장 based 에 load
   - 지점 인스턴스 사용률 > 60%

## 최종 Deliverables

Upon 완료, the 오케스트레이션된 파이프라인 will provide:
- End-에-end ML 파이프라인 와 함께 전체 자동화
- 포괄적인 문서화 및 runbooks
- 프로덕션 준비 완료 인프라 처럼 코드
- 완전한 모니터링 및 경고 시스템
- CI/CD 파이프라인 위한 continuous improvement
- Cost 최적화 및 확장 strategies
- Disaster 복구 및 롤백 절차