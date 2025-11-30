# Kubernetes 서비스 사양 참조

포괄적인 참조 위한 Kubernetes 서비스 리소스, covering 서비스 유형, networking, load 균형, 및 서비스 발견 패턴.

## Overview

A 서비스 제공합니다 안정적인 네트워크 엔드포인트 위한 accessing Pods. 서비스 enable loose 결합 사이 microservices 에 의해 providing 서비스 발견 및 load 균형.

## 서비스 유형

### 1. ClusterIP (default)

노출합니다 the 서비스 에 an 내부 클러스터 IP. 오직 도달 가능한 에서 내에 the 클러스터.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  sessionAffinity: None
```

**Use cases:**
- 내부 microservice communication
- 데이터베이스 서비스
- 내부 APIs
- 메시지 대기열에 넣습니다

### 2. NodePort

노출합니다 the 서비스 에 각 노드's IP 에서 a 정적 port (30000-32767 범위).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - name: http
    port: 80
    targetPort: 8080
    nodePort: 30080  # Optional, auto-assigned if omitted
    protocol: TCP
```

**Use cases:**
- 개발/테스트 외부 access
- Small deployments 없이 load balancer
- 직접 노드 access 요구사항

**Limitations:**
- 제한된 port 범위 (30000-32767)
- Must handle 노드 실패
- 아니요 구축된-에서 load 균형 전반에 걸쳐 노드

### 3. LoadBalancer

노출합니다 the 서비스 사용하여 a cloud 프로바이더's load balancer.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: public-api
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
spec:
  type: LoadBalancer
  selector:
    app: api
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  loadBalancerSourceRanges:
  - 203.0.113.0/24
```

**Cloud-특정 annotations:**

**AWS:**
```yaml
annotations:
  service.beta.kubernetes.io/aws-load-balancer-type: "nlb"  # or "external"
  service.beta.kubernetes.io/aws-load-balancer-scheme: "internet-facing"
  service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
  service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
  service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
```

**Azure:**
```yaml
annotations:
  service.beta.kubernetes.io/azure-load-balancer-internal: "true"
  service.beta.kubernetes.io/azure-pip-name: "my-public-ip"
```

**GCP:**
```yaml
annotations:
  cloud.google.com/load-balancer-type: "Internal"
  cloud.google.com/backend-config: '{"default": "my-backend-config"}'
```

### 4. ExternalName

맵 서비스 에 외부 DNS name (CNAME 레코드).

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.external.example.com
  ports:
  - port: 5432
```

**Use cases:**
- Accessing 외부 서비스
- 서비스 마이그레이션 scenarios
- Multi-클러스터 서비스 참조

## 완전한 서비스 사양

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: production
  labels:
    app: my-app
    tier: backend
  annotations:
    description: "Main application service"
    prometheus.io/scrape: "true"
spec:
  # Service type
  type: ClusterIP

  # Pod selector
  selector:
    app: my-app
    version: v1

  # Ports configuration
  ports:
  - name: http
    port: 80           # Service port
    targetPort: 8080   # Container port (or named port)
    protocol: TCP      # TCP, UDP, or SCTP

  # Session affinity
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800

  # IP configuration
  clusterIP: 10.0.0.10  # Optional: specific IP
  clusterIPs:
  - 10.0.0.10
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack

  # External traffic policy
  externalTrafficPolicy: Local

  # Internal traffic policy
  internalTrafficPolicy: Local

  # Health check
  healthCheckNodePort: 30000

  # Load balancer config (for type: LoadBalancer)
  loadBalancerIP: 203.0.113.100
  loadBalancerSourceRanges:
  - 203.0.113.0/24

  # External IPs
  externalIPs:
  - 80.11.12.10

  # Publishing strategy
  publishNotReadyAddresses: false
```

## Port 구성

### Named Ports

Use named ports 에서 Pods 위한 flexibility:

**배포:**
```yaml
spec:
  template:
    spec:
      containers:
      - name: app
        ports:
        - name: http
          containerPort: 8080
        - name: metrics
          containerPort: 9090
```

**서비스:**
```yaml
spec:
  ports:
  - name: http
    port: 80
    targetPort: http  # References named port
  - name: metrics
    port: 9090
    targetPort: metrics
```

### 여러 Ports

```yaml
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: 9090
    protocol: TCP
```

## 세션 Affinity

### 없음 (default)

분산합니다 요청 무작위로 전반에 걸쳐 pods.

```yaml
spec:
  sessionAffinity: None
```

### ClientIP

라우트 요청 에서 same 클라이언트 IP 에 same pod.

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
```

**Use cases:**
- Stateful 애플리케이션
- 세션-based 애플리케이션
- WebSocket 연결

## Traffic 정책

### 외부 Traffic 정책

**클러스터 (default):**
```yaml
spec:
  externalTrafficPolicy: Cluster
```
- Load 균형을 맞춥니다 전반에 걸쳐 모든 노드
- May add extra 네트워크 hop
- 소스 IP is 마스킹된

**로컬:**
```yaml
spec:
  externalTrafficPolicy: Local
```
- Traffic goes 오직 에 pods 에 수신하는 노드
- 보존합니다 클라이언트 소스 IP
- 더 나은 성능 (아니요 extra hop)
- May cause imbalanced load

### 내부 Traffic 정책

```yaml
spec:
  internalTrafficPolicy: Local  # or Cluster
```

제어합니다 traffic 라우팅 위한 클러스터-내부 클라이언트.

## Headless 서비스

서비스 없이 클러스터 IP 위한 직접 pod access.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
spec:
  clusterIP: None  # Headless
  selector:
    app: database
  ports:
  - port: 5432
    targetPort: 5432
```

**Use cases:**
- StatefulSet pod 발견
- 직접 pod-에-pod communication
- 사용자 정의 load 균형
- 데이터베이스 클러스터

**DNS returns:**
- 개별 pod IPs instead of 서비스 IP
- Format: `<pod-name>.<service-name>.<namespace>.svc.cluster.local`

## 서비스 발견

### DNS

**ClusterIP 서비스:**
```
<service-name>.<namespace>.svc.cluster.local
```

예제:
```bash
curl http://backend-service.production.svc.cluster.local
```

**내에 same namespace:**
```bash
curl http://backend-service
```

**Headless 서비스 (returns pod IPs):**
```
<pod-name>.<service-name>.<namespace>.svc.cluster.local
```

### 환경 변수

Kubernetes injects 서비스 info into pods:

```bash
# Service host and port
BACKEND_SERVICE_SERVICE_HOST=10.0.0.100
BACKEND_SERVICE_SERVICE_PORT=80

# For named ports
BACKEND_SERVICE_SERVICE_PORT_HTTP=80
```

**노트:** Pods must be 생성된 이후 the 서비스 위한 env vars 에 be injected.

## Load 균형

### Algorithms

Kubernetes uses random 선택 에 의해 default. 위한 고급 load 균형:

**서비스 메시 (Istio 예제):**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-destination-rule
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_REQUEST  # or ROUND_ROBIN, RANDOM, PASSTHROUGH
    connectionPool:
      tcp:
        maxConnections: 100
```

### 연결 제한합니다

Use pod disruption budgets 및 리소스 제한합니다:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: my-app
```

## 서비스 메시 통합

### Istio Virtual 서비스

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-service
spec:
  hosts:
  - my-service
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: my-service
        subset: v2
  - route:
    - destination:
        host: my-service
        subset: v1
      weight: 90
    - destination:
        host: my-service
        subset: v2
      weight: 10
```

## 일반적인 패턴

### 패턴 1: 내부 Microservice

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: backend
  labels:
    app: user-service
    tier: backend
spec:
  type: ClusterIP
  selector:
    app: user-service
  ports:
  - name: http
    port: 8080
    targetPort: http
    protocol: TCP
  - name: grpc
    port: 9090
    targetPort: grpc
    protocol: TCP
```

### 패턴 2: 공개 API 와 함께 Load Balancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: "arn:aws:acm:..."
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
  selector:
    app: api-gateway
  ports:
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  loadBalancerSourceRanges:
  - 0.0.0.0/0
```

### 패턴 3: StatefulSet 와 함께 Headless 서비스

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cassandra
spec:
  clusterIP: None
  selector:
    app: cassandra
  ports:
  - port: 9042
    targetPort: 9042
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cassandra
spec:
  serviceName: cassandra
  replicas: 3
  selector:
    matchLabels:
      app: cassandra
  template:
    metadata:
      labels:
        app: cassandra
    spec:
      containers:
      - name: cassandra
        image: cassandra:4.0
```

### Pattern 4: External Service Mapping

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-database
spec:
  type: ExternalName
  externalName: prod-db.cxyz.us-west-2.rds.amazonaws.com
---
# Or with Endpoints for IP-based external service
apiVersion: v1
kind: Service
metadata:
  name: external-api
spec:
  ports:
  - port: 443
    targetPort: 443
    protocol: TCP
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-api
subsets:
- addresses:
  - ip: 203.0.113.100
  ports:
  - port: 443
```

### 패턴 5: Multi-Port 서비스 와 함께 메트릭

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9090"
    prometheus.io/path: "/metrics"
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 8080
  - name: metrics
    port: 9090
    targetPort: 9090
```

## 네트워크 정책

Control traffic 에 서비스:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## 최선의 관행

### 서비스 구성

1. **Use named ports** 위한 flexibility
2. **세트 적절한 서비스 유형** based 에 exposure needs
3. **Use 라벨링합니다 및 selectors consistently** 전반에 걸쳐 Deployments 및 서비스
4. **Configure 세션 affinity** 위한 stateful apps
5. **세트 외부 traffic 정책 에 로컬** 위한 IP preservation
6. **Use headless 서비스** 위한 StatefulSets
7. **Implement 네트워크 정책** 위한 security
8. **Add 모니터링 annotations** 위한 observability

### Production Checklist

- [ ] 서비스 유형 적절한 위한 use case
- [ ] Selector 일치합니다 pod 라벨링합니다
- [ ] Named ports used 위한 clarity
- [ ] 세션 affinity 구성된 만약 필요한
- [ ] Traffic 정책 세트 적절하게
- [ ] Load balancer annotations 구성된 (만약 적용 가능한)
- [ ] 소스 IP ranges 제한된 (위한 공개 서비스)
- [ ] Health check 구성 검증된
- [ ] 모니터링 annotations added
- [ ] 네트워크 정책 정의된

### 성능 Tuning

**위한 high traffic:**
```yaml
spec:
  externalTrafficPolicy: Local
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

**위한 WebSocket/long 연결:**
```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 86400  # 24 hours
```

## 문제 해결

### 서비스 not 접근 가능한

```bash
# Check service exists
kubectl get service <service-name>

# Check endpoints (should show pod IPs)
kubectl get endpoints <service-name>

# Describe service
kubectl describe service <service-name>

# Check if pods match selector
kubectl get pods -l app=<app-name>
```

**일반적인 이슈:**
- Selector doesn't match pod 라벨링합니다
- 아니요 pods 실행 중 (엔드포인트 빈)
- Ports misconfigured
- 네트워크 정책 차단 traffic

### DNS 해결 failing

```bash
# Test DNS from pod
kubectl run debug --rm -it --image=busybox -- nslookup <service-name>

# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns
```

### Load balancer 이슈

```bash
# Check load balancer status
kubectl describe service <service-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Verify cloud provider configuration
kubectl describe node
```

## 관련됨 리소스

- [Kubernetes Service API Reference](__URL0__)
- [Service Networking](__URL0__)
- [DNS for Services and Pods](__URL0__)
