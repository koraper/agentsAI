---
name: workflow-orchestration-patterns
description: 설계 내구성 워크플로우 와 함께 Temporal 위한 분산 시스템. Covers 워크플로우 vs activity 분리, saga 패턴, 상태 관리, 및 determinism constraints. Use 때 구축 long-실행 중 프로세스, 분산 transactions, 또는 microservice 오케스트레이션.
---

# 워크플로우 오케스트레이션 패턴

마스터 워크플로우 오케스트레이션 아키텍처 와 함께 Temporal, covering 기본 설계 decisions, 복원력 패턴, 및 최선의 관행 위한 구축 reliable 분산 시스템.

## 때 에 Use 워크플로우 오케스트레이션

### 이상적인 Use Cases (소스: docs.temporal.io)

- **Multi-단계 프로세스** spanning machines/서비스/databases
- **분산 transactions** requiring 모든-또는-nothing 의미론
- **Long-실행 중 워크플로우** (hours 에 years) 와 함께 automatic 상태 지속성
- **실패 복구** 것 must resume 에서 마지막 성공한 단계
- **비즈니스 프로세스**: bookings, 정렬합니다, campaigns, approvals
- **엔터티 lifecycle 관리**: 인벤토리 추적, 계정 관리, cart 워크플로우
- **인프라 자동화**: CI/CD 파이프라인, provisioning, deployments
- **Human-에서-the-루프** 시스템 requiring timeouts 및 escalations

### 때 NOT 에 Use

- 간단한 CRUD 작업 (use 직접 API calls)
- Pure 데이터 처리 파이프라인 (use Airflow, batch 처리)
- Stateless 요청/응답 (use 표준 APIs)
- Real-시간 스트리밍 (use Kafka, 이벤트 processors)

## 긴급 설계 결정: 워크플로우 vs Activities

**The 기본 규칙** (소스: temporal.io/blog/워크플로우-engine-원칙):
- **워크플로우** = 오케스트레이션 logic 및 결정-making
- **Activities** = 외부 interactions (APIs, databases, 네트워크 calls)

### 워크플로우 (오케스트레이션)

**Characteristics:**
- Contain 비즈니스 logic 및 조정
- **MUST be deterministic** (same 입력 → same 출력)
- **Cannot** perform 직접 외부 calls
- 상태 automatically 보존됨 전반에 걸쳐 실패
- Can run 위한 years despite 인프라 실패

**예제 워크플로우 tasks:**
- Decide 어느 steps 에 execute
- Handle compensation logic
- Manage timeouts 및 재시도합니다
- 좌표 child 워크플로우

### Activities (외부 Interactions)

**Characteristics:**
- Handle 모든 외부 시스템 interactions
- Can be non-deterministic (API calls, DB 씁니다)
- Include 구축된-에서 timeouts 및 재시도 logic
- **Must be idempotent** (calling N times = calling once)
- Short-lived (seconds 에 minutes 일반적으로)

**예제 activity tasks:**
- 호출 payment 게이트웨이 API
- Write 에 데이터베이스
- Send emails 또는 알림
- 쿼리 외부 서비스

### 설계 결정 프레임워크

```
Does it touch external systems? → Activity
Is it orchestration/decision logic? → Workflow
```

## 핵심 워크플로우 패턴

### 1. Saga 패턴 와 함께 Compensation

**Purpose**: Implement 분산 transactions 와 함께 롤백 역량

**패턴** (소스: temporal.io/blog/compensating-actions-part-of-a-완전한-breakfast-와 함께-sagas):

```
For each step:
  1. Register compensation BEFORE executing
  2. Execute the step (via activity)
  3. On failure, run all compensations in reverse order (LIFO)
```

**예제: Payment 워크플로우**
1. Reserve 인벤토리 (compensation: 릴리스 인벤토리)
2. Charge payment (compensation: refund payment)
3. Fulfill 순서 (compensation: cancel fulfillment)

**긴급 요구사항:**
- Compensations must be idempotent
- Register compensation 이전 executing 단계
- Run compensations 에서 역방향 순서
- Handle 부분 실패 gracefully

### 2. 엔터티 워크플로우 (액터 모델)

**Purpose**: Long-lived 워크플로우 representing single 엔터티 인스턴스

**패턴** (소스: docs.temporal.io/evaluate/use-cases-설계-패턴):
- One 워크플로우 실행 = one 엔터티 (cart, 계정, 인벤토리 item)
- 워크플로우 유지합니다 위한 엔터티 lifetime
- 수신합니다 신호 위한 상태 변경합니다
- 지원합니다 쿼리 위한 현재 상태

**예제 Use Cases:**
- Shopping cart (add items, checkout, expiration)
- Bank 계정 (deposits, withdrawals, balance 확인합니다)
- Product 인벤토리 (stock 업데이트합니다, reservations)

**Benefits:**
- 캡슐화합니다 엔터티 behavior
- 보증합니다 일관성 per 엔터티
- Natural 이벤트 sourcing

### 3. Fan-Out/Fan-에서 (병렬로 실행)

**Purpose**: Execute 여러 tasks 에서 병렬로, 집계 results

**패턴:**
- Spawn child 워크플로우 또는 병렬로 activities
- Wait 위한 모든 에 완전한
- 집계 results
- Handle 부분 실패

**확장 규칙** (소스: temporal.io/blog/워크플로우-engine-원칙):
- Don't scale 개별 워크플로우
- 위한 1M tasks: spawn 1K child 워크플로우 × 1K tasks 각
- Keep 각 워크플로우 제한된

### 4. 비동기 콜백 패턴

**Purpose**: Wait 위한 외부 이벤트 또는 human approval

**패턴:**
- 워크플로우 전송합니다 요청 및 waits 위한 신호
- 외부 시스템 프로세스 비동기적으로
- 전송합니다 신호 에 resume 워크플로우
- 워크플로우 계속합니다 와 함께 응답

**Use Cases:**
- Human approval 워크플로우
- Webhook callbacks
- Long-실행 중 외부 프로세스

## 상태 관리 및 Determinism

### Automatic 상태 Preservation

**어떻게 Temporal 작동합니다** (소스: docs.temporal.io/워크플로우):
- 완전한 프로그램 상태 보존됨 automatically
- 이벤트 History 레코드 모든 명령 및 이벤트
- Seamless 복구 에서 crashes
- 애플리케이션 restore pre-실패 상태

### Determinism Constraints

**워크플로우 Execute 처럼 상태 Machines**:
- Replay behavior must be 일관된
- Same 입력 → identical 출력 모든 시간

**Prohibited 에서 워크플로우** (소스: docs.temporal.io/워크플로우):
- ❌ Threading, locks, 동기화 primitives
- ❌ Random 숫자 세대 (`random()`)
- ❌ 전역 상태 또는 정적 변수
- ❌ 시스템 시간 (`datetime.now()`)
- ❌ 직접 파일 I/O 또는 네트워크 calls
- ❌ Non-deterministic 라이브러리

**허용된 에서 워크플로우**:
- ✅ `workflow.now()` (deterministic 시간)
- ✅ `workflow.random()` (deterministic random)
- ✅ Pure 함수 및 calculations
- ✅ Calling activities (non-deterministic 작업)

### Versioning Strategies

**Challenge**: Changing 워크플로우 코드 동안 오래된 executions 여전히 실행 중

**Solutions**:
1. **Versioning API**: Use `workflow.get_version()` 위한 safe 변경합니다
2. **새로운 워크플로우 유형**: Create 새로운 워크플로우, 라우트 새로운 executions 에 it
3. **뒤로 Compatibility**: Ensure 오래된 이벤트 replay 올바르게

## 복원력 및 오류 처리

### 재시도 정책

**default Behavior**: Temporal 재시도합니다 activities 영원히

**Configure 재시도**:
- 초기 재시도 간격
- Backoff coefficient (exponential backoff)
- Maximum 간격 (cap 재시도 delay)
- Maximum attempts (eventually fail)

**Non-Retryable 오류**:
- 유효하지 않은 입력 (검증 실패)
- 비즈니스 규칙 위반
- 영구 실패 (리소스 not 찾은)

### Idempotency 요구사항

**왜 긴급** (소스: docs.temporal.io/activities):
- Activities may execute 여러 times
- 네트워크 실패 trigger 재시도합니다
- 중복 실행 must be safe

**구현 Strategies**:
- Idempotency 키 (deduplication)
- Check-then-act 와 함께 고유한 constraints
- Upsert 작업 instead of insert
- Track 처리된 요청 IDs

### Activity Heartbeats

**Purpose**: Detect stalled long-실행 중 activities

**패턴**:
- Activity 전송합니다 periodic heartbeat
- 포함합니다 진행 정보
- 타임아웃 만약 아니요 heartbeat 수신된
- 가능하게 합니다 진행-based 재시도

## 최선의 관행

### 워크플로우 설계

1. **Keep 워크플로우 focused** - Single responsibility per 워크플로우
2. **Small 워크플로우** - Use child 워크플로우 위한 scalability
3. **명확한 boundaries** - 워크플로우 오케스트레이션합니다, activities execute
4. **Test locally** - Use 시간-skipping test 환경

### Activity 설계

1. **Idempotent 작업** - Safe 에 재시도
2. **Short-lived** - Seconds 에 minutes, not hours
3. **타임아웃 구성** - 항상 세트 timeouts
4. **Heartbeat 위한 long tasks** - 보고서 진행
5. **오류 처리** - Distinguish retryable vs non-retryable

### 일반적인 Pitfalls

**워크플로우 위반**:
- 사용하여 `datetime.now()` instead of `workflow.now()`
- Threading 또는 비동기 작업 에서 워크플로우 코드
- Calling 외부 APIs 직접 에서 워크플로우
- Non-deterministic logic 에서 워크플로우

**Activity Mistakes**:
- Non-idempotent 작업 (can't handle 재시도합니다)
- Missing timeouts (activities run 영원히)
- 아니요 오류 분류 (재시도 검증 오류)
- Ignoring 페이로드 제한합니다 (2MB per 인수)

### Operational Considerations

**모니터링**:
- 워크플로우 실행 기간
- Activity 실패 평가합니다
- 재시도 attempts 및 backoff
- 대기 중 워크플로우 계산합니다

**Scalability**:
- Horizontal 확장 와 함께 workers
- 작업 큐 분할
- Child 워크플로우 분해
- Activity 배치 때 적절한

## Additional 리소스

**Official 문서화**:
- Temporal 핵심 개념: docs.temporal.io/워크플로우
- 워크플로우 패턴: docs.temporal.io/evaluate/use-cases-설계-패턴
- 최선의 관행: docs.temporal.io/develop/최선의-관행
- Saga 패턴: temporal.io/blog/saga-패턴-made-쉬운

**키 원칙**:
1. 워크플로우 = 오케스트레이션, Activities = 외부 calls
2. Determinism is non-negotiable 위한 워크플로우
3. Idempotency is 긴급 위한 activities
4. 상태 preservation is automatic
5. 설계 위한 실패 및 복구
