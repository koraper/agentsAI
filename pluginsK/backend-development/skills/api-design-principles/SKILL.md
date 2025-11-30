---
name: api-design-principles
description: 마스터 REST 및 GraphQL API 설계 원칙 에 빌드 intuitive, scalable, 및 maintainable APIs 것 delight developers. Use 때 designing 새로운 APIs, 검토하는 API 사양, 또는 establishing API 설계 표준.
---

# API 설계 원칙

마스터 REST 및 GraphQL API 설계 원칙 에 빌드 intuitive, scalable, 및 maintainable APIs 것 delight developers 및 stand the test of 시간.

## 때 에 Use This Skill

- Designing 새로운 REST 또는 GraphQL APIs
- 리팩토링 기존 APIs 위한 더 나은 사용성
- Establishing API 설계 표준 위한 your 팀
- 검토하는 API 사양 이전 구현
- Migrating 사이 API paradigms (REST 에 GraphQL, etc.)
- 생성하는 개발자 친화적인 API 문서화
- Optimizing APIs 위한 특정 use cases (mobile, third-party integrations)

## 핵심 개념

### 1. RESTful 설계 원칙

**리소스-Oriented 아키텍처**
- 리소스 are nouns (사용자, 정렬합니다, products), not verbs
- Use HTTP 메서드 위한 actions (GET, POST, PUT, PATCH, DELETE)
- URLs represent 리소스 hierarchies
- 일관된 naming 규약

**HTTP 메서드 의미론:**
- `GET`: Retrieve 리소스 (idempotent, safe)
- `POST`: Create 새로운 리소스
- `PUT`: Replace entire 리소스 (idempotent)
- `PATCH`: 부분 리소스 업데이트합니다
- `DELETE`: Remove 리소스 (idempotent)

### 2. GraphQL 설계 원칙

**스키마 우선 개발**
- 유형 define your 도메인 모델
- 쿼리 위한 읽는 데이터
- Mutations 위한 modifying 데이터
- Subscriptions 위한 real-시간 업데이트합니다

**쿼리 구조:**
- 클라이언트 요청 정확하게 무엇 they need
- Single 엔드포인트, 여러 작업
- 강하게 typed 스키마
- Introspection 구축된-에서

### 3. API Versioning Strategies

**URL Versioning:**
```
/api/v1/users
/api/v2/users
```

**헤더 Versioning:**
```
Accept: application/vnd.api+json; version=1
```

**쿼리 매개변수 Versioning:**
```
/api/users?version=1
```

## REST API 설계 패턴

### 패턴 1: 리소스 컬렉션 설계

```python
# Good: Resource-oriented endpoints
GET    /api/users              # List users (with pagination)
POST   /api/users              # Create user
GET    /api/users/{id}         # Get specific user
PUT    /api/users/{id}         # Replace user
PATCH  /api/users/{id}         # Update user fields
DELETE /api/users/{id}         # Delete user

# Nested resources
GET    /api/users/{id}/orders  # Get user's orders
POST   /api/users/{id}/orders  # Create order for user

# Bad: Action-oriented endpoints (avoid)
POST   /api/createUser
POST   /api/getUserById
POST   /api/deleteUser
```

### 패턴 2: Pagination 및 필터링

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

class FilterParams(BaseModel):
    status: Optional[str] = None
    created_after: Optional[str] = None
    search: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

# FastAPI endpoint example
from fastapi import FastAPI, Query, Depends

app = FastAPI()

@app.get("/api/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    # Apply filters
    query = build_query(status=status, search=search)

    # Count total
    total = await count_users(query)

    # Fetch page
    offset = (page - 1) * page_size
    users = await fetch_users(query, limit=page_size, offset=offset)

    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )
```

### 패턴 3: 오류 처리 및 상태 Codes

```python
from fastapi import HTTPException, status
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: str
    path: str

class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    value: Any

# Consistent error responses
STATUS_CODES = {
    "success": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "unprocessable": 422,
    "internal_error": 500
}

def raise_not_found(resource: str, id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NotFound",
            "message": f"{resource} not found",
            "details": {"id": id}
        }
    )

def raise_validation_error(errors: List[ValidationErrorDetail]):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "error": "ValidationError",
            "message": "Request validation failed",
            "details": {"errors": [e.dict() for e in errors]}
        }
    )

# Example usage
@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    user = await fetch_user(user_id)
    if not user:
        raise_not_found("User", user_id)
    return user
```

### 패턴 4: HATEOAS (Hypermedia 처럼 the Engine of 애플리케이션 상태)

```python
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    _links: dict

    @classmethod
    def from_user(cls, user: User, base_url: str):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            _links={
                "self": {"href": f"{base_url}/api/users/{user.id}"},
                "orders": {"href": f"{base_url}/api/users/{user.id}/orders"},
                "update": {
                    "href": f"{base_url}/api/users/{user.id}",
                    "method": "PATCH"
                },
                "delete": {
                    "href": f"{base_url}/api/users/{user.id}",
                    "method": "DELETE"
                }
            }
        )
```

## GraphQL 설계 패턴

### 패턴 1: 스키마 설계

```graphql
# schema.graphql

# Clear type definitions
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!

  # Relationships
  orders(
    first: Int = 20
    after: String
    status: OrderStatus
  ): OrderConnection!

  profile: UserProfile
}

type Order {
  id: ID!
  status: OrderStatus!
  total: Money!
  items: [OrderItem!]!
  createdAt: DateTime!

  # Back-reference
  user: User!
}

# Pagination pattern (Relay-style)
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Enums for type safety
enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

# Custom scalars
scalar DateTime
scalar Money

# Query root
type Query {
  user(id: ID!): User
  users(
    first: Int = 20
    after: String
    search: String
  ): UserConnection!

  order(id: ID!): Order
}

# Mutation root
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!

  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}

# Input types for mutations
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

# Payload types for mutations
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
}
```

### 패턴 2: 리졸버 설계

```python
from typing import Optional, List
from ariadne import QueryType, MutationType, ObjectType
from dataclasses import dataclass

query = QueryType()
mutation = MutationType()
user_type = ObjectType("User")

@query.field("user")
async def resolve_user(obj, info, id: str) -> Optional[dict]:
    """Resolve single user by ID."""
    return await fetch_user_by_id(id)

@query.field("users")
async def resolve_users(
    obj,
    info,
    first: int = 20,
    after: Optional[str] = None,
    search: Optional[str] = None
) -> dict:
    """Resolve paginated user list."""
    # Decode cursor
    offset = decode_cursor(after) if after else 0

    # Fetch users
    users = await fetch_users(
        limit=first + 1,  # Fetch one extra to check hasNextPage
        offset=offset,
        search=search
    )

    # Pagination
    has_next = len(users) > first
    if has_next:
        users = users[:first]

    edges = [
        {
            "node": user,
            "cursor": encode_cursor(offset + i)
        }
        for i, user in enumerate(users)
    ]

    return {
        "edges": edges,
        "pageInfo": {
            "hasNextPage": has_next,
            "hasPreviousPage": offset > 0,
            "startCursor": edges[0]["cursor"] if edges else None,
            "endCursor": edges[-1]["cursor"] if edges else None
        },
        "totalCount": await count_users(search=search)
    }

@user_type.field("orders")
async def resolve_user_orders(user: dict, info, first: int = 20) -> dict:
    """Resolve user's orders (N+1 prevention with DataLoader)."""
    # Use DataLoader to batch requests
    loader = info.context["loaders"]["orders_by_user"]
    orders = await loader.load(user["id"])

    return paginate_orders(orders, first)

@mutation.field("createUser")
async def resolve_create_user(obj, info, input: dict) -> dict:
    """Create new user."""
    try:
        # Validate input
        validate_user_input(input)

        # Create user
        user = await create_user(
            email=input["email"],
            name=input["name"],
            password=hash_password(input["password"])
        )

        return {
            "user": user,
            "errors": []
        }
    except ValidationError as e:
        return {
            "user": None,
            "errors": [{"field": e.field, "message": e.message}]
        }
```

### 패턴 3: DataLoader (N+1 문제 방지)

```python
from aiodataloader import DataLoader
from typing import List, Optional

class UserLoader(DataLoader):
    """Batch load users by ID."""

    async def batch_load_fn(self, user_ids: List[str]) -> List[Optional[dict]]:
        """Load multiple users in single query."""
        users = await fetch_users_by_ids(user_ids)

        # Map results back to input order
        user_map = {user["id"]: user for user in users}
        return [user_map.get(user_id) for user_id in user_ids]

class OrdersByUserLoader(DataLoader):
    """Batch load orders by user ID."""

    async def batch_load_fn(self, user_ids: List[str]) -> List[List[dict]]:
        """Load orders for multiple users in single query."""
        orders = await fetch_orders_by_user_ids(user_ids)

        # Group orders by user_id
        orders_by_user = {}
        for order in orders:
            user_id = order["user_id"]
            if user_id not in orders_by_user:
                orders_by_user[user_id] = []
            orders_by_user[user_id].append(order)

        # Return in input order
        return [orders_by_user.get(user_id, []) for user_id in user_ids]

# Context setup
def create_context():
    return {
        "loaders": {
            "user": UserLoader(),
            "orders_by_user": OrdersByUserLoader()
        }
    }
```

## 최선의 관행

### REST APIs
1. **일관된 Naming**: Use plural nouns 위한 collections (`/users`, not `/user`)
2. **Stateless**: 각 요청 contains 모든 필요한 정보
3. **Use HTTP 상태 Codes 올바르게**: 2xx success, 4xx 클라이언트 오류, 5xx 서버 오류
4. **버전 Your API**: Plan 위한 breaking 변경합니다 에서 day one
5. **Pagination**: 항상 paginate large collections
6. **속도 제한**: Protect your API 와 함께 rate 제한합니다
7. **문서화**: Use OpenAPI/Swagger 위한 interactive docs

### GraphQL APIs
1. **스키마 첫 번째**: 설계 스키마 이전 작성 resolvers
2. **Avoid N+1**: Use DataLoaders 위한 efficient 데이터 가져오는
3. **입력 검증**: Validate 에서 스키마 및 리졸버 levels
4. **오류 처리**: 반환 구조화된 오류 에서 mutation 페이로드
5. **Pagination**: Use cursor-based pagination (Relay spec)
6. **Deprecation**: Use `@deprecated` 지시문 위한 gradual 마이그레이션
7. **모니터링**: Track 쿼리 complexity 및 실행 시간

## 일반적인 Pitfalls

- **Over-가져오는/Under-가져오는 (REST)**: 고정된 에서 GraphQL 그러나 필요합니다 DataLoaders
- **Breaking 변경합니다**: 버전 APIs 또는 use deprecation strategies
- **일관되지 않은 오류 형식을 지정합니다**: Standardize 오류 응답
- **Missing Rate 제한합니다**: APIs 없이 제한합니다 are vulnerable 에 abuse
- **Poor 문서화**: Undocumented APIs frustrate developers
- **Ignoring HTTP 의미론**: POST 위한 idempotent 작업 breaks expectations
- **Tight 결합**: API 구조 shouldn't mirror 데이터베이스 스키마

## 리소스

- **참조/rest-최선의-관행.md**: 포괄적인 REST API 설계 가이드
- **참조/graphql-스키마-설계.md**: GraphQL 스키마 패턴 및 anti-패턴
- **참조/api-versioning-strategies.md**: Versioning approaches 및 마이그레이션 경로
- **자산/rest-api-템플릿.py**: FastAPI REST API 템플릿
- **자산/graphql-스키마-템플릿.graphql**: 완전한 GraphQL 스키마 예제
- **자산/api-설계-checklist.md**: Pre-구현 review checklist
- **스크립트/openapi-생성기.py**: Generate OpenAPI specs 에서 코드
