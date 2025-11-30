---
name: github-actions-templates
description: Create 프로덕션 준비 완료 GitHub Actions 워크플로우 위한 자동화된 테스트, 구축, 및 deploying 애플리케이션. Use 때 설정하는 CI/CD 와 함께 GitHub Actions, automating 개발 워크플로우, 또는 생성하는 reusable 워크플로우 템플릿.
---

# GitHub Actions 템플릿

프로덕션 준비 완료 GitHub Actions 워크플로우 패턴 위한 테스트, 구축, 및 deploying 애플리케이션.

## Purpose

Create efficient, secure GitHub Actions 워크플로우 위한 continuous 통합 및 배포 전반에 걸쳐 various tech 스택합니다.

## 때 에 Use

- Automate 테스트 및 배포
- 빌드 Docker images 및 push 에 registries
- Deploy 에 Kubernetes 클러스터
- Run security scans
- Implement 매트릭스 빌드 위한 여러 환경

## 일반적인 워크플로우 패턴

### 패턴 1: Test 워크플로우

```yaml
name: Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Run tests
      run: npm test

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage/lcov.info
```

**참조:** See `assets/test-workflow.yml`

### 패턴 2: 빌드 및 Push Docker Image

```yaml
name: Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v4

    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

**참조:** See `assets/deploy-workflow.yml`

### 패턴 3: Deploy 에 Kubernetes

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2

    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --name production-cluster --region us-west-2

    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/
        kubectl rollout status deployment/my-app -n production
        kubectl get services -n production

    - name: Verify deployment
      run: |
        kubectl get pods -n production
        kubectl describe deployment my-app -n production
```

### 패턴 4: 매트릭스 빌드

```yaml
name: Matrix Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest
```

**참조:** See `assets/matrix-build.yml`

## 워크플로우 최선의 관행

1. **Use 특정 action 버전** (@v4, not @최신)
2. **캐시 종속성** 에 속도 up 빌드
3. **Use secrets** 위한 sensitive 데이터
4. **Implement 상태 확인합니다** 에 PRs
5. **Use 매트릭스 빌드** 위한 multi-버전 테스트
6. **세트 적절한 권한**
7. **Use reusable 워크플로우** 위한 일반적인 패턴
8. **Implement approval gates** 위한 production
9. **Add 알림 steps** 위한 실패
10. **Use 자체 호스팅 runners** 위한 sensitive workloads

## Reusable 워크플로우

```yaml
# .github/workflows/reusable-test.yml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
    - run: npm test
```

**Use reusable 워크플로우:**
```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: '20.x'
    secrets:
      NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Security Scanning

```yaml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

    - name: Run Snyk Security Scan
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## 배포 와 함께 Approvals

```yaml
name: Deploy to Production

on:
  push:
    tags: [ 'v*' ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com

    steps:
    - uses: actions/checkout@v4

    - name: Deploy application
      run: |
        echo "Deploying to production..."
        # Deployment commands here

    - name: Notify Slack
      if: success()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "Deployment to production completed successfully!"
          }
```

## 참조 파일

- `assets/test-workflow.yml` - 테스트 워크플로우 템플릿
- `assets/deploy-workflow.yml` - 배포 워크플로우 템플릿
- `assets/matrix-build.yml` - 매트릭스 빌드 템플릿
- `references/common-workflows.md` - 일반적인 워크플로우 패턴

## 관련됨 Skills

- `gitlab-ci-patterns` - 위한 GitLab CI 워크플로우
- `deployment-pipeline-design` - 위한 파이프라인 아키텍처
- `secrets-management` - 위한 secrets 처리
