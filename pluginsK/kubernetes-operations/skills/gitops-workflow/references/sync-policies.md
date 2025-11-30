# GitOps 동기 정책

## ArgoCD 동기 정책

### 자동화된 동기
```yaml
syncPolicy:
  automated:
    prune: true       # Delete resources removed from Git
    selfHeal: true    # Reconcile manual changes
    allowEmpty: false # Prevent empty sync
```

### Manual 동기
```yaml
syncPolicy:
  syncOptions:
  - PrunePropagationPolicy=foreground
  - CreateNamespace=true
```

### 동기 Windows
```yaml
syncWindows:
- kind: allow
  schedule: "0 8 * * *"
  duration: 1h
  applications:
  - my-app
- kind: deny
  schedule: "0 22 * * *"
  duration: 8h
  applications:
  - '*'
```

### 재시도 정책
```yaml
syncPolicy:
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

## Flux 동기 정책

### Kustomization 동기
```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
spec:
  interval: 5m
  prune: true
  wait: true
  timeout: 5m
  retryInterval: 1m
  force: false
```

### 소스 동기 간격
```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
spec:
  interval: 1m
  timeout: 60s
```

## Health 평가

### 사용자 정의 Health 확인합니다
```yaml
# ArgoCD
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.MyCustomResource: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
          if condition.type == "Ready" and condition.status == "False" then
            hs.status = "Degraded"
            hs.message = condition.message
            return hs
          end
          if condition.type == "Ready" and condition.status == "True" then
            hs.status = "Healthy"
            hs.message = condition.message
            return hs
          end
        end
      end
    end
    hs.status = "Progressing"
    hs.message = "Waiting for status"
    return hs
```

## 동기 Options

### 일반적인 동기 Options
- `PrunePropagationPolicy=foreground` - Wait 위한 pruned 리소스 에 be deleted
- `CreateNamespace=true` - Auto-create namespace
- `Validate=false` - Skip kubectl 검증
- `PruneLast=true` - Prune 리소스 이후 동기
- `RespectIgnoreDifferences=true` - Honor ignore differences
- `ApplyOutOfSyncOnly=true` - 오직 apply out-of-동기 리소스

## 최선의 관행

1. Use 자동화된 동기 위한 non-production
2. Require manual approval 위한 production
3. Configure 동기 windows 위한 유지보수
4. Implement health 확인합니다 위한 사용자 정의 리소스
5. Use selective 동기 위한 large 애플리케이션
6. Configure 적절한 재시도 정책
7. 모니터 동기 실패 와 함께 경고
8. Use prune 와 함께 caution 에서 production
9. Test 동기 정책 에서 staging
10. Document 동기 behavior 위한 teams
