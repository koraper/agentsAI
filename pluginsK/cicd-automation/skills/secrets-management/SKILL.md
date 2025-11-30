---
name: secrets-management
description: Implement secure secrets 관리 위한 CI/CD 파이프라인 사용하여 Vault, AWS Secrets Manager, 또는 native 플랫폼 solutions. Use 때 처리 sensitive 자격 증명, rotating secrets, 또는 securing CI/CD 환경.
---

# Secrets 관리

Secure secrets 관리 관행 위한 CI/CD 파이프라인 사용하여 Vault, AWS Secrets Manager, 및 other tools.

## Purpose

Implement secure secrets 관리 에서 CI/CD 파이프라인 없이 hardcoding sensitive 정보.

## 때 에 Use

- Store API 키 및 자격 증명
- Manage 데이터베이스 passwords
- Handle TLS certificates
- Rotate secrets automatically
- Implement least-privilege access

## Secrets 관리 Tools

### HashiCorp Vault
- 중앙 집중화된 secrets 관리
- 동적 secrets 세대
- Secret rotation
- Audit 로깅
- 세밀한-grained access control

### AWS Secrets Manager
- AWS-native solution
- Automatic rotation
- 통합 와 함께 RDS
- CloudFormation 지원

### Azure 키 Vault
- Azure-native solution
- HSM-backed 키
- Certificate 관리
- RBAC 통합

### Google Secret Manager
- GCP-native solution
- Versioning
- IAM 통합

## HashiCorp Vault 통합

### 설정 Vault

```bash
# Start Vault dev server
vault server -dev

# Set environment
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Store secret
vault kv put secret/database/config username=admin password=secret
```

### GitHub Actions 와 함께 Vault

```yaml
name: Deploy with Vault Secrets

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Import Secrets from Vault
      uses: hashicorp/vault-action@v2
      with:
        url: https://vault.example.com:8200
        token: ${{ secrets.VAULT_TOKEN }}
        secrets: |
          secret/data/database username | DB_USERNAME ;
          secret/data/database password | DB_PASSWORD ;
          secret/data/api key | API_KEY

    - name: Use secrets
      run: |
        echo "Connecting to database as $DB_USERNAME"
        # Use $DB_PASSWORD, $API_KEY
```

### GitLab CI 와 함께 Vault

```yaml
deploy:
  image: vault:latest
  before_script:
    - export VAULT_ADDR=https://vault.example.com:8200
    - export VAULT_TOKEN=$VAULT_TOKEN
    - apk add curl jq
  script:
    - |
      DB_PASSWORD=$(vault kv get -field=password secret/database/config)
      API_KEY=$(vault kv get -field=key secret/api/credentials)
      echo "Deploying with secrets..."
      # Use $DB_PASSWORD, $API_KEY
```

**참조:** See `references/vault-setup.md`

## AWS Secrets Manager

### Store Secret

```bash
aws secretsmanager create-secret \
  --name production/database/password \
  --secret-string "super-secret-password"
```

### Retrieve 에서 GitHub Actions

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-west-2

- name: Get secret from AWS
  run: |
    SECRET=$(aws secretsmanager get-secret-value \
      --secret-id production/database/password \
      --query SecretString \
      --output text)
    echo "::add-mask::$SECRET"
    echo "DB_PASSWORD=$SECRET" >> $GITHUB_ENV

- name: Use secret
  run: |
    # Use $DB_PASSWORD
    ./deploy.sh
```

### Terraform 와 함께 AWS Secrets Manager

```hcl
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "production/database/password"
}

resource "aws_db_instance" "main" {
  allocated_storage    = 100
  engine              = "postgres"
  instance_class      = "db.t3.large"
  username            = "admin"
  password            = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

## GitHub Secrets

### 조직/저장소 Secrets

```yaml
- name: Use GitHub secret
  run: |
    echo "API Key: ${{ secrets.API_KEY }}"
    echo "Database URL: ${{ secrets.DATABASE_URL }}"
```

### 환경 Secrets

```yaml
deploy:
  runs-on: ubuntu-latest
  environment: production
  steps:
  - name: Deploy
    run: |
      echo "Deploying with ${{ secrets.PROD_API_KEY }}"
```

**참조:** See `references/github-secrets.md`

## GitLab CI/CD 변수

### Project 변수

```yaml
deploy:
  script:
    - echo "Deploying with $API_KEY"
    - echo "Database: $DATABASE_URL"
```

### 보호된 및 마스킹된 변수
- 보호된: 오직 사용 가능한 에서 보호된 branches
- 마스킹된: 숨겨진 에서 작업 로깅합니다
- 파일 유형: 저장됨 처럼 파일

## 최선의 관행

1. **절대 ~하지 않음 커밋 secrets** 에 Git
2. **Use 다른 secrets** per 환경
3. **Rotate secrets 정기적으로**
4. **Implement least-privilege access**
5. **Enable audit 로깅**
6. **Use secret scanning** (GitGuardian, TruffleHog)
7. **Mask secrets 에서 로깅합니다**
8. **Encrypt secrets 에서 rest**
9. **Use short-lived 토큰** 때 possible
10. **Document secret 요구사항**

## Secret Rotation

### 자동화된 Rotation 와 함께 AWS

```python
import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('secretsmanager')

    # Get current secret
    response = client.get_secret_value(SecretId='my-secret')
    current_secret = json.loads(response['SecretString'])

    # Generate new password
    new_password = generate_strong_password()

    # Update database password
    update_database_password(new_password)

    # Update secret
    client.put_secret_value(
        SecretId='my-secret',
        SecretString=json.dumps({
            'username': current_secret['username'],
            'password': new_password
        })
    )

    return {'statusCode': 200}
```

### Manual Rotation 프로세스

1. Generate 새로운 secret
2. 업데이트 secret 에서 secret store
3. 업데이트 애플리케이션 에 use 새로운 secret
4. Verify 기능
5. Revoke 오래된 secret

## 외부 Secrets 운영자

### Kubernetes 통합

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "production"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: database/config
      property: username
  - secretKey: password
    remoteRef:
      key: database/config
      property: password
```

## Secret Scanning

### Pre-커밋 Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for secrets with TruffleHog
docker run --rm -v "$(pwd):/repo" \
  trufflesecurity/trufflehog:latest \
  filesystem --directory=/repo

if [ $? -ne 0 ]; then
  echo "❌ Secret detected! Commit blocked."
  exit 1
fi
```

### CI/CD Secret Scanning

```yaml
secret-scan:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem .
  allow_failure: false
```

## 참조 파일

- `references/vault-setup.md` - HashiCorp Vault 구성
- `references/github-secrets.md` - GitHub Secrets 최선의 관행

## 관련됨 Skills

- `github-actions-templates` - 위한 GitHub Actions 통합
- `gitlab-ci-patterns` - 위한 GitLab CI 통합
- `deployment-pipeline-design` - 위한 파이프라인 아키텍처
