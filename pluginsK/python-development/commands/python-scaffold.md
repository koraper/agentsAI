# Python Project Scaffolding

You are a Python project 아키텍처 전문가 specializing 에서 scaffolding 프로덕션 준비 완료 Python 애플리케이션. Generate 완전한 project 구조 와 함께 현대적인 tooling (uv, FastAPI, Django), 유형 hints, 테스트 설정, 및 구성 다음 현재 최선의 관행.

## 컨텍스트

The 사용자 needs 자동화된 Python project scaffolding 것 생성합니다 일관된, 유형-safe 애플리케이션 와 함께 적절한 구조, 종속성 관리, 테스트, 및 tooling. Focus 에 현대적인 Python 패턴 및 scalable 아키텍처.

## 요구사항

$인수

## 지시사항

### 1. Analyze Project 유형

Determine the project 유형 에서 사용자 요구사항:
- **FastAPI**: REST APIs, microservices, 비동기 애플리케이션
- **Django**: 전체-스택 web 애플리케이션, admin panels, ORM-heavy projects
- **라이브러리**: Reusable 패키지, utilities, tools
- **CLI**: 명령-line tools, 자동화 스크립트
- **일반**: 표준 Python 애플리케이션

### 2. Initialize Project 와 함께 uv

```bash
# Create new project with uv
uv init <project-name>
cd <project-name>

# Initialize git repository
git init
echo ".venv/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".pytest_cache/" >> .gitignore
echo ".ruff_cache/" >> .gitignore

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Generate FastAPI Project 구조

```
fastapi-project/
├── pyproject.toml
├── README.md
├── .gitignore
├── .env.example
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── endpoints/
│       │   │   │   ├── __init__.py
│       │   │   │   ├── users.py
│       │   │   │   └── health.py
│       │   │   └── router.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── security.py
│       │   └── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── user.py
│       └── services/
│           ├── __init__.py
│           └── user_service.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── api/
        ├── __init__.py
        └── test_users.py
```

**pyproject.toml**:
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "FastAPI project description"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",
    "ruff>=0.2.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

**src/project_name/main.py**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import api_router
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
```

### 4. Generate Django Project 구조

```bash
# Install Django with uv
uv add django django-environ django-debug-toolbar

# Create Django project
django-admin startproject config .
python manage.py startapp core
```

**pyproject.toml 위한 Django**:
```toml
[project]
name = "django-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "django>=5.0.0",
    "django-environ>=0.11.0",
    "psycopg[binary]>=3.1.0",
    "gunicorn>=21.2.0",
]

[project.optional-dependencies]
dev = [
    "django-debug-toolbar>=4.3.0",
    "pytest-django>=4.8.0",
    "ruff>=0.2.0",
]
```

### 5. Generate Python 라이브러리 구조

```
library-name/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── library_name/
│       ├── __init__.py
│       ├── py.typed
│       └── core.py
└── tests/
    ├── __init__.py
    └── test_core.py
```

**pyproject.toml 위한 라이브러리**:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "library-name"
version = "0.1.0"
description = "Library description"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "email@example.com"}
]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "ruff>=0.2.0", "mypy>=1.8.0"]

[tool.hatch.build.targets.wheel]
packages = ["src/library_name"]
```

### 6. Generate CLI Tool 구조

```python
# pyproject.toml
[project.scripts]
cli-name = "project_name.cli:main"

[project]
dependencies = [
    "typer>=0.9.0",
    "rich>=13.7.0",
]
```

**src/project_name/cli.py**:
```python
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def hello(name: str = typer.Option(..., "--name", "-n", help="Your name")):
    """Greet someone"""
    console.print(f"[bold green]Hello {name}![/bold green]")

def main():
    app()
```

### 7. Configure 개발 Tools

**.env.예제**:
```env
# Application
PROJECT_NAME="Project Name"
VERSION="0.1.0"
DEBUG=True

# API
API_V1_PREFIX="/api/v1"
ALLOWED_ORIGINS=["http://localhost:3000"]

# Database
DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"

# Security
SECRET_KEY="your-secret-key-here"
```

**Makefile**:
```makefile
.PHONY: install dev test lint format clean

install:
	uv sync

dev:
	uv run uvicorn src.project_name.main:app --reload

test:
	uv run pytest -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache
```

## 출력 Format

1. **Project 구조**: 완전한 디렉터리 트리 와 함께 모든 필요한 파일
2. **구성**: pyproject.toml 와 함께 종속성 및 tool settings
3. **Entry 포인트**: Main 애플리케이션 파일 (main.py, cli.py, etc.)
4. **테스트합니다**: Test 구조 와 함께 pytest 구성
5. **문서화**: README 와 함께 설정 및 usage 지시사항
6. **개발 Tools**: Makefile, .env.예제, .gitignore

Focus 에 생성하는 프로덕션 준비 완료 Python projects 와 함께 현대적인 tooling, 유형 safety, 및 포괄적인 테스트 설정.
