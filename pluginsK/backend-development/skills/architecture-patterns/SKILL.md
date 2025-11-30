---
name: architecture-patterns
description: Implement 입증된 backend 아키텍처 패턴 포함하여 Clean 아키텍처, Hexagonal 아키텍처, 및 도메인 주도 설계. Use 때 architecting 복잡한 backend 시스템 또는 리팩토링 기존 애플리케이션 위한 더 나은 유지보수성.
---

# 아키텍처 패턴

마스터 입증된 backend 아키텍처 패턴 포함하여 Clean 아키텍처, Hexagonal 아키텍처, 및 도메인 주도 설계 에 빌드 maintainable, testable, 및 scalable 시스템.

## 때 에 Use This Skill

- Designing 새로운 backend 시스템 에서 scratch
- 리팩토링 모놀리식 애플리케이션 위한 더 나은 유지보수성
- Establishing 아키텍처 표준 위한 your 팀
- Migrating 에서 밀접하게 결합된 에 느슨하게 결합된 아키텍처
- Implementing 도메인 주도 설계 원칙
- 생성하는 testable 및 mockable codebases
- 계획 microservices 분해

## 핵심 개념

### 1. Clean 아키텍처 (Uncle Bob)

**Layers (종속성 흐릅니다 inward):**
- **엔터티**: 핵심 비즈니스 모델
- **Use Cases**: 애플리케이션 비즈니스 규칙
- **인터페이스 Adapters**: 컨트롤러, presenters, gateways
- **프레임워크 & Drivers**: UI, 데이터베이스, 외부 서비스

**키 원칙:**
- 종속성 포인트 inward
- 내부 layers know nothing 약 외부 layers
- 비즈니스 logic 독립적인 of 프레임워크
- Testable 없이 UI, 데이터베이스, 또는 외부 서비스

### 2. Hexagonal 아키텍처 (Ports 및 Adapters)

**컴포넌트:**
- **도메인 핵심**: 비즈니스 logic
- **Ports**: 인터페이스 defining interactions
- **Adapters**: Implementations of ports (데이터베이스, REST, 메시지 큐)

**Benefits:**
- Swap implementations easily (mock 위한 테스트)
- Technology-agnostic 핵심
- 명확한 분리 of concerns

### 3. 도메인 주도 설계 (DDD)

**Strategic 패턴:**
- **제한된 Contexts**: 별도 모델 위한 다른 domains
- **컨텍스트 매핑**: 어떻게 contexts relate
- **Ubiquitous Language**: Shared 용어

**Tactical 패턴:**
- **엔터티**: 객체 와 함께 아이덴티티
- **값 객체**: 불변 객체 정의된 에 의해 속성
- **집계합니다**: 일관성 boundaries
- **Repositories**: 데이터 access 추상화
- **도메인 이벤트**: Things 것 happened

## Clean 아키텍처 패턴

### 디렉터리 구조
```
app/
├── domain/           # Entities & business rules
│   ├── entities/
│   │   ├── user.py
│   │   └── order.py
│   ├── value_objects/
│   │   ├── email.py
│   │   └── money.py
│   └── interfaces/   # Abstract interfaces
│       ├── user_repository.py
│       └── payment_gateway.py
├── use_cases/        # Application business rules
│   ├── create_user.py
│   ├── process_order.py
│   └── send_notification.py
├── adapters/         # Interface implementations
│   ├── repositories/
│   │   ├── postgres_user_repository.py
│   │   └── redis_cache_repository.py
│   ├── controllers/
│   │   └── user_controller.py
│   └── gateways/
│       ├── stripe_payment_gateway.py
│       └── sendgrid_email_gateway.py
└── infrastructure/   # Framework & external concerns
    ├── database.py
    ├── config.py
    └── logging.py
```

### 구현 예제

```python
# domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """Core user entity - no framework dependencies."""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        """Business rule: deactivating user."""
        self.is_active = False

    def can_place_order(self) -> bool:
        """Business rule: active users can order."""
        return self.is_active

# domain/interfaces/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.user import User

class IUserRepository(ABC):
    """Port: defines contract, no implementation."""

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

# use_cases/create_user.py
from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass
class CreateUserResponse:
    user: User
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """Use case: orchestrates business logic."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # Business validation
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(
                user=None,
                success=False,
                error="Email already exists"
            )

        # Create entity
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now(),
            is_active=True
        )

        # Persist
        saved_user = await self.user_repository.save(user)

        return CreateUserResponse(
            user=saved_user,
            success=True
        )

# adapters/repositories/postgres_user_repository.py
from domain.interfaces.user_repository import IUserRepository
from domain.entities.user import User
from typing import Optional
import asyncpg

class PostgresUserRepository(IUserRepository):
    """Adapter: PostgreSQL implementation."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return self._to_entity(row) if row else None

    async def find_by_email(self, email: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1", email
            )
            return self._to_entity(row) if row else None

    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (id, email, name, created_at, is_active)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (id) DO UPDATE
                SET email = $2, name = $3, is_active = $5
                """,
                user.id, user.email, user.name, user.created_at, user.is_active
            )
            return user

    async def delete(self, user_id: str) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM users WHERE id = $1", user_id
            )
            return result == "DELETE 1"

    def _to_entity(self, row) -> User:
        """Map database row to entity."""
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            created_at=row["created_at"],
            is_active=row["is_active"]
        )

# adapters/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from use_cases.create_user import CreateUserUseCase, CreateUserRequest
from pydantic import BaseModel

router = APIRouter()

class CreateUserDTO(BaseModel):
    email: str
    name: str

@router.post("/users")
async def create_user(
    dto: CreateUserDTO,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """Controller: handles HTTP concerns only."""
    request = CreateUserRequest(email=dto.email, name=dto.name)
    response = await use_case.execute(request)

    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)

    return {"user": response.user}
```

## Hexagonal 아키텍처 패턴

```python
# Core domain (hexagon center)
class OrderService:
    """Domain service - no infrastructure dependencies."""

    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        payment_gateway: PaymentGatewayPort,
        notification_service: NotificationPort
    ):
        self.orders = order_repository
        self.payments = payment_gateway
        self.notifications = notification_service

    async def place_order(self, order: Order) -> OrderResult:
        # Business logic
        if not order.is_valid():
            return OrderResult(success=False, error="Invalid order")

        # Use ports (interfaces)
        payment = await self.payments.charge(
            amount=order.total,
            customer=order.customer_id
        )

        if not payment.success:
            return OrderResult(success=False, error="Payment failed")

        order.mark_as_paid()
        saved_order = await self.orders.save(order)

        await self.notifications.send(
            to=order.customer_email,
            subject="Order confirmed",
            body=f"Order {order.id} confirmed"
        )

        return OrderResult(success=True, order=saved_order)

# Ports (interfaces)
class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save(self, order: Order) -> Order:
        pass

class PaymentGatewayPort(ABC):
    @abstractmethod
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        pass

class NotificationPort(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str):
        pass

# Adapters (implementations)
class StripePaymentAdapter(PaymentGatewayPort):
    """Primary adapter: connects to Stripe API."""

    def __init__(self, api_key: str):
        self.stripe = stripe
        self.stripe.api_key = api_key

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        try:
            charge = self.stripe.Charge.create(
                amount=amount.cents,
                currency=amount.currency,
                customer=customer
            )
            return PaymentResult(success=True, transaction_id=charge.id)
        except stripe.error.CardError as e:
            return PaymentResult(success=False, error=str(e))

class MockPaymentAdapter(PaymentGatewayPort):
    """Test adapter: no external dependencies."""

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-123")
```

## 도메인 주도 설계 패턴

```python
# Value Objects (immutable)
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Email:
    """Value object: validated email."""
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email")

@dataclass(frozen=True)
class Money:
    """Value object: amount with currency."""
    amount: int  # cents
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

# Entities (with identity)
class Order:
    """Entity: has identity, mutable state."""

    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.customer = customer
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []

    def add_item(self, product: Product, quantity: int):
        """Business logic in entity."""
        item = OrderItem(product, quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(self.id, item))

    def total(self) -> Money:
        """Calculated property."""
        return sum(item.subtotal() for item in self.items)

    def submit(self):
        """State transition with business rules."""
        if not self.items:
            raise ValueError("Cannot submit empty order")
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order already submitted")

        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))

# Aggregates (consistency boundary)
class Customer:
    """Aggregate root: controls access to entities."""

    def __init__(self, id: str, email: Email):
        self.id = id
        self.email = email
        self._addresses: List[Address] = []
        self._orders: List[str] = []  # Order IDs, not full objects

    def add_address(self, address: Address):
        """Aggregate enforces invariants."""
        if len(self._addresses) >= 5:
            raise ValueError("Maximum 5 addresses allowed")
        self._addresses.append(address)

    @property
    def primary_address(self) -> Optional[Address]:
        return next((a for a in self._addresses if a.is_primary), None)

# Domain Events
@dataclass
class OrderSubmittedEvent:
    order_id: str
    occurred_at: datetime = field(default_factory=datetime.now)

# Repository (aggregate persistence)
class OrderRepository:
    """Repository: persist/retrieve aggregates."""

    async def find_by_id(self, order_id: str) -> Optional[Order]:
        """Reconstitute aggregate from storage."""
        pass

    async def save(self, order: Order):
        """Persist aggregate and publish events."""
        await self._persist(order)
        await self._publish_events(order._events)
        order._events.clear()
```

## 리소스

- **참조/clean-아키텍처-가이드.md**: 상세한 레이어 breakdown
- **참조/hexagonal-아키텍처-가이드.md**: Ports 및 adapters 패턴
- **참조/ddd-tactical-패턴.md**: 엔터티, 값 객체, 집계합니다
- **자산/clean-아키텍처-템플릿/**: 완전한 project 구조
- **자산/ddd-예제/**: 도메인 modeling 예제

## 최선의 관행

1. **종속성 규칙**: 종속성 항상 포인트 inward
2. **인터페이스 Segregation**: Small, focused 인터페이스
3. **비즈니스 Logic 에서 도메인**: Keep 프레임워크 out of 핵심
4. **Test Independence**: 핵심 testable 없이 인프라
5. **제한된 Contexts**: 명확한 도메인 boundaries
6. **Ubiquitous Language**: 일관된 용어
7. **Thin 컨트롤러**: Delegate 에 use cases
8. **Rich 도메인 모델**: Behavior 와 함께 데이터

## 일반적인 Pitfalls

- **Anemic 도메인**: 엔터티 와 함께 오직 데이터, 아니요 behavior
- **프레임워크 결합**: 비즈니스 logic depends 에 프레임워크
- **Fat 컨트롤러**: 비즈니스 logic 에서 컨트롤러
- **저장소 Leakage**: 노출하는 ORM 객체
- **Missing Abstractions**: Concrete 종속성 에서 핵심
- **Over-Engineering**: Clean 아키텍처 위한 간단한 CRUD
