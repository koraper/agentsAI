---
name: cost-optimization
description: Optimize cloud costs 통해 리소스 rightsizing, 태깅 strategies, reserved 인스턴스, 및 spending 분석. Use 때 reducing cloud expenses, analyzing 인프라 costs, 또는 implementing cost governance 정책.
---

# Cloud Cost 최적화

Strategies 및 패턴 위한 optimizing cloud costs 전반에 걸쳐 AWS, Azure, 및 GCP.

## Purpose

Implement systematic cost 최적화 strategies 에 reduce cloud spending 동안 maintaining 성능 및 신뢰성.

## 때 에 Use

- Reduce cloud spending
- 맞는-size 리소스
- Implement cost governance
- Optimize 멀티 클라우드 costs
- Meet budget constraints

## Cost 최적화 프레임워크

### 1. Visibility
- Implement cost allocation 태그합니다
- Use cloud cost 관리 tools
- 세트 up budget 경고
- Create cost 대시보드

### 2. 맞는-Sizing
- Analyze 리소스 사용률
- Downsize over-provisioned 리소스
- Use auto-확장
- Remove idle 리소스

### 3. Pricing 모델
- Use reserved 용량
- Leverage 지점/preemptible 인스턴스
- Implement savings 계획합니다
- Use committed use discounts

### 4. 아키텍처 최적화
- Use 관리형 서비스
- Implement 캐싱
- Optimize 데이터 전송
- Use lifecycle 정책

## AWS Cost 최적화

### Reserved 인스턴스
```
Savings: 30-72% vs On-Demand
Term: 1 or 3 years
Payment: All/Partial/No upfront
Flexibility: Standard or Convertible
```

### Savings 계획합니다
```
Compute Savings Plans: 66% savings
EC2 Instance Savings Plans: 72% savings
Applies to: EC2, Fargate, Lambda
Flexible across: Instance families, regions, OS
```

### 지점 인스턴스
```
Savings: Up to 90% vs On-Demand
Best for: Batch jobs, CI/CD, stateless workloads
Risk: 2-minute interruption notice
Strategy: Mix with On-Demand for resilience
```

### S3 Cost 최적화
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

## Azure Cost 최적화

### Reserved VM 인스턴스
- 1 또는 3 year terms
- Up 에 72% savings
- 유연한 sizing
- Exchangeable

### Azure 하이브리드 Benefit
- Use 기존 Windows 서버 licenses
- Up 에 80% savings 와 함께 RI
- 사용 가능한 위한 Windows 및 SQL 서버

### Azure 어드바이저 Recommendations
- 맞는-size VMs
- Delete unused 리소스
- Use reserved 용량
- Optimize 스토리지

## GCP Cost 최적화

### Committed Use Discounts
- 1 또는 3 year commitment
- Up 에 57% savings
- Applies 에 vCPUs 및 메모리
- 리소스-based 또는 spend-based

### Sustained Use Discounts
- Automatic discounts
- Up 에 30% 위한 실행 중 인스턴스
- 아니요 commitment 필수
- Applies 에 Compute Engine, GKE

### Preemptible VMs
- Up 에 80% savings
- 24-hour maximum 런타임
- 최선의 위한 batch workloads

## 태깅 전략

### AWS 태깅
```hcl
locals {
  common_tags = {
    Environment = "production"
    Project     = "my-project"
    CostCenter  = "engineering"
    Owner       = "team@example.com"
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "example" {
  ami           = "ami-12345678"
  instance_type = "t3.medium"

  tags = merge(
    local.common_tags,
    {
      Name = "web-server"
    }
  )
}
```

**참조:** See `references/tagging-standards.md`

## Cost 모니터링

### Budget 경고
```hcl
# AWS Budget
resource "aws_budgets_budget" "monthly" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "1000"
  limit_unit        = "USD"
  time_period_start = "2024-01-01_00:00"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = ["team@example.com"]
  }
}
```

### Cost Anomaly 감지
- AWS Cost Anomaly 감지
- Azure Cost 관리 경고
- GCP Budget 경고

## 아키텍처 패턴

### 패턴 1: 서버리스 첫 번째
- Use Lambda/함수 위한 이벤트 기반
- Pay 오직 위한 실행 시간
- Auto-확장 포함된
- 아니요 idle costs

### 패턴 2: 맞는-Sized Databases
```
Development: t3.small RDS
Staging: t3.large RDS
Production: r6g.2xlarge RDS with read replicas
```

### 패턴 3: Multi-티어 스토리지
```
Hot data: S3 Standard
Warm data: S3 Standard-IA (30 days)
Cold data: S3 Glacier (90 days)
Archive: S3 Deep Archive (365 days)
```

### 패턴 4: Auto-확장
```hcl
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  threshold           = "80"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
}
```

## Cost 최적화 Checklist

- [ ] Implement cost allocation 태그합니다
- [ ] Delete unused 리소스 (EBS, EIPs, snapshots)
- [ ] 맞는-size 인스턴스 based 에 사용률
- [ ] Use reserved 용량 위한 steady workloads
- [ ] Implement auto-확장
- [ ] Optimize 스토리지 클래스
- [ ] Use lifecycle 정책
- [ ] Enable cost anomaly 감지
- [ ] 세트 budget 경고
- [ ] Review costs weekly
- [ ] Use 지점/preemptible 인스턴스
- [ ] Optimize 데이터 전송 costs
- [ ] Implement 캐싱 layers
- [ ] Use 관리형 서비스
- [ ] 모니터 및 optimize 지속적으로

## Tools

- **AWS:** Cost 탐색기, Cost Anomaly 감지, Compute 최적화기
- **Azure:** Cost 관리, 어드바이저
- **GCP:** Cost 관리, Recommender
- **멀티 클라우드:** CloudHealth, Cloudability, Kubecost

## 참조 파일

- `references/tagging-standards.md` - 태깅 규약
- `assets/cost-analysis-template.xlsx` - Cost 분석 spreadsheet

## 관련됨 Skills

- `terraform-module-library` - 위한 리소스 provisioning
- `multi-cloud-architecture` - 위한 cloud 선택
