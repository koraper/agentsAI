---
name: dependency-upgrade
description: Manage 주요 종속성 버전 업그레이드합니다 와 함께 compatibility 분석, staged rollout, 및 포괄적인 테스트. Use 때 upgrading 프레임워크 버전, updating 주요 종속성, 또는 managing breaking 변경합니다 에서 라이브러리.
---

# 종속성 업그레이드

마스터 주요 종속성 버전 업그레이드합니다, compatibility 분석, staged 업그레이드 strategies, 및 포괄적인 테스트 approaches.

## 때 에 Use This Skill

- Upgrading 주요 프레임워크 버전
- Updating security-vulnerable 종속성
- Modernizing 레거시 종속성
- 해결하는 종속성 conflicts
- 계획 incremental 업그레이드 경로
- 테스트 compatibility matrices
- Automating 종속성 업데이트합니다

## Semantic Versioning Review

```
MAJOR.MINOR.PATCH (e.g., 2.3.1)

MAJOR: Breaking changes
MINOR: New features, backward compatible
PATCH: Bug fixes, backward compatible

^2.3.1 = >=2.3.1 <3.0.0 (minor updates)
~2.3.1 = >=2.3.1 <2.4.0 (patch updates)
2.3.1 = exact version
```

## 종속성 분석

### Audit 종속성
```bash
# npm
npm outdated
npm audit
npm audit fix

# yarn
yarn outdated
yarn audit

# Check for major updates
npx npm-check-updates
npx npm-check-updates -u  # Update package.json
```

### Analyze 종속성 트리
```bash
# See why a package is installed
npm ls package-name
yarn why package-name

# Find duplicate packages
npm dedupe
yarn dedupe

# Visualize dependencies
npx madge --image graph.png src/
```

## Compatibility 매트릭스

```javascript
// compatibility-matrix.js
const compatibilityMatrix = {
  'react': {
    '16.x': {
      'react-dom': '^16.0.0',
      'react-router-dom': '^5.0.0',
      '@testing-library/react': '^11.0.0'
    },
    '17.x': {
      'react-dom': '^17.0.0',
      'react-router-dom': '^5.0.0 || ^6.0.0',
      '@testing-library/react': '^12.0.0'
    },
    '18.x': {
      'react-dom': '^18.0.0',
      'react-router-dom': '^6.0.0',
      '@testing-library/react': '^13.0.0'
    }
  }
};

function checkCompatibility(packages) {
  // Validate package versions against matrix
}
```

## Staged 업그레이드 전략

### 단계 1: 계획
```bash
# 1. Identify current versions
npm list --depth=0

# 2. Check for breaking changes
# Read CHANGELOG.md and MIGRATION.md

# 3. Create upgrade plan
echo "Upgrade order:
1. TypeScript
2. React
3. React Router
4. Testing libraries
5. Build tools" > UPGRADE_PLAN.md
```

### 단계 2: Incremental 업데이트합니다
```bash
# Don't upgrade everything at once!

# Step 1: Update TypeScript
npm install typescript@latest

# Test
npm run test
npm run build

# Step 2: Update React (one major version at a time)
npm install react@17 react-dom@17

# Test again
npm run test

# Step 3: Continue with other packages
npm install react-router-dom@6

# And so on...
```

### 단계 3: 검증
```javascript
// tests/compatibility.test.js
describe('Dependency Compatibility', () => {
  it('should have compatible React versions', () => {
    const reactVersion = require('react/package.json').version;
    const reactDomVersion = require('react-dom/package.json').version;

    expect(reactVersion).toBe(reactDomVersion);
  });

  it('should not have peer dependency warnings', () => {
    // Run npm ls and check for warnings
  });
});
```

## Breaking 변경 처리

### Identifying Breaking 변경합니다
```bash
# Use changelog parsers
npx changelog-parser react 16.0.0 17.0.0

# Or manually check
curl https://raw.githubusercontent.com/facebook/react/main/CHANGELOG.md
```

### Codemod 위한 자동화된 수정합니다
```bash
# React upgrade codemods
npx react-codeshift <transform> <path>

# Example: Update lifecycle methods
npx react-codeshift \
  --parser tsx \
  --transform react-codeshift/transforms/rename-unsafe-lifecycles.js \
  src/
```

### 사용자 정의 마이그레이션 스크립트
```javascript
// migration-script.js
const fs = require('fs');
const glob = require('glob');

glob('src/**/*.tsx', (err, files) => {
  files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');

    // Replace old API with new API
    content = content.replace(
      /componentWillMount/g,
      'UNSAFE_componentWillMount'
    );

    // Update imports
    content = content.replace(
      /import { Component } from 'react'/g,
      "import React, { Component } from 'react'"
    );

    fs.writeFileSync(file, content);
  });
});
```

## 테스트 전략

### 단위 테스트합니다
```javascript
// Ensure tests pass before and after upgrade
npm run test

// Update test utilities if needed
npm install @testing-library/react@latest
```

### 통합 테스트합니다
```javascript
// tests/integration/app.test.js
describe('App Integration', () => {
  it('should render without crashing', () => {
    render(<App />);
  });

  it('should handle navigation', () => {
    const { getByText } = render(<App />);
    fireEvent.click(getByText('Navigate'));
    expect(screen.getByText('New Page')).toBeInTheDocument();
  });
});
```

### Visual Regression 테스트합니다
```javascript
// visual-regression.test.js
describe('Visual Regression', () => {
  it('should match snapshot', () => {
    const { container } = render(<App />);
    expect(container.firstChild).toMatchSnapshot();
  });
});
```

### E2E 테스트합니다
```javascript
// cypress/e2e/app.cy.js
describe('E2E Tests', () => {
  it('should complete user flow', () => {
    cy.visit('/');
    cy.get('[data-testid="login"]').click();
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

## 자동화된 종속성 업데이트합니다

### Renovate 구성
```json
// renovate.json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["major-update"]
    }
  ],
  "schedule": ["before 3am on Monday"],
  "timezone": "America/New_York"
}
```

### Dependabot 구성
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "team-leads"
    commit-message:
      prefix: "chore"
      include: "scope"
```

## 롤백 Plan

```javascript
// rollback.sh
#!/bin/bash

# Save current state
git stash
git checkout -b upgrade-branch

# Attempt upgrade
npm install package@latest

# Run tests
if npm run test; then
  echo "Upgrade successful"
  git add package.json package-lock.json
  git commit -m "chore: upgrade package"
else
  echo "Upgrade failed, rolling back"
  git checkout main
  git branch -D upgrade-branch
  npm install  # Restore from package-lock.json
fi
```

## 일반적인 업그레이드 패턴

### 잠금 파일 관리
```bash
# npm
npm install --package-lock-only  # Update lock file only
npm ci  # Clean install from lock file

# yarn
yarn install --frozen-lockfile  # CI mode
yarn upgrade-interactive  # Interactive upgrades
```

### Peer 종속성 해결
```bash
# npm 7+: strict peer dependencies
npm install --legacy-peer-deps  # Ignore peer deps

# npm 8+: override peer dependencies
npm install --force
```

### Workspace 업그레이드합니다
```bash
# Update all workspace packages
npm install --workspaces

# Update specific workspace
npm install package@latest --workspace=packages/app
```

## 리소스

- **참조/semver.md**: Semantic versioning 가이드
- **참조/compatibility-매트릭스.md**: 일반적인 compatibility 이슈
- **참조/staged-업그레이드합니다.md**: Incremental 업그레이드 strategies
- **참조/테스트-전략.md**: 포괄적인 테스트 approaches
- **자산/업그레이드-checklist.md**: 단계-에 의해-단계 checklist
- **자산/compatibility-매트릭스.csv**: 버전 compatibility 테이블
- **스크립트/audit-종속성.sh**: 종속성 audit 스크립트

## 최선의 관행

1. **읽은 Changelogs**: Understand 무엇 변경된
2. **업그레이드 점진적으로**: One 주요 버전 에서 a 시간
3. **Test 철저히**: 단위, 통합, E2E 테스트합니다
4. **Check Peer 종속성**: Resolve conflicts early
5. **Use 잠금 파일**: Ensure reproducible installs
6. **Automate 업데이트합니다**: Use Renovate 또는 Dependabot
7. **모니터**: Watch 위한 런타임 오류 post-업그레이드
8. **Document**: Keep 업그레이드 notes

## 업그레이드 Checklist

```markdown
Pre-Upgrade:
- [ ] Review current dependency versions
- [ ] Read changelogs for breaking changes
- [ ] Create feature branch
- [ ] Backup current state (git tag)
- [ ] Run full test suite (baseline)

During Upgrade:
- [ ] Upgrade one dependency at a time
- [ ] Update peer dependencies
- [ ] Fix TypeScript errors
- [ ] Update tests if needed
- [ ] Run test suite after each upgrade
- [ ] Check bundle size impact

Post-Upgrade:
- [ ] Full regression testing
- [ ] Performance testing
- [ ] Update documentation
- [ ] Deploy to staging
- [ ] Monitor for errors
- [ ] Deploy to production
```

## 일반적인 Pitfalls

- Upgrading 모든 종속성 에서 once
- Not 테스트 이후 각 업그레이드
- Ignoring peer 종속성 경고
- Forgetting 에 업데이트 잠금 파일
- Not 읽는 breaking 변경 notes
- Skipping 주요 버전
- Not having 롤백 plan
