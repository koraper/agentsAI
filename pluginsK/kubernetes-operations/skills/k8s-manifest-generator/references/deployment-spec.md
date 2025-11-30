# Kubernetes 배포 사양 참조

포괄적인 참조 위한 Kubernetes 배포 리소스, covering 모든 키 필드, 최선의 관행, 및 일반적인 패턴.

## Overview

A 배포 제공합니다 declarative 업데이트합니다 위한 Pods 및 ReplicaSets. It 관리합니다 the 원하는 상태 of your 애플리케이션, 처리 rollouts, rollbacks, 및 확장 작업.

## 완전한 배포 사양

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: my-system
  annotations:
    description: "Main application deployment"
    contact: "backend-team@example.com"
spec:
  # Replica management
  replicas: 3
  revisionHistoryLimit: 10

  # Pod selection
  selector:
    matchLabels:
      app: my-app
      version: v1

  # Update strategy
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  # Minimum time for pod to be ready
  minReadySeconds: 10

  # Deployment will fail if it doesn't progress in this time
  progressDeadlineSeconds: 600

  # Pod template
  template:
    metadata:
      labels:
        app: my-app
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
    spec:
      # Service account for RBAC
      serviceAccountName: my-app

      # Security context for the pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      # Init containers run before main containers
      initContainers:
      - name: init-db
        image: busybox:1.36
        command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 1; done']
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 1000

      # Main containers
      containers:
      - name: app
        image: myapp:1.0.0
        imagePullPolicy: IfNotPresent

        # Container ports
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP

        # Environment variables
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url

        # ConfigMap and Secret references
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets

        # Resource requests and limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Liveness probe
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
            httpHeaders:
            - name: Custom-Header
              value: Awesome
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3

        # Readiness probe
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        # Startup probe (for slow-starting containers)
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 10
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 30

        # Volume mounts
        volumeMounts:
        - name: data
          mountPath: /var/lib/app
        - name: config
          mountPath: /etc/app
          readOnly: true
        - name: tmp
          mountPath: /tmp

        # Security context for container
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          capabilities:
            drop:
            - ALL

        # Lifecycle hooks
        lifecycle:
          postStart:
            exec:
              command: ["/bin/sh", "-c", "echo Container started > /tmp/started"]
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

      # Volumes
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: app-data
      - name: config
        configMap:
          name: app-config
      - name: tmp
        emptyDir: {}

      # DNS configuration
      dnsPolicy: ClusterFirst
      dnsConfig:
        options:
        - name: ndots
          value: "2"

      # Scheduling
      nodeSelector:
        disktype: ssd

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - my-app
              topologyKey: kubernetes.io/hostname

      tolerations:
      - key: "app"
        operator: "Equal"
        value: "my-app"
        effect: "NoSchedule"

      # Termination
      terminationGracePeriodSeconds: 30

      # Image pull secrets
      imagePullSecrets:
      - name: regcred
```

## 분야 참조

### 메타데이터 필드

#### 필수 필드
- `apiVersion`: `apps/v1` (현재 안정적인 버전)
- `kind`: `Deployment`
- `metadata.name`: 고유한 name 내에 namespace

#### 권장됨 메타데이터
- `metadata.namespace`: Target namespace (defaults 에 `default`)
- `metadata.labels`: 키-값 쌍 위한 조직
- `metadata.annotations`: Non-identifying 메타데이터

### Spec 필드

#### Replica 관리

**`replicas`** (정수, default: 1)
- 숫자 of 원하는 pod 인스턴스
- 최선의 관행: Use 3+ 위한 production high 가용성
- Can be 확장된 manually 또는 를 통해 HorizontalPodAutoscaler

**`revisionHistoryLimit`** (정수, default: 10)
- 숫자 of 오래된 ReplicaSets 에 retain 위한 롤백
- 세트 에 0 에 disable 롤백 역량
- 감소합니다 스토리지 overhead 위한 long-실행 중 deployments

#### 업데이트 전략

**`strategy.type`** (string)
- `RollingUpdate` (default): Gradual pod replacement
- `Recreate`: Delete 모든 pods 이전 생성하는 새로운 ones

**`strategy.rollingUpdate.maxSurge`** (int 또는 percent, default: 25%)
- Maximum pods above 원하는 replicas 동안 업데이트
- 예제: 와 함께 3 replicas 및 maxSurge=1, up 에 4 pods 동안 업데이트

**`strategy.rollingUpdate.maxUnavailable`** (int 또는 percent, default: 25%)
- Maximum pods below 원하는 replicas 동안 업데이트
- 세트 에 0 위한 zero-downtime deployments
- Cannot be 0 만약 maxSurge is 0

**최선의 관행:**
```yaml
# Zero-downtime deployment
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# Fast deployment (can have brief downtime)
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 2
    maxUnavailable: 1

# Complete replacement
strategy:
  type: Recreate
```

#### Pod 템플릿

**`template.metadata.labels`**
- Must include 라벨링합니다 일치하는 `spec.selector.matchLabels`
- Add 버전 라벨링합니다 위한 blue/green deployments
- Include 표준 Kubernetes 라벨링합니다

**`template.spec.containers`** (필수)
- 배열 of 컨테이너 사양
- 에서 least one 컨테이너 필수
- 각 컨테이너 needs 고유한 name

#### 컨테이너 구성

**Image 관리:**
```yaml
containers:
- name: app
  image: registry.example.com/myapp:1.0.0
  imagePullPolicy: IfNotPresent  # or Always, Never
```

Image pull 정책:
- `IfNotPresent`: Pull 만약 not 캐시됨 (default 위한 태그된 images)
- `Always`: 항상 pull (default 위한 :최신)
- `Never`: 절대 ~하지 않음 pull, fail 만약 not 캐시됨

**Port Declarations:**
```yaml
ports:
- name: http      # Named for referencing in Service
  containerPort: 8080
  protocol: TCP   # TCP (default), UDP, or SCTP
  hostPort: 8080  # Optional: Bind to host port (rarely used)
```

#### 리소스 관리

**요청 vs 제한합니다:**

```yaml
resources:
  requests:
    memory: "256Mi"  # Guaranteed resources
    cpu: "250m"      # 0.25 CPU cores
  limits:
    memory: "512Mi"  # Maximum allowed
    cpu: "500m"      # 0.5 CPU cores
```

**QoS 클래스 (결정된 automatically):**

1. **보증된**: 요청 = 제한합니다 위한 모든 컨테이너
   - Highest priority
   - 마지막 에 be evicted

2. **Burstable**: 요청 < 제한합니다 또는 오직 요청 세트
   - Medium priority
   - Evicted 이전 보증된

3. **BestEffort**: 아니요 요청 또는 제한합니다 세트
   - Lowest priority
   - 첫 번째 에 be evicted

**최선의 관행:**
- 항상 세트 요청 에서 production
- 세트 제한합니다 에 prevent 리소스 monopolization
- 메모리 제한합니다 should be 1.5-2x 요청
- CPU 제한합니다 can be higher 위한 bursty workloads

#### Health 확인합니다

**Probe 유형:**

1. **startupProbe** - 위한 slow-시작하는 애플리케이션
   ```yaml
   startupProbe:
     httpGet:
       path: /health/startup
       port: 8080
     initialDelaySeconds: 0
     periodSeconds: 10
     failureThreshold: 30  # 5 minutes to start (10s * 30)
   ```

2. **livenessProbe** - Restarts unhealthy 컨테이너
   ```yaml
   livenessProbe:
     httpGet:
       path: /health/live
       port: 8080
     initialDelaySeconds: 30
     periodSeconds: 10
     timeoutSeconds: 5
     failureThreshold: 3  # Restart after 3 failures
   ```

3. **readinessProbe** - 제어합니다 traffic 라우팅
   ```yaml
   readinessProbe:
     httpGet:
       path: /health/ready
       port: 8080
     initialDelaySeconds: 5
     periodSeconds: 5
     failureThreshold: 3  # Remove from service after 3 failures
   ```

**Probe Mechanisms:**

```yaml
# HTTP GET
httpGet:
  path: /health
  port: 8080
  httpHeaders:
  - name: Authorization
    value: Bearer token

# TCP Socket
tcpSocket:
  port: 3306

# Command execution
exec:
  command:
  - cat
  - /tmp/healthy

# gRPC (Kubernetes 1.24+)
grpc:
  port: 9090
  service: my.service.health.v1.Health
```

**Probe Timing 매개변수:**

- `initialDelaySeconds`: Wait 이전 첫 번째 probe
- `periodSeconds`: 어떻게 자주 에 probe
- `timeoutSeconds`: Probe 타임아웃
- `successThreshold`: Successes 필요한 에 마크 healthy (1 위한 liveness/startup)
- `failureThreshold`: 실패 이전 taking action

#### Security 컨텍스트

**Pod-레벨 security 컨텍스트:**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    fsGroupChangePolicy: OnRootMismatch
    seccompProfile:
      type: RuntimeDefault
```

**컨테이너-레벨 security 컨텍스트:**
```yaml
containers:
- name: app
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 1000
    capabilities:
      drop:
      - ALL
      add:
      - NET_BIND_SERVICE  # Only if needed
```

**Security 최선의 관행:**
- 항상 run 처럼 non-근 (`runAsNonRoot: true`)
- Drop 모든 역량 및 add 오직 필요한 ones
- Use 읽은-오직 근 filesystem 때 possible
- Enable seccomp 프로필
- Disable privilege escalation

#### Volumes

**볼륨 유형:**

```yaml
volumes:
# PersistentVolumeClaim
- name: data
  persistentVolumeClaim:
    claimName: app-data

# ConfigMap
- name: config
  configMap:
    name: app-config
    items:
    - key: app.properties
      path: application.properties

# Secret
- name: secrets
  secret:
    secretName: app-secrets
    defaultMode: 0400

# EmptyDir (ephemeral)
- name: cache
  emptyDir:
    sizeLimit: 1Gi

# HostPath (avoid in production)
- name: host-data
  hostPath:
    path: /data
    type: DirectoryOrCreate
```

#### 예약

**노드 선택:**

```yaml
# Simple node selector
nodeSelector:
  disktype: ssd
  zone: us-west-1a

# Node affinity (more expressive)
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/arch
          operator: In
          values:
          - amd64
          - arm64
```

**Pod Affinity/Anti-Affinity:**

```yaml
# Spread pods across nodes
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: my-app
      topologyKey: kubernetes.io/hostname

# Co-locate with database
affinity:
  podAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: database
        topologyKey: kubernetes.io/hostname
```

**Tolerations:**

```yaml
tolerations:
- key: "node.kubernetes.io/unreachable"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 30
- key: "dedicated"
  operator: "Equal"
  value: "database"
  effect: "NoSchedule"
```

## 일반적인 패턴

### High 가용성 배포

```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: my-app
            topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: my-app
```

### Sidecar 컨테이너 패턴

```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log
      - name: log-forwarder
        image: fluent-bit:2.0
        volumeMounts:
        - name: shared-logs
          mountPath: /var/log
          readOnly: true
      volumes:
      - name: shared-logs
        emptyDir: {}
```

### Init 컨테이너 위한 종속성

```yaml
spec:
  template:
    spec:
      initContainers:
      - name: wait-for-db
        image: busybox:1.36
        command:
        - sh
        - -c
        - |
          until nc -z database-service 5432; do
            echo "Waiting for database..."
            sleep 2
          done
      - name: run-migrations
        image: myapp:1.0.0
        command: ["./migrate", "up"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
      containers:
      - name: app
        image: myapp:1.0.0
```

## 최선의 관행

### Production Checklist

- [ ] 세트 리소스 요청 및 제한합니다
- [ ] Implement 모든 three probe 유형 (startup, liveness, readiness)
- [ ] Use 특정 image 태그합니다 (not :최신)
- [ ] Configure security 컨텍스트 (non-근, 읽은-오직 filesystem)
- [ ] 세트 replica 개수 >= 3 위한 HA
- [ ] Configure pod anti-affinity 위한 분산
- [ ] 세트 적절한 업데이트 전략 (maxUnavailable: 0 위한 zero-downtime)
- [ ] Use ConfigMaps 및 Secrets 위한 구성
- [ ] Add 표준 라벨링합니다 및 annotations
- [ ] Configure graceful shutdown (preStop hook, terminationGracePeriodSeconds)
- [ ] 세트 revisionHistoryLimit 위한 롤백 역량
- [ ] Use ServiceAccount 와 함께 최소 RBAC 권한

### 성능 Tuning

**Fast startup:**
```yaml
spec:
  minReadySeconds: 5
  strategy:
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**Zero-downtime 업데이트합니다:**
```yaml
spec:
  minReadySeconds: 10
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

**Graceful shutdown:**
```yaml
spec:
  template:
    spec:
      terminationGracePeriodSeconds: 60
      containers:
      - name: app
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15 && kill -SIGTERM 1"]
```

## 문제 해결

### 일반적인 이슈

**Pods not 시작하는:**
```bash
kubectl describe deployment <name>
kubectl get pods -l app=<app-name>
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**ImagePullBackOff:**
- Check image name 및 tag
- Verify imagePullSecrets
- Check 레지스트리 자격 증명

**CrashLoopBackOff:**
- Check 컨테이너 로깅합니다
- Verify liveness probe is not 또한 aggressive
- Check 리소스 제한합니다
- Verify 애플리케이션 종속성

**배포 stuck 에서 진행:**
- Check progressDeadlineSeconds
- Verify readiness probes
- Check 리소스 가용성

## 관련됨 리소스

- [Kubernetes Deployment API Reference](__URL0__)
- [Pod Security Standards](__URL0__)
- [Resource Management](__URL0__)
