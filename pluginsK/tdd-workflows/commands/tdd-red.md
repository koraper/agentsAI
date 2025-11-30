Write 포괄적인 failing 테스트합니다 following TDD red phase principles.

[Extended thinking: Generates failing 테스트합니다 that properly define expected behavior 사용하여 test-automator agent.]

## Role

Generate failing 테스트합니다 사용하여 Task tool 와 함께 subagent_type="unit-테스트::test-automator".

## Prompt Template

"Generate 포괄적인 FAILING 테스트합니다 위한: $ARGUMENTS

## Core Requirements

1. **Test Structure**
   - Framework-appropriate setup (Jest/pytest/JUnit/Go/RSpec)
   - Arrange-Act-Assert 패턴
   - should_X_when_Y naming convention
   - Isolated fixtures 와 함께 no interdependencies

2. **Behavior Coverage**
   - Happy path scenarios
   - Edge cases (empty, null, boundary values)
   - Error handling 및 exceptions
   - Concurrent access (if applicable)

3. **Failure Verification**
   - 테스트합니다 MUST fail when run
   - Failures 위한 RIGHT reasons (not syntax/import errors)
   - Meaningful diagnostic error messages
   - No cascading failures

4. **Test Categories**
   - Unit: Isolated component behavior
   - 통합: Component interaction
   - Contract: API/interface contracts
   - Property: Mathematical invariants

## Framework Patterns

**JavaScript/TypeScript (Jest/Vitest)**
- Mock dependencies 와 함께 `vi.fn()` 또는 `jest.fn()`
- Use `@testing-library` 위한 React components
- Property 테스트합니다 와 함께 `fast-check`

**Python (pytest)**
- Fixtures 와 함께 appropriate scopes
- Parametrize 위한 multiple test cases
- Hypothesis 위한 property-based 테스트합니다

**Go**
- Table-driven 테스트합니다 와 함께 subtests
- `t.Parallel()` 위한 parallel execution
- Use `testify/assert` 위한 cleaner assertions

**Ruby (RSpec)**
- `let` 위한 lazy loading, `let!` 위한 eager
- Contexts 위한 different scenarios
- Shared examples 위한 common behavior

## Quality Checklist

- Readable test names documenting intent
- One behavior per test
- No 구현 leakage
- Meaningful test data (not 'foo'/'bar')
- 테스트합니다 serve as living 문서화

## Anti-Patterns 에 Avoid

- 테스트합니다 passing immediately
- 테스트 구현 vs behavior
- 복잡한 setup code
- Multiple responsibilities per test
- Brittle 테스트합니다 tied 에 specifics

## Edge Case Categories

- **Null/Empty**: undefined, null, empty string/array/object
- **Boundaries**: min/max values, single element, capacity limits
- **Special Cases**: Unicode, whitespace, special characters
- **State**: Invalid transitions, concurrent modifications
- **Errors**: Network failures, timeouts, permissions

## Output Requirements

- Complete test files 와 함께 imports
- 문서화 of test purpose
- Commands 에 run 및 verify failures
- Metrics: test count, coverage areas
- Next steps 위한 green phase"

## Validation

이후 generation:
1. Run 테스트합니다 - confirm they fail
2. Verify helpful failure messages
3. Check test independence
4. Ensure 포괄적인 coverage

## Example (Minimal)

```typescript
// auth.service.test.ts
describe('AuthService', () => {
  let authService: AuthService;
  let mockUserRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepo = { findByEmail: jest.fn() } as any;
    authService = new AuthService(mockUserRepo);
  });

  it('should_return_token_when_valid_credentials', async () => {
    const user = { id: '1', email: 'test@example.com', passwordHash: 'hashed' };
    mockUserRepo.findByEmail.mockResolvedValue(user);

    const result = await authService.authenticate('test@example.com', 'pass');

    expect(result.success).toBe(true);
    expect(result.token).toBeDefined();
  });

  it('should_fail_when_user_not_found', async () => {
    mockUserRepo.findByEmail.mockResolvedValue(null);

    const result = await authService.authenticate('none@example.com', 'pass');

    expect(result.success).toBe(false);
    expect(result.error).toBe('INVALID_CREDENTIALS');
  });
});
```

Test requirements: $ARGUMENTS
