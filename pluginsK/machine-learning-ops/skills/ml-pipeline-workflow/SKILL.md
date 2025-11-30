---
name: ml-pipeline-workflow
description: 빌드 end-에-end MLOps 파이프라인 에서 데이터 준비 통해 모델 training, 검증, 및 production 배포. Use 때 생성하는 ML 파이프라인, implementing MLOps 관행, 또는 automating 모델 training 및 배포 워크플로우.
---

# ML 파이프라인 워크플로우

완전한 end-에-end MLOps 파이프라인 오케스트레이션 에서 데이터 준비 통해 모델 배포.

## Overview

This skill 제공합니다 포괄적인 guidance 위한 구축 production ML 파이프라인 것 handle the 전체 lifecycle: 데이터 ingestion → 준비 → training → 검증 → 배포 → 모니터링.

## 때 에 Use This Skill

- 구축 새로운 ML 파이프라인 에서 scratch
- Designing 워크플로우 오케스트레이션 위한 ML 시스템
- Implementing 데이터 → 모델 → 배포 자동화
- 설정하는 reproducible training 워크플로우
- 생성하는 DAG-based ML 오케스트레이션
- Integrating ML 컴포넌트 into production 시스템

## 무엇 This Skill 제공합니다

### 핵심 역량

1. **파이프라인 아키텍처**
   - End-에-end 워크플로우 설계
   - DAG 오케스트레이션 패턴 (Airflow, Dagster, Kubeflow)
   - 컴포넌트 종속성 및 데이터 흐름
   - 오류 처리 및 재시도 strategies

2. **데이터 준비**
   - 데이터 검증 및 품질 확인합니다
   - 기능 engineering 파이프라인
   - 데이터 versioning 및 lineage
   - Train/검증/test 분할하는 strategies

3. **모델 Training**
   - Training 작업 오케스트레이션
   - Hyperparameter 관리
   - Experiment 추적 통합
   - 분산 training 패턴

4. **모델 검증**
   - 검증 프레임워크 및 메트릭
   - A/B 테스트 인프라
   - 성능 regression 감지
   - 모델 비교 워크플로우

5. **배포 자동화**
   - 모델 serving 패턴
   - Canary deployments
   - Blue-green 배포 strategies
   - 롤백 mechanisms

### 참조 문서화

See the `references/` 디렉터리 위한 상세한 안내합니다:
- **데이터-준비.md** - 데이터 정리, 검증, 및 기능 engineering
- **모델-training.md** - Training 워크플로우 및 최선의 관행
- **모델-검증.md** - 검증 strategies 및 메트릭
- **모델-배포.md** - 배포 패턴 및 serving 아키텍처

### 자산 및 템플릿

The `assets/` 디렉터리 contains:
- **파이프라인-dag.yaml.템플릿** - DAG 템플릿 위한 워크플로우 오케스트레이션
- **training-config.yaml** - Training 구성 템플릿
- **검증-checklist.md** - Pre-배포 검증 checklist

## Usage 패턴

### 기본 파이프라인 설정

```python
# 1. Define pipeline stages
stages = [
    "data_ingestion",
    "data_validation",
    "feature_engineering",
    "model_training",
    "model_validation",
    "model_deployment"
]

# 2. Configure dependencies
# See assets/pipeline-dag.yaml.template for full example
```

### Production 워크플로우

1. **데이터 준비 단계**
   - Ingest raw 데이터 에서 sources
   - Run 데이터 품질 확인합니다
   - Apply 기능 transformations
   - 버전 처리된 datasets

2. **Training 단계**
   - Load versioned training 데이터
   - Execute training jobs
   - Track experiments 및 메트릭
   - Save trained 모델

3. **검증 단계**
   - Run 검증 test suite
   - Compare against baseline
   - Generate 성능 보고서
   - Approve 위한 배포

4. **배포 단계**
   - 패키지 모델 아티팩트
   - Deploy 에 serving 인프라
   - Configure 모니터링
   - Validate production traffic

## 최선의 관행

### 파이프라인 설계

- **Modularity**: 각 단계 should be independently testable
- **Idempotency**: Re-실행 중 stages should be safe
- **Observability**: Log 메트릭 에서 모든 단계
- **Versioning**: Track 데이터, 코드, 및 모델 버전
- **실패 처리**: Implement 재시도 logic 및 경고

### 데이터 관리

- Use 데이터 검증 라이브러리 (Great Expectations, TFX)
- 버전 datasets 와 함께 DVC 또는 similar tools
- Document 기능 engineering transformations
- Maintain 데이터 lineage 추적

### 모델 작업

- 별도 training 및 serving 인프라
- Use 모델 registries (MLflow, 가중치를 부여합니다 & Biases)
- Implement gradual rollouts 위한 새로운 모델
- 모니터 모델 성능 drift
- Maintain 롤백 역량

### 배포 Strategies

- Start 와 함께 shadow deployments
- Use canary 릴리스 위한 검증
- Implement A/B 테스트 인프라
- 세트 up 자동화된 롤백 트리거합니다
- 모니터 지연 시간 및 처리량

## 통합 Points

### 오케스트레이션 Tools

- **Apache Airflow**: DAG-based 워크플로우 오케스트레이션
- **Dagster**: 자산-based 파이프라인 오케스트레이션
- **Kubeflow 파이프라인**: Kubernetes-native ML 워크플로우
- **Prefect**: 현대적인 dataflow 자동화

### Experiment 추적

- MLflow 위한 experiment 추적 및 모델 레지스트리
- 가중치를 부여합니다 & Biases 위한 시각화 및 collaboration
- TensorBoard 위한 training 메트릭

### 배포 플랫폼

- AWS SageMaker 위한 관리형 ML 인프라
- Google Vertex AI 위한 GCP deployments
- Azure ML 위한 Azure cloud
- Kubernetes + KServe 위한 클라우드 독립적 serving

## Progressive Disclosure

Start 와 함께 the basics 및 점진적으로 add complexity:

1. **레벨 1**: 간단한 linear 파이프라인 (데이터 → train → deploy)
2. **레벨 2**: Add 검증 및 모니터링 stages
3. **레벨 3**: Implement hyperparameter tuning
4. **레벨 4**: Add A/B 테스트 및 gradual rollouts
5. **레벨 5**: Multi-모델 파이프라인 와 함께 ensemble strategies

## 일반적인 패턴

### Batch Training 파이프라인

```yaml
# See assets/pipeline-dag.yaml.template
stages:
  - name: data_preparation
    dependencies: []
  - name: model_training
    dependencies: [data_preparation]
  - name: model_evaluation
    dependencies: [model_training]
  - name: model_deployment
    dependencies: [model_evaluation]
```

### Real-시간 기능 파이프라인

```python
# Stream processing for real-time features
# Combined with batch training
# See references/data-preparation.md
```

### Continuous Training

```python
# Automated retraining on schedule
# Triggered by data drift detection
# See references/model-training.md
```

## 문제 해결

### 일반적인 이슈

- **파이프라인 실패**: Check 종속성 및 데이터 가용성
- **Training instability**: Review hyperparameters 및 데이터 품질
- **배포 이슈**: Validate 모델 아티팩트 및 serving config
- **성능 degradation**: 모니터 데이터 drift 및 모델 메트릭

### 디버깅 Steps

1. Check 파이프라인 로깅합니다 위한 각 단계
2. Validate 입력/출력 데이터 에서 boundaries
3. Test 컴포넌트 에서 격리
4. Review experiment 추적 메트릭
5. Inspect 모델 아티팩트 및 메타데이터

## 다음 Steps

이후 설정하는 your 파이프라인:

1. Explore **hyperparameter-tuning** skill 위한 최적화
2. Learn **experiment-추적-설정** 위한 MLflow/W&B
3. Review **모델-배포-패턴** 위한 serving strategies
4. Implement 모니터링 와 함께 observability tools

## 관련됨 Skills

- **experiment-추적-설정**: MLflow 및 가중치를 부여합니다 & Biases 통합
- **hyperparameter-tuning**: 자동화된 hyperparameter 최적화
- **모델-배포-패턴**: 고급 배포 strategies
