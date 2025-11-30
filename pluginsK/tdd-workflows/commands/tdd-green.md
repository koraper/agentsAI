Implement minimal code 에 make failing 테스트합니다 pass 에서 TDD green phase:

[Extended thinking: This tool uses the test-automator agent 에 implement the minimal code necessary 에 make 테스트합니다 pass. It 집중합니다 simplicity, avoiding over-engineering 동안 ensuring all 테스트합니다 become green.]

## 구현 Process

Use Task tool 와 함께 subagent_type="unit-테스트::test-automator" 에 implement minimal passing code.

Prompt: "Implement MINIMAL code 에 make these failing 테스트합니다 pass: $ARGUMENTS. Follow TDD green phase principles:

1. **Pre-구현 Analysis**
   - Review all failing 테스트합니다 및 their error messages
   - Identify the simplest path 에 make 테스트합니다 pass
   - Map test requirements 에 minimal 구현 needs
   - Avoid premature 최적화 또는 over-engineering
   - Focus only 에 making 테스트합니다 green, not perfect code

2. **구현 Strategy**
   - **Fake It**: Return hard-coded values when appropriate
   - **Obvious 구현**: When solution is trivial 및 clear
   - **Triangulation**: Generalize only when multiple 테스트합니다 require it
   - Start 와 함께 the simplest test 및 work incrementally
   - One test 에서 a time - don't try 에 pass all 에서 once

3. **Code Structure Guidelines**
   - Write the minimal code that could possibly work
   - Avoid adding functionality not required 에 의해 테스트합니다
   - Use 간단한 data structures initially
   - Defer architectural decisions until refactor phase
   - Keep methods/functions small 및 focused
   - Don't add error handling unless 테스트합니다 require it

4. **Language-Specific Patterns**
   - **JavaScript/TypeScript**: 간단한 functions, avoid classes initially
   - **Python**: Functions 이전 classes, 간단한 returns
   - **Java**: Minimal class structure, no patterns yet
   - **C#**: 기본 implementations, no interfaces yet
   - **Go**: 간단한 functions, defer goroutines/channels
   - **Ruby**: Procedural 이전 object-oriented when possible

5. **Progressive 구현**
   - Make first test pass 와 함께 simplest possible code
   - Run 테스트합니다 이후 each change 에 verify progress
   - Add just enough code 위한 next failing test
   - Resist urge 에 implement beyond test requirements
   - Keep track of 기술 부채 위한 refactor phase
   - Document assumptions 및 shortcuts taken

6. **Common Green Phase Techniques**
   - Hard-coded returns 위한 initial 테스트합니다
   - 간단한 if/else 위한 limited test cases
   - 기본 loops only when iteration 테스트합니다 require
   - Minimal data structures (arrays 이전 복잡한 objects)
   - 에서-memory storage 이전 database 통합
   - 동기 이전 비동기 구현

7. **Success Criteria**
   ✓ All 테스트합니다 pass (green)
   ✓ No extra functionality beyond test requirements
   ✓ Code is readable even if not optimal
   ✓ No broken existing functionality
   ✓ 구현 time is minimized
   ✓ Clear path 에 refactoring identified

8. **Anti-Patterns 에 Avoid**
   - Gold plating 또는 adding unrequested features
   - Implementing 설계 patterns prematurely
   - 복잡한 abstractions 없이 test justification
   - 성능 optimizations 없이 metrics
   - Adding 테스트합니다 동안 green phase
   - Refactoring 동안 구현
   - Ignoring test failures 에 move forward

9. **구현 Metrics**
   - Time 에 green: Track 구현 duration
   - Lines of code: Measure 구현 size
   - Cyclomatic complexity: Keep it low initially
   - Test pass rate: Must reach 100%
   - Code coverage: Verify all paths tested

10. **Validation Steps**
    - Run all 테스트합니다 및 confirm they pass
    - Verify no regression 에서 existing 테스트합니다
    - Check that 구현 is truly minimal
    - Document any 기술 부채 created
    - Prepare notes 위한 refactoring phase

Output should include:
- Complete 구현 code
- Test execution results showing all green
- List of shortcuts taken 위한 later refactoring
- 구현 time metrics
- 기술 부채 문서화
- Readiness assessment 위한 refactor phase"

## Post-구현 Checks

이후 구현:
1. Run full test suite 에 confirm all 테스트합니다 pass
2. Verify no existing 테스트합니다 were broken
3. Document areas needing refactoring
4. Check 구현 is truly minimal
5. Record 구현 time 위한 metrics

## Recovery Process

If 테스트합니다 still fail:
- Review test requirements carefully
- Check 위한 misunderstood assertions
- Add minimal code 에 address specific failures
- Avoid the temptation 에 rewrite 처음부터
- Consider if 테스트합니다 themselves need adjustment

## 통합 Points

- Follows 에서 tdd-red.md test creation
- Prepares 위한 tdd-refactor.md improvements
- Updates test coverage metrics
- Triggers CI/CD 파이프라인 verification
- Documents 기술 부채 위한 tracking

## 모범 사례

- Embrace "good enough" 위한 this phase
- Speed over perfection (perfection comes 에서 refactor)
- Make it work, then make it right, then make it fast
- Trust that refactoring phase will improve code
- Keep changes small 및 incremental
- Celebrate reaching green state!

## Complete 구현 Examples

### Example 1: Minimal → Production-Ready (User Service)

**Test Requirements:**
```typescript
describe('UserService', () => {
  it('should create a new user', async () => {
    const user = await userService.create({ email: 'test@example.com', name: 'Test' });
    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });

  it('should find user by email', async () => {
    await userService.create({ email: 'test@example.com', name: 'Test' });
    const user = await userService.findByEmail('test@example.com');
    expect(user).toBeDefined();
  });
});
```

**Stage 1: Fake It (Minimal)**
```typescript
class UserService {
  create(data: { email: string; name: string }) {
    return { id: '123', email: data.email, name: data.name };
  }

  findByEmail(email: string) {
    return { id: '123', email: email, name: 'Test' };
  }
}
```
*테스트합니다 pass. 구현 is obviously fake but 검증합니다 test structure.*

**Stage 2: 간단한 Real 구현**
```typescript
class UserService {
  private users: Map<string, User> = new Map();
  private nextId = 1;

  create(data: { email: string; name: string }) {
    const user = { id: String(this.nextId++), ...data };
    this.users.set(user.email, user);
    return user;
  }

  findByEmail(email: string) {
    return this.users.get(email) || null;
  }
}
```
*에서-memory storage. 테스트합니다 pass. Good enough 위한 green phase.*

**Stage 3: Production-Ready (Refactor Phase)**
```typescript
class UserService {
  constructor(private db: Database) {}

  async create(data: { email: string; name: string }) {
    const existing = await this.db.query('SELECT * FROM users WHERE email = ?', [data.email]);
    if (existing) throw new Error('User exists');

    const id = await this.db.insert('users', data);
    return { id, ...data };
  }

  async findByEmail(email: string) {
    return this.db.queryOne('SELECT * FROM users WHERE email = ?', [email]);
  }
}
```
*Database 통합, error handling, validation - saved 위한 refactor phase.*

### Example 2: API-First 구현 (Express)

**Test Requirements:**
```javascript
describe('POST /api/tasks', () => {
  it('should create task and return 201', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send({ title: 'Test Task' });

    expect(res.status).toBe(201);
    expect(res.body.id).toBeDefined();
    expect(res.body.title).toBe('Test Task');
  });
});
```

**Stage 1: Hardcoded Response**
```javascript
app.post('/api/tasks', (req, res) => {
  res.status(201).json({ id: '1', title: req.body.title });
});
```
*테스트합니다 pass immediately. No logic needed yet.*

**Stage 2: 간단한 Logic**
```javascript
let tasks = [];
let nextId = 1;

app.post('/api/tasks', (req, res) => {
  const task = { id: String(nextId++), title: req.body.title };
  tasks.push(task);
  res.status(201).json(task);
});
```
*Minimal state management. Ready 위한 more 테스트합니다.*

**Stage 3: Layered 아키텍처 (Refactor)**
```javascript
// Controller
app.post('/api/tasks', async (req, res) => {
  try {
    const task = await taskService.create(req.body);
    res.status(201).json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Service layer
class TaskService {
  constructor(private repository: TaskRepository) {}

  async create(data: CreateTaskDto): Promise<Task> {
    this.validate(data);
    return this.repository.save(data);
  }
}
```
*Proper separation of concerns added 동안 refactor phase.*

### Example 3: Database 통합 (Django)

**Test Requirements:**
```python
def test_product_creation():
    product = Product.objects.create(name="Widget", price=9.99)
    assert product.id is not None
    assert product.name == "Widget"

def test_product_price_validation():
    with pytest.raises(ValidationError):
        Product.objects.create(name="Widget", price=-1)
```

**Stage 1: Model Only**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```
*First test passes. Second test fails - validation not implemented.*

**Stage 2: Add Validation**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
```
*All 테스트합니다 pass. Minimal validation logic added.*

**Stage 3: Rich Domain Model (Refactor)**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['category', '-created_at'])]

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.price > 10000:
            raise ValidationError("Price exceeds maximum")

    def apply_discount(self, percentage: float) -> Decimal:
        return self.price * (1 - percentage / 100)
```
*Additional features, indexes, 비즈니스 로직 added 필요할 때.*

### Example 4: React Component 구현

**Test Requirements:**
```typescript
describe('UserProfile', () => {
  it('should display user name', () => {
    render(<UserProfile user={{ name: 'John', email: 'john@test.com' }} />);
    expect(screen.getByText('John')).toBeInTheDocument();
  });

  it('should display email', () => {
    render(<UserProfile user={{ name: 'John', email: 'john@test.com' }} />);
    expect(screen.getByText('john@test.com')).toBeInTheDocument();
  });
});
```

**Stage 1: Minimal JSX**
```typescript
interface UserProfileProps {
  user: { name: string; email: string };
}

const UserProfile: React.FC<UserProfileProps> = ({ user }) => (
  <div>
    <div>{user.name}</div>
    <div>{user.email}</div>
  </div>
);
```
*테스트합니다 pass. No styling, no structure.*

**Stage 2: 기본 Structure**
```typescript
const UserProfile: React.FC<UserProfileProps> = ({ user }) => (
  <div className="user-profile">
    <h2>{user.name}</h2>
    <p>{user.email}</p>
  </div>
);
```
*Added semantic HTML, className 위한 styling hook.*

**Stage 3: Production Component (Refactor)**
```typescript
const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="user-profile" role="article" aria-label="User profile">
      <header>
        <h2>{user.name}</h2>
        <button onClick={() => setIsEditing(true)} aria-label="Edit profile">
          Edit
        </button>
      </header>
      <section>
        <p>{user.email}</p>
        {user.bio && <p>{user.bio}</p>}
      </section>
    </div>
  );
};
```
*Accessibility, interaction, additional features added incrementally.*

## Decision Frameworks

### Framework 1: Fake vs. Real 구현

**When 에 Fake It:**
- First test 위한 a new feature
- 복잡한 external dependencies (payment gateways, APIs)
- 구현 approach is still uncertain
- Need 에 validate test structure first
- Time pressure 에 see all 테스트합니다 green

**When 에 Go Real:**
- Second 또는 third test reveals 패턴
- 구현 is obvious 및 간단한
- Faking would be more 복잡한 than real code
- Need 에 test 통합 points
- 테스트합니다 explicitly require real behavior

**Decision Matrix:**
```
Complexity Low     | High
         ↓         | ↓
Simple   → REAL    | FAKE first, real later
Complex  → REAL    | FAKE, evaluate alternatives
```

### Framework 2: Complexity Trade-off Analysis

**Simplicity Score Calculation:**
```
Score = (Lines of Code) + (Cyclomatic Complexity × 2) + (Dependencies × 3)

< 20  → Simple enough, implement directly
20-50 → Consider simpler alternative
> 50  → Defer complexity to refactor phase
```

**Example Evaluation:**
```typescript
// Option A: Direct implementation (Score: 45)
function calculateShipping(weight: number, distance: number, express: boolean): number {
  let base = weight * 0.5 + distance * 0.1;
  if (express) base *= 2;
  if (weight > 50) base += 10;
  if (distance > 1000) base += 20;
  return base;
}

// Option B: Simplest for green phase (Score: 15)
function calculateShipping(weight: number, distance: number, express: boolean): number {
  return express ? 50 : 25; // Fake it until more tests drive real logic
}
```
*Choose Option B 위한 green phase, evolve 에 Option A as 테스트합니다 require.*

### Framework 3: 성능 Consideration Timing

**Green Phase: Focus 에 Correctness**
```
❌ Avoid:
- Caching strategies
- Database query optimization
- Algorithmic complexity improvements
- Premature memory optimization

✓ Accept:
- O(n²) if it makes code simpler
- Multiple database queries
- Synchronous operations
- Inefficient but clear algorithms
```

**When 성능 Matters 에서 Green Phase:**
1. 성능 is explicit test requirement
2. 구현 would cause timeout 에서 test suite
3. Memory leak would crash 테스트합니다
4. Resource exhaustion prevents 테스트

**성능 테스트 통합:**
```typescript
// Add performance test AFTER functional tests pass
describe('Performance', () => {
  it('should handle 1000 users within 100ms', () => {
    const start = Date.now();
    for (let i = 0; i < 1000; i++) {
      userService.create({ email: `user${i}@test.com`, name: `User ${i}` });
    }
    expect(Date.now() - start).toBeLessThan(100);
  });
});
```

## Framework-Specific Patterns

### React Patterns

**간단한 Component → Hooks → Context:**
```typescript
// Green Phase: Props only
const Counter = ({ count, onIncrement }) => (
  <button onClick={onIncrement}>{count}</button>
);

// Refactor: Add hooks
const Counter = () => {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
};

// Refactor: Extract to context
const Counter = () => {
  const { count, increment } = useCounter();
  return <button onClick={increment}>{count}</button>;
};
```

### Django Patterns

**Function View → Class View → Generic View:**
```python
# Green Phase: Simple function
def product_list(request):
    products = Product.objects.all()
    return JsonResponse({'products': list(products.values())})

# Refactor: Class-based view
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return JsonResponse({'products': list(products.values())})

# Refactor: Generic view
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
```

### Express Patterns

**Inline → Middleware → Service Layer:**
```javascript
// Green Phase: Inline logic
app.post('/api/users', (req, res) => {
  const user = { id: Date.now(), ...req.body };
  users.push(user);
  res.json(user);
});

// Refactor: Extract middleware
app.post('/api/users', validateUser, (req, res) => {
  const user = userService.create(req.body);
  res.json(user);
});

// Refactor: Full layering
app.post('/api/users',
  validateUser,
  asyncHandler(userController.create)
);
```

## Refactoring Resistance Patterns

### 패턴 1: Test Anchor Points

Keep 테스트합니다 green 동안 refactoring 에 의해 maintaining interface contracts:

```typescript
// Original implementation (tests green)
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// Refactoring: Add tax calculation (keep interface)
function calculateTotal(items: Item[]): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  const tax = subtotal * 0.1;
  return subtotal + tax;
}

// Tests still green because return type/behavior unchanged
```

### 패턴 2: Parallel 구현

Run old 및 new implementations side 에 의해 side:

```python
def process_order(order):
    # Old implementation (tests depend on this)
    result_old = legacy_process(order)

    # New implementation (testing in parallel)
    result_new = new_process(order)

    # Verify they match
    assert result_old == result_new, "Implementation mismatch"

    return result_old  # Keep tests green
```

### 패턴 3: Feature Flags 위한 Refactoring

```javascript
class PaymentService {
  processPayment(amount) {
    if (config.USE_NEW_PAYMENT_PROCESSOR) {
      return this.newPaymentProcessor(amount);
    }
    return this.legacyPaymentProcessor(amount);
  }
}
```

## 성능-First Green Phase Strategies

### Strategy 1: Type-Driven Development

Use types 에 guide minimal 구현:

```typescript
// Types define contract
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

// Green phase: In-memory implementation
class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async findById(id: string) {
    return this.users.get(id) || null;
  }

  async save(user: User) {
    this.users.set(user.id, user);
  }
}

// Refactor: Database implementation (same interface)
class DatabaseUserRepository implements UserRepository {
  constructor(private db: Database) {}

  async findById(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }

  async save(user: User) {
    await this.db.insert('users', user);
  }
}
```

### Strategy 2: Contract 테스트 통합

```typescript
// Define contract
const userServiceContract = {
  create: {
    input: { email: 'string', name: 'string' },
    output: { id: 'string', email: 'string', name: 'string' }
  }
};

// Green phase: Implementation matches contract
class UserService {
  create(data: { email: string; name: string }) {
    return { id: '123', ...data }; // Minimal but contract-compliant
  }
}

// Contract test ensures compliance
describe('UserService Contract', () => {
  it('should match create contract', () => {
    const result = userService.create({ email: 'test@test.com', name: 'Test' });
    expect(typeof result.id).toBe('string');
    expect(typeof result.email).toBe('string');
    expect(typeof result.name).toBe('string');
  });
});
```

### Strategy 3: Continuous Refactoring 워크플로우

**Micro-Refactoring 동안 Green Phase:**

```python
# Test passes with this
def calculate_discount(price, customer_type):
    if customer_type == 'premium':
        return price * 0.8
    return price

# Immediate micro-refactor (tests still green)
DISCOUNT_RATES = {
    'premium': 0.8,
    'standard': 1.0
}

def calculate_discount(price, customer_type):
    rate = DISCOUNT_RATES.get(customer_type, 1.0)
    return price * rate
```

**Safe Refactoring Checklist:**
- ✓ 테스트합니다 green 이전 refactoring
- ✓ Change one thing 에서 a time
- ✓ Run 테스트합니다 이후 each change
- ✓ Commit 이후 each successful refactor
- ✓ No behavior changes, only structure

## 현대적인 Development Practices (2024/2025)

### Type-Driven Development

**Python Type Hints:**
```python
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    name: str

class UserService:
    def create(self, email: str, name: str) -> User:
        return User(id="123", email=email, name=name)

    def find_by_email(self, email: str) -> Optional[User]:
        return None  # Minimal implementation
```

**TypeScript Strict Mode:**
```typescript
// Enable strict mode in tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}

// Implementation guided by types
interface CreateUserDto {
  email: string;
  name: string;
}

class UserService {
  create(data: CreateUserDto): User {
    // Type system enforces contract
    return { id: '123', email: data.email, name: data.name };
  }
}
```

### AI-Assisted Green Phase

**사용하여 Copilot/AI Tools:**
1. Write test first (human-driven)
2. Let AI suggest minimal 구현
3. Verify suggestion passes 테스트합니다
4. Accept if truly minimal, reject if over-engineered
5. Iterate 와 함께 AI 위한 refactoring phase

**AI Prompt 패턴:**
```
Given these failing tests:
[paste tests]

Provide the MINIMAL implementation that makes tests pass.
Do not add error handling, validation, or features beyond test requirements.
Focus on simplicity over completeness.
```

### Cloud-Native Patterns

**Local → Container → Cloud:**
```javascript
// Green Phase: Local implementation
class CacheService {
  private cache = new Map();

  get(key) { return this.cache.get(key); }
  set(key, value) { this.cache.set(key, value); }
}

// Refactor: Redis-compatible interface
class CacheService {
  constructor(private redis) {}

  async get(key) { return this.redis.get(key); }
  async set(key, value) { return this.redis.set(key, value); }
}

// Production: Distributed cache with fallback
class CacheService {
  constructor(private redis, private fallback) {}

  async get(key) {
    try {
      return await this.redis.get(key);
    } catch {
      return this.fallback.get(key);
    }
  }
}
```

### 관찰 가능성-Driven Development

**Add 관찰 가능성 hooks 동안 green phase:**
```typescript
class OrderService {
  async createOrder(data: CreateOrderDto): Promise<Order> {
    console.log('[OrderService] Creating order', { data }); // Simple logging

    const order = { id: '123', ...data };

    console.log('[OrderService] Order created', { orderId: order.id }); // Success log

    return order;
  }
}

// Refactor: Structured logging
class OrderService {
  constructor(private logger: Logger) {}

  async createOrder(data: CreateOrderDto): Promise<Order> {
    this.logger.info('order.create.start', { data });

    const order = await this.repository.save(data);

    this.logger.info('order.create.success', {
      orderId: order.id,
      duration: Date.now() - start
    });

    return order;
  }
}
```

테스트합니다 에 make pass: $ARGUMENTS