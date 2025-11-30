---
name: k8s-manifest-generator
description: Create 프로덕션 준비 완료 Kubernetes manifests 위한 Deployments, 서비스, ConfigMaps, 및 Secrets 다음 최선의 관행 및 security 표준. Use 때 generating Kubernetes YAML manifests, 생성하는 K8s 리소스, 또는 implementing production-grade Kubernetes configurations.
---

# Kubernetes 매니페스트 생성기

단계-에 의해-단계 guidance 위한 생성하는 프로덕션 준비 완료 Kubernetes manifests 포함하여 Deployments, 서비스, ConfigMaps, Secrets, 및 PersistentVolumeClaims.

## Purpose

This skill 제공합니다 포괄적인 guidance 위한 generating well-구조화된, secure, 및 프로덕션 준비 완료 Kubernetes manifests 다음 클라우드 네이티브 최선의 관행 및 Kubernetes 규약.

## 때 에 Use This Skill

Use this skill 때 you need 에:
- Create 새로운 Kubernetes 배포 manifests
- Define 서비스 리소스 위한 네트워크 connectivity
- Generate ConfigMap 및 Secret 리소스 위한 구성 관리
- Create PersistentVolumeClaim manifests 위한 stateful workloads
- Follow Kubernetes 최선의 관행 및 naming 규약
- Implement 리소스 제한합니다, health 확인합니다, 및 security contexts
- 설계 manifests 위한 multi-환경 deployments

## 단계-에 의해-단계 워크플로우

### 1. Gather 요구사항

**Understand the workload:**
- 애플리케이션 유형 (stateless/stateful)
- 컨테이너 image 및 버전
- 환경 변수 및 구성 needs
- 스토리지 요구사항
- 네트워크 exposure 요구사항 (내부/외부)
- 리소스 요구사항 (CPU, 메모리)
- 확장 요구사항
- Health check 엔드포인트

**Questions 에 ask:**
- 무엇 is the 애플리케이션 name 및 purpose?
- 무엇 컨테이너 image 및 tag will be used?
- Does the 애플리케이션 need 영구적 스토리지?
- 무엇 ports does the 애플리케이션 expose?
- Are there 어떤 secrets 또는 구성 파일 필요한?
- 무엇 are the CPU 및 메모리 요구사항?
- Does the 애플리케이션 need 에 be 노출된 externally?

### 2. Create 배포 매니페스트

**Follow this 구조:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
    version: <version>
spec:
  replicas: 3
  selector:
    matchLabels:
      app: <app-name>
  template:
    metadata:
      labels:
        app: <app-name>
        version: <version>
    spec:
      containers:
      - name: <container-name>
        image: <image>:<tag>
        ports:
        - containerPort: <port>
          name: http
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: ENV_VAR
          value: "value"
        envFrom:
        - configMapRef:
            name: <app-name>-config
        - secretRef:
            name: <app-name>-secret
```

**최선의 관행 에 apply:**
- 항상 세트 리소스 요청 및 제한합니다
- Implement 둘 다 liveness 및 readiness probes
- Use 특정 image 태그합니다 (절대 ~하지 않음 `:latest`)
- Apply security 컨텍스트 위한 non-근 사용자
- Use 라벨링합니다 위한 조직 및 선택
- 세트 적절한 replica 개수 based 에 가용성 needs

**참조:** See `references/deployment-spec.md` 위한 상세한 배포 options

### 3. Create 서비스 매니페스트

**Choose the 적절한 서비스 유형:**

**ClusterIP (내부 오직):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
spec:
  type: ClusterIP
  selector:
    app: <app-name>
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
```

**LoadBalancer (외부 access):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app-name>
  namespace: <namespace>
  labels:
    app: <app-name>
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: LoadBalancer
  selector:
    app: <app-name>
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
```

**참조:** See `references/service-spec.md` 위한 서비스 유형 및 networking

### 4. Create ConfigMap

**위한 애플리케이션 구성:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: <app-name>-config
  namespace: <namespace>
data:
  APP_MODE: production
  LOG_LEVEL: info
  DATABASE_HOST: db.example.com
  # For config files
  app.properties: |
    server.port=8080
    server.host=0.0.0.0
    logging.level=INFO
```

**최선의 관행:**
- Use ConfigMaps 위한 non-sensitive 데이터 오직
- Organize 관련됨 구성 together
- Use 의미 있는 names 위한 키
- Consider 사용하여 one ConfigMap per 컴포넌트
- 버전 ConfigMaps 때 making 변경합니다

**참조:** See `assets/configmap-template.yaml` 위한 예제

### 5. Create Secret

**위한 sensitive 데이터:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: <app-name>-secret
  namespace: <namespace>
type: Opaque
stringData:
  DATABASE_PASSWORD: "changeme"
  API_KEY: "secret-api-key"
  # For certificate files
  tls.crt: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
  tls.key: |
    -----BEGIN PRIVATE KEY-----
    ...
    -----END PRIVATE KEY-----
```

**Security considerations:**
- 절대 ~하지 않음 커밋 secrets 에 Git 에서 plain text
- Use Sealed Secrets, 외부 Secrets 운영자, 또는 Vault
- Rotate secrets 정기적으로
- Use RBAC 에 limit secret access
- Consider 사용하여 Secret 유형: `kubernetes.io/tls` 위한 TLS secrets

### 6. Create PersistentVolumeClaim (만약 필요한)

**위한 stateful 애플리케이션:**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: <app-name>-data
  namespace: <namespace>
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: gp3
  resources:
    requests:
      storage: 10Gi
```

**Mount 에서 배포:**
```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        volumeMounts:
        - name: data
          mountPath: /var/lib/app
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: <app-name>-data
```

**스토리지 considerations:**
- Choose 적절한 StorageClass 위한 성능 needs
- Use ReadWriteOnce 위한 single-pod access
- Use ReadWriteMany 위한 multi-pod shared 스토리지
- Consider 백업 strategies
- 세트 적절한 retention 정책

### 7. Apply Security 최선의 관행

**Add security 컨텍스트 에 배포:**

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: app
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
```

**Security checklist:**
- [ ] Run 처럼 non-근 사용자
- [ ] Drop 모든 역량
- [ ] Use 읽은-오직 근 filesystem
- [ ] Disable privilege escalation
- [ ] 세트 seccomp 프로필
- [ ] Use Pod Security 표준

### 8. Add 라벨링합니다 및 Annotations

**표준 라벨링합니다 (권장됨):**

```yaml
metadata:
  labels:
    app.kubernetes.io/name: <app-name>
    app.kubernetes.io/instance: <instance-name>
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: <system-name>
    app.kubernetes.io/managed-by: kubectl
```

**Useful annotations:**

```yaml
metadata:
  annotations:
    description: "Application description"
    contact: "team@example.com"
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
```

### 9. Organize Multi-리소스 Manifests

**파일 조직 options:**

**Option 1: Single 파일 와 함께 `---` separator**
```yaml
# app-name.yaml
---
apiVersion: v1
kind: ConfigMap
...
---
apiVersion: v1
kind: Secret
...
---
apiVersion: apps/v1
kind: Deployment
...
---
apiVersion: v1
kind: Service
...
```

**Option 2: 별도 파일**
```
manifests/
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
├── service.yaml
└── pvc.yaml
```

**Option 3: Kustomize 구조**
```
base/
├── kustomization.yaml
├── deployment.yaml
├── service.yaml
└── configmap.yaml
overlays/
├── dev/
│   └── kustomization.yaml
└── prod/
    └── kustomization.yaml
```

### 10. Validate 및 Test

**검증 steps:**

```bash
# Dry-run validation
kubectl apply -f manifest.yaml --dry-run=client

# Server-side validation
kubectl apply -f manifest.yaml --dry-run=server

# Validate with kubeval
kubeval manifest.yaml

# Validate with kube-score
kube-score score manifest.yaml

# Check with kube-linter
kube-linter lint manifest.yaml
```

**테스트 checklist:**
- [ ] 매니페스트 passes dry-run 검증
- [ ] 모든 필수 필드 are 현재
- [ ] 리소스 제한합니다 are 합리적인
- [ ] Health 확인합니다 are 구성된
- [ ] Security 컨텍스트 is 세트
- [ ] 라벨링합니다 follow 규약
- [ ] Namespace exists 또는 is 생성된

## 일반적인 패턴

### 패턴 1: 간단한 Stateless Web 애플리케이션

**Use case:** 표준 web API 또는 microservice

**컴포넌트 필요한:**
- 배포 (3 replicas 위한 HA)
- ClusterIP 서비스
- ConfigMap 위한 구성
- Secret 위한 API 키
- HorizontalPodAutoscaler (선택적)

**참조:** See `assets/deployment-template.yaml`

### 패턴 2: Stateful 데이터베이스 애플리케이션

**Use case:** 데이터베이스 또는 영구적 스토리지 애플리케이션

**컴포넌트 필요한:**
- StatefulSet (not 배포)
- Headless 서비스
- PersistentVolumeClaim 템플릿
- ConfigMap 위한 DB 구성
- Secret 위한 자격 증명

### 패턴 3: Background 작업 또는 Cron

**Use case:** 예약됨 tasks 또는 batch 처리

**컴포넌트 필요한:**
- CronJob 또는 작업
- ConfigMap 위한 작업 매개변수
- Secret 위한 자격 증명
- ServiceAccount 와 함께 RBAC

### 패턴 4: Multi-컨테이너 Pod

**Use case:** 애플리케이션 와 함께 sidecar 컨테이너

**컴포넌트 필요한:**
- 배포 와 함께 여러 컨테이너
- Shared volumes 사이 컨테이너
- Init 컨테이너 위한 설정
- 서비스 (만약 필요한)

## 템플릿

The 다음 템플릿 are 사용 가능한 에서 the `assets/` 디렉터리:

- `deployment-template.yaml` - 표준 배포 와 함께 최선의 관행
- `service-template.yaml` - 서비스 configurations (ClusterIP, LoadBalancer, NodePort)
- `configmap-template.yaml` - ConfigMap 예제 와 함께 다른 데이터 유형
- `secret-template.yaml` - Secret 예제 (에 be 생성된, not committed)
- `pvc-template.yaml` - PersistentVolumeClaim 템플릿

## 참조 문서화

- `references/deployment-spec.md` - 상세한 배포 사양
- `references/service-spec.md` - 서비스 유형 및 networking details

## 최선의 관행 Summary

1. **항상 세트 리소스 요청 및 제한합니다** - 방지합니다 리소스 starvation
2. **Implement health 확인합니다** - 보장합니다 Kubernetes can manage your 애플리케이션
3. **Use 특정 image 태그합니다** - Avoid unpredictable deployments
4. **Apply security contexts** - Run 처럼 non-근, drop 역량
5. **Use ConfigMaps 및 Secrets** - 별도 config 에서 코드
6. **Label everything** - 가능하게 합니다 필터링 및 조직
7. **Follow naming 규약** - Use 표준 Kubernetes 라벨링합니다
8. **Validate 이전 applying** - Use dry-run 및 검증 tools
9. **버전 your manifests** - Keep 에서 Git 와 함께 버전 control
10. **Document 와 함께 annotations** - Add 컨텍스트 위한 other developers

## 문제 해결

**Pods not 시작하는:**
- Check image pull 오류: `kubectl describe pod <pod-name>`
- Verify 리소스 가용성: `kubectl get nodes`
- Check 이벤트: `kubectl get events --sort-by='.lastTimestamp'`

**서비스 not 접근 가능한:**
- Verify selector 일치합니다 pod 라벨링합니다: `kubectl get endpoints <service-name>`
- Check 서비스 유형 및 port 구성
- Test 에서 내에 클러스터: `kubectl run debug --rm -it --image=busybox -- sh`

**ConfigMap/Secret not 로드:**
- Verify names match 에서 배포
- Check namespace
- Ensure 리소스 exist: `kubectl get configmap,secret`

## 다음 Steps

이후 생성하는 manifests:
1. Store 에서 Git 저장소
2. 세트 up CI/CD 파이프라인 위한 배포
3. Consider 사용하여 Helm 또는 Kustomize 위한 templating
4. Implement GitOps 와 함께 ArgoCD 또는 Flux
5. Add 모니터링 및 observability

## 관련됨 Skills

- `helm-chart-scaffolding` - 위한 templating 및 패키징
- `gitops-workflow` - 위한 자동화된 deployments
- `k8s-security-policies` - 위한 고급 security configurations
