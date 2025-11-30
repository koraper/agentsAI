---
name: deployment-pipeline-design
description: 설계 multi-단계 CI/CD 파이프라인 와 함께 approval gates, security 확인합니다, 및 배포 오케스트레이션. Use 때 architecting 배포 워크플로우, 설정하는 continuous 전달, 또는 implementing GitOps 관행.
---

# 배포 파이프라인 설계

아키텍처 패턴 위한 multi-단계 CI/CD 파이프라인 와 함께 approval gates 및 배포 strategies.

## Purpose

설계 강력한, secure 배포 파이프라인 것 balance 속도 와 함께 safety 통해 적절한 단계 조직 및 approval 워크플로우.

## 때 에 Use

- 설계 CI/CD 아키텍처
- Implement 배포 gates
- Configure multi-환경 파이프라인
- Establish 배포 최선의 관행
- Implement progressive 전달

## 파이프라인 Stages

### 표준 파이프라인 흐름

```
┌─────────┐   ┌──────┐   ┌─────────┐   ┌────────┐   ┌──────────┐
│  Build  │ → │ Test │ → │ Staging │ → │ Approve│ → │Production│
└─────────┘   └──────┘   └─────────┘   └────────┘   └──────────┘
```

### 상세한 단계 Breakdown

1. **소스** - 코드 checkout
2. **빌드** - Compile, 패키지, containerize
3. **Test** - 단위, 통합, security scans
4. **Staging Deploy** - Deploy 에 staging 환경
5. **통합 테스트합니다** - E2E, smoke 테스트합니다
6. **Approval Gate** - Manual approval 필수
7. **Production Deploy** - Canary, blue-green, rolling
8. **확인** - Health 확인합니다, 모니터링
9. **롤백** - 자동화된 롤백 에 실패

## Approval Gate 패턴

### 패턴 1: Manual Approval

```yaml
# GitHub Actions
production-deploy:
  needs: staging-deploy
  environment:
    name: production
    url: https://app.example.com
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to production
      run: |
        # Deployment commands
```

### 패턴 2: 시간-Based Approval

```yaml
# GitLab CI
deploy:production:
  stage: deploy
  script:
    - deploy.sh production
  environment:
    name: production
  when: delayed
  start_in: 30 minutes
  only:
    - main
```

### 패턴 3: Multi-Approver

```yaml
# Azure Pipelines
stages:
- stage: Production
  dependsOn: Staging
  jobs:
  - deployment: Deploy
    environment:
      name: production
      resourceType: Kubernetes
    strategy:
      runOnce:
        preDeploy:
          steps:
          - task: ManualValidation@0
            inputs:
              notifyUsers: 'team-leads@example.com'
              instructions: 'Review staging metrics before approving'
```

**참조:** See `assets/approval-gate-template.yml`

## 배포 Strategies

### 1. Rolling 배포

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**Characteristics:**
- Gradual rollout
- Zero downtime
- 쉬운 롤백
- 최선의 위한 most 애플리케이션

### 2. Blue-Green 배포

```yaml
# Blue (current)
kubectl apply -f blue-deployment.yaml
kubectl label service my-app version=blue

# Green (new)
kubectl apply -f green-deployment.yaml
# Test green environment
kubectl label service my-app version=green

# Rollback if needed
kubectl label service my-app version=blue
```

**Characteristics:**
- 순간 switchover
- 쉬운 롤백
- Doubles 인프라 cost temporarily
- 좋은 위한 high-위험 deployments

### 3. Canary 배포

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - setWeight: 25
      - pause: {duration: 5m}
      - setWeight: 50
      - pause: {duration: 5m}
      - setWeight: 100
```

**Characteristics:**
- Gradual traffic shift
- 위험 mitigation
- Real 사용자 테스트
- 필요합니다 서비스 메시 또는 similar

### 4. 기능 Flags

```python
from flagsmith import Flagsmith

flagsmith = Flagsmith(environment_key="API_KEY")

if flagsmith.has_feature("new_checkout_flow"):
    # New code path
    process_checkout_v2()
else:
    # Existing code path
    process_checkout_v1()
```

**Characteristics:**
- Deploy 없이 releasing
- A/B 테스트
- 순간 롤백
- 세분화된 control

## 파이프라인 오케스트레이션

### Multi-단계 파이프라인 예제

```yaml
name: Production Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build application
        run: make build
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Unit tests
        run: make test
      - name: Security scan
        run: trivy image myapp:${{ github.sha }}

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: staging
    steps:
      - name: Deploy to staging
        run: kubectl apply -f k8s/staging/

  integration-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E tests
        run: npm run test:e2e

  deploy-production:
    needs: integration-test
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: Canary deployment
        run: |
          kubectl apply -f k8s/production/
          kubectl argo rollouts promote my-app

  verify:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: Health check
        run: curl -f https://app.example.com/health
      - name: Notify team
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"Production deployment successful!"}'
```

## 파이프라인 최선의 관행

1. **Fail fast** - Run quick 테스트합니다 첫 번째
2. **병렬로 실행** - Run 독립적인 jobs 동시에
3. **캐싱** - 캐시 종속성 사이 실행합니다
4. **아티팩트 관리** - Store 빌드 아티팩트
5. **환경 parity** - Keep 환경 일관된
6. **Secrets 관리** - Use secret 저장합니다 (Vault, etc.)
7. **배포 windows** - Schedule deployments 적절하게
8. **모니터링 통합** - Track 배포 메트릭
9. **롤백 자동화** - Auto-롤백 에 실패
10. **문서화** - Document 파이프라인 stages

## 롤백 Strategies

### 자동화된 롤백

```yaml
deploy-and-verify:
  steps:
    - name: Deploy new version
      run: kubectl apply -f k8s/

    - name: Wait for rollout
      run: kubectl rollout status deployment/my-app

    - name: Health check
      id: health
      run: |
        for i in {1..10}; do
          if curl -sf https://app.example.com/health; then
            exit 0
          fi
          sleep 10
        done
        exit 1

    - name: Rollback on failure
      if: failure()
      run: kubectl rollout undo deployment/my-app
```

### Manual 롤백

```bash
# List revision history
kubectl rollout history deployment/my-app

# Rollback to previous version
kubectl rollout undo deployment/my-app

# Rollback to specific revision
kubectl rollout undo deployment/my-app --to-revision=3
```

## 모니터링 및 메트릭

### 키 파이프라인 메트릭

- **배포 Frequency** - 어떻게 자주 deployments occur
- **리드 시간** - 시간 에서 커밋 에 production
- **변경 실패 Rate** - 백분율 of 실패 deployments
- **평균 시간 에 복구 (MTTR)** - 시간 에 recover 에서 실패
- **파이프라인 Success Rate** - 백분율 of 성공한 실행합니다
- **평균 파이프라인 기간** - 시간 에 완전한 파이프라인

### 통합 와 함께 모니터링

```yaml
- name: Post-deployment verification
  run: |
    # Wait for metrics stabilization
    sleep 60

    # Check error rate
    ERROR_RATE=$(curl -s "$PROMETHEUS_URL/api/v1/query?query=rate(http_errors_total[5m])" | jq '.data.result[0].value[1]')

    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "Error rate too high: $ERROR_RATE"
      exit 1
    fi
```

## 참조 파일

- `references/pipeline-orchestration.md` - 복잡한 파이프라인 패턴
- `assets/approval-gate-template.yml` - Approval 워크플로우 템플릿

## 관련됨 Skills

- `github-actions-templates` - 위한 GitHub Actions 구현
- `gitlab-ci-patterns` - 위한 GitLab CI 구현
- `secrets-management` - 위한 secrets 처리
