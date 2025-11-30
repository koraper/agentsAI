---
name: helm-chart-scaffolding
description: 설계, organize, 및 manage Helm 차트 위한 templating 및 패키징 Kubernetes 애플리케이션 와 함께 reusable configurations. Use 때 생성하는 Helm 차트, 패키징 Kubernetes 애플리케이션, 또는 implementing templated deployments.
---

# Helm 차트 Scaffolding

포괄적인 guidance 위한 생성하는, organizing, 및 managing Helm 차트 위한 패키징 및 deploying Kubernetes 애플리케이션.

## Purpose

This skill 제공합니다 단계-에 의해-단계 지시사항 위한 구축 프로덕션 준비 완료 Helm 차트, 포함하여 차트 구조, templating 패턴, 값 관리, 및 검증 strategies.

## 때 에 Use This Skill

Use this skill 때 you need 에:
- Create 새로운 Helm 차트 에서 scratch
- 패키지 Kubernetes 애플리케이션 위한 배포
- Manage multi-환경 deployments 와 함께 Helm
- Implement templating 위한 reusable Kubernetes manifests
- 세트 up Helm 차트 repositories
- Follow Helm 최선의 관행 및 규약

## Helm Overview

**Helm** is the 패키지 manager 위한 Kubernetes 것:
- 템플릿 Kubernetes manifests 위한 reusability
- 관리합니다 애플리케이션 릴리스 및 rollbacks
- 처리합니다 종속성 사이 차트
- 제공합니다 버전 control 위한 deployments
- 단순화합니다 구성 관리 전반에 걸쳐 환경

## 단계-에 의해-단계 워크플로우

### 1. Initialize 차트 구조

**Create 새로운 차트:**
```bash
helm create my-app
```

**표준 차트 구조:**
```
my-app/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration values
├── charts/              # Chart dependencies
├── templates/           # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install notes
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   └── tests/
│       └── test-connection.yaml
└── .helmignore         # Files to ignore
```

### 2. Configure 차트.yaml

**차트 메타데이터 정의합니다 the 패키지:**

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for My Application
type: application
version: 1.0.0      # Chart version
appVersion: "2.1.0" # Application version

# Keywords for chart discovery
keywords:
  - web
  - api
  - backend

# Maintainer information
maintainers:
  - name: DevOps Team
    email: devops@example.com
    url: https://github.com/example/my-app

# Source code repository
sources:
  - https://github.com/example/my-app

# Homepage
home: https://example.com

# Chart icon
icon: https://example.com/icon.png

# Dependencies
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
  - name: redis
    version: "17.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

**참조:** See `assets/Chart.yaml.template` 위한 완전한 예제

### 3. 설계 값.yaml 구조

**Organize 값 hierarchically:**

```yaml
# Image configuration
image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

# Number of replicas
replicaCount: 3

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8080

# Ingress configuration
ingress:
  enabled: false
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

# Resources
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

# Autoscaling
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

# Environment variables
env:
  - name: LOG_LEVEL
    value: "info"

# ConfigMap data
configMap:
  data:
    APP_MODE: production

# Dependencies
postgresql:
  enabled: true
  auth:
    database: myapp
    username: myapp

redis:
  enabled: false
```

**참조:** See `assets/values.yaml.template` 위한 완전한 구조

### 4. Create 템플릿 파일

**Use Go templating 와 함께 Helm 함수:**

**템플릿/배포.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        env:
          {{- toYaml .Values.env | nindent 12 }}
```

### 5. Create 템플릿 Helpers

**템플릿/_helpers.tpl:**
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-app.labels" -}}
helm.sh/chart: {{ include "my-app.chart" . }}
{{ include "my-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### 6. Manage 종속성

**Add 종속성 에서 차트.yaml:**
```yaml
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

**업데이트 종속성:**
```bash
helm dependency update
helm dependency build
```

**Override 종속성 값:**
```yaml
# values.yaml
postgresql:
  enabled: true
  auth:
    database: myapp
    username: myapp
    password: changeme
  primary:
    persistence:
      enabled: true
      size: 10Gi
```

### 7. Test 및 Validate

**검증 명령:**
```bash
# Lint the chart
helm lint my-app/

# Dry-run installation
helm install my-app ./my-app --dry-run --debug

# Template rendering
helm template my-app ./my-app

# Template with values
helm template my-app ./my-app -f values-prod.yaml

# Show computed values
helm show values ./my-app
```

**검증 스크립트:**
```bash
#!/bin/bash
set -e

echo "Linting chart..."
helm lint .

echo "Testing template rendering..."
helm template test-release . --dry-run

echo "Checking for required values..."
helm template test-release . --validate

echo "All validations passed!"
```

**참조:** See `scripts/validate-chart.sh`

### 8. 패키지 및 Distribute

**패키지 the 차트:**
```bash
helm package my-app/
# Creates: my-app-1.0.0.tgz
```

**Create 차트 저장소:**
```bash
# Create index
helm repo index .

# Upload to repository
# AWS S3 example
aws s3 sync . s3://my-helm-charts/ --exclude "*" --include "*.tgz" --include "index.yaml"
```

**Use the 차트:**
```bash
helm repo add my-repo https://charts.example.com
helm repo update
helm install my-app my-repo/my-app
```

### 9. Multi-환경 구성

**환경-특정 값 파일:**

```
my-app/
├── values.yaml          # Defaults
├── values-dev.yaml      # Development
├── values-staging.yaml  # Staging
└── values-prod.yaml     # Production
```

**값-prod.yaml:**
```yaml
replicaCount: 5

image:
  tag: "2.1.0"

resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20

ingress:
  enabled: true
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix

postgresql:
  enabled: true
  primary:
    persistence:
      size: 100Gi
```

**Install 와 함께 환경:**
```bash
helm install my-app ./my-app -f values-prod.yaml --namespace production
```

### 10. Implement Hooks 및 테스트합니다

**Pre-install hook:**
```yaml
# templates/pre-install-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "my-app.fullname" . }}-db-setup
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
      - name: db-setup
        image: postgres:15
        command: ["psql", "-c", "CREATE DATABASE myapp"]
      restartPolicy: Never
```

**Test 연결:**
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
  - name: wget
    image: busybox
    command: ['wget']
    args: ['{{ include "my-app.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

**Run 테스트합니다:**
```bash
helm test my-app
```

## 일반적인 패턴

### 패턴 1: Conditional 리소스

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "my-app.fullname" . }}
spec:
  # ...
{{- end }}
```

### 패턴 2: Iterating Over 목록

```yaml
env:
{{- range .Values.env }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}
```

### 패턴 3: 포함하여 파일

```yaml
data:
  config.yaml: |
    {{- .Files.Get "config/application.yaml" | nindent 4 }}
```

### 패턴 4: 전역 값

```yaml
global:
  imageRegistry: docker.io
  imagePullSecrets:
    - name: regcred

# Use in templates:
image: {{ .Values.global.imageRegistry }}/{{ .Values.image.repository }}
```

## 최선의 관행

1. **Use semantic versioning** 위한 차트 및 app 버전
2. **Document 모든 값** 에서 값.yaml 와 함께 comments
3. **Use 템플릿 helpers** 위한 반복된 logic
4. **Validate 차트** 이전 패키징
5. **Pin 종속성 버전** 명시적으로
6. **Use conditions** 위한 선택적 리소스
7. **Follow naming 규약** (lowercase, hyphens)
8. **Include NOTES.txt** 와 함께 usage 지시사항
9. **Add 라벨링합니다** consistently 사용하여 helpers
10. **Test installations** 에서 모든 환경

## 문제 해결

**템플릿 렌더링 오류:**
```bash
helm template my-app ./my-app --debug
```

**종속성 이슈:**
```bash
helm dependency update
helm dependency list
```

**Installation 실패:**
```bash
helm install my-app ./my-app --dry-run --debug
kubectl get events --sort-by='.lastTimestamp'
```

## 참조 파일

- `assets/Chart.yaml.template` - 차트 메타데이터 템플릿
- `assets/values.yaml.template` - 값 구조 템플릿
- `scripts/validate-chart.sh` - 검증 스크립트
- `references/chart-structure.md` - 상세한 차트 조직

## 관련됨 Skills

- `k8s-manifest-generator` - 위한 생성하는 밑 Kubernetes manifests
- `gitops-workflow` - 위한 자동화된 Helm 차트 deployments
