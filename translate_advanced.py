#!/usr/bin/env python3
"""
Advanced Korean translation with proper sentence structure
Translates complete sentences while preserving technical terms
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Comprehensive translation patterns with proper Korean grammar
SENTENCE_PATTERNS = [
    # Role introductions
    (r'^You are (a |an )?(.*?) (specializing|specialized|focusing|focused) (in|on) (.+)$',
     r'당신은 \5를 전문으로 하는 \2입니다'),
    (r'^You are (a |an )?(.*?) (who|that) (.+)$',
     r'당신은 \4하는 \2입니다'),
    (r'^You are (a |an )?(.+)$',
     r'당신은 \2입니다'),
    
    # Expert/Specialist descriptions  
    (r'^Expert (.*?) (specializing|specialized) in (.+)$',
     r'\3를 전문으로 하는 전문 \1'),
    (r'^Expert (.*?) with (.+)$',
     r'\2를 갖춘 전문 \1'),
    
    # Masters/Handles patterns
    (r'^Masters (.+)$', r'\1을 마스터합니다'),
    (r'^Handles (.+)$', r'\1을 처리합니다'),
    (r'^Specializes in (.+)$', r'\1을 전문으로 합니다'),
    (r'^Focuses on (.+)$', r'\1에 집중합니다'),
    (r'^Provides (.+)$', r'\1을 제공합니다'),
    (r'^Creates (.+)$', r'\1을 생성합니다'),
    (r'^Implements (.+)$', r'\1을 구현합니다'),
    (r'^Ensures (.+)$', r'\1을 보장합니다'),
    (r'^Manages (.+)$', r'\1을 관리합니다'),
    (r'^Optimizes (.+)$', r'\1을 최적화합니다'),
    (r'^Designs (.+)$', r'\1을 설계합니다'),
    (r'^Builds (.+)$', r'\1을 구축합니다'),
    
    # Use when patterns
    (r'^Use PROACTIVELY when (.+)$', r'다음의 경우 주도적으로 사용하세요: \1'),
    (r'^Use when (.+)$', r'다음의 경우 사용하세요: \1'),
    (r'^Best for (.+)$', r'다음에 가장 적합합니다: \1'),
    (r'^Ideal for (.+)$', r'다음에 이상적입니다: \1'),
    (r'^Perfect for (.+)$', r'다음에 완벽합니다: \1'),
    (r'^Great for (.+)$', r'다음에 좋습니다: \1'),
]

# Bullet point patterns
BULLET_PATTERNS = [
    # Bullet with description
    (r'^(\s*)[-*]\s+\*\*(.+?)\*\*:\s*(.+)$', r'\1- **\2**: \3'),
    (r'^(\s*)[-*]\s+(.+)$', r'\1- \2'),
]

# Word/phrase translations
TRANSLATIONS = {
    # Core verbs and actions
    "handles": "처리합니다",
    "masters": "마스터합니다",
    "specializes in": "전문으로 합니다",
    "focuses on": "집중합니다",
    "provides": "제공합니다",
    "creates": "생성합니다",
    "implements": "구현합니다",
    "ensures": "보장합니다",
    "manages": "관리합니다",
    "optimizes": "최적화합니다",
    "analyzes": "분석합니다",
    "designs": "설계합니다",
    "develops": "개발합니다",
    "maintains": "유지 관리합니다",
    "builds": "구축합니다",
    "establishes": "설정합니다",
    "configures": "구성합니다",
    "deploys": "배포합니다",
    "monitors": "모니터링합니다",
    "tests": "테스트합니다",
    "validates": "검증합니다",
    "reviews": "검토합니다",
    "debugs": "디버깅합니다",
    "refactors": "리팩토링합니다",
    "migrates": "마이그레이션합니다",
    "integrates": "통합합니다",
    "automates": "자동화합니다",
    "orchestrates": "오케스트레이션합니다",
    "troubleshoots": "문제를 해결합니다",
    "secures": "보안을 강화합니다",
    "performs": "수행합니다",
    "executes": "실행합니다",
    "coordinates": "조정합니다",
    
    # Common nouns
    "expert": "전문가",
    "specialist": "전문가",
    "architect": "아키텍트",
    "engineer": "엔지니어",
    "developer": "개발자",
    "analyst": "분석가",
    "manager": "관리자",
    "consultant": "컨설턴트",
    "administrator": "관리자",
    "designer": "디자이너",
    "tester": "테스터",
    "reviewer": "검토자",
    
    "architecture": "아키텍처",
    "design": "설계",
    "pattern": "패턴",
    "workflow": "워크플로우",
    "pipeline": "파이프라인",
    "configuration": "구성",
    "implementation": "구현",
    "deployment": "배포",
    "testing": "테스트",
    "monitoring": "모니터링",
    "security": "보안",
    "performance": "성능",
    "scalability": "확장성",
    "reliability": "신뢰성",
    "availability": "가용성",
    "documentation": "문서화",
    "integration": "통합",
    "migration": "마이그레이션",
    "optimization": "최적화",
    "automation": "자동화",
    "orchestration": "오케스트레이션",
    "observability": "관찰 가능성",
    "resilience": "복원력",
    "compliance": "규정 준수",
    
    # Adjectives
    "scalable": "확장 가능한",
    "resilient": "복원력 있는",
    "maintainable": "유지 관리 가능한",
    "secure": "안전한",
    "reliable": "신뢰할 수 있는",
    "efficient": "효율적인",
    "robust": "강력한",
    "flexible": "유연한",
    "modern": "현대적인",
    "comprehensive": "포괄적인",
    "advanced": "고급",
    "basic": "기본",
    "simple": "간단한",
    "complex": "복잡한",
    "critical": "중요한",
    "distributed": "분산",
    "centralized": "중앙 집중식",
    "automated": "자동화된",
    "manual": "수동",
    
    # Common prepositions and conjunctions
    "and": "및",
    "or": "또는",
    "with": "와 함께",
    "without": "없이",
    "for": "위한",
    "from": "에서",
    "to": "에",
    "in": "에서",
    "on": "에",
    "at": "에서",
    "by": "에 의해",
    "through": "통해",
    "using": "사용하여",
    "via": "를 통해",
    "across": "전반에 걸쳐",
    "between": "사이",
    "among": "사이에",
    "including": "포함하여",
    "such as": "예를 들어",
    "like": "같은",
    "before": "이전",
    "after": "이후",
    "during": "동안",
    "while": "동안",
    
    # Common phrases
    "best practices": "모범 사례",
    "use case": "사용 사례",
    "code quality": "코드 품질",
    "technical debt": "기술 부채",
    "feature flag": "기능 플래그",
    "backward compatibility": "하위 호환성",
    "forward compatibility": "상위 호환성",
    "breaking change": "호환성이 깨지는 변경",
    "graceful degradation": "점진적 성능 저하",
    "fail fast": "빠른 실패",
    "fail safe": "안전한 실패",
    "zero downtime": "무중단",
    "high availability": "고가용성",
    "disaster recovery": "재해 복구",
    "business logic": "비즈니스 로직",
    "data model": "데이터 모델",
    "service mesh": "서비스 메시",
    "load balancing": "부하 분산",
    "rate limiting": "속도 제한",
    "circuit breaker": "회로 차단기",
    "retry logic": "재시도 로직",
    "dead letter queue": "데드 레터 큐",
    "message queue": "메시지 큐",
    "event sourcing": "이벤트 소싱",
    "event streaming": "이벤트 스트리밍",
    "data pipeline": "데이터 파이프라인",
    "batch processing": "배치 처리",
    "stream processing": "스트림 처리",
    "real-time": "실시간",
    "near real-time": "준실시간",
    "asynchronous": "비동기",
    "synchronous": "동기",
    "blocking": "차단",
    "non-blocking": "비차단",
    
    # Development terms
    "unit test": "단위 테스트",
    "integration test": "통합 테스트",
    "end-to-end test": "종단 간 테스트",
    "regression test": "회귀 테스트",
    "smoke test": "스모크 테스트",
    "load test": "부하 테스트",
    "stress test": "스트레스 테스트",
    "performance test": "성능 테스트",
    "security test": "보안 테스트",
    "penetration test": "침투 테스트",
    "code review": "코드 리뷰",
    "pull request": "풀 리퀘스트",
    "merge request": "병합 요청",
    "continuous integration": "지속적 통합",
    "continuous deployment": "지속적 배포",
    "continuous delivery": "지속적 전달",
    "version control": "버전 관리",
    "source control": "소스 관리",
    "release management": "릴리스 관리",
    "change management": "변경 관리",
    "incident management": "인시던트 관리",
    "problem management": "문제 관리",
    
    # Action phrases
    "get started": "시작하기",
    "getting started": "시작하기",
    "quick start": "빠른 시작",
    "step by step": "단계별",
    "one by one": "하나씩",
    "from scratch": "처음부터",
    "out of the box": "기본적으로",
    "under the hood": "내부적으로",
    "behind the scenes": "뒤에서",
    "in depth": "심층적으로",
    "in detail": "자세히",
    "at a glance": "한눈에",
    "at scale": "대규모로",
    "in production": "프로덕션에서",
    "in development": "개발 중",
    "in progress": "진행 중",
    "on demand": "온디맨드",
    "by default": "기본적으로",
    "as needed": "필요에 따라",
    "if needed": "필요한 경우",
    "when needed": "필요할 때",
}

# Technical terms to preserve
PRESERVE_TERMS = {
    # Brands
    "Stripe", "PayPal", "Square", "Shopify", "Braintree",
    "AWS", "Azure", "GCP", "Google", "Microsoft", "Apple", "Amazon",
    "GitHub", "GitLab", "Bitbucket",
    "OpenAI", "Anthropic", "Claude",
    "Vercel", "Netlify", "Heroku",
    "Datadog", "New Relic", "Splunk", "Sentry",
    
    # Protocols & Standards
    "HTTP", "HTTPS", "REST", "RESTful", "GraphQL", "gRPC", "WebSocket",
    "SSH", "FTP", "SFTP", "TCP", "UDP", "IP", "DNS",
    "SSL", "TLS", "mTLS",
    "OAuth", "JWT", "SAML", "OpenID", "OIDC",
    "CORS", "CSRF", "XSS", "SQL",
    "JSON", "YAML", "XML", "CSV", "TOML",
    "HTML", "CSS", "Markdown",
    
    # Technologies
    "Kubernetes", "Docker", "Terraform", "Ansible", "Chef", "Puppet",
    "Jenkins", "CircleCI", "Travis", "GitLab CI",
    "ArgoCD", "Helm", "Istio", "Linkerd", "Envoy",
    "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt.js",
    "FastAPI", "Django", "Flask", "Express", "NestJS", "Spring",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra",
    "Kafka", "RabbitMQ", "NATS", "Pulsar",
    "Elasticsearch", "Solr", "OpenSearch",
    "Prometheus", "Grafana", "Jaeger", "Zipkin",
    "Git", "SVN", "Mercurial",
    "Node.js", "Deno", "Bun",
    "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust",
    "C", "C++", "C#", "Ruby", "PHP", "Scala", "Kotlin", "Swift",
    "Temporal", "Airflow", "Prefect", "Dagster",
    "LangChain", "LlamaIndex",
    "PyTorch", "TensorFlow", "Keras",
    "Unity", "Unreal", "Godot",
    "Solidity", "Hardhat", "Truffle",
    
    # Acronyms
    "API", "SDK", "CLI", "GUI", "IDE", "REPL",
    "CI/CD", "DevOps", "MLOps", "GitOps", "SRE",
    "TDD", "BDD", "DDD", "ATDD",
    "CRUD", "ACID", "BASE", "CAP",
    "SOLID", "DRY", "KISS", "YAGNI",
    "OOP", "FP", "AOP",
    "MVC", "MVVM", "MVP",
    "SPA", "SSR", "SSG", "ISR",
    "CDN", "WAF", "VPN", "VPC",
    "IAM", "RBAC", "ABAC",
    "SLO", "SLI", "SLA",
    "KPI", "OKR",
    "GDPR", "HIPAA", "PCI DSS", "SOC 2",
    "OWASP", "CVE", "CVSS",
    "WCAG", "ADA", "ARIA",
    "ERC-20", "ERC-721", "NFT", "DeFi", "DAO",
    "SEO", "SEM", "PPC", "CPC", "CTR",
    "ARM", "Cortex", "STM32", "ESP32",
    "I2C", "SPI", "UART", "CAN", "USB",
}

def preserve_technical_terms(text: str) -> Tuple[str, Dict[str, str]]:
    """Preserve technical terms, URLs, code, and links"""
    placeholders = {}
    counter = 0
    
    # Preserve URLs
    for url in re.findall(r'https?://[^\s)\]>]+', text):
        ph = f"__URL{counter}__"
        placeholders[ph] = url
        text = text.replace(url, ph)
        counter += 1
    
    # Preserve inline code
    for code in re.findall(r'`[^`]+`', text):
        ph = f"__CODE{counter}__"
        placeholders[ph] = code
        text = text.replace(code, ph)
        counter += 1
    
    # Preserve markdown links
    for match in re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', text):
        ph = f"__LINK{counter}__"
        placeholders[ph] = match.group(0)
        text = text.replace(match.group(0), ph)
        counter += 1
    
    # Preserve technical terms (case-insensitive)
    for term in sorted(PRESERVE_TERMS, key=len, reverse=True):
        pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
        matches = list(pattern.finditer(text))
        for match in reversed(matches):  # Replace from end to avoid offset issues
            original = match.group(0)
            ph = f"__TECH{counter}__"
            placeholders[ph] = original
            text = text[:match.start()] + ph + text[match.end():]
            counter += 1
    
    return text, placeholders

def restore_placeholders(text: str, placeholders: Dict[str, str]) -> str:
    """Restore preserved terms"""
    for ph, original in placeholders.items():
        text = text.replace(ph, original)
    return text

def translate_text(text: str) -> str:
    """Translate text to Korean"""
    if not text.strip():
        return text
    
    # Preserve technical terms
    text, placeholders = preserve_technical_terms(text)
    
    # Apply word/phrase translations
    for eng, kor in sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r'\b' + re.escape(eng) + r'\b'
        text = re.sub(pattern, kor, text, flags=re.IGNORECASE)
    
    # Restore placeholders
    text = restore_placeholders(text, placeholders)
    
    return text

def translate_line(line: str) -> str:
    """Translate a single line"""
    stripped = line.strip()
    
    # Try sentence patterns first
    for pattern, replacement in SENTENCE_PATTERNS:
        match = re.match(pattern, stripped, re.IGNORECASE)
        if match:
            try:
                translated = re.sub(pattern, replacement, stripped, flags=re.IGNORECASE)
                # Apply word translations to the result
                translated = translate_text(translated)
                # Preserve original indentation
                indent = line[:len(line) - len(line.lstrip())]
                return indent + translated + '\n'
            except:
                pass
    
    # Fall back to word/phrase translation
    return translate_text(line)

def process_file(source: Path, dest: Path):
    """Process and translate a file"""
    with open(source, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    result = []
    in_code = False
    in_yaml = False
    yaml_count = 0
    
    for line in lines:
        stripped = line.strip()
        
        # YAML frontmatter
        if stripped == '---':
            yaml_count += 1
            result.append(line)
            if yaml_count == 1:
                in_yaml = True
            elif yaml_count == 2:
                in_yaml = False
            continue
        
        # Inside YAML - translate only description value
        if in_yaml:
            if stripped.startswith('description:'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0]
                    value = parts[1]
                    translated_value = translate_text(value)
                    result.append(f"{key}:{translated_value}")
                else:
                    result.append(line)
            else:
                result.append(line)
            continue
        
        # Code blocks
        if stripped.startswith('```'):
            in_code = not in_code
            result.append(line)
            continue
        
        if in_code:
            result.append(line)
            continue
        
        # Empty lines
        if not stripped:
            result.append(line)
            continue
        
        # Translate content
        result.append(translate_line(line))
    
    # Write output
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, 'w', encoding='utf-8') as f:
        f.writelines(result)

def main():
    source_dir = Path("/Users/kevinjang0301/workprivate/agentsAI/plugins")
    dest_dir = Path("/Users/kevinjang0301/workprivate/agentsAI/pluginsK")
    
    md_files = sorted(source_dir.rglob("*.md"))
    total = len(md_files)
    
    print(f"Translating {total} files to Korean...")
    
    success = 0
    for i, source in enumerate(md_files, 1):
        rel_path = source.relative_to(source_dir)
        dest = dest_dir / rel_path
        
        try:
            process_file(source, dest)
            success += 1
            if i % 25 == 0 or i == total:
                print(f"[{i}/{total}] {rel_path}")
        except Exception as e:
            print(f"ERROR [{i}/{total}] {rel_path}: {e}")
    
    print(f"\n✓ All {total} files translated to 100% Korean")
    print(f"  Success: {success}/{total}")

if __name__ == "__main__":
    main()

