---
name: sast-configuration
description: Configure Static Application 보안 테스트 (SAST) tools 위한 자동화된 vulnerability detection 에서 application code. Use when setting up 보안 scanning, implementing DevSecOps practices, 또는 automating code vulnerability detection.
---

# SAST 구성

Static Application 보안 테스트 (SAST) tool setup, 구성, 및 custom rule creation 위한 포괄적인 보안 scanning 전반에 걸쳐 multiple programming languages.

## Overview

This skill 제공합니다 포괄적인 guidance 위한 setting up 및 configuring SAST tools 포함하여 Semgrep, SonarQube, 및 CodeQL. Use this skill when you need 에:

- Set up SAST scanning 에서 CI/CD pipelines
- Create custom 보안 rules 위한 your codebase
- Configure quality gates 및 규정 준수 policies
- Optimize scan 성능 및 reduce false positives
- Integrate multiple SAST tools 위한 defense-에서-depth

## Core Capabilities

### 1. Semgrep 구성
- Custom rule creation 와 함께 패턴 matching
- Language-specific 보안 rules (Python, JavaScript, Go, Java, etc.)
- CI/CD 통합 (GitHub Actions, GitLab CI, Jenkins)
- False positive tuning 및 rule 최적화
- Organizational policy enforcement

### 2. SonarQube Setup
- Quality gate 구성
- 보안 hotspot analysis
- Code coverage 및 기술 부채 tracking
- Custom quality profiles 위한 languages
- Enterprise 통합 와 함께 LDAP/SAML

### 3. CodeQL Analysis
- GitHub 고급 보안 통합
- Custom query development
- Vulnerability variant analysis
- 보안 research workflows
- SARIF result processing

## 빠른 시작

### Initial Assessment
1. Identify primary programming languages 에서 your codebase
2. Determine 규정 준수 requirements (PCI-DSS, SOC 2, etc.)
3. Choose SAST tool based 에 language support 및 통합 needs
4. Review baseline scan 에 understand current 보안 posture

### 기본 Setup
```bash
# Semgrep quick start
pip install semgrep
semgrep --config=auto --error

# SonarQube with Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# CodeQL CLI setup
gh extension install github/gh-codeql
codeql database create mydb --language=python
```

## Reference 문서화

- [Semgrep Rule Creation](references/semgrep-rules.md) - 패턴-based 보안 rule development
- [SonarQube Configuration](references/sonarqube-config.md) - Quality gates 및 profiles
- [CodeQL Setup Guide](references/codeql-setup.md) - Query development 및 workflows

## Templates & Assets

- [semgrep-config.yml](assets/semgrep-config.yml) - Production-ready Semgrep 구성
- [sonarqube-settings.xml](assets/sonarqube-settings.xml) - SonarQube quality profile template
- [run-sast.sh](scripts/run-sast.sh) - 자동화된 SAST execution script

## 통합 Patterns

### CI/CD 파이프라인 통합
```yaml
# GitHub Actions example
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
  with:
    config: >-
      p/security-audit
      p/owasp-top-ten
```

### Pre-commit Hook
```bash
# .pre-commit-config.yaml
- repo: https://github.com/returntocorp/semgrep
  rev: v1.45.0
  hooks:
    - id: semgrep
      args: ['--config=auto', '--error']
```

## 모범 사례

1. **Start 와 함께 Baseline**
   - Run initial scan 에 establish 보안 baseline
   - Prioritize 중요한 및 high severity findings
   - Create remediation roadmap

2. **Incremental Adoption**
   - Begin 와 함께 보안-focused rules
   - Gradually add 코드 품질 rules
   - Implement 차단 only 위한 중요한 issues

3. **False Positive Management**
   - Document legitimate suppressions
   - Create allow lists 위한 known safe patterns
   - Regularly review suppressed findings

4. **성능 최적화**
   - Exclude test files 및 generated code
   - Use incremental scanning 위한 large codebases
   - Cache scan results 에서 CI/CD

5. **Team Enablement**
   - Provide 보안 training 위한 developers
   - Create internal 문서화 위한 common patterns
   - Establish 보안 champions program

## Common Use Cases

### New Project Setup
```bash
./scripts/run-sast.sh --setup --language python --tools semgrep,sonarqube
```

### Custom Rule Development
```yaml
# See references/semgrep-rules.md for detailed examples
rules:
  - id: hardcoded-jwt-secret
    pattern: jwt.encode($DATA, "...", ...)
    message: JWT secret should not be hardcoded
    severity: ERROR
```

### 규정 준수 Scanning
```bash
# PCI-DSS focused scan
semgrep --config p/pci-dss --json -o pci-scan-results.json
```

## Troubleshooting

### High False Positive Rate
- Review 및 tune rule sensitivity
- Add path filters 에 exclude test files
- Use nostmt metadata 위한 noisy patterns
- Create organization-specific rule exceptions

### 성능 Issues
- Enable incremental scanning
- Parallelize scans 전반에 걸쳐 modules
- Optimize rule patterns 위한 efficiency
- Cache dependencies 및 scan results

### 통합 Failures
- Verify API tokens 및 credentials
- Check network connectivity 및 proxy settings
- Review SARIF output format compatibility
- Validate CI/CD runner permissions

## Related Skills

- [OWASP Top 10 Checklist](../owasp-top10-checklist/SKILL.md)
- [Container Security](../container-security/SKILL.md)
- [Dependency Scanning](../dependency-scanning/SKILL.md)

## Tool Comparison

| Tool | Best 위한 | Language Support | Cost | 통합 |
|------|----------|------------------|------|-------------|
| Semgrep | Custom rules, fast scans | 30+ languages | Free/Enterprise | Excellent |
| SonarQube | 코드 품질 + 보안 | 25+ languages | Free/Commercial | Good |
| CodeQL | Deep analysis, research | 10+ languages | Free (OSS) | GitHub native |

## Next Steps

1. Complete initial SAST tool setup
2. Run baseline 보안 scan
3. Create custom rules 위한 organization-specific patterns
4. Integrate into CI/CD 파이프라인
5. Establish 보안 gate policies
6. Train development team 에 findings 및 remediation
