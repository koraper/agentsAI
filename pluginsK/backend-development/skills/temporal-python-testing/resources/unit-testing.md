# 단위 테스트 Temporal 워크플로우 및 Activities

Focused 가이드 위한 테스트 개별 워크플로우 및 activities 에서 격리 사용하여 WorkflowEnvironment 및 ActivityEnvironment.

## WorkflowEnvironment 와 함께 시간-Skipping

**Purpose**: Test 워크플로우 에서 격리 와 함께 순간 시간 진행 (month-long 워크플로우 → seconds)

### 기본 설정 패턴

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.fixture
async def workflow_env():
    """Reusable time-skipping test environment"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.mark.asyncio
async def test_workflow_execution(workflow_env):
    """Test workflow with time-skipping"""
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            YourWorkflow.run,
            "test-input",
            id="test-wf-id",
            task_queue="test-queue",
        )
        assert result == "expected-output"
```

**키 Benefits**:
- `workflow.sleep(timedelta(days=30))` 완료합니다 즉시
- Fast feedback 루프 (milliseconds vs hours)
- Deterministic test 실행

### 시간-Skipping 예제

**Sleep Advancement**:
```python
@pytest.mark.asyncio
async def test_workflow_with_delays(workflow_env):
    """Workflow sleeps are instant in time-skipping mode"""

    @workflow.defn
    class DelayedWorkflow:
        @workflow.run
        async def run(self) -> str:
            await workflow.sleep(timedelta(hours=24))  # Instant in tests
            return "completed"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DelayedWorkflow],
    ):
        result = await workflow_env.client.execute_workflow(
            DelayedWorkflow.run,
            id="delayed-wf",
            task_queue="test",
        )
        assert result == "completed"
```

**Manual 시간 Control**:
```python
@pytest.mark.asyncio
async def test_workflow_manual_time(workflow_env):
    """Manually advance time for precise control"""

    handle = await workflow_env.client.start_workflow(
        TimeBasedWorkflow.run,
        id="time-wf",
        task_queue="test",
    )

    # Advance time by specific amount
    await workflow_env.sleep(timedelta(hours=1))

    # Verify intermediate state via query
    state = await handle.query(TimeBasedWorkflow.get_state)
    assert state == "processing"

    # Advance to completion
    await workflow_env.sleep(timedelta(hours=23))
    result = await handle.result()
    assert result == "completed"
```

### 테스트 워크플로우 Logic

**결정 테스트**:
```python
@pytest.mark.asyncio
async def test_workflow_branching(workflow_env):
    """Test different execution paths"""

    @workflow.defn
    class ConditionalWorkflow:
        @workflow.run
        async def run(self, condition: bool) -> str:
            if condition:
                return "path-a"
            return "path-b"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ConditionalWorkflow],
    ):
        # Test true path
        result_a = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            True,
            id="cond-wf-true",
            task_queue="test",
        )
        assert result_a == "path-a"

        # Test false path
        result_b = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            False,
            id="cond-wf-false",
            task_queue="test",
        )
        assert result_b == "path-b"
```

## ActivityEnvironment 테스트

**Purpose**: Test activities 에서 격리 없이 워크플로우 또는 Temporal 서버

### 기본 Activity Test

```python
from temporalio.testing import ActivityEnvironment

async def test_activity_basic():
    """Test activity without workflow context"""

    @activity.defn
    async def process_data(input: str) -> str:
        return input.upper()

    env = ActivityEnvironment()
    result = await env.run(process_data, "test")
    assert result == "TEST"
```

### 테스트 Activity 컨텍스트

**Heartbeat 테스트**:
```python
async def test_activity_heartbeat():
    """Verify heartbeat calls"""

    @activity.defn
    async def long_running_activity(total_items: int) -> int:
        for i in range(total_items):
            activity.heartbeat(i)  # Report progress
            await asyncio.sleep(0.1)
        return total_items

    env = ActivityEnvironment()
    result = await env.run(long_running_activity, 10)
    assert result == 10
```

**Cancellation 테스트**:
```python
async def test_activity_cancellation():
    """Test activity cancellation handling"""

    @activity.defn
    async def cancellable_activity() -> str:
        try:
            while True:
                if activity.is_cancelled():
                    return "cancelled"
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            return "cancelled"

    env = ActivityEnvironment(cancellation_reason="test-cancel")
    result = await env.run(cancellable_activity)
    assert result == "cancelled"
```

### 테스트 오류 처리

**예외 전파**:
```python
async def test_activity_error():
    """Test activity error handling"""

    @activity.defn
    async def failing_activity(should_fail: bool) -> str:
        if should_fail:
            raise ApplicationError("Validation failed", non_retryable=True)
        return "success"

    env = ActivityEnvironment()

    # Test success path
    result = await env.run(failing_activity, False)
    assert result == "success"

    # Test error path
    with pytest.raises(ApplicationError) as exc_info:
        await env.run(failing_activity, True)
    assert "Validation failed" in str(exc_info.value)
```

## Pytest 통합 패턴

### Shared Fixtures

```python
# conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.fixture(scope="module")
async def workflow_env():
    """Module-scoped environment (reused across tests)"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def activity_env():
    """Function-scoped environment (fresh per test)"""
    return ActivityEnvironment()
```

### Parameterized 테스트합니다

```python
@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
    ("123", "123"),
])
async def test_activity_parameterized(activity_env, input, expected):
    """Test multiple input scenarios"""
    result = await activity_env.run(process_data, input)
    assert result == expected
```

## 최선의 관행

1. **Fast 실행**: Use 시간-skipping 위한 모든 워크플로우 테스트합니다
2. **격리**: Test 워크플로우 및 activities separately
3. **Shared Fixtures**: Reuse WorkflowEnvironment 전반에 걸쳐 관련됨 테스트합니다
4. **Coverage Target**: ≥80% 위한 워크플로우 logic
5. **Mock Activities**: Use ActivityEnvironment 위한 activity-특정 logic
6. **Determinism**: Ensure test results are 일관된 전반에 걸쳐 실행합니다
7. **오류 Cases**: Test 둘 다 success 및 실패 scenarios

## 일반적인 패턴

**테스트 재시도 Logic**:
```python
@pytest.mark.asyncio
async def test_workflow_with_retries(workflow_env):
    """Test activity retry behavior"""

    call_count = 0

    @activity.defn
    async def flaky_activity() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Transient error")
        return "success"

    @workflow.defn
    class RetryWorkflow:
        @workflow.run
        async def run(self) -> str:
            return await workflow.execute_activity(
                flaky_activity,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=1),
                    maximum_attempts=5,
                ),
            )

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[flaky_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            id="retry-wf",
            task_queue="test",
        )
        assert result == "success"
        assert call_count == 3  # Verify retry attempts
```

## Additional 리소스

- Python SDK 테스트: docs.temporal.io/develop/python/테스트-suite
- pytest 문서화: docs.pytest.org
- Temporal 샘플: github.com/temporalio/샘플-python
