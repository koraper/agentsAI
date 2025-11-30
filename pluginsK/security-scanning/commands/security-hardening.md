Implement 포괄적인 보안 hardening 와 함께 defense-에서-depth strategy 통해 coordinated multi-agent 오케스트레이션:

[Extended thinking: This 워크플로우 구현합니다 a defense-에서-depth 보안 strategy 전반에 걸쳐 all application layers. It 조정합니다 specialized 보안 agents 에 perform 포괄적인 assessments, implement layered 보안 controls, 및 establish continuous 보안 모니터링. The approach follows 현대적인 DevSecOps principles 와 함께 shift-left 보안, 자동화된 scanning, 및 규정 준수 validation. Each phase 구축합니다 upon previous findings 에 create a 복원력 있는 보안 posture that addresses both current vulnerabilities 및 future threats.]

## Phase 1: 포괄적인 보안 Assessment

### 1. Initial Vulnerability Scanning
- Use Task tool 와 함께 subagent_type="보안-auditor"
- Prompt: "Perform 포괄적인 보안 assessment 에: $ARGUMENTS. Execute SAST analysis 와 함께 Semgrep/SonarQube, DAST scanning 와 함께 OWASP ZAP, dependency audit 와 함께 Snyk/Trivy, secrets detection 와 함께 GitLeaks/TruffleHog. Generate SBOM 위한 supply chain analysis. Identify OWASP Top 10 vulnerabilities, CWE weaknesses, 및 CVE exposures."
- Output: Detailed vulnerability report 와 함께 CVSS scores, exploitability analysis, attack surface mapping, secrets exposure report, SBOM inventory
- Context: Initial baseline 위한 all remediation efforts

### 2. Threat Modeling 및 Risk Analysis
- Use Task tool 와 함께 subagent_type="보안-auditor"
- Prompt: "Conduct threat modeling 사용하여 STRIDE methodology 위한: $ARGUMENTS. Analyze attack vectors, create attack trees, assess business impact of identified vulnerabilities. Map threats 에 MITRE ATT&CK framework. Prioritize risks based 에 likelihood 및 impact."
- Output: Threat model diagrams, risk matrix 와 함께 prioritized vulnerabilities, attack scenario 문서화, business impact analysis
- Context: Uses vulnerability scan results 에 inform threat priorities

### 3. 아키텍처 보안 Review
- Use Task tool 와 함께 subagent_type="backend-api-보안::backend-아키텍트"
- Prompt: "Review 아키텍처 위한 보안 weaknesses 에서: $ARGUMENTS. Evaluate service boundaries, data flow 보안, authentication/authorization 아키텍처, encryption 구현, network segmentation. 설계 zero-trust 아키텍처 patterns. Reference threat model 및 vulnerability findings."
- Output: 보안 아키텍처 assessment, zero-trust 설계 recommendations, 서비스 메시 보안 requirements, data classification matrix
- Context: Incorporates threat model 에 address architectural vulnerabilities

## Phase 2: Vulnerability Remediation

### 4. 중요한 Vulnerability Fixes
- Use Task tool 와 함께 subagent_type="보안-auditor"
- Prompt: "Coordinate immediate remediation of 중요한 vulnerabilities (CVSS 7+) 에서: $ARGUMENTS. Fix SQL injections 와 함께 parameterized queries, XSS 와 함께 output encoding, authentication bypasses 와 함께 안전한 session management, insecure deserialization 와 함께 input validation. Apply 보안 patches 위한 CVEs."
- Output: Patched code 와 함께 vulnerability fixes, 보안 patch 문서화, 회귀 테스트 requirements
- Context: Addresses high-priority items 에서 vulnerability assessment

### 5. Backend 보안 Hardening
- Use Task tool 와 함께 subagent_type="backend-api-보안::backend-보안-coder"
- Prompt: "Implement 포괄적인 backend 보안 controls 위한: $ARGUMENTS. Add input validation 와 함께 OWASP ESAPI, implement 속도 제한 및 DDoS protection, 안전한 API endpoints 와 함께 OAuth2/JWT validation, add encryption 위한 data 에서 rest/transit 사용하여 AES-256/TLS 1.3. Implement 안전한 logging 없이 PII exposure."
- Output: Hardened API endpoints, validation middleware, encryption 구현, 안전한 구성 templates
- Context: 구축합니다 upon vulnerability fixes 와 함께 preventive controls

### 6. Frontend 보안 구현
- Use Task tool 와 함께 subagent_type="frontend-mobile-보안::frontend-보안-coder"
- Prompt: "Implement frontend 보안 measures 위한: $ARGUMENTS. Configure CSP headers 와 함께 nonce-based policies, implement XSS prevention 와 함께 DOMPurify, 안전한 authentication flows 와 함께 PKCE OAuth2, add SRI 위한 external resources, implement 안전한 cookie handling 와 함께 SameSite/HttpOnly/안전한 flags."
- Output: 안전한 frontend components, CSP policy 구성, authentication flow 구현, 보안 headers 구성
- Context: Complements backend 보안 와 함께 client-side protections

### 7. Mobile 보안 Hardening
- Use Task tool 와 함께 subagent_type="frontend-mobile-보안::mobile-보안-coder"
- Prompt: "Implement mobile app 보안 위한: $ARGUMENTS. Add certificate pinning, implement biometric authentication, 안전한 local storage 와 함께 encryption, obfuscate code 와 함께 ProGuard/R8, implement anti-tampering 및 root/jailbreak detection, 안전한 IPC communications."
- Output: Hardened mobile application, 보안 구성 files, obfuscation rules, certificate pinning 구현
- Context: Extends 보안 에 mobile platforms if applicable

## Phase 3: 보안 Controls 구현

### 8. Authentication 및 Authorization Enhancement
- Use Task tool 와 함께 subagent_type="보안-auditor"
- Prompt: "Implement 현대적인 authentication system 위한: $ARGUMENTS. Deploy OAuth2/OIDC 와 함께 PKCE, implement MFA 와 함께 TOTP/WebAuthn/FIDO2, add risk-based authentication, implement RBAC/ABAC 와 함께 principle of least privilege, add session management 와 함께 안전한 token rotation."
- Output: Authentication service 구성, MFA 구현, authorization policies, session management system
- Context: Strengthens access controls based 에 아키텍처 review

### 9. Infrastructure 보안 Controls
- Use Task tool 와 함께 subagent_type="배포-strategies::배포-엔지니어"
- Prompt: "Deploy infrastructure 보안 controls 위한: $ARGUMENTS. Configure WAF rules 위한 OWASP protection, implement network segmentation 와 함께 micro-segmentation, deploy IDS/IPS systems, configure cloud 보안 groups 및 NACLs, implement DDoS protection 와 함께 속도 제한 및 geo-차단."
- Output: WAF 구성, network 보안 policies, IDS/IPS rules, cloud 보안 configurations
- Context: 구현합니다 network-level defenses

### 10. Secrets Management 구현
- Use Task tool 와 함께 subagent_type="배포-strategies::배포-엔지니어"
- Prompt: "Implement enterprise secrets management 위한: $ARGUMENTS. Deploy HashiCorp Vault 또는 AWS Secrets 관리자, implement secret rotation policies, remove hardcoded secrets, configure least-privilege IAM roles, implement encryption key management 와 함께 HSM support."
- Output: Secrets management 구성, rotation policies, IAM role definitions, key management procedures
- Context: Eliminates secrets exposure vulnerabilities

## Phase 4: Validation 및 규정 준수

### 11. Penetration 테스트 및 Validation
- Use Task tool 와 함께 subagent_type="보안-auditor"
- Prompt: "Execute 포괄적인 penetration 테스트 위한: $ARGUMENTS. Perform authenticated 및 unauthenticated 테스트, API 보안 테스트, 비즈니스 로직 테스트, privilege escalation attempts. Use Burp Suite, Metasploit, 및 custom exploits. Validate all 보안 controls effectiveness."
- Output: 침투 테스트 report, proof-of-concept exploits, remediation validation, 보안 control effectiveness metrics
- Context: 검증합니다 all implemented 보안 measures

### 12. 규정 준수 및 Standards Verification
- Use Task tool 와 함께 subagent_type="보안-auditor"
- Prompt: "Verify 규정 준수 와 함께 보안 frameworks 위한: $ARGUMENTS. Validate against OWASP ASVS Level 2, CIS Benchmarks, SOC2 Type II requirements, GDPR/CCPA privacy controls, HIPAA/PCI-DSS if applicable. Generate 규정 준수 attestation reports."
- Output: 규정 준수 assessment report, gap analysis, remediation requirements, audit evidence collection
- Context: 보장합니다 regulatory 및 industry standard 규정 준수

### 13. 보안 모니터링 및 SIEM 통합
- Use Task tool 와 함께 subagent_type="incident-response::devops-troubleshooter"
- Prompt: "Implement 보안 모니터링 및 SIEM 위한: $ARGUMENTS. Deploy Splunk/ELK/Sentinel 통합, configure 보안 event correlation, implement behavioral analytics 위한 anomaly detection, set up 자동화된 incident response playbooks, create 보안 dashboards 및 alerting."
- Output: SIEM 구성, correlation rules, incident response playbooks, 보안 dashboards, alert definitions
- Context: 설정합니다 continuous 보안 모니터링

## 구성 Options
- scanning_depth: "quick" | "standard" | "포괄적인" (default: 포괄적인)
- compliance_frameworks: ["OWASP", "CIS", "SOC2", "GDPR", "HIPAA", "PCI-DSS"]
- remediation_priority: "cvss_score" | "exploitability" | "business_impact"
- monitoring_integration: "splunk" | "elastic" | "sentinel" | "custom"
- authentication_methods: ["oauth2", "saml", "mfa", "biometric", "passwordless"]

## Success Criteria
- All 중요한 vulnerabilities (CVSS 7+) remediated
- OWASP Top 10 vulnerabilities addressed
- Zero high-risk findings 에서 penetration 테스트
- 규정 준수 frameworks validation passed
- 보안 모니터링 detecting 및 alerting 에 threats
- Incident response time < 15 minutes 위한 중요한 alerts
- SBOM generated 및 vulnerabilities tracked
- All secrets managed 통해 안전한 vault
- Authentication 구현합니다 MFA 및 안전한 session management
- 보안 테스트합니다 integrated into CI/CD 파이프라인

## Coordination Notes
- Each phase 제공합니다 detailed findings that inform subsequent phases
- 보안-auditor agent 조정합니다 와 함께 domain-specific agents 위한 fixes
- All code changes undergo 보안 review 이전 구현
- Continuous feedback loop 사이 assessment 및 remediation
- 보안 findings tracked 에서 중앙 집중식 vulnerability management system
- Regular 보안 검토합니다 scheduled post-구현

보안 hardening target: $ARGUMENTS