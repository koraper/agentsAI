# 통합 테스트 와 함께 Mocked Activities

포괄적인 패턴 위한 테스트 워크플로우 와 함께 mocked 외부 종속성, 오류 인젝션, 및 복잡한 scenarios.

## Activity Mocking 전략

**Purpose**: Test 워크플로우 오케스트레이션 logic 없이 calling real 외부 서비스

### 기본 Mock 패턴

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from unittest.mock import Mock

@pytest.mark.asyncio
async def test_workflow_with_mocked_activity(workflow_env):
    """Mock activity to test workflow logic"""

    # Create mock activity
    mock_activity = Mock(return_value="mocked-result")

    @workflow.defn
    class WorkflowWithActivity:
        @workflow.run
        async def run(self, input: str) -> str:
            result = await workflow.execute_activity(
                process_external_data,
                input,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return f"processed: {result}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[WorkflowWithActivity],
        activities=[mock_activity],  # Use mock instead of real activity
    ):
        result = await workflow_env.client.execute_workflow(
            WorkflowWithActivity.run,
            "test-input",
            id="wf-mock",
            task_queue="test",
        )
        assert result == "processed: mocked-result"
        mock_activity.assert_called_once()
```

### 동적 Mock 응답

**시나리오-Based Mocking**:
```python
@pytest.mark.asyncio
async def test_workflow_multiple_mock_scenarios(workflow_env):
    """Test different workflow paths with dynamic mocks"""

    # Mock returns different values based on input
    def dynamic_activity(input: str) -> str:
        if input == "error-case":
            raise ApplicationError("Validation failed", non_retryable=True)
        return f"processed-{input}"

    @workflow.defn
    class DynamicWorkflow:
        @workflow.run
        async def run(self, input: str) -> str:
            try:
                result = await workflow.execute_activity(
                    dynamic_activity,
                    input,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                return f"success: {result}"
            except ApplicationError as e:
                return f"error: {e.message}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DynamicWorkflow],
        activities=[dynamic_activity],
    ):
        # Test success path
        result_success = await workflow_env.client.execute_workflow(
            DynamicWorkflow.run,
            "valid-input",
            id="wf-success",
            task_queue="test",
        )
        assert result_success == "success: processed-valid-input"

        # Test error path
        result_error = await workflow_env.client.execute_workflow(
            DynamicWorkflow.run,
            "error-case",
            id="wf-error",
            task_queue="test",
        )
        assert "Validation failed" in result_error
```

## 오류 인젝션 패턴

### 테스트 일시적 실패

**재시도 Behavior**:
```python
@pytest.mark.asyncio
async def test_workflow_transient_errors(workflow_env):
    """Test retry logic with controlled failures"""

    attempt_count = 0

    @activity.defn
    async def transient_activity() -> str:
        nonlocal attempt_count
        attempt_count += 1

        if attempt_count < 3:
            raise Exception(f"Transient error {attempt_count}")
        return "success-after-retries"

    @workflow.defn
    class RetryWorkflow:
        @workflow.run
        async def run(self) -> str:
            return await workflow.execute_activity(
                transient_activity,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=10),
                    maximum_attempts=5,
                    backoff_coefficient=1.0,
                ),
            )

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[transient_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            id="retry-wf",
            task_queue="test",
        )
        assert result == "success-after-retries"
        assert attempt_count == 3
```

### 테스트 Non-Retryable 오류

**비즈니스 검증 실패**:
```python
@pytest.mark.asyncio
async def test_workflow_non_retryable_error(workflow_env):
    """Test handling of permanent failures"""

    @activity.defn
    async def validation_activity(input: dict) -> str:
        if not input.get("valid"):
            raise ApplicationError(
                "Invalid input",
                non_retryable=True,  # Don't retry validation errors
            )
        return "validated"

    @workflow.defn
    class ValidationWorkflow:
        @workflow.run
        async def run(self, input: dict) -> str:
            try:
                return await workflow.execute_activity(
                    validation_activity,
                    input,
                    start_to_close_timeout=timedelta(seconds=10),
                )
            except ApplicationError as e:
                return f"validation-failed: {e.message}"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ValidationWorkflow],
        activities=[validation_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            ValidationWorkflow.run,
            {"valid": False},
            id="validation-wf",
            task_queue="test",
        )
        assert "validation-failed" in result
```

## Multi-Activity 워크플로우 테스트

### Sequential Activity 패턴

```python
@pytest.mark.asyncio
async def test_workflow_sequential_activities(workflow_env):
    """Test workflow orchestrating multiple activities"""

    activity_calls = []

    @activity.defn
    async def step_1(input: str) -> str:
        activity_calls.append("step_1")
        return f"{input}-step1"

    @activity.defn
    async def step_2(input: str) -> str:
        activity_calls.append("step_2")
        return f"{input}-step2"

    @activity.defn
    async def step_3(input: str) -> str:
        activity_calls.append("step_3")
        return f"{input}-step3"

    @workflow.defn
    class SequentialWorkflow:
        @workflow.run
        async def run(self, input: str) -> str:
            result_1 = await workflow.execute_activity(
                step_1,
                input,
                start_to_close_timeout=timedelta(seconds=10),
            )
            result_2 = await workflow.execute_activity(
                step_2,
                result_1,
                start_to_close_timeout=timedelta(seconds=10),
            )
            result_3 = await workflow.execute_activity(
                step_3,
                result_2,
                start_to_close_timeout=timedelta(seconds=10),
            )
            return result_3

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[SequentialWorkflow],
        activities=[step_1, step_2, step_3],
    ):
        result = await workflow_env.client.execute_workflow(
            SequentialWorkflow.run,
            "start",
            id="seq-wf",
            task_queue="test",
        )
        assert result == "start-step1-step2-step3"
        assert activity_calls == ["step_1", "step_2", "step_3"]
```

### 병렬로 Activity 패턴

```python
@pytest.mark.asyncio
async def test_workflow_parallel_activities(workflow_env):
    """Test concurrent activity execution"""

    @activity.defn
    async def parallel_task(task_id: int) -> str:
        return f"task-{task_id}"

    @workflow.defn
    class ParallelWorkflow:
        @workflow.run
        async def run(self, task_count: int) -> list[str]:
            # Execute activities in parallel
            tasks = [
                workflow.execute_activity(
                    parallel_task,
                    i,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                for i in range(task_count)
            ]
            return await asyncio.gather(*tasks)

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ParallelWorkflow],
        activities=[parallel_task],
    ):
        result = await workflow_env.client.execute_workflow(
            ParallelWorkflow.run,
            3,
            id="parallel-wf",
            task_queue="test",
        )
        assert result == ["task-0", "task-1", "task-2"]
```

## 신호 및 쿼리 테스트

### 신호 핸들러

```python
@pytest.mark.asyncio
async def test_workflow_signals(workflow_env):
    """Test workflow signal handling"""

    @workflow.defn
    class SignalWorkflow:
        def __init__(self) -> None:
            self._status = "initialized"

        @workflow.run
        async def run(self) -> str:
            # Wait for completion signal
            await workflow.wait_condition(lambda: self._status == "completed")
            return self._status

        @workflow.signal
        async def update_status(self, new_status: str) -> None:
            self._status = new_status

        @workflow.query
        def get_status(self) -> str:
            return self._status

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[SignalWorkflow],
    ):
        # Start workflow
        handle = await workflow_env.client.start_workflow(
            SignalWorkflow.run,
            id="signal-wf",
            task_queue="test",
        )

        # Verify initial state via query
        initial_status = await handle.query(SignalWorkflow.get_status)
        assert initial_status == "initialized"

        # Send signal
        await handle.signal(SignalWorkflow.update_status, "processing")

        # Verify updated state
        updated_status = await handle.query(SignalWorkflow.get_status)
        assert updated_status == "processing"

        # Complete workflow
        await handle.signal(SignalWorkflow.update_status, "completed")
        result = await handle.result()
        assert result == "completed"
```

## Coverage Strategies

### 워크플로우 Logic Coverage

**Target**: ≥80% coverage of 워크플로우 결정 logic

```python
# Test all branches
@pytest.mark.parametrize("condition,expected", [
    (True, "branch-a"),
    (False, "branch-b"),
])
async def test_workflow_branches(workflow_env, condition, expected):
    """Ensure all code paths are tested"""
    # Test implementation
    pass
```

### Activity Coverage

**Target**: ≥80% coverage of activity logic

```python
# Test activity edge cases
@pytest.mark.parametrize("input,expected", [
    ("valid", "success"),
    ("", "empty-input-error"),
    (None, "null-input-error"),
])
async def test_activity_edge_cases(activity_env, input, expected):
    """Test activity error handling"""
    # Test implementation
    pass
```

## 통합 Test 조직

### Test 구조

```
tests/
├── integration/
│   ├── conftest.py              # Shared fixtures
│   ├── test_order_workflow.py   # Order processing tests
│   ├── test_payment_workflow.py # Payment tests
│   └── test_fulfillment_workflow.py
├── unit/
│   ├── test_order_activities.py
│   └── test_payment_activities.py
└── fixtures/
    └── test_data.py             # Test data builders
```

### Shared Fixtures

```python
# conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.fixture(scope="session")
async def workflow_env():
    """Session-scoped environment for integration tests"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def mock_payment_service():
    """Mock external payment service"""
    return Mock()

@pytest.fixture
def mock_inventory_service():
    """Mock external inventory service"""
    return Mock()
```

## 최선의 관행

1. **Mock 외부 종속성**: 절대 ~하지 않음 호출 real APIs 에서 테스트합니다
2. **Test 오류 Scenarios**: Verify compensation 및 재시도 logic
3. **병렬로 테스트**: Use pytest-xdist 위한 faster test 실행합니다
4. **격리된 테스트합니다**: 각 test should be 독립적인
5. **명확한 Assertions**: Verify 둘 다 results 및 side effects
6. **Coverage Target**: ≥80% 위한 긴급 워크플로우
7. **Fast 실행**: Use 시간-skipping, avoid real delays

## Additional 리소스

- Mocking Strategies: docs.temporal.io/develop/python/테스트-suite
- pytest 최선의 관행: docs.pytest.org/en/안정적인/goodpractices.html
- Python SDK 샘플: github.com/temporalio/샘플-python
