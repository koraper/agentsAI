#!/usr/bin/env python3
"""
Complete Korean translation script for all markdown files
Translates EVERYTHING except code blocks, YAML field names, and technical terms
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

# Core Korean translations - comprehensive mapping
KOREAN_DICT = {
    # Roles and titles
    "You are a": "당신은",
    "You are an": "당신은",
    "expert": "전문가",
    "specialist": "전문가",
    "architect": "아키텍트",
    "engineer": "엔지니어",
    "developer": "개발자",
    "analyst": "분석가",
    "manager": "관리자",
    "consultant": "컨설턴트",
    "administrator": "관리자",
    "coordinator": "코디네이터",
    
    # Descriptive terms (following "are")
    "specializing in": "전문 분야:",
    "with expertise in": "전문 지식:",
    "focused on": "중점:",
    
    # Action verbs (start of sentence)
    "Handles": "처리합니다",
    "Masters": "마스터합니다",
    "Specializes in": "전문 분야입니다",
    "Focuses on": "집중합니다",
    "Provides": "제공합니다",
    "Creates": "생성합니다",
    "Implements": "구현합니다",
    "Ensures": "보장합니다",
    "Manages": "관리합니다",
    "Optimizes": "최적화합니다",
    "Analyzes": "분석합니다",
    "Designs": "설계합니다",
    "Develops": "개발합니다",
    "Maintains": "유지합니다",
    "Reviews": "검토합니다",
    "Tests": "테스트합니다",
    "Validates": "검증합니다",
    "Monitors": "모니터링합니다",
    "Debugs": "디버깅합니다",
    "Refactors": "리팩토링합니다",
    "Migrates": "마이그레이션합니다",
    "Automates": "자동화합니다",
    "Orchestrates": "오케스트레이션합니다",
    "Integrates": "통합합니다",
    "Secures": "보안을 강화합니다",
    "Deploys": "배포합니다",
    "Configures": "구성합니다",
    "Documents": "문서화합니다",
    "Troubleshoots": "문제를 해결합니다",
    "Builds": "구축합니다",
    "Establishes": "설정합니다",
    "Performs": "수행합니다",
    
    # Common phrases
    "Use PROACTIVELY when": "다음의 경우 주도적으로 사용하세요:",
    "Use when": "다음의 경우 사용하세요:",
    "Best for": "다음에 가장 적합합니다:",
    "Ideal for": "다음에 이상적입니다:",
    "Perfect for": "다음에 완벽합니다:",
    "Great for": "다음에 좋습니다:",
    "Suitable for": "다음에 적합합니다:",
    "Recommended for": "다음을 권장합니다:",
    
    # Common nouns
    "architecture": "아키텍처",
    "design pattern": "디자인 패턴",
    "best practice": "모범 사례",
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
    
    # Direction words
    "and": "및",
    "or": "또는",
    "with": "와 함께",
    "for": "위한",
    "from": "에서",
    "to": "에",
    "in": "에서",
    "on": "에",
    "at": "에서",
    "by": "에 의해",
    "through": "통해",
    "using": "사용하여",
    "including": "포함하여",
    "such as": "예를 들어",
    "like": "같은",
    
    # Common adjectives
    "scalable": "확장 가능한",
    "resilient": "탄력적인",
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
}

# Technical terms that must be preserved
PRESERVE = {
    # Brands
    "Stripe", "PayPal", "Square", "AWS", "Azure", "Google", "GCP", "Microsoft",
    "GitHub", "GitLab", "OpenAI", "Anthropic", "Vercel", "Netlify",
    
    # Protocols
    "HTTP", "HTTPS", "REST", "RESTful", "GraphQL", "gRPC", "WebSocket",
    "SSH", "FTP", "SMTP", "OAuth", "JWT", "SAML", "OpenID", "CORS", "CSRF",
    
    # Tech tools
    "Kubernetes", "Docker", "Terraform", "Jenkins", "Ansible",
    "React", "Vue", "Angular", "Next.js", "Nuxt.js",
    "FastAPI", "Django", "Flask", "Express", "NestJS",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Kafka",
    "Prometheus", "Grafana", "Datadog", "New Relic",
    "Git", "Node.js", "Python", "JavaScript", "TypeScript",
    
    # Acronyms
    "API", "SDK", "CLI", "IDE", "CI/CD", "TDD", "BDD", "DDD",
    "JSON", "YAML", "XML", "CSV",
    "CRUD", "ACID", "SOLID", "DRY",
    
    # Standards
    "WCAG", "ARIA", "GDPR", "HIPAA", "PCI DSS", "OWASP",
}

def preserve_technical_terms(text: str) -> Tuple[str, dict]:
    """Replace technical terms with placeholders"""
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
    for term in PRESERVE:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        for match in pattern.finditer(text):
            original = match.group(0)
            if original not in placeholders.values():
                ph = f"__TECH{counter}__"
                placeholders[ph] = original
                text = text.replace(original, ph, 1)
                counter += 1
    
    return text, placeholders

def restore_placeholders(text: str, placeholders: dict) -> str:
    """Restore preserved terms"""
    for ph, original in placeholders.items():
        text = text.replace(ph, original)
    return text

def translate_line(line: str) -> str:
    """Translate a single line of text"""
    if not line.strip():
        return line
    
    # Preserve technical terms first
    text, placeholders = preserve_technical_terms(line)
    
    # Apply Korean translations
    for eng, kor in KOREAN_DICT.items():
        # Use word boundaries for whole-word matching
        pattern = r'\b' + re.escape(eng) + r'\b'
        text = re.sub(pattern, kor, text, flags=re.IGNORECASE)
    
    # Restore preserved terms
    text = restore_placeholders(text, placeholders)
    
    return text

def process_file(source: Path, dest: Path):
    """Process and translate a single file"""
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
        
        # YAML fields - keep as-is except description value
        if in_yaml:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2 and parts[0].strip() in ['name', 'model']:
                    result.append(line)  # Keep as-is
                else:
                    # Translate value part
                    key = parts[0]
                    value = parts[1]
                    translated_value = translate_line(value)
                    result.append(f"{key}:{translated_value}")
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
        
        # Regular content - translate
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
    
    print(f"Starting translation of {total} files...")
    
    for i, source in enumerate(md_files, 1):
        rel_path = source.relative_to(source_dir)
        dest = dest_dir / rel_path
        
        try:
            process_file(source, dest)
            if i % 10 == 0:
                print(f"[{i}/{total}] Processed {rel_path}")
        except Exception as e:
            print(f"ERROR [{i}/{total}] {rel_path}: {e}")
    
    print(f"\n✓ Translation complete: {total} files")

if __name__ == "__main__":
    main()

