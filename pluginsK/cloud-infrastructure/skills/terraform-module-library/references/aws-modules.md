# AWS Terraform 모듈 패턴

## VPC 모듈
- VPC 와 함께 공개/비공개 subnets
- Internet 게이트웨이 및 NAT Gateways
- 라우트 테이블 및 연관
- 네트워크 ACLs
- VPC 흐름 로깅합니다

## EKS 모듈
- EKS 클러스터 와 함께 관리형 노드 그룹화합니다
- IRSA (IAM Roles 위한 서비스 계정)
- 클러스터 autoscaler
- VPC CNI 구성
- 클러스터 로깅

## RDS 모듈
- RDS 인스턴스 또는 클러스터
- 자동화된 backups
- 읽은 replicas
- 매개변수 그룹화합니다
- Subnet 그룹화합니다
- Security 그룹화합니다

## S3 모듈
- S3 bucket 와 함께 versioning
- 암호화 에서 rest
- Bucket 정책
- Lifecycle 규칙
- 복제 구성

## ALB 모듈
- 애플리케이션 Load Balancer
- Target 그룹화합니다
- 리스너 규칙
- SSL/TLS certificates
- Access 로깅합니다

## Lambda 모듈
- Lambda 함수
- IAM 실행 role
- CloudWatch 로깅합니다
- 환경 변수
- VPC 구성 (선택적)

## Security 그룹 모듈
- Reusable security 그룹 규칙
- Ingress/egress 규칙
- 동적 규칙 생성
- 규칙 descriptions

## 최선의 관행

1. Use AWS 프로바이더 버전 ~> 5.0
2. Enable 암호화 에 의해 default
3. Use least-privilege IAM
4. Tag 모든 리소스 consistently
5. Enable 로깅 및 모니터링
6. Use KMS 위한 암호화
7. Implement 백업 strategies
8. Use PrivateLink 때 possible
9. Enable GuardDuty/SecurityHub
10. Follow AWS Well-Architected 프레임워크
