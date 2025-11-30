# REST API 최선의 관행

## URL 구조

### 리소스 Naming
```
# Good - Plural nouns
GET /api/users
GET /api/orders
GET /api/products

# Bad - Verbs or mixed conventions
GET /api/getUser
GET /api/user  (inconsistent singular)
POST /api/createOrder
```

### Nested 리소스
```
# Shallow nesting (preferred)
GET /api/users/{id}/orders
GET /api/orders/{id}

# Deep nesting (avoid)
GET /api/users/{id}/orders/{orderId}/items/{itemId}/reviews
# Better:
GET /api/order-items/{id}/reviews
```

## HTTP 메서드 및 상태 Codes

### GET - Retrieve 리소스
```
GET /api/users              → 200 OK (with list)
GET /api/users/{id}         → 200 OK or 404 Not Found
GET /api/users?page=2       → 200 OK (paginated)
```

### POST - Create 리소스
```
POST /api/users
  Body: {"name": "John", "email": "john@example.com"}
  → 201 Created
  Location: /api/users/123
  Body: {"id": "123", "name": "John", ...}

POST /api/users (validation error)
  → 422 Unprocessable Entity
  Body: {"errors": [...]}
```

### PUT - Replace 리소스
```
PUT /api/users/{id}
  Body: {complete user object}
  → 200 OK (updated)
  → 404 Not Found (doesn't exist)

# Must include ALL fields
```

### PATCH - 부분 업데이트
```
PATCH /api/users/{id}
  Body: {"name": "Jane"}  (only changed fields)
  → 200 OK
  → 404 Not Found
```

### DELETE - Remove 리소스
```
DELETE /api/users/{id}
  → 204 No Content (deleted)
  → 404 Not Found
  → 409 Conflict (can't delete due to references)
```

## 필터링, 정렬, 및 Searching

### 쿼리 매개변수
```
# Filtering
GET /api/users?status=active
GET /api/users?role=admin&status=active

# Sorting
GET /api/users?sort=created_at
GET /api/users?sort=-created_at  (descending)
GET /api/users?sort=name,created_at

# Searching
GET /api/users?search=john
GET /api/users?q=john

# Field selection (sparse fieldsets)
GET /api/users?fields=id,name,email
```

## Pagination 패턴

### 오프셋-Based Pagination
```python
GET /api/users?page=2&page_size=20

Response:
{
  "items": [...],
  "page": 2,
  "page_size": 20,
  "total": 150,
  "pages": 8
}
```

### Cursor-Based Pagination (위한 large datasets)
```python
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ

Response:
{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ",
  "has_more": true
}
```

### 링크 헤더 Pagination (RESTful)
```
GET /api/users?page=2

Response Headers:
Link: <https://api.example.com/users?page=3>; rel="next",
      <https://api.example.com/users?page=1>; rel="prev",
      <https://api.example.com/users?page=1>; rel="first",
      <https://api.example.com/users?page=8>; rel="last"
```

## Versioning Strategies

### URL Versioning (권장됨)
```
/api/v1/users
/api/v2/users

Pros: Clear, easy to route
Cons: Multiple URLs for same resource
```

### 헤더 Versioning
```
GET /api/users
Accept: application/vnd.api+json; version=2

Pros: Clean URLs
Cons: Less visible, harder to test
```

### 쿼리 매개변수
```
GET /api/users?version=2

Pros: Easy to test
Cons: Optional parameter can be forgotten
```

## 속도 제한

### 헤더
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1640000000

Response when limited:
429 Too Many Requests
Retry-After: 3600
```

### 구현 패턴
```python
from fastapi import HTTPException, Request
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.cache = {}

    def check(self, key: str) -> bool:
        now = datetime.now()
        if key not in self.cache:
            self.cache[key] = []

        # Remove old requests
        self.cache[key] = [
            ts for ts in self.cache[key]
            if now - ts < timedelta(seconds=self.period)
        ]

        if len(self.cache[key]) >= self.calls:
            return False

        self.cache[key].append(now)
        return True

limiter = RateLimiter(calls=100, period=60)

@app.get("/api/users")
async def get_users(request: Request):
    if not limiter.check(request.client.host):
        raise HTTPException(
            status_code=429,
            headers={"Retry-After": "60"}
        )
    return {"users": [...]}
```

## 인증 및 인가

### Bearer 토큰
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

401 Unauthorized - Missing/invalid token
403 Forbidden - Valid token, insufficient permissions
```

### API 키
```
X-API-Key: your-api-key-here
```

## 오류 응답 Format

### 일관된 구조
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "not-an-email"
      }
    ],
    "timestamp": "2025-10-16T12:00:00Z",
    "path": "/api/users"
  }
}
```

### 상태 코드 가이드라인
- `200 OK`: 성공한 GET, PATCH, PUT
- `201 Created`: 성공한 POST
- `204 No Content`: 성공한 DELETE
- `400 Bad Request`: Malformed 요청
- `401 Unauthorized`: 인증 필수
- `403 Forbidden`: 인증된 그러나 not 인가된
- `404 Not Found`: 리소스 doesn't exist
- `409 Conflict`: 상태 conflict (중복 email, etc.)
- `422 Unprocessable Entity`: 검증 오류
- `429 Too Many Requests`: Rate 제한된
- `500 Internal Server Error`: 서버 오류
- `503 Service Unavailable`: 임시 downtime

## 캐싱

### 캐시 헤더
```
# Client caching
Cache-Control: public, max-age=3600

# No caching
Cache-Control: no-cache, no-store, must-revalidate

# Conditional requests
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
→ 304 Not Modified
```

## Bulk 작업

### Batch 엔드포인트
```python
POST /api/users/batch
{
  "items": [
    {"name": "User1", "email": "user1@example.com"},
    {"name": "User2", "email": "user2@example.com"}
  ]
}

Response:
{
  "results": [
    {"id": "1", "status": "created"},
    {"id": null, "status": "failed", "error": "Email already exists"}
  ]
}
```

## Idempotency

### Idempotency 키
```
POST /api/orders
Idempotency-Key: unique-key-123

If duplicate request:
→ 200 OK (return cached response)
```

## CORS 구성

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 문서화 와 함께 OpenAPI

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API for managing users",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get(
    "/api/users/{user_id}",
    summary="Get user by ID",
    response_description="User details",
    tags=["Users"]
)
async def get_user(
    user_id: str = Path(..., description="The user ID")
):
    """
    Retrieve user by ID.

    Returns full user profile including:
    - Basic information
    - Contact details
    - Account status
    """
    pass
```

## Health 및 모니터링 엔드포인트

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health/detailed")
async def detailed_health():
    return {
        "status": "healthy",
        "checks": {
            "database": await check_database(),
            "redis": await check_redis(),
            "external_api": await check_external_api()
        }
    }
```
