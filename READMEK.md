# Claude Code 플러그인 사용 가이드 (한글)

## React + TypeScript + Tailwind CSS 개발

이 문서는 Claude Code의 플러그인을 사용하여 React, TypeScript, Tailwind CSS 프로젝트를 개발하는 방법을 설명합니다.

---

## 📋 목차

1. [설치된 플러그인](#설치된-플러그인)
2. [플러그인 설치 방법](#플러그인-설치-방법)
3. [실제 사용법](#실제-사용법)
4. [명령어 레퍼런스](#명령어-레퍼런스)
5. [실무 워크플로우](#실무-워크플로우)
6. [자주 사용하는 패턴](#자주-사용하는-패턴)
7. [팁과 트릭](#팁과-트릭)

---

## 설치된 플러그인

### 필수 플러그인 (3개)

#### 1. **javascript-typescript**
- **용도**: JavaScript/TypeScript 개발
- **포함 내용**:
  - javascript-pro 에이전트
  - typescript-pro 에이전트
  - TypeScript 고급 타입 스킬
  - Node.js 패턴 스킬
  - 현대 JavaScript 패턴 스킬

#### 2. **frontend-mobile-development**
- **용도**: React UI 컴포넌트 개발
- **포함 내용**:
  - frontend-developer 에이전트 (React 전문)
  - mobile-developer 에이전트
  - React 컴포넌트 스캐폴딩 명령

#### 3. **unit-testing**
- **용도**: 자동 테스트 생성
- **포함 내용**:
  - Jest, Vitest 테스트 자동 생성
  - test-automator 에이전트
  - Testing Library 패턴

### 추가 플러그인 (3개)

#### 4. **code-review-ai**
- **용도**: 코드 검토 및 최적화
- **사용법**: `/code-review-ai:ai-review`

#### 5. **accessibility-compliance**
- **용도**: 접근성 검증
- **사용법**: `/accessibility-compliance:accessibility-audit`

#### 6. **code-documentation**
- **용도**: 컴포넌트 문서 생성
- **사용법**: `/code-documentation:doc-generate`

---

## 플러그인 설치 방법

### 마켓플레이스 추가 (1회만)

Claude Code 채팅창에 입력:

```bash
/plugin marketplace add wshobson/agents
```

### 플러그인 설치

```bash
/plugin install javascript-typescript
/plugin install frontend-mobile-development
/plugin install unit-testing
/plugin install code-review-ai
/plugin install accessibility-compliance
/plugin install code-documentation
```

---

## 실제 사용법

### 1단계: React 프로젝트 생성

```bash
/javascript-typescript:typescript-scaffold react-dashboard
```

### 2단계: React 컴포넌트 만들기

#### 방법 A: 슬래시 명령 (권장)

```bash
/frontend-mobile-development:component-scaffold UserProfile component with TypeScript and Tailwind CSS
```

#### 방법 B: 자연어 (더 간단)

```
Create a React form component for user registration with TypeScript validation and Tailwind CSS styling.
Include fields for email, password, and confirm password with error messages.
```

### 3단계: 자동으로 테스트 생성

```bash
/unit-testing:test-generate src/components/UserProfile.tsx
```

### 4단계: 코드 리뷰

```bash
/code-review-ai:ai-review
```

### 5단계: 접근성 검증

```bash
/accessibility-compliance:accessibility-audit
```

### 6단계: 문서 생성

```bash
/code-documentation:doc-generate src/components
```

---

## 명령어 레퍼런스

| 작업 | 명령어 |
|------|--------|
| 새 프로젝트 생성 | `/javascript-typescript:typescript-scaffold app-name` |
| 컴포넌트 생성 | `/frontend-mobile-development:component-scaffold 컴포넌트 설명` |
| 테스트 작성 | `/unit-testing:test-generate src/path/to/file.tsx` |
| 코드 검토 | `/code-review-ai:ai-review` |
| 접근성 검증 | `/accessibility-compliance:accessibility-audit` |
| 문서 생성 | `/code-documentation:doc-generate src/components` |
| 설치 플러그인 확인 | `/plugin installed` |

---

## 실무 워크플로우

### 워크플로우 1: 단일 컴포넌트 개발

```
1. 컴포넌트 생성
   /frontend-mobile-development:component-scaffold ComponentName

2. 테스트 작성
   /unit-testing:test-generate src/components/ComponentName.tsx

3. 코드 검토
   /code-review-ai:ai-review

4. 접근성 확인
   /accessibility-compliance:accessibility-audit
```

### 워크플로우 2: 기능 전체 개발

```
1. 프로젝트 생성
   /javascript-typescript:typescript-scaffold my-app

2. 기능 컴포넌트들 생성
   "Create a login page with LoginForm and LoginCard components"

3. API 훅 생성
   "Create a useAuth hook for authentication management"

4. 테스트 작성
   /unit-testing:test-generate src/components/LoginForm.tsx

5. 전체 검토
   /code-review-ai:ai-review

6. 문서화
   /code-documentation:doc-generate src/components
```

### 워크플로우 3: 대시보드 개발

```
1. 대시보드 구조 설계
   "Create a dashboard layout with header, sidebar, and main content area"

2. 개별 컴포넌트 생성
   - Header 컴포넌트
   - Sidebar 네비게이션
   - Card 컴포넌트
   - Chart 컴포넌트

3. 각 컴포넌트 테스트
   /unit-testing:test-generate src/components/ComponentName.tsx

4. 전체 검토
   /code-review-ai:ai-review

5. 접근성 검증
   /accessibility-compliance:accessibility-audit

6. 문서화
   /code-documentation:doc-generate src
```

---

## 자주 사용하는 패턴

### 패턴 1: 재사용 가능한 Button 컴포넌트

```
Create a comprehensive Button component with TypeScript that includes:
- Multiple variants (primary, secondary, danger)
- Multiple sizes (sm, md, lg)
- Loading state
- Icon support
- Full Tailwind CSS styling
```

### 패턴 2: 폼 관리 훅

```
Create a form hook (useForm) in TypeScript that manages:
- Form state
- Field validation
- Error messages
- Submit handling
- Dirty state tracking
```

### 패턴 3: API 통합 훅

```
Create a custom React hook (useApi) for API calls with:
- Loading state
- Error handling
- Data caching
- TypeScript generics for type safety
```

### 패턴 4: 인증 상태 관리

```
Create a context and hook for user authentication with TypeScript:
- Auth state (user, isLoading, error)
- Login/logout functions
- Type-safe context usage
```

---

## 팁과 트릭

### Tip 1: 자연어가 더 효과적

덜 효과적:
```bash
/frontend-mobile-development:component-scaffold Button
```

더 효과적:
```
Create a fully-featured Button component with:
- Multiple variants (primary, secondary, outlined)
- Multiple sizes (sm, md, lg)
- Icon support
- Loading state
- Tailwind CSS styling
```

### Tip 2: 멀티스텝 작업 한 번에 요청

```
Create a complete user profile management feature with:
1. UserProfile display component
2. EditUserProfile form component
3. useUserProfile custom hook
4. API integration
5. Full TypeScript typing
6. Tailwind CSS styling
```

### Tip 3: 기존 코드 개선

```
Review and improve this component for performance and accessibility:
[코드 붙여넣기]
```

### Tip 4: 특정 패턴으로 구현

```
Create a React component using the compound component pattern with:
- Parent component (Container)
- Child components (Header, Body, Footer)
- TypeScript interfaces
- Tailwind CSS styling
```

### Tip 5: 테스트 케이스 상세 지정

```
Create unit tests for UserCard that cover:
- Rendering with all props
- Rendering with partial props
- User interactions
- Accessibility features
```

---

## 실제 예제

### 예제 1: 카드 컴포넌트

**1단계: 컴포넌트 생성**
```
Create a Card component that displays:
- Title, Description, Image, Action button
- Tailwind CSS styling
```

**2단계: 테스트 생성**
```bash
/unit-testing:test-generate src/components/Card.tsx
```

**3단계: 검토**
```bash
/code-review-ai:ai-review
```

### 예제 2: 폼 컴포넌트

**1단계: 폼 생성**
```
Create a contact form component with:
- Name, Email, Message fields
- Form validation
- Error messages
- Submit button
```

**2단계: 테스트 생성**
```bash
/unit-testing:test-generate src/components/ContactForm.tsx
```

**3단계: 접근성 확인**
```bash
/accessibility-compliance:accessibility-audit
```

**4단계: 문서 생성**
```bash
/code-documentation:doc-generate src/components/ContactForm.tsx
```

### 예제 3: 대시보드 페이지

**1단계: 페이지 구조**
```
Create a user dashboard page with:
- Header with user info
- Sidebar navigation
- Main content area
- Cards showing user stats
```

**2단계: 각 컴포넌트 테스트**
```bash
/unit-testing:test-generate src/components/Header.tsx
/unit-testing:test-generate src/components/Sidebar.tsx
/unit-testing:test-generate src/components/StatCard.tsx
```

**3단계: 전체 검토 및 검증**
```bash
/code-review-ai:ai-review
/accessibility-compliance:accessibility-audit
```

**4단계: 문서화**
```bash
/code-documentation:doc-generate src
```

---

## 빠른 시작 체크리스트

- [ ] 마켓플레이스 추가: `/plugin marketplace add wshobson/agents`
- [ ] 플러그인 설치: `/plugin install javascript-typescript` 등
- [ ] 첫 프로젝트 생성: `/javascript-typescript:typescript-scaffold my-app`
- [ ] 첫 컴포넌트 만들기: 자연어로 요청
- [ ] 테스트 작성: `/unit-testing:test-generate`
- [ ] 코드 검토: `/code-review-ai:ai-review`
- [ ] 접근성 검증: `/accessibility-compliance:accessibility-audit`
- [ ] 문서화: `/code-documentation:doc-generate`

---

## 유용한 리소스

- [Claude Code 공식 문서](https://docs.claude.com/en/docs/claude-code/overview)
- [React 공식 문서](https://react.dev)
- [TypeScript 공식 문서](https://www.typescriptlang.org)
- [Tailwind CSS 공식 문서](https://tailwindcss.com)

---

**작성일**: 2024년 11월
**버전**: 1.0
