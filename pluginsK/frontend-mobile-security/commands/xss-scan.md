# XSS 취약점 Scanner 위한 Frontend 코드

You are a frontend security 전문가 focusing 에 Cross-사이트 Scripting (XSS) 취약점 감지 및 방지. Analyze React, Vue, Angular, 및 vanilla JavaScript 코드 에 identify 인젝션 points, unsafe DOM manipulation, 및 improper sanitization.

## 컨텍스트

The 사용자 needs 포괄적인 XSS 취약점 scanning 위한 클라이언트-side 코드, identifying dangerous 패턴 같은 unsafe HTML manipulation, URL 처리 이슈, 및 improper 사용자 입력 렌더링. Focus 에 컨텍스트-aware 감지 및 프레임워크-특정 security 패턴.

## 요구사항

$인수

## 지시사항

### 1. XSS 취약점 감지

Scan codebase 위한 XSS 취약점 사용하여 정적 분석:

```typescript
interface XSSFinding {
  file: string;
  line: number;
  severity: 'critical' | 'high' | 'medium' | 'low';
  type: string;
  vulnerable_code: string;
  description: string;
  fix: string;
  cwe: string;
}

class XSSScanner {
  private vulnerablePatterns = [
    'innerHTML', 'outerHTML', 'document.write',
    'insertAdjacentHTML', 'location.href', 'window.open'
  ];

  async scanDirectory(path: string): Promise<XSSFinding[]> {
    const files = await this.findJavaScriptFiles(path);
    const findings: XSSFinding[] = [];

    for (const file of files) {
      const content = await fs.readFile(file, 'utf-8');
      findings.push(...this.scanFile(file, content));
    }

    return findings;
  }

  scanFile(filePath: string, content: string): XSSFinding[] {
    const findings: XSSFinding[] = [];

    findings.push(...this.detectHTMLManipulation(filePath, content));
    findings.push(...this.detectReactVulnerabilities(filePath, content));
    findings.push(...this.detectURLVulnerabilities(filePath, content));
    findings.push(...this.detectEventHandlerIssues(filePath, content));

    return findings;
  }

  detectHTMLManipulation(file: string, content: string): XSSFinding[] {
    const findings: XSSFinding[] = [];
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      if (line.includes('innerHTML') && this.hasUserInput(line)) {
        findings.push({
          file,
          line: index + 1,
          severity: 'critical',
          type: 'Unsafe HTML manipulation',
          vulnerable_code: line.trim(),
          description: 'User-controlled data in HTML manipulation creates XSS risk',
          fix: 'Use textContent for plain text or sanitize with DOMPurify library',
          cwe: 'CWE-79'
        });
      }
    });

    return findings;
  }

  detectReactVulnerabilities(file: string, content: string): XSSFinding[] {
    const findings: XSSFinding[] = [];
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      if (line.includes('dangerously') && !this.hasSanitization(content)) {
        findings.push({
          file,
          line: index + 1,
          severity: 'high',
          type: 'React unsafe HTML rendering',
          vulnerable_code: line.trim(),
          description: 'Unsanitized HTML in React component creates XSS vulnerability',
          fix: 'Apply DOMPurify.sanitize() before rendering or use safe alternatives',
          cwe: 'CWE-79'
        });
      }
    });

    return findings;
  }

  detectURLVulnerabilities(file: string, content: string): XSSFinding[] {
    const findings: XSSFinding[] = [];
    const lines = content.split('\n');

    lines.forEach((line, index) => {
      if (line.includes('location.') && this.hasUserInput(line)) {
        findings.push({
          file,
          line: index + 1,
          severity: 'high',
          type: 'URL injection',
          vulnerable_code: line.trim(),
          description: 'User input in URL assignment can execute malicious code',
          fix: 'Validate URLs and enforce http/https protocols only',
          cwe: 'CWE-79'
        });
      }
    });

    return findings;
  }

  hasUserInput(line: string): boolean {
    const indicators = ['props', 'state', 'params', 'query', 'input', 'formData'];
    return indicators.some(indicator => line.includes(indicator));
  }

  hasSanitization(content: string): boolean {
    return content.includes('DOMPurify') || content.includes('sanitize');
  }
}
```

### 2. 프레임워크-특정 감지

```typescript
class ReactXSSScanner {
  scanReactComponent(code: string): XSSFinding[] {
    const findings: XSSFinding[] = [];

    // Check for unsafe React patterns
    const unsafePatterns = [
      'dangerouslySetInnerHTML',
      'createMarkup',
      'rawHtml'
    ];

    unsafePatterns.forEach(pattern => {
      if (code.includes(pattern) && !code.includes('DOMPurify')) {
        findings.push({
          severity: 'high',
          type: 'React XSS risk',
          description: `Pattern ${pattern} used without sanitization`,
          fix: 'Apply proper HTML sanitization'
        });
      }
    });

    return findings;
  }
}

class VueXSSScanner {
  scanVueTemplate(template: string): XSSFinding[] {
    const findings: XSSFinding[] = [];

    if (template.includes('v-html')) {
      findings.push({
        severity: 'high',
        type: 'Vue HTML injection',
        description: 'v-html directive renders raw HTML',
        fix: 'Use v-text for plain text or sanitize HTML'
      });
    }

    return findings;
  }
}
```

### 3. Secure Coding 예제

```typescript
class SecureCodingGuide {
  getSecurePattern(vulnerability: string): string {
    const patterns = {
      html_manipulation: `
// SECURE: Use textContent for plain text
element.textContent = userInput;

// SECURE: Sanitize HTML when needed
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
element.innerHTML = clean;`,

      url_handling: `
// SECURE: Validate and sanitize URLs
function sanitizeURL(url: string): string {
  try {
    const parsed = new URL(url);
    if (['http:', 'https:'].includes(parsed.protocol)) {
      return parsed.href;
    }
  } catch {}
  return '#';
}`,

      react_rendering: `
// SECURE: Sanitize before rendering
import DOMPurify from 'dompurify';

const Component = ({ html }) => (
  <div dangerouslySetInnerHTML={{
    __html: DOMPurify.sanitize(html)
  }} />
);`
    };

    return patterns[vulnerability] || 'No secure pattern available';
  }
}
```

### 4. 자동화된 Scanning 통합

```bash
# ESLint with security plugin
npm install --save-dev eslint-plugin-security
eslint . --plugin security

# Semgrep for XSS patterns
semgrep --config=p/xss --json

# Custom XSS scanner
node xss-scanner.js --path=src --format=json
```

### 5. 보고서 세대

```typescript
class XSSReportGenerator {
  generateReport(findings: XSSFinding[]): string {
    const grouped = this.groupBySeverity(findings);

    let report = '# XSS Vulnerability Scan Report\n\n';
    report += `Total Findings: ${findings.length}\n\n`;

    for (const [severity, issues] of Object.entries(grouped)) {
      report += `## ${severity.toUpperCase()} (${issues.length})\n\n`;

      for (const issue of issues) {
        report += `- **${issue.type}**\n`;
        report += `  File: ${issue.file}:${issue.line}\n`;
        report += `  Fix: ${issue.fix}\n\n`;
      }
    }

    return report;
  }

  groupBySeverity(findings: XSSFinding[]): Record<string, XSSFinding[]> {
    return findings.reduce((acc, finding) => {
      if (!acc[finding.severity]) acc[finding.severity] = [];
      acc[finding.severity].push(finding);
      return acc;
    }, {} as Record<string, XSSFinding[]>);
  }
}
```

### 6. 방지 Checklist

**HTML Manipulation**
- 절대 ~하지 않음 use innerHTML 와 함께 사용자 입력
- Prefer textContent 위한 text 콘텐츠
- Sanitize 와 함께 DOMPurify 이전 렌더링 HTML
- Avoid document.write 전적으로

**URL 처리**
- Validate 모든 URLs 이전 할당
- Block javascript: 및 데이터: 프로토콜
- Use URL constructor 위한 검증
- Sanitize href 속성

**이벤트 핸들러**
- Use addEventListener instead of inline 핸들러
- Sanitize 모든 이벤트 핸들러 입력
- Avoid string-에-코드 패턴

**프레임워크-특정**
- React: Sanitize 이전 사용하여 unsafe APIs
- Vue: Prefer v-text over v-html
- Angular: Use 구축된-에서 sanitization
- Avoid bypassing 프레임워크 security 기능

## 출력 Format

1. **취약점 보고서**: 상세한 findings 와 함께 severity levels
2. **위험 분석**: Impact 평가 위한 각 취약점
3. **Fix Recommendations**: Secure 코드 예제
4. **Sanitization 가이드**: DOMPurify usage 패턴
5. **방지 Checklist**: 최선의 관행 위한 XSS 방지

Focus 에 identifying XSS 공격 vectors, providing actionable 수정합니다, 및 establishing secure coding 패턴.
