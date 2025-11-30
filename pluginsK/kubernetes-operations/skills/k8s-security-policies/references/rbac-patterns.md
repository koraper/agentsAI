# RBAC 패턴 및 최선의 관행

## 일반적인 RBAC 패턴

### 패턴 1: 읽은-오직 Access
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-only
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
```

### 패턴 2: Namespace Admin
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: namespace-admin
  namespace: production
rules:
- apiGroups: ["", "apps", "batch", "extensions"]
  resources: ["*"]
  verbs: ["*"]
```

### 패턴 3: 배포 Manager
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

### 패턴 4: Secret Reader (ServiceAccount)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
  resourceNames: ["app-secrets"]  # Specific secret only
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-secret-reader
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: production
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

### Pattern 5: CI/CD Pipeline Access
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cicd-deployer
rules:
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["services", "configmaps"]
  verbs: ["get", "list", "create", "update", "patch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

## ServiceAccount Best Practices

### Create Dedicated ServiceAccounts
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      serviceAccountName: my-app
      automountServiceAccountToken: false  # Disable if not needed
```

### Least-Privilege ServiceAccount
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get"]
  resourceNames: ["my-app-config"]
```

## Security 최선의 관행

1. **Use Roles over ClusterRoles** 때 possible
2. **Specify resourceNames** 위한 세밀한-grained access
3. **Avoid wildcard 권한** (`*`) 에서 production
4. **Create dedicated ServiceAccounts** 위한 각 app
5. **Disable 토큰 auto-mounting** 만약 not 필요한
6. **일반 RBAC 감사합니다** 에 remove unused 권한
7. **Use 그룹화합니다** 위한 사용자 관리
8. **Implement namespace 격리**
9. **모니터 RBAC usage** 와 함께 audit 로깅합니다
10. **Document role purposes** 에서 메타데이터

## 문제 해결 RBAC

### Check 사용자 권한
```bash
kubectl auth can-i list pods --as john@example.com
kubectl auth can-i '*' '*' --as system:serviceaccount:default:my-app
```

### 뷰 Effective 권한
```bash
kubectl describe clusterrole cluster-admin
kubectl describe rolebinding -n production
```

### Debug Access 이슈
```bash
kubectl get rolebindings,clusterrolebindings --all-namespaces -o wide | grep my-user
```

## 일반적인 RBAC Verbs

- `get` - 읽은 a 특정 리소스
- `list` - 목록 모든 리소스 of a 유형
- `watch` - Watch 위한 리소스 변경합니다
- `create` - Create 새로운 리소스
- `update` - 업데이트 기존 리소스
- `patch` - 부분적으로 업데이트 리소스
- `delete` - Delete 리소스
- `deletecollection` - Delete 여러 리소스
- `*` - 모든 verbs (avoid 에서 production)

## 리소스 범위

### 클러스터-Scoped 리소스
- 노드
- PersistentVolumes
- ClusterRoles
- ClusterRoleBindings
- Namespaces

### Namespace-Scoped 리소스
- Pods
- 서비스
- Deployments
- ConfigMaps
- Secrets
- Roles
- RoleBindings
