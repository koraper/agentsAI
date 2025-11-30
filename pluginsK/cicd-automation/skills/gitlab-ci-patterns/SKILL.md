---
name: gitlab-ci-patterns
description: 빌드 GitLab CI/CD 파이프라인 와 함께 multi-단계 워크플로우, 캐싱, 및 분산 runners 위한 scalable 자동화. Use 때 implementing GitLab CI/CD, optimizing 파이프라인 성능, 또는 설정하는 자동화된 테스트 및 배포.
---

# GitLab CI 패턴

포괄적인 GitLab CI/CD 파이프라인 패턴 위한 자동화된 테스트, 구축, 및 배포.

## Purpose

Create efficient GitLab CI 파이프라인 와 함께 적절한 단계 조직, 캐싱, 및 배포 strategies.

## 때 에 Use

- Automate GitLab-based CI/CD
- Implement multi-단계 파이프라인
- Configure GitLab Runners
- Deploy 에 Kubernetes 에서 GitLab
- Implement GitOps 워크플로우

## 기본 파이프라인 구조

```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

build:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run lint
    - npm test
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -f k8s/
    - kubectl rollout status deployment/my-app
  only:
    - main
  environment:
    name: production
    url: https://app.example.com
```

## Docker 빌드 및 Push

```yaml
build-docker:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - tags
```

## Multi-환경 배포

```yaml
.deploy_template: &deploy_template
  image: bitnami/kubectl:latest
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --insecure-skip-tls-verify=true
    - kubectl config set-credentials admin --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=admin
    - kubectl config use-context default

deploy:staging:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl apply -f k8s/ -n staging
    - kubectl rollout status deployment/my-app -n staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy:production:
  <<: *deploy_template
  stage: deploy
  script:
    - kubectl apply -f k8s/ -n production
    - kubectl rollout status deployment/my-app -n production
  environment:
    name: production
    url: https://app.example.com
  when: manual
  only:
    - main
```

## Terraform 파이프라인

```yaml
stages:
  - validate
  - plan
  - apply

variables:
  TF_ROOT: ${CI_PROJECT_DIR}/terraform
  TF_VERSION: "1.6.0"

before_script:
  - cd ${TF_ROOT}
  - terraform --version

validate:
  stage: validate
  image: hashicorp/terraform:${TF_VERSION}
  script:
    - terraform init -backend=false
    - terraform validate
    - terraform fmt -check

plan:
  stage: plan
  image: hashicorp/terraform:${TF_VERSION}
  script:
    - terraform init
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - ${TF_ROOT}/tfplan
    expire_in: 1 day

apply:
  stage: apply
  image: hashicorp/terraform:${TF_VERSION}
  script:
    - terraform init
    - terraform apply -auto-approve tfplan
  dependencies:
    - plan
  when: manual
  only:
    - main
```

## Security Scanning

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

trivy-scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  allow_failure: true
```

## 캐싱 Strategies

```yaml
# Cache node_modules
build:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull-push

# Global cache
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/
    - vendor/

# Separate cache per job
job1:
  cache:
    key: job1-cache
    paths:
      - build/

job2:
  cache:
    key: job2-cache
    paths:
      - dist/
```

## 동적 Child 파이프라인

```yaml
generate-pipeline:
  stage: build
  script:
    - python generate_pipeline.py > child-pipeline.yml
  artifacts:
    paths:
      - child-pipeline.yml

trigger-child:
  stage: deploy
  trigger:
    include:
      - artifact: child-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

## 참조 파일

- `assets/gitlab-ci.yml.template` - 완전한 파이프라인 템플릿
- `references/pipeline-stages.md` - 단계 조직 패턴

## 최선의 관행

1. **Use 특정 image 태그합니다** (노드:20, not 노드:최신)
2. **캐시 종속성** 적절하게
3. **Use 아티팩트** 위한 빌드 출력
4. **Implement manual gates** 위한 production
5. **Use 환경** 위한 배포 추적
6. **Enable merge 요청 파이프라인**
7. **Use 파이프라인 예약합니다** 위한 recurring jobs
8. **Implement security scanning**
9. **Use CI/CD 변수** 위한 secrets
10. **모니터 파이프라인 성능**

## 관련됨 Skills

- `github-actions-templates` - 위한 GitHub Actions
- `deployment-pipeline-design` - 위한 아키텍처
- `secrets-management` - 위한 secrets 처리
