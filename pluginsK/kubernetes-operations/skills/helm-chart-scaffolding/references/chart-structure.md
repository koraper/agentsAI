# Helm 차트 구조 참조

완전한 가이드 에 Helm 차트 조직, 파일 규약, 및 최선의 관행.

## 표준 차트 디렉터리 구조

```
my-app/
├── Chart.yaml              # Chart metadata (required)
├── Chart.lock              # Dependency lock file (generated)
├── values.yaml             # Default configuration values (required)
├── values.schema.json      # JSON schema for values validation
├── .helmignore             # Patterns to ignore when packaging
├── README.md               # Chart documentation
├── LICENSE                 # Chart license
├── charts/                 # Chart dependencies (bundled)
│   └── postgresql-12.0.0.tgz
├── crds/                   # Custom Resource Definitions
│   └── my-crd.yaml
├── templates/              # Kubernetes manifest templates (required)
│   ├── NOTES.txt          # Post-install instructions
│   ├── _helpers.tpl       # Template helper functions
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml
│   ├── networkpolicy.yaml
│   └── tests/
│       └── test-connection.yaml
└── files/                  # Additional files to include
    └── config/
        └── app.conf
```

## 차트.yaml 사양

### API 버전 v2 (Helm 3+)

```yaml
apiVersion: v2                    # Required: API version
name: my-application              # Required: Chart name
version: 1.2.3                    # Required: Chart version (SemVer)
appVersion: "2.5.0"              # Application version
description: A Helm chart for my application  # Required
type: application                 # Chart type: application or library
keywords:                         # Search keywords
  - web
  - api
  - backend
home: https://example.com         # Project home page
sources:                          # Source code URLs
  - https://github.com/example/my-app
maintainers:                      # Maintainer list
  - name: John Doe
    email: john@example.com
    url: https://github.com/johndoe
icon: https://example.com/icon.png  # Chart icon URL
kubeVersion: ">=1.24.0"          # Compatible Kubernetes versions
deprecated: false                 # Mark chart as deprecated
annotations:                      # Arbitrary annotations
  example.com/release-notes: https://example.com/releases/v1.2.3
dependencies:                     # Chart dependencies
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
    tags:
      - database
    import-values:
      - child: database
        parent: database
    alias: db
```

## 차트 유형

### 애플리케이션 차트
```yaml
type: application
```
- 표준 Kubernetes 애플리케이션
- Can be installed 및 관리형
- Contains 템플릿 위한 K8s 리소스

### 라이브러리 차트
```yaml
type: library
```
- Shared 템플릿 helpers
- Cannot be installed 직접
- Used 처럼 종속성 에 의해 other 차트
- 아니요 템플릿/ 디렉터리

## 값 파일 조직

### 값.yaml (defaults)
```yaml
# Global values (shared with subcharts)
global:
  imageRegistry: docker.io
  imagePullSecrets: []

# Image configuration
image:
  registry: docker.io
  repository: myapp/web
  tag: ""  # Defaults to .Chart.AppVersion
  pullPolicy: IfNotPresent

# Deployment settings
replicaCount: 1
revisionHistoryLimit: 10

# Pod configuration
podAnnotations: {}
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# Container security
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
    - ALL

# Service
service:
  type: ClusterIP
  port: 80
  targetPort: http
  annotations: {}

# Resources
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

# Autoscaling
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80

# Node selection
nodeSelector: {}
tolerations: []
affinity: {}

# Monitoring
serviceMonitor:
  enabled: false
  interval: 30s
```

### 값.스키마.json (검증)
```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1
    },
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": {
          "type": "string"
        },
        "tag": {
          "type": "string"
        },
        "pullPolicy": {
          "type": "string",
          "enum": ["Always", "IfNotPresent", "Never"]
        }
      }
    }
  },
  "required": ["image"]
}
```

## 템플릿 파일

### 템플릿 Naming 규약

- **Lowercase 와 함께 hyphens**: `deployment.yaml`, `service-account.yaml`
- **부분 템플릿**: Prefix 와 함께 underscore `_helpers.tpl`
- **테스트합니다**: 장소 에서 `templates/tests/`
- **CRDs**: 장소 에서 `crds/` (not templated)

### 일반적인 템플릿

#### _helpers.tpl
```yaml
{{/*
Standard naming helpers
*/}}
{{- define "my-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "my-app.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "my-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

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
{{- end -}}

{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Image name helper
*/}}
{{- define "my-app.image" -}}
{{- $registry := .Values.global.imageRegistry | default .Values.image.registry -}}
{{- $repository := .Values.image.repository -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion -}}
{{- printf "%s/%s:%s" $registry $repository $tag -}}
{{- end -}}
```

#### NOTES.txt
```
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}

{{- if .Values.ingress.enabled }}

Application URL:
{{- range .Values.ingress.hosts }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ .host }}{{ .path }}
{{- end }}
{{- else }}

Get the application URL by running:
  export POD_NAME=$(kubectl get pods --namespace {{ .Release.Namespace }} -l "app.kubernetes.io/name={{ include "my-app.name" . }}" -o jsonpath="{.items[0].metadata.name}")
  kubectl port-forward $POD_NAME 8080:80
  echo "Visit http://127.0.0.1:8080"
{{- end }}
```

## 종속성 관리

### Declaring 종속성

```yaml
# Chart.yaml
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled  # Enable/disable via values
    tags:                          # Group dependencies
      - database
    import-values:                 # Import values from subchart
      - child: database
        parent: database
    alias: db                      # Reference as .Values.db
```

### Managing 종속성

```bash
# Update dependencies
helm dependency update

# List dependencies
helm dependency list

# Build dependencies
helm dependency build
```

### 차트.잠금

생성된 automatically 에 의해 `helm dependency update`:

```yaml
dependencies:
- name: postgresql
  repository: https://charts.bitnami.com/bitnami
  version: 12.0.0
digest: sha256:abcd1234...
generated: "2024-01-01T00:00:00Z"
```

## .helmignore

Exclude 파일 에서 차트 패키지:

```
# Development files
.git/
.gitignore
*.md
docs/

# Build artifacts
*.swp
*.bak
*.tmp
*.orig

# CI/CD
.travis.yml
.gitlab-ci.yml
Jenkinsfile

# Testing
test/
*.test

# IDE
.vscode/
.idea/
*.iml
```

## 사용자 정의 리소스 Definitions (CRDs)

장소 CRDs 에서 `crds/` 디렉터리:

```
crds/
├── my-app-crd.yaml
└── another-crd.yaml
```

**중요한 CRD notes:**
- CRDs are installed 이전 어떤 템플릿
- CRDs are NOT templated (아니요 `{{ }}` 구문)
- CRDs are NOT 업그레이드된 또는 deleted 와 함께 차트
- Use `helm install --skip-crds` 에 skip installation

## 차트 Versioning

### Semantic Versioning

- **차트 버전**: Increment 때 차트 변경합니다
  - 주요: Breaking 변경합니다
  - 부수적: 새로운 기능, 뒤로 호환되는
  - PATCH: 버그 수정합니다

- **App 버전**: 애플리케이션 버전 being 배포된
  - Can be 어떤 string
  - Not 필수 에 follow SemVer

```yaml
version: 2.3.1      # Chart version
appVersion: "1.5.0" # Application version
```

## 차트 테스트

### Test 파일

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "my-app.fullname" . }}-test-connection"
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  containers:
  - name: wget
    image: busybox
    command: ['wget']
    args: ['{{ include "my-app.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

### 실행 중 테스트합니다

```bash
helm test my-release
helm test my-release --logs
```

## Hooks

Helm hooks allow intervention 에서 특정 points:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "my-app.fullname" . }}-migration
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
```

### Hook 유형

- `pre-install`: 이전 템플릿 렌더링된
- `post-install`: 이후 모든 리소스 로드된
- `pre-delete`: 이전 어떤 리소스 deleted
- `post-delete`: 이후 모든 리소스 deleted
- `pre-upgrade`: 이전 업그레이드
- `post-upgrade`: 이후 업그레이드
- `pre-rollback`: 이전 롤백
- `post-rollback`: 이후 롤백
- `test`: Run 와 함께 `helm test`

### Hook Weight

제어합니다 hook 실행 순서 (-5 에 5, lower 실행합니다 첫 번째)

### Hook Deletion 정책

- `before-hook-creation`: Delete 이전 hook 이전 새로운 one
- `hook-succeeded`: Delete 이후 성공한 실행
- `hook-failed`: Delete 만약 hook fails

## 최선의 관행

1. **Use helpers** 위한 반복된 템플릿 logic
2. **Quote strings** 에서 템플릿: `{{ .Values.name | quote }}`
3. **Validate 값** 와 함께 값.스키마.json
4. **Document 모든 값** 에서 값.yaml
5. **Use semantic versioning** 위한 차트 버전
6. **Pin 종속성 버전** 정확하게
7. **Include NOTES.txt** 와 함께 usage 지시사항
8. **Add 테스트합니다** 위한 긴급 기능
9. **Use hooks** 위한 데이터베이스 migrations
10. **Keep 차트 focused** - one 애플리케이션 per 차트

## 차트 저장소 구조

```
helm-charts/
├── index.yaml
├── my-app-1.0.0.tgz
├── my-app-1.1.0.tgz
├── my-app-1.2.0.tgz
└── another-chart-2.0.0.tgz
```

### 생성하는 저장소 인덱스

```bash
helm repo index . --url https://charts.example.com
```

## 관련됨 리소스

- [Helm Documentation](__URL0__)
- [Chart Template Guide](__URL0__)
- [Best Practices](__URL0__)
