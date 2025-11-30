# 로컬 개발 설정 위한 Temporal Python 테스트

포괄적인 가이드 위한 설정하는 로컬 Temporal 개발 환경 와 함께 pytest 통합 및 coverage 추적.

## Temporal 서버 설정 와 함께 Docker Compose

### 기본 Docker Compose 구성

```yaml
# docker-compose.yml
version: "3.8"

services:
  temporal:
    image: temporalio/auto-setup:latest
    container_name: temporal-dev
    ports:
      - "7233:7233" # Temporal server
      - "8233:8233" # Web UI
    environment:
      - DB=postgresql
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal
      - POSTGRES_SEEDS=postgresql
      - DYNAMIC_CONFIG_FILE_PATH=config/dynamicconfig/development-sql.yaml
    depends_on:
      - postgresql

  postgresql:
    image: postgres:14-alpine
    container_name: temporal-postgres
    environment:
      - POSTGRES_USER=temporal
      - POSTGRES_PASSWORD=temporal
      - POSTGRES_DB=temporal
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  temporal-ui:
    image: temporalio/ui:latest
    container_name: temporal-ui
    depends_on:
      - temporal
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
      - TEMPORAL_CORS_ORIGINS=http://localhost:3000
    ports:
      - "8080:8080"

volumes:
  postgres_data:
```

### 시작하는 로컬 서버

```bash
# Start Temporal server
docker-compose up -d

# Verify server is running
docker-compose ps

# View logs
docker-compose logs -f temporal

# Access Temporal Web UI
open http://localhost:8080

# Stop server
docker-compose down

# Reset data (clean slate)
docker-compose down -v
```

### Health Check 스크립트

```python
# scripts/health_check.py
import asyncio
from temporalio.client import Client

async def check_temporal_health():
    """Verify Temporal server is accessible"""
    try:
        client = await Client.connect("localhost:7233")
        print("✓ Connected to Temporal server")

        # Test workflow execution
        from temporalio.worker import Worker

        @workflow.defn
        class HealthCheckWorkflow:
            @workflow.run
            async def run(self) -> str:
                return "healthy"

        async with Worker(
            client,
            task_queue="health-check",
            workflows=[HealthCheckWorkflow],
        ):
            result = await client.execute_workflow(
                HealthCheckWorkflow.run,
                id="health-check",
                task_queue="health-check",
            )
            print(f"✓ Workflow execution successful: {result}")

        return True

    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_temporal_health())
```

## pytest 구성

### Project 구조

```
temporal-project/
├── docker-compose.yml
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── src/
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── order_workflow.py
│   │   └── payment_workflow.py
│   └── activities/
│       ├── __init__.py
│       ├── payment_activities.py
│       └── inventory_activities.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_workflows.py
│   │   └── test_activities.py
│   ├── integration/
│   │   └── test_order_flow.py
│   └── replay/
│       └── test_workflow_replay.py
└── scripts/
    ├── health_check.py
    └── export_histories.py
```

### pytest 구성

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers for test categorization
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (require Temporal server)
    replay: Replay tests (require production histories)
    slow: Slow running tests

# Coverage settings
addopts =
    --verbose
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80

# Async test timeout
asyncio_default_fixture_loop_scope = function
```

### Shared Test Fixtures

```python
# tests/conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.client import Client

@pytest.fixture(scope="session")
def event_loop():
    """Provide event loop for async fixtures"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def temporal_client():
    """Provide Temporal client connected to local server"""
    client = await Client.connect("localhost:7233")
    yield client
    await client.close()

@pytest.fixture(scope="module")
async def workflow_env():
    """Module-scoped time-skipping environment"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def activity_env():
    """Function-scoped activity environment"""
    from temporalio.testing import ActivityEnvironment
    return ActivityEnvironment()

@pytest.fixture
async def test_worker(temporal_client, workflow_env):
    """Pre-configured test worker"""
    from temporalio.worker import Worker
    from src.workflows import OrderWorkflow, PaymentWorkflow
    from src.activities import process_payment, update_inventory

    return Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[OrderWorkflow, PaymentWorkflow],
        activities=[process_payment, update_inventory],
    )
```

### 종속성

```txt
# requirements.txt
temporalio>=1.5.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-xdist>=3.3.0  # Parallel test execution
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_backend"

[project]
name = "temporal-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "temporalio>=1.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.3.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Coverage 구성

### Coverage Settings

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    # Exclude type checking blocks
    if TYPE_CHECKING:
    # Exclude debug code
    def __repr__
    # Exclude abstract methods
    @abstractmethod
    # Exclude pass statements
    pass

[html]
directory = htmlcov
```

### 실행 중 테스트합니다 와 함께 Coverage

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Run specific test categories
pytest -m unit  # Unit tests only
pytest -m integration  # Integration tests only
pytest -m "not slow"  # Skip slow tests

# Parallel execution (faster)
pytest -n auto  # Use all CPU cores

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=80
```

### Coverage 보고서 예제

```
---------- coverage: platform darwin, python 3.11.5 -----------
Name                                Stmts   Miss  Cover   Missing
-----------------------------------------------------------------
src/__init__.py                         0      0   100%
src/activities/__init__.py              2      0   100%
src/activities/inventory.py            45      3    93%   78-80
src/activities/payment.py              38      0   100%
src/workflows/__init__.py               2      0   100%
src/workflows/order_workflow.py        67      5    93%   45-49
src/workflows/payment_workflow.py      52      0   100%
-----------------------------------------------------------------
TOTAL                                 206      8    96%

10 files skipped due to complete coverage.
```

## 개발 워크플로우

### Daily 개발 흐름

```bash
# 1. Start Temporal server
docker-compose up -d

# 2. Verify server health
python scripts/health_check.py

# 3. Run tests during development
pytest tests/unit/ --verbose

# 4. Run full test suite before commit
pytest --cov=src --cov-report=term-missing

# 5. Check coverage
open htmlcov/index.html

# 6. Stop server
docker-compose down
```

### Pre-커밋 Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running tests..."
pytest --cov=src --cov-fail-under=80

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi

echo "All tests passed!"
```

### Makefile 위한 일반적인 Tasks

```makefile
# Makefile
.PHONY: setup test test-unit test-integration coverage clean

setup:
	docker-compose up -d
	pip install -r requirements.txt
	python scripts/health_check.py

test:
	pytest --cov=src --cov-report=term-missing

test-unit:
	pytest -m unit --verbose

test-integration:
	pytest -m integration --verbose

test-replay:
	pytest -m replay --verbose

test-parallel:
	pytest -n auto --cov=src

coverage:
	pytest --cov=src --cov-report=html
	open htmlcov/index.html

clean:
	docker-compose down -v
	rm -rf .pytest_cache htmlcov .coverage

ci:
	docker-compose up -d
	sleep 10  # Wait for Temporal to start
	pytest --cov=src --cov-fail-under=80
	docker-compose down
```

### CI/CD 예제

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Start Temporal server
        run: docker-compose up -d

      - name: Wait for Temporal
        run: sleep 10

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

      - name: Cleanup
        if: always()
        run: docker-compose down
```

## 디버깅 Tips

### Enable Temporal SDK 로깅

```python
import logging

# Enable debug logging for Temporal SDK
logging.basicConfig(level=logging.DEBUG)
temporal_logger = logging.getLogger("temporalio")
temporal_logger.setLevel(logging.DEBUG)
```

### Interactive 디버깅

```python
# Add breakpoint in test
@pytest.mark.asyncio
async def test_workflow_with_breakpoint(workflow_env):
    import pdb; pdb.set_trace()  # Debug here

    async with Worker(...):
        result = await workflow_env.client.execute_workflow(...)
```

### Temporal Web UI

```bash
# Access Web UI at http://localhost:8080
# - View workflow executions
# - Inspect event history
# - Replay workflows
# - Monitor workers
```

## 최선의 관행

1. **격리된 환경**: Use Docker Compose 위한 reproducible 로컬 설정
2. **Health 확인합니다**: 항상 verify Temporal 서버 이전 실행 중 테스트합니다
3. **Fast Feedback**: Use pytest markers 에 run 단위 테스트합니다 빠르게
4. **Coverage Targets**: Maintain ≥80% 코드 coverage
5. **병렬로 테스트**: Use pytest-xdist 위한 faster test 실행합니다
6. **CI/CD 통합**: 자동화된 테스트 에 모든 커밋
7. **Cleanup**: 명확한 Docker volumes 사이 test 실행합니다 만약 필요한

## 문제 해결

**이슈: Temporal 서버 not 시작하는**
```bash
# Check logs
docker-compose logs temporal

# Reset database
docker-compose down -v
docker-compose up -d
```

**이슈: 테스트합니다 timing out**
```python
# Increase timeout in pytest.ini
asyncio_default_timeout = 30
```

**이슈: Port 이미 에서 use**
```bash
# Find process using port 7233
lsof -i :7233

# Kill process or change port in docker-compose.yml
```

## Additional 리소스

- Temporal 로컬 개발: docs.temporal.io/develop/python/로컬-dev
- pytest 문서화: docs.pytest.org
- Docker Compose: docs.docker.com/compose
- pytest-asyncio: github.com/pytest-dev/pytest-asyncio
