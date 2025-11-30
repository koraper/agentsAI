# ArgoCD 설정 및 구성

## Installation 메서드

### 1. 표준 Installation
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. High 가용성 Installation
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/ha/install.yaml
```

### 3. Helm Installation
```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace
```

## 초기 구성

### Access ArgoCD UI
```bash
# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
argocd admin initial-password -n argocd
```

### Configure Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  rules:
  - host: argocd.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              number: 443
  tls:
  - hosts:
    - argocd.example.com
    secretName: argocd-secret
```

## CLI 구성

### Login
```bash
argocd login argocd.example.com --username admin
```

### Add 저장소
```bash
argocd repo add https://github.com/org/repo --username user --password token
```

### Create 애플리케이션
```bash
argocd app create my-app \
  --repo https://github.com/org/repo \
  --path apps/my-app \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production
```

## SSO 구성

### GitHub OAuth
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  url: https://argocd.example.com
  dex.config: |
    connectors:
      - type: github
        id: github
        name: GitHub
        config:
          clientID: $GITHUB_CLIENT_ID
          clientSecret: $GITHUB_CLIENT_SECRET
          orgs:
          - name: my-org
```

## RBAC 구성
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    p, role:developers, applications, *, */dev, allow
    p, role:operators, applications, *, */*, allow
    g, my-org:devs, role:developers
    g, my-org:ops, role:operators
```

## 최선의 관행

1. Enable SSO 위한 production
2. Implement RBAC 정책
3. Use 별도 projects 위한 teams
4. Enable audit 로깅
5. Configure 알림
6. Use ApplicationSets 위한 multi-클러스터
7. Implement 리소스 hooks
8. Configure health 확인합니다
9. Use 동기 windows 위한 유지보수
10. 모니터 와 함께 Prometheus 메트릭
