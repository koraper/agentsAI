---
name: python-testing-patterns
description: Implement 포괄적인 테스트 strategies 와 함께 pytest, fixtures, mocking, 및 테스트 주도 개발. Use 때 작성 Python 테스트합니다, 설정하는 test suites, 또는 implementing 테스트 최선의 관행.
---

# Python 테스트 패턴

포괄적인 가이드 에 implementing 강력한 테스트 strategies 에서 Python 사용하여 pytest, fixtures, mocking, parameterization, 및 테스트 주도 개발 관행.

## 때 에 Use This Skill

- 작성 단위 테스트합니다 위한 Python 코드
- 설정하는 test suites 및 test 인프라
- Implementing 테스트 주도 개발 (TDD)
- 생성하는 통합 테스트합니다 위한 APIs 및 서비스
- Mocking 외부 종속성 및 서비스
- 테스트 비동기 코드 및 concurrent 작업
- 설정하는 continuous 테스트 에서 CI/CD
- Implementing 속성-based 테스트
- 테스트 데이터베이스 작업
- 디버깅 failing 테스트합니다

## 핵심 개념

### 1. Test 유형
- **단위 테스트합니다**: Test 개별 함수/클래스 에서 격리
- **통합 테스트합니다**: Test interaction 사이 컴포넌트
- **기능적인 테스트합니다**: Test 완전한 기능 end-에-end
- **성능 테스트합니다**: 측정 속도 및 리소스 usage

### 2. Test 구조 (AAA 패턴)
- **Arrange**: 세트 up test 데이터 및 preconditions
- **Act**: Execute the 코드 under test
- **Assert**: Verify the results

### 3. Test Coverage
- 측정 무엇 코드 is exercised 에 의해 테스트합니다
- Identify untested 코드 경로
- Aim 위한 의미 있는 coverage, not 방금 high percentages

### 4. Test 격리
- 테스트합니다 should be 독립적인
- 아니요 shared 상태 사이 테스트합니다
- 각 test should clean up 이후 itself

## Quick Start

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """Basic test example."""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """Test with negative numbers."""
    assert add(-1, 1) == 0

# Run with: pytest test_example.py
```

## 기본 패턴

### 패턴 1: 기본 pytest 테스트합니다

```python
# test_calculator.py
import pytest

class Calculator:
    """Simple calculator for testing."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def test_addition():
    """Test addition."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0


def test_subtraction():
    """Test subtraction."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_multiplication():
    """Test multiplication."""
    calc = Calculator()
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(0, 5) == 0


def test_division():
    """Test division."""
    calc = Calculator()
    assert calc.divide(6, 3) == 2
    assert calc.divide(5, 2) == 2.5


def test_division_by_zero():
    """Test division by zero raises error."""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(5, 0)
```

### 패턴 2: Fixtures 위한 설정 및 Teardown

```python
# test_database.py
import pytest
from typing import Generator

class Database:
    """Simple database class."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        """Connect to database."""
        self.connected = True

    def disconnect(self):
        """Disconnect from database."""
        self.connected = False

    def query(self, sql: str) -> list:
        """Execute query."""
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]


@pytest.fixture
def db() -> Generator[Database, None, None]:
    """Fixture that provides connected database."""
    # Setup
    database = Database("sqlite:///:memory:")
    database.connect()

    # Provide to test
    yield database

    # Teardown
    database.disconnect()


def test_database_query(db):
    """Test database query with fixture."""
    results = db.query("SELECT * FROM users")
    assert len(results) == 1
    assert results[0]["name"] == "Test"


@pytest.fixture(scope="session")
def app_config():
    """Session-scoped fixture - created once per test session."""
    return {
        "database_url": "postgresql://localhost/test",
        "api_key": "test-key",
        "debug": True
    }


@pytest.fixture(scope="module")
def api_client(app_config):
    """Module-scoped fixture - created once per test module."""
    # Setup expensive resource
    client = {"config": app_config, "session": "active"}
    yield client
    # Cleanup
    client["session"] = "closed"


def test_api_client(api_client):
    """Test using api client fixture."""
    assert api_client["session"] == "active"
    assert api_client["config"]["debug"] is True
```

### 패턴 3: Parameterized 테스트합니다

```python
# test_validation.py
import pytest

def is_valid_email(email: str) -> bool:
    """Check if email is valid."""
    return "@" in email and "." in email.split("@")[1]


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@domain", False),
    ("", False),
])
def test_email_validation(email, expected):
    """Test email validation with various inputs."""
    assert is_valid_email(email) == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -5, -10),
])
def test_addition_parameterized(a, b, expected):
    """Test addition with multiple parameter sets."""
    from test_calculator import Calculator
    calc = Calculator()
    assert calc.add(a, b) == expected


# Using pytest.param for special cases
@pytest.mark.parametrize("value,expected", [
    pytest.param(1, True, id="positive"),
    pytest.param(0, False, id="zero"),
    pytest.param(-1, False, id="negative"),
])
def test_is_positive(value, expected):
    """Test with custom test IDs."""
    assert (value > 0) == expected
```

### 패턴 4: Mocking 와 함께 unittest.mock

```python
# test_api_client.py
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

class APIClient:
    """Simple API client."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        """Fetch user from API."""
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, data: dict) -> dict:
        """Create new user."""
        response = requests.post(f"{self.base_url}/users", json=data)
        response.raise_for_status()
        return response.json()


def test_get_user_success():
    """Test successful API call with mock."""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)

        assert user["id"] == 1
        assert user["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_get_user_not_found():
    """Test API call with 404 error."""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            client.get_user(999)


@patch("requests.post")
def test_create_user(mock_post):
    """Test user creation with decorator syntax."""
    client = APIClient("https://api.example.com")

    mock_post.return_value.json.return_value = {"id": 2, "name": "Jane Doe"}
    mock_post.return_value.raise_for_status.return_value = None

    user_data = {"name": "Jane Doe", "email": "jane@example.com"}
    result = client.create_user(user_data)

    assert result["id"] == 2
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.kwargs["json"] == user_data
```

### 패턴 5: 테스트 예외

```python
# test_exceptions.py
import pytest

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a / b


def test_zero_division():
    """Test exception is raised for division by zero."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_zero_division_with_message():
    """Test exception message."""
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide(5, 0)


def test_type_error():
    """Test type error exception."""
    with pytest.raises(TypeError, match="must be numbers"):
        divide("10", 5)


def test_exception_info():
    """Test accessing exception info."""
    with pytest.raises(ValueError) as exc_info:
        int("not a number")

    assert "invalid literal" in str(exc_info.value)
```

## 고급 패턴

### 패턴 6: 테스트 비동기 코드

```python
# test_async.py
import pytest
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously."""
    await asyncio.sleep(0.1)
    return {"url": url, "data": "result"}


@pytest.mark.asyncio
async def test_fetch_data():
    """Test async function."""
    result = await fetch_data("https://api.example.com")
    assert result["url"] == "https://api.example.com"
    assert "data" in result


@pytest.mark.asyncio
async def test_concurrent_fetches():
    """Test concurrent async operations."""
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    assert len(results) == 3
    assert all("data" in r for r in results)


@pytest.fixture
async def async_client():
    """Async fixture."""
    client = {"connected": True}
    yield client
    client["connected"] = False


@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """Test using async fixture."""
    assert async_client["connected"] is True
```

### 패턴 7: Monkeypatch 위한 테스트

```python
# test_environment.py
import os
import pytest

def get_database_url() -> str:
    """Get database URL from environment."""
    return os.environ.get("DATABASE_URL", "sqlite:///:memory:")


def test_database_url_default():
    """Test default database URL."""
    # Will use actual environment variable if set
    url = get_database_url()
    assert url


def test_database_url_custom(monkeypatch):
    """Test custom database URL with monkeypatch."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    assert get_database_url() == "postgresql://localhost/test"


def test_database_url_not_set(monkeypatch):
    """Test when env var is not set."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == "sqlite:///:memory:"


class Config:
    """Configuration class."""

    def __init__(self):
        self.api_key = "production-key"

    def get_api_key(self):
        return self.api_key


def test_monkeypatch_attribute(monkeypatch):
    """Test monkeypatching object attributes."""
    config = Config()
    monkeypatch.setattr(config, "api_key", "test-key")
    assert config.get_api_key() == "test-key"
```

### 패턴 8: 임시 파일 및 디렉터리

```python
# test_file_operations.py
import pytest
from pathlib import Path

def save_data(filepath: Path, data: str):
    """Save data to file."""
    filepath.write_text(data)


def load_data(filepath: Path) -> str:
    """Load data from file."""
    return filepath.read_text()


def test_file_operations(tmp_path):
    """Test file operations with temporary directory."""
    # tmp_path is a pathlib.Path object
    test_file = tmp_path / "test_data.txt"

    # Save data
    save_data(test_file, "Hello, World!")

    # Verify file exists
    assert test_file.exists()

    # Load and verify data
    data = load_data(test_file)
    assert data == "Hello, World!"


def test_multiple_files(tmp_path):
    """Test with multiple temporary files."""
    files = {
        "file1.txt": "Content 1",
        "file2.txt": "Content 2",
        "file3.txt": "Content 3"
    }

    for filename, content in files.items():
        filepath = tmp_path / filename
        save_data(filepath, content)

    # Verify all files created
    assert len(list(tmp_path.iterdir())) == 3

    # Verify contents
    for filename, expected_content in files.items():
        filepath = tmp_path / filename
        assert load_data(filepath) == expected_content
```

### 패턴 9: 사용자 정의 Fixtures 및 Conftest

```python
# conftest.py
"""Shared fixtures for all tests."""
import pytest

@pytest.fixture(scope="session")
def database_url():
    """Provide database URL for all tests."""
    return "postgresql://localhost/test_db"


@pytest.fixture(autouse=True)
def reset_database(database_url):
    """Auto-use fixture that runs before each test."""
    # Setup: Clear database
    print(f"Clearing database: {database_url}")
    yield
    # Teardown: Clean up
    print("Test completed")


@pytest.fixture
def sample_user():
    """Provide sample user data."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def sample_users():
    """Provide list of sample users."""
    return [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
        {"id": 3, "name": "User 3"},
    ]


# Parametrized fixture
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db_backend(request):
    """Fixture that runs tests with different database backends."""
    return request.param


def test_with_db_backend(db_backend):
    """This test will run 3 times with different backends."""
    print(f"Testing with {db_backend}")
    assert db_backend in ["sqlite", "postgresql", "mysql"]
```

### 패턴 10: 속성-Based 테스트

```python
# test_properties.py
from hypothesis import given, strategies as st
import pytest

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]


@given(st.text())
def test_reverse_twice_is_original(s):
    """Property: reversing twice returns original."""
    assert reverse_string(reverse_string(s)) == s


@given(st.text())
def test_reverse_length(s):
    """Property: reversed string has same length."""
    assert len(reverse_string(s)) == len(s)


@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Property: addition is commutative."""
    assert a + b == b + a


@given(st.lists(st.integers()))
def test_sorted_list_properties(lst):
    """Property: sorted list is ordered."""
    sorted_lst = sorted(lst)

    # Same length
    assert len(sorted_lst) == len(lst)

    # All elements present
    assert set(sorted_lst) == set(lst)

    # Is ordered
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

## 테스트 최선의 관행

### Test 조직

```python
# tests/
#   __init__.py
#   conftest.py           # Shared fixtures
#   test_unit/            # Unit tests
#     test_models.py
#     test_utils.py
#   test_integration/     # Integration tests
#     test_api.py
#     test_database.py
#   test_e2e/            # End-to-end tests
#     test_workflows.py
```

### Test Naming

```python
# Good test names
def test_user_creation_with_valid_data():
    """Clear name describes what is being tested."""
    pass


def test_login_fails_with_invalid_password():
    """Name describes expected behavior."""
    pass


def test_api_returns_404_for_missing_resource():
    """Specific about inputs and expected outcomes."""
    pass


# Bad test names
def test_1():  # Not descriptive
    pass


def test_user():  # Too vague
    pass


def test_function():  # Doesn't explain what's tested
    pass
```

### Test Markers

```python
# test_markers.py
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Mark slow tests."""
    import time
    time.sleep(2)


@pytest.mark.integration
def test_database_integration():
    """Mark integration tests."""
    pass


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Skip tests temporarily."""
    pass


@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific():
    """Conditional skip."""
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """Mark expected failures."""
    assert False


# Run with:
# pytest -m slow          # Run only slow tests
# pytest -m "not slow"    # Skip slow tests
# pytest -m integration   # Run integration tests
```

### Coverage Reporting

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=myapp tests/

# Generate HTML report
pytest --cov=myapp --cov-report=html tests/

# Fail if coverage below threshold
pytest --cov=myapp --cov-fail-under=80 tests/

# Show missing lines
pytest --cov=myapp --cov-report=term-missing tests/
```

## 테스트 데이터베이스 코드

```python
# test_database_models.py
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """Create in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()


def test_create_user(db_session):
    """Test creating a user."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == "Test User"


def test_query_user(db_session):
    """Test querying users."""
    user1 = User(name="User 1", email="user1@example.com")
    user2 = User(name="User 2", email="user2@example.com")

    db_session.add_all([user1, user2])
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 2


def test_unique_email_constraint(db_session):
    """Test unique email constraint."""
    from sqlalchemy.exc import IntegrityError

    user1 = User(name="User 1", email="same@example.com")
    user2 = User(name="User 2", email="same@example.com")

    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

## CI/CD 통합

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 구성 파일

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=myapp
    --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks integration tests
    unit: marks unit tests
    e2e: marks end-to-end tests
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--cov=myapp",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## 리소스

- **pytest 문서화**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **가설**: 속성-based 테스트
- **pytest-asyncio**: 테스트 비동기 코드
- **pytest-cov**: Coverage reporting
- **pytest-mock**: pytest 래퍼 위한 mock

## 최선의 관행 Summary

1. **Write 테스트합니다 첫 번째** (TDD) 또는 alongside 코드
2. **One assertion per test** 때 possible
3. **Use descriptive test names** 것 explain behavior
4. **Keep 테스트합니다 독립적인** 및 격리된
5. **Use fixtures** 위한 설정 및 teardown
6. **Mock 외부 종속성** 적절하게
7. **Parametrize 테스트합니다** 에 reduce duplication
8. **Test 엣지 cases** 및 오류 conditions
9. **측정 coverage** 그러나 focus 에 품질
10. **Run 테스트합니다 에서 CI/CD** 에 모든 커밋
