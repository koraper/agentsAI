---
name: temporal-python-testing
description: Test Temporal 워크플로우 와 함께 pytest, 시간-skipping, 및 mocking strategies. Covers 단위 테스트, 통합 테스트, replay 테스트, 및 로컬 개발 설정. Use 때 implementing Temporal 워크플로우 테스트합니다 또는 디버깅 test 실패.
---

# Temporal Python 테스트 Strategies

포괄적인 테스트 approaches 위한 Temporal 워크플로우 사용하여 pytest, progressive disclosure 리소스 위한 특정 테스트 scenarios.

## 때 에 Use This Skill

- **단위 테스트 워크플로우** - Fast 테스트합니다 와 함께 시간-skipping
- **통합 테스트** - 워크플로우 와 함께 mocked activities
- **Replay 테스트** - Validate determinism against production histories
- **로컬 개발** - 세트 up Temporal 서버 및 pytest
- **CI/CD 통합** - 자동화된 테스트 파이프라인
- **Coverage strategies** - Achieve ≥80% test coverage

## 테스트 Philosophy

**권장됨 접근법** (소스: docs.temporal.io/develop/python/테스트-suite):
- Write majority 처럼 통합 테스트합니다
- Use pytest 와 함께 비동기 fixtures
- 시간-skipping 가능하게 합니다 fast feedback (month-long 워크플로우 → seconds)
- Mock activities 에 isolate 워크플로우 logic
- Validate determinism 와 함께 replay 테스트

**Three Test 유형**:
1. **단위**: 워크플로우 와 함께 시간-skipping, activities 와 함께 ActivityEnvironment
2. **통합**: Workers 와 함께 mocked activities
3. **End-에-end**: 전체 Temporal 서버 와 함께 real activities (use sparingly)

## 사용 가능한 리소스

This skill 제공합니다 상세한 guidance 통해 progressive disclosure. Load 특정 리소스 based 에 your 테스트 needs:

### 단위 테스트 리소스
**파일**: `resources/unit-testing.md`
**때 에 load**: 테스트 개별 워크플로우 또는 activities 에서 격리
**Contains**:
- WorkflowEnvironment 와 함께 시간-skipping
- ActivityEnvironment 위한 activity 테스트
- Fast 실행 of long-실행 중 워크플로우
- Manual 시간 advancement 패턴
- pytest fixtures 및 패턴

### 통합 테스트 리소스
**파일**: `resources/integration-testing.md`
**때 에 load**: 테스트 워크플로우 와 함께 mocked 외부 종속성
**Contains**:
- Activity mocking strategies
- 오류 인젝션 패턴
- Multi-activity 워크플로우 테스트
- 신호 및 쿼리 테스트
- Coverage strategies

### Replay 테스트 리소스
**파일**: `resources/replay-testing.md`
**때 에 load**: Validating determinism 또는 deploying 워크플로우 변경합니다
**Contains**:
- Determinism 검증
- Production history replay
- CI/CD 통합 패턴
- 버전 compatibility 테스트

### 로컬 개발 리소스
**파일**: `resources/local-setup.md`
**때 에 load**: 설정하는 개발 환경
**Contains**:
- Docker Compose 구성
- pytest 설정 및 구성
- Coverage tool 통합
- 개발 워크플로우

## Quick Start 가이드

### 기본 워크플로우 Test

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.fixture
async def workflow_env():
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.mark.asyncio
async def test_workflow(workflow_env):
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            YourWorkflow.run,
            args,
            id="test-wf-id",
            task_queue="test-queue",
        )
        assert result == expected
```

### 기본 Activity Test

```python
from temporalio.testing import ActivityEnvironment

async def test_activity():
    env = ActivityEnvironment()
    result = await env.run(your_activity, "test-input")
    assert result == expected_output
```

## Coverage Targets

**권장됨 Coverage** (소스: docs.temporal.io 최선의 관행):
- **워크플로우**: ≥80% logic coverage
- **Activities**: ≥80% logic coverage
- **통합**: 긴급 경로 와 함께 mocked activities
- **Replay**: 모든 워크플로우 버전 이전 배포

## 키 테스트 원칙

1. **시간-Skipping** - Month-long 워크플로우 test 에서 seconds
2. **Mock Activities** - Isolate 워크플로우 logic 에서 외부 종속성
3. **Replay 테스트** - Validate determinism 이전 배포
4. **High Coverage** - ≥80% target 위한 production 워크플로우
5. **Fast Feedback** - 단위 테스트합니다 run 에서 milliseconds

## 어떻게 에 Use 리소스

**Load 특정 리소스 때 필요한**:
- "Show me 단위 테스트 패턴" → Load `resources/unit-testing.md`
- "어떻게 do I mock activities?" → Load `resources/integration-testing.md`
- "설정 로컬 Temporal 서버" → Load `resources/local-setup.md`
- "Validate determinism" → Load `resources/replay-testing.md`

## Additional 참조

- Python SDK 테스트: docs.temporal.io/develop/python/테스트-suite
- 테스트 패턴: github.com/temporalio/temporal/blob/main/docs/개발/테스트.md
- Python 샘플: github.com/temporalio/샘플-python
