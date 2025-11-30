---
name: gitops-workflow
description: Implement GitOps 워크플로우 와 함께 ArgoCD 및 Flux 위한 자동화된, declarative Kubernetes deployments 와 함께 continuous reconciliation. Use 때 implementing GitOps 관행, automating Kubernetes deployments, 또는 설정하는 declarative 인프라 관리.
---

# GitOps 워크플로우

완전한 가이드 에 implementing GitOps 워크플로우 와 함께 ArgoCD 및 Flux 위한 자동화된 Kubernetes deployments.

## Purpose

Implement declarative, Git-based continuous 전달 위한 Kubernetes 사용하여 ArgoCD 또는 Flux CD, 다음 OpenGitOps 원칙.

## 때 에 Use This Skill

- 세트 up GitOps 위한 Kubernetes 클러스터
- Automate 애플리케이션 deployments 에서 Git
- Implement progressive 전달 strategies
- Manage multi-클러스터 deployments
- Configure 자동화된 동기 정책
- 세트 up secret 관리 에서 GitOps

## OpenGitOps 원칙

1. **Declarative** - Entire 시스템 설명된 declaratively
2. **Versioned 및 불변** - 원하는 상태 저장됨 에서 Git
3. **Pulled Automatically** - 소프트웨어 에이전트 pull 원하는 상태
4. **지속적으로 Reconciled** - 에이전트 reconcile actual vs 원하는 상태

## ArgoCD 설정

### 1. Installation

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**참조:** See `references/argocd-setup.md` 위한 상세한 설정

### 2. 저장소 구조

```
gitops-repo/
├── apps/
│   ├── production/
│   │   ├── app1/
│   │   │   ├── kustomization.yaml
│   │   │   └── deployment.yaml
│   │   └── app2/
│   └── staging/
├── infrastructure/
│   ├── ingress-nginx/
│   ├── cert-manager/
│   └── monitoring/
└── argocd/
    ├── applications/
    └── projects/
```

### 3. Create 애플리케이션

```yaml
# argocd/applications/my-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: apps/production/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### 4. App of Apps 패턴

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: applications
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: argocd/applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated: {}
```

## Flux CD 설정

### 1. Installation

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux
flux bootstrap github \
  --owner=org \
  --repository=gitops-repo \
  --branch=main \
  --path=clusters/production \
  --personal
```

### 2. Create GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/my-app
  ref:
    branch: main
```

### 3. Create Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./deploy
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app
```

## 동기 정책

### Auto-동기 구성

**ArgoCD:**
```yaml
syncPolicy:
  automated:
    prune: true      # Delete resources not in Git
    selfHeal: true   # Reconcile manual changes
    allowEmpty: false
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

**Flux:**
```yaml
spec:
  interval: 1m
  prune: true
  wait: true
  timeout: 5m
```

**참조:** See `references/sync-policies.md`

## Progressive 전달

### Canary 배포 와 함께 ArgoCD Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 1m}
      - setWeight: 50
      - pause: {duration: 2m}
      - setWeight: 100
```

### Blue-Green 배포

```yaml
strategy:
  blueGreen:
    activeService: my-app
    previewService: my-app-preview
    autoPromotionEnabled: false
```

## Secret 관리

### 외부 Secrets 운영자

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: prod/db/password
```

### Sealed Secrets

```bash
# Encrypt secret
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Commit sealed-secret.yaml to Git
```

## 최선의 관행

1. **Use 별도 repos 또는 branches** 위한 다른 환경
2. **Implement RBAC** 위한 Git repositories
3. **Enable 알림** 위한 동기 실패
4. **Use health 확인합니다** 위한 사용자 정의 리소스
5. **Implement approval gates** 위한 production
6. **Keep secrets out of Git** (use 외부 Secrets)
7. **Use App of Apps 패턴** 위한 조직
8. **Tag 릴리스** 위한 쉬운 롤백
9. **모니터 동기 상태** 와 함께 경고
10. **Test 변경합니다** 에서 staging 첫 번째

## 문제 해결

**동기 실패:**
```bash
argocd app get my-app
argocd app sync my-app --prune
```

**Out of 동기 상태:**
```bash
argocd app diff my-app
argocd app sync my-app --force
```

## 관련됨 Skills

- `k8s-manifest-generator` - 위한 생성하는 manifests
- `helm-chart-scaffolding` - 위한 패키징 애플리케이션
