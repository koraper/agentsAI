---
name: code-review-excellence
description: 마스터 effective 코드 review 관행 에 provide constructive feedback, catch 버그 early, 및 foster 지식 sharing 동안 maintaining 팀 morale. Use 때 검토하는 pull 요청, establishing review 표준, 또는 mentoring developers.
---

# 코드 Review 우수성

Transform 코드 검토합니다 에서 gatekeeping 에 지식 sharing 통해 constructive feedback, systematic 분석, 및 collaborative improvement.

## 때 에 Use This Skill

- 검토하는 pull 요청 및 코드 변경합니다
- Establishing 코드 review 표준 위한 teams
- Mentoring 주니어 developers 통해 검토합니다
- Conducting 아키텍처 검토합니다
- 생성하는 review checklists 및 가이드라인
- Improving 팀 collaboration
- Reducing 코드 review 사이클 시간
- Maintaining 코드 품질 표준

## 핵심 원칙

### 1. The Review Mindset

**Goals of 코드 Review:**
- catch 버그 및 엣지 cases
- Ensure 코드 유지보수성
- Share 지식 전반에 걸쳐 팀
- Enforce coding 표준
- Improve 설계 및 아키텍처
- 빌드 팀 culture

**Not the Goals:**
- Show 꺼짐 지식
- Nitpick 형식 지정 (use linters)
- Block 진행 unnecessarily
- Rewrite 에 your preference

### 2. Effective Feedback

**좋은 Feedback is:**
- 특정 및 actionable
- Educational, not judgmental
- Focused 에 the 코드, not the person
- 균형된 (praise 좋은 work 또한)
- 우선순위가 지정됨 (긴급 vs nice-에-have)

```markdown
❌ Bad: "This is wrong."
✅ Good: "This could cause a race condition when multiple users
         access simultaneously. Consider using a mutex here."

❌ Bad: "Why didn't you use X pattern?"
✅ Good: "Have you considered the Repository pattern? It would
         make this easier to test. Here's an example: [link]"

❌ Bad: "Rename this variable."
✅ Good: "[nit] Consider `userCount` instead of `uc` for
         clarity. Not blocking if you prefer to keep it."
```

### 3. Review 범위

**무엇 에 Review:**
- Logic 정확성 및 엣지 cases
- Security 취약점
- 성능 implications
- Test coverage 및 품질
- 오류 처리
- 문서화 및 comments
- API 설계 및 naming
- Architectural 적합한

**무엇 Not 에 Review Manually:**
- 코드 형식 지정 (use Prettier, Black, etc.)
- Import 조직
- Linting 위반
- 간단한 typos

## Review 프로세스

### 단계 1: 컨텍스트 수집 (2-3 minutes)

```markdown
Before diving into code, understand:

1. Read PR description and linked issue
2. Check PR size (>400 lines? Ask to split)
3. Review CI/CD status (tests passing?)
4. Understand the business requirement
5. Note any relevant architectural decisions
```

### 단계 2: High-레벨 Review (5-10 minutes)

```markdown
1. **Architecture & Design**
   - Does the solution fit the problem?
   - Are there simpler approaches?
   - Is it consistent with existing patterns?
   - Will it scale?

2. **File Organization**
   - Are new files in the right places?
   - Is code grouped logically?
   - Are there duplicate files?

3. **Testing Strategy**
   - Are there tests?
   - Do tests cover edge cases?
   - Are tests readable?
```

### 단계 3: Line-에 의해-Line Review (10-20 minutes)

```markdown
For each file:

1. **Logic & Correctness**
   - Edge cases handled?
   - Off-by-one errors?
   - Null/undefined checks?
   - Race conditions?

2. **Security**
   - Input validation?
   - SQL injection risks?
   - XSS vulnerabilities?
   - Sensitive data exposure?

3. **Performance**
   - N+1 queries?
   - Unnecessary loops?
   - Memory leaks?
   - Blocking operations?

4. **Maintainability**
   - Clear variable names?
   - Functions doing one thing?
   - Complex code commented?
   - Magic numbers extracted?
```

### 단계 4: Summary & 결정 (2-3 minutes)

```markdown
1. Summarize key concerns
2. Highlight what you liked
3. Make clear decision:
   - ✅ Approve
   - 💬 Comment (minor suggestions)
   - 🔄 Request Changes (must address)
4. Offer to pair if complex
```

## Review Techniques

### 기법 1: The Checklist 메서드

```markdown
## Security Checklist
- [ ] User input validated and sanitized
- [ ] SQL queries use parameterization
- [ ] Authentication/authorization checked
- [ ] Secrets not hardcoded
- [ ] Error messages don't leak info

## Performance Checklist
- [ ] No N+1 queries
- [ ] Database queries indexed
- [ ] Large lists paginated
- [ ] Expensive operations cached
- [ ] No blocking I/O in hot paths

## Testing Checklist
- [ ] Happy path tested
- [ ] Edge cases covered
- [ ] Error cases tested
- [ ] Test names are descriptive
- [ ] Tests are deterministic
```

### 기법 2: The Question 접근법

Instead of stating 문제, ask questions 에 encourage thinking:

```markdown
❌ "This will fail if the list is empty."
✅ "What happens if `items` is an empty array?"

❌ "You need error handling here."
✅ "How should this behave if the API call fails?"

❌ "This is inefficient."
✅ "I see this loops through all users. Have we considered
    the performance impact with 100k users?"
```

### 기법 3: Suggest, Don't 명령

```markdown
## Use Collaborative Language

❌ "You must change this to use async/await"
✅ "Suggestion: async/await might make this more readable:
    ```typescript
    비동기 함수 fetchUser(id: string) {
        const 사용자 = await db.쿼리('SELECT * 에서 사용자 곳 id = ?', id);
        반환 사용자;
    }
    ```
    What do you think?"

❌ "Extract this into a function"
✅ "This logic appears in 3 places. Would it make sense to
    extract it into a shared utility function?"
```

### 기법 4: Differentiate Severity

```markdown
Use labels to indicate priority:

🔴 [blocking] - Must fix before merge
🟡 [important] - Should fix, discuss if disagree
🟢 [nit] - Nice to have, not blocking
💡 [suggestion] - Alternative approach to consider
📚 [learning] - Educational comment, no action needed
🎉 [praise] - Good work, keep it up!

Example:
"🔴 [blocking] This SQL query is vulnerable to injection.
 Please use parameterized queries."

"🟢 [nit] Consider renaming `data` to `userData` for clarity."

"🎉 [praise] Excellent test coverage! This will catch edge cases."
```

## Language-특정 패턴

### Python 코드 Review

```python
# Check for Python-specific issues

# ❌ Mutable default arguments
def add_item(item, items=[]):  # Bug! Shared across calls
    items.append(item)
    return items

# ✅ Use None as default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# ❌ Catching too broad
try:
    result = risky_operation()
except:  # Catches everything, even KeyboardInterrupt!
    pass

# ✅ Catch specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise

# ❌ Using mutable class attributes
class User:
    permissions = []  # Shared across all instances!

# ✅ Initialize in __init__
class User:
    def __init__(self):
        self.permissions = []
```

### TypeScript/JavaScript 코드 Review

```typescript
// Check for TypeScript-specific issues

// ❌ Using any defeats type safety
function processData(data: any) {  // Avoid any
    return data.value;
}

// ✅ Use proper types
interface DataPayload {
    value: string;
}
function processData(data: DataPayload) {
    return data.value;
}

// ❌ Not handling async errors
async function fetchUser(id: string) {
    const response = await fetch(`/api/users/${id}`);
    return response.json();  // What if network fails?
}

// ✅ Handle errors properly
async function fetchUser(id: string): Promise<User> {
    try {
        const response = await fetch(`/api/users/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
}

// ❌ Mutation of props
function UserProfile({ user }: Props) {
    user.lastViewed = new Date();  // Mutating prop!
    return <div>{user.name}</div>;
}

// ✅ Don't mutate props
function UserProfile({ user, onView }: Props) {
    useEffect(() => {
        onView(user.id);  // Notify parent to update
    }, [user.id]);
    return <div>{user.name}</div>;
}
```

## 고급 Review 패턴

### 패턴 1: Architectural Review

```markdown
When reviewing significant changes:

1. **Design Document First**
   - For large features, request design doc before code
   - Review design with team before implementation
   - Agree on approach to avoid rework

2. **Review in Stages**
   - First PR: Core abstractions and interfaces
   - Second PR: Implementation
   - Third PR: Integration and tests
   - Easier to review, faster to iterate

3. **Consider Alternatives**
   - "Have we considered using [pattern/library]?"
   - "What's the tradeoff vs. the simpler approach?"
   - "How will this evolve as requirements change?"
```

### 패턴 2: Test 품질 Review

```typescript
// ❌ Poor test: Implementation detail testing
test('increments counter variable', () => {
    const component = render(<Counter />);
    const button = component.getByRole('button');
    fireEvent.click(button);
    expect(component.state.counter).toBe(1);  // Testing internal state
});

// ✅ Good test: Behavior testing
test('displays incremented count when clicked', () => {
    render(<Counter />);
    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

// Review questions for tests:
// - Do tests describe behavior, not implementation?
// - Are test names clear and descriptive?
// - Do tests cover edge cases?
// - Are tests independent (no shared state)?
// - Can tests run in any order?
```

### 패턴 3: Security Review

```markdown
## Security Review Checklist

### Authentication & Authorization
- [ ] Is authentication required where needed?
- [ ] Are authorization checks before every action?
- [ ] Is JWT validation proper (signature, expiry)?
- [ ] Are API keys/secrets properly secured?

### Input Validation
- [ ] All user inputs validated?
- [ ] File uploads restricted (size, type)?
- [ ] SQL queries parameterized?
- [ ] XSS protection (escape output)?

### Data Protection
- [ ] Passwords hashed (bcrypt/argon2)?
- [ ] Sensitive data encrypted at rest?
- [ ] HTTPS enforced for sensitive data?
- [ ] PII handled according to regulations?

### Common Vulnerabilities
- [ ] No eval() or similar dynamic execution?
- [ ] No hardcoded secrets?
- [ ] CSRF protection for state-changing operations?
- [ ] Rate limiting on public endpoints?
```

## Giving 어려운 Feedback

### 패턴: The Sandwich 메서드 (수정된)

```markdown
Traditional: Praise + Criticism + Praise (feels fake)

Better: Context + Specific Issue + Helpful Solution

Example:
"I noticed the payment processing logic is inline in the
controller. This makes it harder to test and reuse.

[Specific Issue]
The calculateTotal() function mixes tax calculation,
discount logic, and database queries, making it difficult
to unit test and reason about.

[Helpful Solution]
Could we extract this into a PaymentService class? That
would make it testable and reusable. I can pair with you
on this if helpful."
```

### 처리 Disagreements

```markdown
When author disagrees with your feedback:

1. **Seek to Understand**
   "Help me understand your approach. What led you to
    choose this pattern?"

2. **Acknowledge Valid Points**
   "That's a good point about X. I hadn't considered that."

3. **Provide Data**
   "I'm concerned about performance. Can we add a benchmark
    to validate the approach?"

4. **Escalate if Needed**
   "Let's get [architect/senior dev] to weigh in on this."

5. **Know When to Let Go**
   If it's working and not a critical issue, approve it.
   Perfection is the enemy of progress.
```

## 최선의 관행

1. **Review 즉시**: 내에 24 hours, 이상적으로 same day
2. **Limit PR Size**: 200-400 lines max 위한 effective review
3. **Review 에서 시간 차단합니다**: 60 minutes max, take breaks
4. **Use Review Tools**: GitHub, GitLab, 또는 dedicated tools
5. **Automate 무엇 You Can**: Linters, formatters, security scans
6. **빌드 Rapport**: Emoji, praise, 및 empathy matter
7. **Be 사용 가능한**: Offer 에 쌍 에 복잡한 이슈
8. **Learn 에서 Others**: Review others' review comments

## 일반적인 Pitfalls

- **Perfectionism**: 차단 PRs 위한 부수적 스타일 preferences
- **범위 Creep**: "동안 you're 에서 it, can you 또한..."
- **Inconsistency**: 다른 표준 위한 다른 people
- **지연됨 검토합니다**: Letting PRs sit 위한 days
- **Ghosting**: Requesting 변경합니다 then disappearing
- **Rubber Stamping**: Approving 없이 actually 검토하는
- **Bike Shedding**: Debating 사소한 details 광범위하게

## 템플릿

### PR Review 주석 템플릿

```markdown
## Summary
[Brief overview of what was reviewed]

## Strengths
- [What was done well]
- [Good patterns or approaches]

## Required Changes
🔴 [Blocking issue 1]
🔴 [Blocking issue 2]

## Suggestions
💡 [Improvement 1]
💡 [Improvement 2]

## Questions
❓ [Clarification needed on X]
❓ [Alternative approach consideration]

## Verdict
✅ Approve after addressing required changes
```

## 리소스

- **참조/코드-review-최선의-관행.md**: 포괄적인 review 가이드라인
- **참조/일반적인-버그-checklist.md**: Language-특정 버그 에 watch 위한
- **참조/security-review-가이드.md**: Security-focused review checklist
- **자산/pr-review-템플릿.md**: 표준 review 주석 템플릿
- **자산/review-checklist.md**: Quick 참조 checklist
- **스크립트/pr-분석기.py**: Analyze PR complexity 및 suggest reviewers
