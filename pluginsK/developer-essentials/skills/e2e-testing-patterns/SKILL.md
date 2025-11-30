---
name: e2e-testing-patterns
description: 마스터 end-에-end 테스트 와 함께 Playwright 및 Cypress 에 빌드 reliable test suites 것 catch 버그, improve confidence, 및 enable fast 배포. Use 때 implementing E2E 테스트합니다, 디버깅 flaky 테스트합니다, 또는 establishing 테스트 표준.
---

# E2E 테스트 패턴

빌드 reliable, fast, 및 maintainable end-에-end test suites 것 provide confidence 에 ship 코드 빠르게 및 catch regressions 이전 사용자 do.

## 때 에 Use This Skill

- Implementing end-에-end test 자동화
- 디버깅 flaky 또는 unreliable 테스트합니다
- 테스트 긴급 사용자 워크플로우
- 설정하는 CI/CD test 파이프라인
- 테스트 전반에 걸쳐 여러 browsers
- Validating 접근성 요구사항
- 테스트 responsive 설계
- Establishing E2E 테스트 표준

## 핵심 개념

### 1. E2E 테스트 Fundamentals

**무엇 에 Test 와 함께 E2E:**
- 긴급 사용자 journeys (login, checkout, signup)
- 복잡한 interactions (drag-및-drop, multi-단계 폼)
- Cross-browser compatibility
- Real API 통합
- 인증 흐릅니다

**무엇 NOT 에 Test 와 함께 E2E:**
- 단위-레벨 logic (use 단위 테스트합니다)
- API 계약 (use 통합 테스트합니다)
- 엣지 cases (또한 slow)
- 내부 구현 details

### 2. Test Philosophy

**The 테스트 Pyramid:**
```
        /\
       /E2E\         ← Few, focused on critical paths
      /─────\
     /Integr\        ← More, test component interactions
    /────────\
   /Unit Tests\      ← Many, fast, isolated
  /────────────\
```

**최선의 관행:**
- Test 사용자 behavior, not 구현
- Keep 테스트합니다 독립적인
- Make 테스트합니다 deterministic
- Optimize 위한 속도
- Use 데이터-testid, not CSS selectors

## Playwright 패턴

### 설정 및 구성

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './e2e',
    timeout: 30000,
    expect: {
        timeout: 5000,
    },
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: [
        ['html'],
        ['junit', { outputFile: 'results.xml' }],
    ],
    use: {
        baseURL: 'http://localhost:3000',
        trace: 'on-first-retry',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
        { name: 'mobile', use: { ...devices['iPhone 13'] } },
    ],
});
```

### 패턴 1: 페이지 객체 모델

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
    readonly page: Page;
    readonly emailInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;
    readonly errorMessage: Locator;

    constructor(page: Page) {
        this.page = page;
        this.emailInput = page.getByLabel('Email');
        this.passwordInput = page.getByLabel('Password');
        this.loginButton = page.getByRole('button', { name: 'Login' });
        this.errorMessage = page.getByRole('alert');
    }

    async goto() {
        await this.page.goto('/login');
    }

    async login(email: string, password: string) {
        await this.emailInput.fill(email);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
    }

    async getErrorMessage(): Promise<string> {
        return await this.errorMessage.textContent() ?? '';
    }
}

// Test using Page Object
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test('successful login', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Dashboard' }))
        .toBeVisible();
});

test('failed login shows error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('invalid@example.com', 'wrong');

    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
});
```

### 패턴 2: Fixtures 위한 Test 데이터

```typescript
// fixtures/test-data.ts
import { test as base } from '@playwright/test';

type TestData = {
    testUser: {
        email: string;
        password: string;
        name: string;
    };
    adminUser: {
        email: string;
        password: string;
    };
};

export const test = base.extend<TestData>({
    testUser: async ({}, use) => {
        const user = {
            email: `test-${Date.now()}@example.com`,
            password: 'Test123!@#',
            name: 'Test User',
        };
        // Setup: Create user in database
        await createTestUser(user);
        await use(user);
        // Teardown: Clean up user
        await deleteTestUser(user.email);
    },

    adminUser: async ({}, use) => {
        await use({
            email: 'admin@example.com',
            password: process.env.ADMIN_PASSWORD!,
        });
    },
});

// Usage in tests
import { test } from './fixtures/test-data';

test('user can update profile', async ({ page, testUser }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill(testUser.email);
    await page.getByLabel('Password').fill(testUser.password);
    await page.getByRole('button', { name: 'Login' }).click();

    await page.goto('/profile');
    await page.getByLabel('Name').fill('Updated Name');
    await page.getByRole('button', { name: 'Save' }).click();

    await expect(page.getByText('Profile updated')).toBeVisible();
});
```

### 패턴 3: Waiting Strategies

```typescript
// ❌ Bad: Fixed timeouts
await page.waitForTimeout(3000);  // Flaky!

// ✅ Good: Wait for specific conditions
await page.waitForLoadState('networkidle');
await page.waitForURL('/dashboard');
await page.waitForSelector('[data-testid="user-profile"]');

// ✅ Better: Auto-waiting with assertions
await expect(page.getByText('Welcome')).toBeVisible();
await expect(page.getByRole('button', { name: 'Submit' }))
    .toBeEnabled();

// Wait for API response
const responsePromise = page.waitForResponse(
    response => response.url().includes('/api/users') && response.status() === 200
);
await page.getByRole('button', { name: 'Load Users' }).click();
const response = await responsePromise;
const data = await response.json();
expect(data.users).toHaveLength(10);

// Wait for multiple conditions
await Promise.all([
    page.waitForURL('/success'),
    page.waitForLoadState('networkidle'),
    expect(page.getByText('Payment successful')).toBeVisible(),
]);
```

### 패턴 4: 네트워크 Mocking 및 Interception

```typescript
// Mock API responses
test('displays error when API fails', async ({ page }) => {
    await page.route('**/api/users', route => {
        route.fulfill({
            status: 500,
            contentType: 'application/json',
            body: JSON.stringify({ error: 'Internal Server Error' }),
        });
    });

    await page.goto('/users');
    await expect(page.getByText('Failed to load users')).toBeVisible();
});

// Intercept and modify requests
test('can modify API request', async ({ page }) => {
    await page.route('**/api/users', async route => {
        const request = route.request();
        const postData = JSON.parse(request.postData() || '{}');

        // Modify request
        postData.role = 'admin';

        await route.continue({
            postData: JSON.stringify(postData),
        });
    });

    // Test continues...
});

// Mock third-party services
test('payment flow with mocked Stripe', async ({ page }) => {
    await page.route('**/api/stripe/**', route => {
        route.fulfill({
            status: 200,
            body: JSON.stringify({
                id: 'mock_payment_id',
                status: 'succeeded',
            }),
        });
    });

    // Test payment flow with mocked response
});
```

## Cypress 패턴

### 설정 및 구성

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
    e2e: {
        baseUrl: 'http://localhost:3000',
        viewportWidth: 1280,
        viewportHeight: 720,
        video: false,
        screenshotOnRunFailure: true,
        defaultCommandTimeout: 10000,
        requestTimeout: 10000,
        setupNodeEvents(on, config) {
            // Implement node event listeners
        },
    },
});
```

### 패턴 1: 사용자 정의 명령

```typescript
// cypress/support/commands.ts
declare global {
    namespace Cypress {
        interface Chainable {
            login(email: string, password: string): Chainable<void>;
            createUser(userData: UserData): Chainable<User>;
            dataCy(value: string): Chainable<JQuery<HTMLElement>>;
        }
    }
}

Cypress.Commands.add('login', (email: string, password: string) => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type(email);
    cy.get('[data-testid="password"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    cy.url().should('include', '/dashboard');
});

Cypress.Commands.add('createUser', (userData: UserData) => {
    return cy.request('POST', '/api/users', userData)
        .its('body');
});

Cypress.Commands.add('dataCy', (value: string) => {
    return cy.get(`[data-cy="${value}"]`);
});

// Usage
cy.login('user@example.com', 'password');
cy.dataCy('submit-button').click();
```

### 패턴 2: Cypress Intercept

```typescript
// Mock API calls
cy.intercept('GET', '/api/users', {
    statusCode: 200,
    body: [
        { id: 1, name: 'John' },
        { id: 2, name: 'Jane' },
    ],
}).as('getUsers');

cy.visit('/users');
cy.wait('@getUsers');
cy.get('[data-testid="user-list"]').children().should('have.length', 2);

// Modify responses
cy.intercept('GET', '/api/users', (req) => {
    req.reply((res) => {
        // Modify response
        res.body.users = res.body.users.slice(0, 5);
        res.send();
    });
});

// Simulate slow network
cy.intercept('GET', '/api/data', (req) => {
    req.reply((res) => {
        res.delay(3000);  // 3 second delay
        res.send();
    });
});
```

## 고급 패턴

### 패턴 1: Visual Regression 테스트

```typescript
// With Playwright
import { test, expect } from '@playwright/test';

test('homepage looks correct', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
        fullPage: true,
        maxDiffPixels: 100,
    });
});

test('button in all states', async ({ page }) => {
    await page.goto('/components');

    const button = page.getByRole('button', { name: 'Submit' });

    // Default state
    await expect(button).toHaveScreenshot('button-default.png');

    // Hover state
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');

    // Disabled state
    await button.evaluate(el => el.setAttribute('disabled', 'true'));
    await expect(button).toHaveScreenshot('button-disabled.png');
});
```

### 패턴 2: 병렬로 테스트 와 함께 샤딩

```typescript
// playwright.config.ts
export default defineConfig({
    projects: [
        {
            name: 'shard-1',
            use: { ...devices['Desktop Chrome'] },
            grepInvert: /@slow/,
            shard: { current: 1, total: 4 },
        },
        {
            name: 'shard-2',
            use: { ...devices['Desktop Chrome'] },
            shard: { current: 2, total: 4 },
        },
        // ... more shards
    ],
});

// Run in CI
// npx playwright test --shard=1/4
// npx playwright test --shard=2/4
```

### 패턴 3: 접근성 테스트

```typescript
// Install: npm install @axe-core/playwright
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('page should not have accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
        .exclude('#third-party-widget')
        .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
});

test('form is accessible', async ({ page }) => {
    await page.goto('/signup');

    const results = await new AxeBuilder({ page })
        .include('form')
        .analyze();

    expect(results.violations).toEqual([]);
});
```

## 최선의 관행

1. **Use 데이터 속성**: `data-testid` 또는 `data-cy` 위한 안정적인 selectors
2. **Avoid 부서지기 쉬운 Selectors**: Don't rely 에 CSS 클래스 또는 DOM 구조
3. **Test 사용자 Behavior**: Click, 유형, see - not 구현 details
4. **Keep 테스트합니다 독립적인**: 각 test should run 에서 격리
5. **Clean Up Test 데이터**: Create 및 destroy test 데이터 에서 각 test
6. **Use 페이지 객체**: Encapsulate 페이지 logic
7. **의미 있는 Assertions**: Check actual 사용자-표시되는 behavior
8. **Optimize 위한 속도**: Mock 때 possible, 병렬로 실행

```typescript
// ❌ Bad selectors
cy.get('.btn.btn-primary.submit-button').click();
cy.get('div > form > div:nth-child(2) > input').type('text');

// ✅ Good selectors
cy.getByRole('button', { name: 'Submit' }).click();
cy.getByLabel('Email address').type('user@example.com');
cy.get('[data-testid="email-input"]').type('user@example.com');
```

## 일반적인 Pitfalls

- **Flaky 테스트합니다**: Use 적절한 waits, not 고정된 timeouts
- **Slow 테스트합니다**: Mock 외부 APIs, use 병렬로 실행
- **Over-테스트**: Don't test 모든 엣지 case 와 함께 E2E
- **결합된 테스트합니다**: 테스트합니다 should not depend 에 각 other
- **Poor Selectors**: Avoid CSS 클래스 및 nth-child
- **아니요 Cleanup**: Clean up test 데이터 이후 각 test
- **테스트 구현**: Test 사용자 behavior, not internals

## 디버깅 Failing 테스트합니다

```typescript
// Playwright debugging
// 1. Run in headed mode
npx playwright test --headed

// 2. Run in debug mode
npx playwright test --debug

// 3. Use trace viewer
await page.screenshot({ path: 'screenshot.png' });
await page.video()?.saveAs('video.webm');

// 4. Add test.step for better reporting
test('checkout flow', async ({ page }) => {
    await test.step('Add item to cart', async () => {
        await page.goto('/products');
        await page.getByRole('button', { name: 'Add to Cart' }).click();
    });

    await test.step('Proceed to checkout', async () => {
        await page.goto('/cart');
        await page.getByRole('button', { name: 'Checkout' }).click();
    });
});

// 5. Inspect page state
await page.pause();  // Pauses execution, opens inspector
```

## 리소스

- **참조/playwright-최선의-관행.md**: Playwright-특정 패턴
- **참조/cypress-최선의-관행.md**: Cypress-특정 패턴
- **참조/flaky-test-디버깅.md**: 디버깅 unreliable 테스트합니다
- **자산/e2e-테스트-checklist.md**: 무엇 에 test 와 함께 E2E
- **자산/selector-strategies.md**: 찾는 reliable selectors
- **스크립트/test-분석기.ts**: Analyze test flakiness 및 기간
