---
name: error-handling-patterns
description: 마스터 오류 처리 패턴 전반에 걸쳐 languages 포함하여 예외, Result 유형, 오류 전파, 및 graceful degradation 에 빌드 복원력 있는 애플리케이션. Use 때 implementing 오류 처리, designing APIs, 또는 improving 애플리케이션 신뢰성.
---

# 오류 처리 패턴

빌드 복원력 있는 애플리케이션 와 함께 강력한 오류 처리 strategies 것 gracefully handle 실패 및 provide excellent 디버깅 experiences.

## 때 에 Use This Skill

- Implementing 오류 처리 에서 새로운 기능
- Designing 오류-복원력 있는 APIs
- 디버깅 production 이슈
- Improving 애플리케이션 신뢰성
- 생성하는 더 나은 오류 메시지 위한 사용자 및 developers
- Implementing 재시도 및 회로 breaker 패턴
- 처리 비동기/concurrent 오류
- 구축 장애 허용 분산 시스템

## 핵심 개념

### 1. 오류 처리 Philosophies

**예외 vs Result 유형:**
- **예외**: 전통적인 try-catch, disrupts control 흐름
- **Result 유형**: 명시적인 success/실패, 기능적인 접근법
- **오류 Codes**: C-스타일, 필요합니다 discipline
- **Option/아마도 유형**: 위한 nullable 값

**때 에 Use 각:**
- 예외: Unexpected 오류, 예외적인 conditions
- Result 유형: 예상되는 오류, 검증 실패
- Panics/Crashes: Unrecoverable 오류, programming 버그

### 2. 오류 Categories

**Recoverable 오류:**
- 네트워크 timeouts
- Missing 파일
- 유효하지 않은 사용자 입력
- API rate 제한합니다

**Unrecoverable 오류:**
- Out of 메모리
- 스택 overflow
- Programming 버그 (null 포인터, etc.)

## Language-특정 패턴

### Python 오류 처리

**사용자 정의 예외 계층:**
```python
class ApplicationError(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class ValidationError(ApplicationError):
    """Raised when validation fails."""
    pass

class NotFoundError(ApplicationError):
    """Raised when resource not found."""
    pass

class ExternalServiceError(ApplicationError):
    """Raised when external service fails."""
    def __init__(self, message: str, service: str, **kwargs):
        super().__init__(message, **kwargs)
        self.service = service

# Usage
def get_user(user_id: str) -> User:
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise NotFoundError(
            f"User not found",
            code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )
    return user
```

**컨텍스트 Managers 위한 Cleanup:**
```python
from contextlib import contextmanager

@contextmanager
def database_transaction(session):
    """Ensure transaction is committed or rolled back."""
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with database_transaction(db.session) as session:
    user = User(name="Alice")
    session.add(user)
    # Automatic commit or rollback
```

**재시도 와 함께 Exponential Backoff:**
```python
import time
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar('T')

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        time.sleep(sleep_time)
                        continue
                    raise
            raise last_exception
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, exceptions=(NetworkError,))
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### TypeScript/JavaScript 오류 처리

**사용자 정의 오류 클래스:**
```typescript
// Custom error classes
class ApplicationError extends Error {
    constructor(
        message: string,
        public code: string,
        public statusCode: number = 500,
        public details?: Record<string, any>
    ) {
        super(message);
        this.name = this.constructor.name;
        Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends ApplicationError {
    constructor(message: string, details?: Record<string, any>) {
        super(message, 'VALIDATION_ERROR', 400, details);
    }
}

class NotFoundError extends ApplicationError {
    constructor(resource: string, id: string) {
        super(
            `${resource} not found`,
            'NOT_FOUND',
            404,
            { resource, id }
        );
    }
}

// Usage
function getUser(id: string): User {
    const user = users.find(u => u.id === id);
    if (!user) {
        throw new NotFoundError('User', id);
    }
    return user;
}
```

**Result 유형 패턴:**
```typescript
// Result type for explicit error handling
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

// Helper functions
function Ok<T>(value: T): Result<T, never> {
    return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
    return { ok: false, error };
}

// Usage
function parseJSON<T>(json: string): Result<T, SyntaxError> {
    try {
        const value = JSON.parse(json) as T;
        return Ok(value);
    } catch (error) {
        return Err(error as SyntaxError);
    }
}

// Consuming Result
const result = parseJSON<User>(userJson);
if (result.ok) {
    console.log(result.value.name);
} else {
    console.error('Parse failed:', result.error.message);
}

// Chaining Results
function chain<T, U, E>(
    result: Result<T, E>,
    fn: (value: T) => Result<U, E>
): Result<U, E> {
    return result.ok ? fn(result.value) : result;
}
```

**비동기 오류 처리:**
```typescript
// Async/await with proper error handling
async function fetchUserOrders(userId: string): Promise<Order[]> {
    try {
        const user = await getUser(userId);
        const orders = await getOrders(user.id);
        return orders;
    } catch (error) {
        if (error instanceof NotFoundError) {
            return [];  // Return empty array for not found
        }
        if (error instanceof NetworkError) {
            // Retry logic
            return retryFetchOrders(userId);
        }
        // Re-throw unexpected errors
        throw error;
    }
}

// Promise error handling
function fetchData(url: string): Promise<Data> {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new NetworkError(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Fetch failed:', error);
            throw error;
        });
}
```

### Rust 오류 처리

**Result 및 Option 유형:**
```rust
use std::fs::File;
use std::io::{self, Read};

// Result type for operations that can fail
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // ? operator propagates errors
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Custom error types
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    NotFound(String),
    Validation(String),
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> Self {
        AppError::Io(error)
    }
}

// Using custom error type
fn read_number_from_file(path: &str) -> Result<i32, AppError> {
    let contents = read_file(path)?;  // Auto-converts io::Error
    let number = contents.trim().parse()
        .map_err(AppError::Parse)?;   // Explicitly convert ParseIntError
    Ok(number)
}

// Option for nullable values
fn find_user(id: &str) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Combining Option and Result
fn get_user_age(id: &str) -> Result<u32, AppError> {
    find_user(id)
        .ok_or_else(|| AppError::NotFound(id.to_string()))
        .map(|user| user.age)
}
```

### Go 오류 처리

**명시적인 오류 Returns:**
```go
// Basic error handling
func getUser(id string) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to query user: %w", err)
    }
    if user == nil {
        return nil, errors.New("user not found")
    }
    return user, nil
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}

// Sentinel errors for comparison
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

// Error checking
user, err := getUser("123")
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // Handle not found
    } else {
        // Handle other errors
    }
}

// Error wrapping and unwrapping
func processUser(id string) error {
    user, err := getUser(id)
    if err != nil {
        return fmt.Errorf("process user failed: %w", err)
    }
    // Process user
    return nil
}

// Unwrap errors
err := processUser("123")
if err != nil {
    var valErr *ValidationError
    if errors.As(err, &valErr) {
        fmt.Printf("Validation error: %s\n", valErr.Field)
    }
}
```

## 범용 패턴

### 패턴 1: 회로 Breaker

Prevent 계단식 전파 실패 에서 분산 시스템.

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, TypeVar

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: timedelta = timedelta(seconds=60),
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func: Callable[[], T]) -> T:
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker()

def fetch_data():
    return circuit_breaker.call(lambda: external_api.get_data())
```

### 패턴 2: 오류 집계

Collect 여러 오류 instead of failing 에 첫 번째 오류.

```typescript
class ErrorCollector {
    private errors: Error[] = [];

    add(error: Error): void {
        this.errors.push(error);
    }

    hasErrors(): boolean {
        return this.errors.length > 0;
    }

    getErrors(): Error[] {
        return [...this.errors];
    }

    throw(): never {
        if (this.errors.length === 1) {
            throw this.errors[0];
        }
        throw new AggregateError(
            this.errors,
            `${this.errors.length} errors occurred`
        );
    }
}

// Usage: Validate multiple fields
function validateUser(data: any): User {
    const errors = new ErrorCollector();

    if (!data.email) {
        errors.add(new ValidationError('Email is required'));
    } else if (!isValidEmail(data.email)) {
        errors.add(new ValidationError('Email is invalid'));
    }

    if (!data.name || data.name.length < 2) {
        errors.add(new ValidationError('Name must be at least 2 characters'));
    }

    if (!data.age || data.age < 18) {
        errors.add(new ValidationError('Age must be 18 or older'));
    }

    if (errors.hasErrors()) {
        errors.throw();
    }

    return data as User;
}
```

### 패턴 3: Graceful Degradation

Provide fallback 기능 때 오류 occur.

```python
from typing import Optional, Callable, TypeVar

T = TypeVar('T')

def with_fallback(
    primary: Callable[[], T],
    fallback: Callable[[], T],
    log_error: bool = True
) -> T:
    """Try primary function, fall back to fallback on error."""
    try:
        return primary()
    except Exception as e:
        if log_error:
            logger.error(f"Primary function failed: {e}")
        return fallback()

# Usage
def get_user_profile(user_id: str) -> UserProfile:
    return with_fallback(
        primary=lambda: fetch_from_cache(user_id),
        fallback=lambda: fetch_from_database(user_id)
    )

# Multiple fallbacks
def get_exchange_rate(currency: str) -> float:
    return (
        try_function(lambda: api_provider_1.get_rate(currency))
        or try_function(lambda: api_provider_2.get_rate(currency))
        or try_function(lambda: cache.get_rate(currency))
        or DEFAULT_RATE
    )

def try_function(func: Callable[[], Optional[T]]) -> Optional[T]:
    try:
        return func()
    except Exception:
        return None
```

## 최선의 관행

1. **Fail Fast**: Validate 입력 early, fail 빠르게
2. **Preserve 컨텍스트**: Include 스택 추적합니다, 메타데이터, timestamps
3. **의미 있는 메시지**: Explain 무엇 happened 및 어떻게 에 fix it
4. **Log 적절하게**: 오류 = log, 예상되는 실패 = don't 스팸 로깅합니다
5. **Handle 에서 맞는 레벨**: catch 곳 you can meaningfully handle
6. **Clean Up 리소스**: Use try-finally, 컨텍스트 managers, defer
7. **Don't Swallow 오류**: Log 또는 re-throw, don't silently ignore
8. **유형-Safe 오류**: Use typed 오류 때 possible

```python
# Good error handling example
def process_order(order_id: str) -> Order:
    """Process order with comprehensive error handling."""
    try:
        # Validate input
        if not order_id:
            raise ValidationError("Order ID is required")

        # Fetch order
        order = db.get_order(order_id)
        if not order:
            raise NotFoundError("Order", order_id)

        # Process payment
        try:
            payment_result = payment_service.charge(order.total)
        except PaymentServiceError as e:
            # Log and wrap external service error
            logger.error(f"Payment failed for order {order_id}: {e}")
            raise ExternalServiceError(
                f"Payment processing failed",
                service="payment_service",
                details={"order_id": order_id, "amount": order.total}
            ) from e

        # Update order
        order.status = "completed"
        order.payment_id = payment_result.id
        db.save(order)

        return order

    except ApplicationError:
        # Re-raise known application errors
        raise
    except Exception as e:
        # Log unexpected errors
        logger.exception(f"Unexpected error processing order {order_id}")
        raise ApplicationError(
            "Order processing failed",
            code="INTERNAL_ERROR"
        ) from e
```

## 일반적인 Pitfalls

- **Catching 또한 넓게**: `except Exception` 숨깁니다 버그
- **빈 catch 차단합니다**: Silently swallowing 오류
- **로깅 및 Re-throwing**: 생성합니다 중복 log entries
- **Not 정리 Up**: Forgetting 에 close 파일, 연결
- **Poor 오류 메시지**: "오류 occurred" is not helpful
- **Returning 오류 Codes**: Use 예외 또는 Result 유형
- **Ignoring 비동기 오류**: Unhandled 프로미스 rejections

## 리소스

- **참조/예외-계층-설계.md**: Designing 오류 클래스 hierarchies
- **참조/오류-복구-strategies.md**: 복구 패턴 위한 다른 scenarios
- **참조/비동기-오류-처리.md**: 처리 오류 에서 concurrent 코드
- **자산/오류-처리-checklist.md**: Review checklist 위한 오류 처리
- **자산/오류-메시지-가이드.md**: 작성 helpful 오류 메시지
- **스크립트/오류-분석기.py**: Analyze 오류 패턴 에서 로깅합니다
