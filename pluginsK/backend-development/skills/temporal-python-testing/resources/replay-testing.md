# Replay 테스트 위한 Determinism 및 Compatibility

포괄적인 가이드 위한 validating 워크플로우 determinism 및 보장하는 safe 코드 변경합니다 사용하여 replay 테스트.

## 무엇 is Replay 테스트?

**Purpose**: Verify 것 워크플로우 코드 변경합니다 are 하위 호환 와 함께 기존 워크플로우 executions

**어떻게 it 작동합니다**:
1. Temporal 레코드 모든 워크플로우 결정 처럼 이벤트 History
2. Replay 테스트 re-실행합니다 워크플로우 코드 against 기록된 history
3. 만약 새로운 코드 makes same decisions → deterministic (safe 에 deploy)
4. 만약 decisions differ → non-deterministic (breaking 변경)

**긴급 Use Cases**:
- Deploying 워크플로우 코드 변경합니다 에 production
- Validating 리팩토링 doesn't break 실행 중 워크플로우
- CI/CD 자동화된 compatibility 확인합니다
- 버전 마이그레이션 검증

## 기본 Replay 테스트

### Replayer 설정

```python
from temporalio.worker import Replayer
from temporalio.client import Client

async def test_workflow_replay():
    """Test workflow against production history"""

    # Connect to Temporal server
    client = await Client.connect("localhost:7233")

    # Create replayer with current workflow code
    replayer = Replayer(
        workflows=[OrderWorkflow, PaymentWorkflow]
    )

    # Fetch workflow history from production
    handle = client.get_workflow_handle("order-123")
    history = await handle.fetch_history()

    # Replay history with current code
    await replayer.replay_workflow(history)
    # Success = deterministic, Exception = breaking change
```

### 테스트 Against 여러 Histories

```python
import pytest
from temporalio.worker import Replayer

@pytest.mark.asyncio
async def test_replay_multiple_workflows():
    """Replay against multiple production histories"""

    replayer = Replayer(workflows=[OrderWorkflow])

    # Test against different workflow executions
    workflow_ids = [
        "order-success-123",
        "order-cancelled-456",
        "order-retry-789",
    ]

    for workflow_id in workflow_ids:
        handle = client.get_workflow_handle(workflow_id)
        history = await handle.fetch_history()

        # Replay should succeed for all variants
        await replayer.replay_workflow(history)
```

## Determinism 검증

### 일반적인 Non-Deterministic 패턴

**문제: Random 숫자 세대**
```python
# ❌ Non-deterministic (breaks replay)
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> int:
        return random.randint(1, 100)  # Different on replay!

# ✅ Deterministic (safe for replay)
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> int:
        return workflow.random().randint(1, 100)  # Deterministic random
```

**문제: 현재 시간**
```python
# ❌ Non-deterministic
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> str:
        now = datetime.now()  # Different on replay!
        return now.isoformat()

# ✅ Deterministic
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> str:
        now = workflow.now()  # Deterministic time
        return now.isoformat()
```

**문제: 직접 외부 Calls**
```python
# ❌ Non-deterministic
@workflow.defn
class BadWorkflow:
    @workflow.run
    async def run(self) -> dict:
        response = requests.get("https://api.example.com/data")  # External call!
        return response.json()

# ✅ Deterministic
@workflow.defn
class GoodWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # Use activity for external calls
        return await workflow.execute_activity(
            fetch_external_data,
            start_to_close_timeout=timedelta(seconds=30),
        )
```

### 테스트 Determinism

```python
@pytest.mark.asyncio
async def test_workflow_determinism():
    """Verify workflow produces same output on multiple runs"""

    @workflow.defn
    class DeterministicWorkflow:
        @workflow.run
        async def run(self, seed: int) -> list[int]:
            # Use workflow.random() for determinism
            rng = workflow.random()
            rng.seed(seed)
            return [rng.randint(1, 100) for _ in range(10)]

    env = await WorkflowEnvironment.start_time_skipping()

    # Run workflow twice with same input
    results = []
    for i in range(2):
        async with Worker(
            env.client,
            task_queue="test",
            workflows=[DeterministicWorkflow],
        ):
            result = await env.client.execute_workflow(
                DeterministicWorkflow.run,
                42,  # Same seed
                id=f"determinism-test-{i}",
                task_queue="test",
            )
            results.append(result)

    await env.shutdown()

    # Verify identical outputs
    assert results[0] == results[1]
```

## Production History Replay

### Exporting 워크플로우 History

```python
from temporalio.client import Client

async def export_workflow_history(workflow_id: str, output_file: str):
    """Export workflow history for replay testing"""

    client = await Client.connect("production.temporal.io:7233")

    # Fetch workflow history
    handle = client.get_workflow_handle(workflow_id)
    history = await handle.fetch_history()

    # Save to file for replay testing
    with open(output_file, "wb") as f:
        f.write(history.SerializeToString())

    print(f"Exported history to {output_file}")
```

### Replaying 에서 파일

```python
from temporalio.worker import Replayer
from temporalio.api.history.v1 import History

async def test_replay_from_file():
    """Replay workflow from exported history file"""

    # Load history from file
    with open("workflow_histories/order-123.pb", "rb") as f:
        history = History.FromString(f.read())

    # Replay with current workflow code
    replayer = Replayer(workflows=[OrderWorkflow])
    await replayer.replay_workflow(history)
    # Success = safe to deploy
```

## CI/CD 통합 패턴

### GitHub Actions 예제

```yaml
# .github/workflows/replay-tests.yml
name: Replay Tests

on:
  pull_request:
    branches: [main]

jobs:
  replay-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Download production histories
        run: |
          # Fetch recent workflow histories from production
          python scripts/export_histories.py

      - name: Run replay tests
        run: |
          pytest tests/replay/ --verbose

      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: replay-failures
          path: replay-failures/
```

### 자동화된 History Export

```python
# scripts/export_histories.py
import asyncio
from temporalio.client import Client
from datetime import datetime, timedelta

async def export_recent_histories():
    """Export recent production workflow histories"""

    client = await Client.connect("production.temporal.io:7233")

    # Query recent completed workflows
    workflows = client.list_workflows(
        query="WorkflowType='OrderWorkflow' AND CloseTime > '7 days ago'"
    )

    count = 0
    async for workflow in workflows:
        # Export history
        history = await workflow.fetch_history()

        # Save to file
        filename = f"workflow_histories/{workflow.id}.pb"
        with open(filename, "wb") as f:
            f.write(history.SerializeToString())

        count += 1
        if count >= 100:  # Limit to 100 most recent
            break

    print(f"Exported {count} workflow histories")

if __name__ == "__main__":
    asyncio.run(export_recent_histories())
```

### Replay Test Suite

```python
# tests/replay/test_workflow_replay.py
import pytest
import glob
from temporalio.worker import Replayer
from temporalio.api.history.v1 import History
from workflows import OrderWorkflow, PaymentWorkflow

@pytest.mark.asyncio
async def test_replay_all_histories():
    """Replay all production histories"""

    replayer = Replayer(
        workflows=[OrderWorkflow, PaymentWorkflow]
    )

    # Load all history files
    history_files = glob.glob("workflow_histories/*.pb")

    failures = []
    for history_file in history_files:
        try:
            with open(history_file, "rb") as f:
                history = History.FromString(f.read())

            await replayer.replay_workflow(history)
            print(f"✓ {history_file}")

        except Exception as e:
            failures.append((history_file, str(e)))
            print(f"✗ {history_file}: {e}")

    # Report failures
    if failures:
        pytest.fail(
            f"Replay failed for {len(failures)} workflows:\n"
            + "\n".join(f"  {file}: {error}" for file, error in failures)
        )
```

## 버전 Compatibility 테스트

### 테스트 코드 Evolution

```python
@pytest.mark.asyncio
async def test_workflow_version_compatibility():
    """Test workflow with version changes"""

    @workflow.defn
    class EvolvingWorkflow:
        @workflow.run
        async def run(self) -> str:
            # Use versioning for safe code evolution
            version = workflow.get_version("feature-flag", 1, 2)

            if version == 1:
                # Old behavior
                return "version-1"
            else:
                # New behavior
                return "version-2"

    env = await WorkflowEnvironment.start_time_skipping()

    # Test version 1 behavior
    async with Worker(
        env.client,
        task_queue="test",
        workflows=[EvolvingWorkflow],
    ):
        result_v1 = await env.client.execute_workflow(
            EvolvingWorkflow.run,
            id="evolving-v1",
            task_queue="test",
        )
        assert result_v1 == "version-1"

        # Simulate workflow executing again with version 2
        result_v2 = await env.client.execute_workflow(
            EvolvingWorkflow.run,
            id="evolving-v2",
            task_queue="test",
        )
        # New workflows use version 2
        assert result_v2 == "version-2"

    await env.shutdown()
```

### 마이그레이션 전략

```python
# Phase 1: Add version check
@workflow.defn
class MigratingWorkflow:
    @workflow.run
    async def run(self) -> dict:
        version = workflow.get_version("new-logic", 1, 2)

        if version == 1:
            # Old logic (existing workflows)
            return await self._old_implementation()
        else:
            # New logic (new workflows)
            return await self._new_implementation()

# Phase 2: After all old workflows complete, remove old code
@workflow.defn
class MigratedWorkflow:
    @workflow.run
    async def run(self) -> dict:
        # Only new logic remains
        return await self._new_implementation()
```

## 최선의 관행

1. **Replay 이전 Deploy**: 항상 run replay 테스트합니다 이전 deploying 워크플로우 변경합니다
2. **Export 정기적으로**: 지속적으로 export production histories 위한 테스트
3. **CI/CD 통합**: 자동화된 replay 테스트 에서 pull 요청 확인합니다
4. **버전 추적**: Use 워크플로우.get_version() 위한 safe 코드 evolution
5. **History Retention**: Keep representative 워크플로우 histories 위한 regression 테스트
6. **Determinism**: 절대 ~하지 않음 use random(), 날짜시간.now(), 또는 직접 외부 calls
7. **포괄적인 테스트**: Test against various 워크플로우 실행 경로

## 일반적인 Replay 오류

**Non-Deterministic 오류**:
```
WorkflowNonDeterministicError: Workflow command mismatch at position 5
Expected: ScheduleActivityTask(activity_id='activity-1')
Got: ScheduleActivityTask(activity_id='activity-2')
```

**Solution**: 코드 변경 변경된 워크플로우 결정 시퀀스

**버전 Mismatch 오류**:
```
WorkflowVersionError: Workflow version changed from 1 to 2 without using get_version()
```

**Solution**: Use 워크플로우.get_version() 위한 하위 호환 변경합니다

## Additional 리소스

- Replay 테스트: docs.temporal.io/develop/python/테스트-suite#replay-테스트
- 워크플로우 Versioning: docs.temporal.io/워크플로우#versioning
- Determinism 가이드: docs.temporal.io/워크플로우#deterministic-constraints
- CI/CD 통합: github.com/temporalio/샘플-python/트리/main/.github/워크플로우
