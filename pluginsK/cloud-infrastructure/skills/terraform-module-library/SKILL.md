---
name: terraform-module-library
description: 빌드 reusable Terraform 모듈 위한 AWS, Azure, 및 GCP 인프라 다음 인프라-처럼-코드 최선의 관행. Use 때 생성하는 인프라 모듈, standardizing cloud provisioning, 또는 implementing reusable IaC 컴포넌트.
---

# Terraform 모듈 라이브러리

프로덕션 준비 완료 Terraform 모듈 패턴 위한 AWS, Azure, 및 GCP 인프라.

## Purpose

Create reusable, well-테스트된 Terraform 모듈 위한 일반적인 cloud 인프라 패턴 전반에 걸쳐 여러 cloud providers.

## 때 에 Use

- 빌드 reusable 인프라 컴포넌트
- Standardize cloud 리소스 provisioning
- Implement 인프라 처럼 코드 최선의 관행
- Create 멀티 클라우드 호환되는 모듈
- Establish organizational Terraform 표준

## 모듈 구조

```
terraform-modules/
├── aws/
│   ├── vpc/
│   ├── eks/
│   ├── rds/
│   └── s3/
├── azure/
│   ├── vnet/
│   ├── aks/
│   └── storage/
└── gcp/
    ├── vpc/
    ├── gke/
    └── cloud-sql/
```

## 표준 모듈 패턴

```
module-name/
├── main.tf          # Main resources
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Provider versions
├── README.md        # Documentation
├── examples/        # Usage examples
│   └── complete/
│       ├── main.tf
│       └── variables.tf
└── tests/           # Terratest files
    └── module_test.go
```

## AWS VPC 모듈 예제

**main.tf:**
```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    {
      Name = var.name
    },
    var.tags
  )
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    {
      Name = "${var.name}-private-${count.index + 1}"
      Tier = "private"
    },
    var.tags
  )
}

resource "aws_internet_gateway" "main" {
  count  = var.create_internet_gateway ? 1 : 0
  vpc_id = aws_vpc.main.id

  tags = merge(
    {
      Name = "${var.name}-igw"
    },
    var.tags
  )
}
```

**변수.tf:**
```hcl
variable "name" {
  description = "Name of the VPC"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  validation {
    condition     = can(regex("^([0-9]{1,3}\\.){3}[0-9]{1,3}/[0-9]{1,2}$", var.cidr_block))
    error_message = "CIDR block must be valid IPv4 CIDR notation."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = []
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
```

**출력.tf:**
```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "vpc_cidr_block" {
  description = "CIDR block of VPC"
  value       = aws_vpc.main.cidr_block
}
```

## 최선의 관행

1. **Use semantic versioning** 위한 모듈
2. **Document 모든 변수** 와 함께 descriptions
3. **Provide 예제** 에서 예제/ 디렉터리
4. **Use 검증 차단합니다** 위한 입력 검증
5. **출력 중요한 속성** 위한 모듈 composition
6. **Pin 프로바이더 버전** 에서 버전.tf
7. **Use locals** 위한 계산된 값
8. **Implement conditional 리소스** 와 함께 개수/for_each
9. **Test 모듈** 와 함께 Terratest
10. **Tag 모든 리소스** consistently

## 모듈 Composition

```hcl
module "vpc" {
  source = "../../modules/aws/vpc"

  name               = "production"
  cidr_block         = "10.0.0.0/16"
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]

  private_subnet_cidrs = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24"
  ]

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

module "rds" {
  source = "../../modules/aws/rds"

  identifier     = "production-db"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = "db.t3.large"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  tags = {
    Environment = "production"
  }
}
```

## 참조 파일

- `assets/vpc-module/` - 완전한 VPC 모듈 예제
- `assets/rds-module/` - RDS 모듈 예제
- `references/aws-modules.md` - AWS 모듈 패턴
- `references/azure-modules.md` - Azure 모듈 패턴
- `references/gcp-modules.md` - GCP 모듈 패턴

## 테스트

```go
// tests/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/complete",
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcID)
}
```

## 관련됨 Skills

- `multi-cloud-architecture` - 위한 architectural decisions
- `cost-optimization` - 위한 cost-effective 설계
