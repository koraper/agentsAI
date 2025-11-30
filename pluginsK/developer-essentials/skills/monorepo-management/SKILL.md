---
name: monorepo-management
description: 마스터 monorepo 관리 와 함께 Turborepo, Nx, 및 pnpm workspaces 에 빌드 efficient, scalable multi-패키지 repositories 와 함께 최적화된 빌드 및 종속성 관리. Use 때 설정하는 monorepos, optimizing 빌드, 또는 managing shared 종속성.
---

# Monorepo 관리

빌드 efficient, scalable monorepos 것 enable 코드 sharing, 일관된 tooling, 및 원자적 변경합니다 전반에 걸쳐 여러 패키지 및 애플리케이션.

## 때 에 Use This Skill

- 설정하는 새로운 monorepo projects
- Migrating 에서 multi-repo 에 monorepo
- Optimizing 빌드 및 test 성능
- Managing shared 종속성
- Implementing 코드 sharing strategies
- 설정하는 CI/CD 위한 monorepos
- Versioning 및 게시 패키지
- 디버깅 monorepo-특정 이슈

## 핵심 개념

### 1. 왜 Monorepos?

**Advantages:**
- Shared 코드 및 종속성
- 원자적 commits 전반에 걸쳐 projects
- 일관된 tooling 및 표준
- Easier 리팩토링
- 단순화된 종속성 관리
- 더 나은 코드 visibility

**Challenges:**
- 빌드 성능 에서 scale
- CI/CD complexity
- Access control
- Large Git 저장소

### 2. Monorepo Tools

**패키지 Managers:**
- pnpm workspaces (권장됨)
- npm workspaces
- Yarn workspaces

**빌드 시스템:**
- Turborepo (권장됨 위한 most)
- Nx (기능이 풍부한, 복잡한)
- Lerna (older, 유지보수 최빈값)

## Turborepo 설정

### 초기 설정

```bash
# Create new monorepo
npx create-turbo@latest my-monorepo
cd my-monorepo

# Structure:
# apps/
#   web/          - Next.js app
#   docs/         - Documentation site
# packages/
#   ui/           - Shared UI components
#   config/       - Shared configurations
#   tsconfig/     - Shared TypeScript configs
# turbo.json      - Turborepo configuration
# package.json    - Root package.json
```

### 구성

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  }
}
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "format": "prettier --write \"**/*.{ts,tsx,md}\"",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0"
  },
  "packageManager": "pnpm@8.0.0"
}
```

### 패키지 구조

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./button": {
      "import": "./dist/button.js",
      "types": "./dist/button.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "dev": "tsup src/index.ts --format esm,cjs --dts --watch",
    "lint": "eslint src/",
    "type-check": "tsc --noEmit"
  },
  "devDependencies": {
    "@repo/tsconfig": "workspace:*",
    "tsup": "^7.0.0",
    "typescript": "^5.0.0"
  },
  "dependencies": {
    "react": "^18.2.0"
  }
}
```

## pnpm Workspaces

### 설정

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

```json
// .npmrc
# Hoist shared dependencies
shamefully-hoist=true

# Strict peer dependencies
auto-install-peers=true
strict-peer-dependencies=true

# Performance
store-dir=~/.pnpm-store
```

### 종속성 관리

```bash
# Install dependency in specific package
pnpm add react --filter @repo/ui
pnpm add -D typescript --filter @repo/ui

# Install workspace dependency
pnpm add @repo/ui --filter web

# Install in all packages
pnpm add -D eslint -w

# Update all dependencies
pnpm update -r

# Remove dependency
pnpm remove react --filter @repo/ui
```

### 스크립트

```bash
# Run script in specific package
pnpm --filter web dev
pnpm --filter @repo/ui build

# Run in all packages
pnpm -r build
pnpm -r test

# Run in parallel
pnpm -r --parallel dev

# Filter by pattern
pnpm --filter "@repo/*" build
pnpm --filter "...web" build  # Build web and dependencies
```

## Nx Monorepo

### 설정

```bash
# Create Nx monorepo
npx create-nx-workspace@latest my-org

# Generate applications
nx generate @nx/react:app my-app
nx generate @nx/next:app my-next-app

# Generate libraries
nx generate @nx/react:lib ui-components
nx generate @nx/js:lib utils
```

### 구성

```json
// nx.json
{
  "extends": "nx/presets/npm.json",
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production", "{workspaceRoot}/jest.preset.js"],
      "cache": true
    },
    "lint": {
      "inputs": ["default", "{workspaceRoot}/.eslintrc.json"],
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json"
    ],
    "sharedGlobals": []
  }
}
```

### 실행 중 Tasks

```bash
# Run task for specific project
nx build my-app
nx test ui-components
nx lint utils

# Run for affected projects
nx affected:build
nx affected:test --base=main

# Visualize dependencies
nx graph

# Run in parallel
nx run-many --target=build --all --parallel=3
```

## Shared Configurations

### TypeScript 구성

```json
// packages/tsconfig/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "incremental": true,
    "declaration": true
  },
  "exclude": ["node_modules"]
}

// packages/tsconfig/react.json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}

// apps/web/tsconfig.json
{
  "extends": "@repo/tsconfig/react.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### ESLint 구성

```javascript
// packages/config/eslint-preset.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    'react/react-in-jsx-scope': 'off',
  },
};

// apps/web/.eslintrc.js
module.exports = {
  extends: ['@repo/config/eslint-preset'],
  rules: {
    // App-specific rules
  },
};
```

## 코드 Sharing 패턴

### 패턴 1: Shared UI 컴포넌트

```typescript
// packages/ui/src/button.tsx
import * as React from 'react';

export interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// packages/ui/src/index.ts
export { Button, type ButtonProps } from './button';
export { Input, type InputProps } from './input';

// apps/web/src/app.tsx
import { Button } from '@repo/ui';

export function App() {
  return <Button variant="primary">Click me</Button>;
}
```

### 패턴 2: Shared Utilities

```typescript
// packages/utils/src/string.ts
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function truncate(str: string, length: number): string {
  return str.length > length ? str.slice(0, length) + '...' : str;
}

// packages/utils/src/index.ts
export * from './string';
export * from './array';
export * from './date';

// Usage in apps
import { capitalize, truncate } from '@repo/utils';
```

### 패턴 3: Shared 유형

```typescript
// packages/types/src/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
}

export interface CreateUserInput {
  email: string;
  name: string;
  password: string;
}

// Used in both frontend and backend
import type { User, CreateUserInput } from '@repo/types';
```

## 빌드 최적화

### Turborepo 캐싱

```json
// turbo.json
{
  "pipeline": {
    "build": {
      // Build depends on dependencies being built first
      "dependsOn": ["^build"],

      // Cache these outputs
      "outputs": ["dist/**", ".next/**"],

      // Cache based on these inputs (default: all files)
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "package.json"]
    },
    "test": {
      // Run tests in parallel, don't depend on build
      "cache": true,
      "outputs": ["coverage/**"]
    }
  }
}
```

### Remote 캐싱

```bash
# Turborepo Remote Cache (Vercel)
npx turbo login
npx turbo link

# Custom remote cache
# turbo.json
{
  "remoteCache": {
    "signature": true,
    "enabled": true
  }
}
```

## CI/CD 위한 Monorepos

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # For Nx affected commands

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo run build

      - name: Test
        run: pnpm turbo run test

      - name: Lint
        run: pnpm turbo run lint

      - name: Type check
        run: pnpm turbo run type-check
```

### Deploy Affected 오직

```yaml
# Deploy only changed apps
- name: Deploy affected apps
  run: |
    if pnpm nx affected:apps --base=origin/main --head=HEAD | grep -q "web"; then
      echo "Deploying web app"
      pnpm --filter web deploy
    fi
```

## 최선의 관행

1. **일관된 Versioning**: 잠금 종속성 버전 전반에 걸쳐 workspace
2. **Shared Configs**: Centralize ESLint, TypeScript, Prettier configs
3. **종속성 그래프**: Keep it acyclic, avoid circular 종속성
4. **캐시 Effectively**: Configure 입력/출력 올바르게
5. **유형 Safety**: Share 유형 사이 frontend/backend
6. **테스트 전략**: 단위 테스트합니다 에서 패키지, E2E 에서 apps
7. **문서화**: README 에서 각 패키지
8. **릴리스 전략**: Use changesets 위한 versioning

## 일반적인 Pitfalls

- **Circular 종속성**: A depends 에 B, B depends 에 A
- **Phantom 종속성**: 사용하여 deps not 에서 패키지.json
- **올바르지 않은 캐시 입력**: Missing 파일 에서 Turborepo 입력
- **Over-Sharing**: Sharing 코드 것 should be 별도
- **Under-Sharing**: Duplicating 코드 전반에 걸쳐 패키지
- **Large Monorepos**: 없이 적절한 tooling, 빌드 slow down

## 게시 패키지

```bash
# Using Changesets
pnpm add -Dw @changesets/cli
pnpm changeset init

# Create changeset
pnpm changeset

# Version packages
pnpm changeset version

# Publish
pnpm changeset publish
```

```yaml
# .github/workflows/release.yml
- name: Create Release Pull Request or Publish
  uses: changesets/action@v1
  with:
    publish: pnpm release
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## 리소스

- **참조/turborepo-가이드.md**: 포괄적인 Turborepo 문서화
- **참조/nx-가이드.md**: Nx monorepo 패턴
- **참조/pnpm-workspaces.md**: pnpm workspace 기능
- **자산/monorepo-checklist.md**: 설정 checklist
- **자산/마이그레이션-가이드.md**: Multi-repo 에 monorepo 마이그레이션
- **스크립트/종속성-그래프.ts**: Visualize 패키지 종속성
