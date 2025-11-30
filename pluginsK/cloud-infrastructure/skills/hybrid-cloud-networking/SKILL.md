---
name: hybrid-cloud-networking
description: Configure secure, high-성능 connectivity 사이 온프레미스 인프라 및 cloud 플랫폼 사용하여 VPN 및 dedicated 연결. Use 때 구축 하이브리드 cloud 아키텍처, connecting 데이터 centers 에 cloud, 또는 implementing secure cross-전제 networking.
---

# 하이브리드 Cloud Networking

Configure secure, high-성능 connectivity 사이 온프레미스 및 cloud 환경 사용하여 VPN, 직접 Connect, 및 ExpressRoute.

## Purpose

Establish secure, reliable 네트워크 connectivity 사이 온프레미스 데이터 centers 및 cloud providers (AWS, Azure, GCP).

## 때 에 Use

- Connect 온프레미스 에 cloud
- Extend datacenter 에 cloud
- Implement 하이브리드 활성-활성 setups
- Meet compliance 요구사항
- Migrate 에 cloud 점진적으로

## 연결 Options

### AWS Connectivity

#### 1. 사이트-에-사이트 VPN
- IPSec VPN over internet
- Up 에 1.25 Gbps per tunnel
- Cost-effective 위한 moderate 대역폭
- Higher 지연 시간, internet-dependent

```hcl
resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-vpn-gateway"
  }
}

resource "aws_customer_gateway" "main" {
  bgp_asn    = 65000
  ip_address = "203.0.113.1"
  type       = "ipsec.1"
}

resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"
  static_routes_only  = false
}
```

#### 2. AWS 직접 Connect
- Dedicated 네트워크 연결
- 1 Gbps 에 100 Gbps
- Lower 지연 시간, 일관된 대역폭
- More expensive, 설정 시간 필수

**참조:** See `references/direct-connect.md`

### Azure Connectivity

#### 1. 사이트-에-사이트 VPN
```hcl
resource "azurerm_virtual_network_gateway" "vpn" {
  name                = "vpn-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  type     = "Vpn"
  vpn_type = "RouteBased"
  sku      = "VpnGw1"

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway.id
  }
}
```

#### 2. Azure ExpressRoute
- 비공개 연결 를 통해 connectivity 프로바이더
- Up 에 100 Gbps
- Low 지연 시간, high 신뢰성
- 프리미엄 위한 전역 connectivity

### GCP Connectivity

#### 1. Cloud VPN
- IPSec VPN (클래식 또는 HA VPN)
- HA VPN: 99.99% SLA
- Up 에 3 Gbps per tunnel

#### 2. Cloud Interconnect
- Dedicated (10 Gbps, 100 Gbps)
- 파트너 (50 Mbps 에 50 Gbps)
- Lower 지연 시간 보다 VPN

## 하이브리드 네트워크 패턴

### 패턴 1: Hub-및-Spoke
```
On-Premises Datacenter
         ↓
    VPN/Direct Connect
         ↓
    Transit Gateway (AWS) / vWAN (Azure)
         ↓
    ├─ Production VPC/VNet
    ├─ Staging VPC/VNet
    └─ Development VPC/VNet
```

### 패턴 2: 다중 리전 하이브리드
```
On-Premises
    ├─ Direct Connect → us-east-1
    └─ Direct Connect → us-west-2
            ↓
        Cross-Region Peering
```

### 패턴 3: 멀티 클라우드 하이브리드
```
On-Premises Datacenter
    ├─ Direct Connect → AWS
    ├─ ExpressRoute → Azure
    └─ Interconnect → GCP
```

## 라우팅 구성

### BGP 구성
```
On-Premises Router:
- AS Number: 65000
- Advertise: 10.0.0.0/8

Cloud Router:
- AS Number: 64512 (AWS), 65515 (Azure)
- Advertise: Cloud VPC/VNet CIDRs
```

### 라우트 전파
- Enable 라우트 전파 에 라우트 테이블
- Use BGP 위한 동적 라우팅
- Implement 라우트 필터링
- 모니터 라우트 advertisements

## Security 최선의 관행

1. **Use 비공개 connectivity** (직접 Connect/ExpressRoute)
2. **Implement 암호화** 위한 VPN tunnels
3. **Use VPC 엔드포인트** 에 avoid internet 라우팅
4. **Configure 네트워크 ACLs** 및 security 그룹화합니다
5. **Enable VPC 흐름 로깅합니다** 위한 모니터링
6. **Implement DDoS 보호**
7. **Use PrivateLink/비공개 엔드포인트**
8. **모니터 연결** 와 함께 CloudWatch/모니터
9. **Implement redundancy** (dual tunnels)
10. **일반 security 감사합니다**

## High 가용성

### Dual VPN Tunnels
```hcl
resource "aws_vpn_connection" "primary" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.primary.id
  type                = "ipsec.1"
}

resource "aws_vpn_connection" "secondary" {
  vpn_gateway_id      = aws_vpn_gateway.main.id
  customer_gateway_id = aws_customer_gateway.secondary.id
  type                = "ipsec.1"
}
```

### 활성-활성 구성
- 여러 연결 에서 다른 위치
- BGP 위한 automatic failover
- Equal-cost multi-경로 (ECMP) 라우팅
- 모니터 health of 모든 연결

## 모니터링 및 문제 해결

### 키 메트릭
- Tunnel 상태 (up/down)
- Bytes 에서/out
- Packet loss
- 지연 시간
- BGP 세션 상태

### 문제 해결
```bash
# AWS VPN
aws ec2 describe-vpn-connections
aws ec2 get-vpn-connection-telemetry

# Azure VPN
az network vpn-connection show
az network vpn-connection show-device-config-script
```

## Cost 최적화

1. **맞는-size 연결** based 에 traffic
2. **Use VPN 위한 low-대역폭** workloads
3. **Consolidate traffic** 통해 fewer 연결
4. **Minimize 데이터 전송** costs
5. **Use 직접 Connect** 위한 high 대역폭
6. **Implement 캐싱** 에 reduce traffic

## 참조 파일

- `references/vpn-setup.md` - VPN 구성 가이드
- `references/direct-connect.md` - 직접 Connect 설정

## 관련됨 Skills

- `multi-cloud-architecture` - 위한 아키텍처 decisions
- `terraform-module-library` - 위한 IaC 구현
