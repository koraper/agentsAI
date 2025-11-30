---
name: k8s-security-policies
description: Implement Kubernetes security 정책 포함하여 NetworkPolicy, PodSecurityPolicy, 및 RBAC 위한 production-grade security. Use 때 securing Kubernetes 클러스터, implementing 네트워크 격리, 또는 enforcing pod security 표준.
---

# Kubernetes Security 정책

포괄적인 가이드 위한 implementing NetworkPolicy, PodSecurityPolicy, RBAC, 및 Pod Security 표준 에서 Kubernetes.

## Purpose

Implement defense-에서-depth security 위한 Kubernetes 클러스터 사용하여 네트워크 정책, pod security 표준, 및 RBAC.

## 때 에 Use This Skill

- Implement 네트워크 세그먼테이션
- Configure pod security 표준
- 세트 up RBAC 위한 least-privilege access
- Create security 정책 위한 compliance
- Implement admission control
- Secure multi-tenant 클러스터

## Pod Security 표준

### 1. Privileged (제한 없는)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: privileged-ns
  labels:
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/audit: privileged
    pod-security.kubernetes.io/warn: privileged
```

### 2. Baseline (최소한 restrictive)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: baseline-ns
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: baseline
```

### 3. 제한된 (Most restrictive)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: restricted-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## 네트워크 정책

### default Deny 모든
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Frontend 에 Backend
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: production
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

### Allow DNS
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```

**참조:** See `assets/network-policy-template.yaml`

## RBAC 구성

### Role (Namespace-scoped)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

### ClusterRole (클러스터-넓은)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

### RoleBinding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
- kind: User
  name: jane
  apiGroup: rbac.authorization.k8s.io
- kind: ServiceAccount
  name: default
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**참조:** See `references/rbac-patterns.md`

## Pod Security 컨텍스트

### 제한된 Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
```

## 정책 Enforcement 와 함께 OPA Gatekeeper

### ConstraintTemplate
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("missing required labels: %v", [missing])
        }
```

### 제약
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-app-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    labels: ["app", "environment"]
```

## 서비스 메시 Security (Istio)

### PeerAuthentication (mTLS)
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

### AuthorizationPolicy
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
```

## 최선의 관행

1. **Implement Pod Security 표준** 에서 namespace 레벨
2. **Use 네트워크 정책** 위한 네트워크 세그먼테이션
3. **Apply least-privilege RBAC** 위한 모든 서비스 계정
4. **Enable admission control** (OPA Gatekeeper/Kyverno)
5. **Run 컨테이너 처럼 non-근**
6. **Use 읽은-오직 근 filesystem**
7. **Drop 모든 역량** 하지 않는 한 필요한
8. **Implement 리소스 quotas** 및 limit ranges
9. **Enable audit 로깅** 위한 security 이벤트
10. **일반 security scanning** of images

## Compliance 프레임워크

### CIS Kubernetes Benchmark
- Use RBAC 인가
- Enable audit 로깅
- Use Pod Security 표준
- Configure 네트워크 정책
- Implement secrets 암호화 에서 rest
- Enable 노드 인증

### NIST Cybersecurity 프레임워크
- Implement defense 에서 depth
- Use 네트워크 세그먼테이션
- Configure security 모니터링
- Implement access 제어합니다
- Enable 로깅 및 모니터링

## 문제 해결

**NetworkPolicy not 작업:**
```bash
# Check if CNI supports NetworkPolicy
kubectl get nodes -o wide
kubectl describe networkpolicy <name>
```

**RBAC 권한 거부된:**
```bash
# Check effective permissions
kubectl auth can-i list pods --as system:serviceaccount:default:my-sa
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-sa
```

## 참조 파일

- `assets/network-policy-template.yaml` - 네트워크 정책 예제
- `assets/pod-security-template.yaml` - Pod security 정책
- `references/rbac-patterns.md` - RBAC 구성 패턴

## 관련됨 Skills

- `k8s-manifest-generator` - 위한 생성하는 secure manifests
- `gitops-workflow` - 위한 자동화된 정책 배포
