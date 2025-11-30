---
name: python-packaging
description: Create distributable Python 패키지 와 함께 적절한 project 구조, 설정.py/pyproject.toml, 및 게시 에 PyPI. Use 때 패키징 Python 라이브러리, 생성하는 CLI tools, 또는 distributing Python 코드.
---

# Python 패키징

포괄적인 가이드 에 생성하는, structuring, 및 distributing Python 패키지 사용하여 현대적인 패키징 tools, pyproject.toml, 및 게시 에 PyPI.

## 때 에 Use This Skill

- 생성하는 Python 라이브러리 위한 배포
- 구축 명령-line tools 와 함께 entry points
- 게시 패키지 에 PyPI 또는 비공개 repositories
- 설정하는 Python project 구조
- 생성하는 installable 패키지 와 함께 종속성
- 구축 wheels 및 소스 distributions
- Versioning 및 releasing Python 패키지
- 생성하는 namespace 패키지
- Implementing 패키지 메타데이터 및 classifiers

## 핵심 개념

### 1. 패키지 구조
- **소스 레이아웃**: `src/package_name/` (권장됨)
- **Flat 레이아웃**: `package_name/` (simpler 그러나 less 유연한)
- **패키지 메타데이터**: pyproject.toml, 설정.py, 또는 설정.cfg
- **배포 형식을 지정합니다**: wheel (.whl) 및 소스 배포 (.tar.gz)

### 2. 현대적인 패키징 표준
- **PEP 517/518**: 빌드 시스템 요구사항
- **PEP 621**: 메타데이터 에서 pyproject.toml
- **PEP 660**: Editable installs
- **pyproject.toml**: Single 소스 of 구성

### 3. 빌드 Backends
- **setuptools**: 전통적인, 넓게 used
- **hatchling**: 현대적인, opinionated
- **flit**: 경량, 위한 pure Python
- **poetry**: 종속성 관리 + 패키징

### 4. 배포
- **PyPI**: Python 패키지 인덱스 (공개)
- **TestPyPI**: 테스트 이전 production
- **비공개 repositories**: JFrog, AWS CodeArtifact, etc.

## Quick Start

### 최소 패키지 구조

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

### 최소 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
]
```

## 패키지 구조 패턴

### 패턴 1: 소스 레이아웃 (권장됨)

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── py.typed          # For type hints
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
└── docs/
    └── index.md
```

**Advantages:**
- 방지합니다 우연히 importing 에서 소스
- Cleaner test imports
- 더 나은 격리

**pyproject.toml 위한 소스 레이아웃:**
```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### 패턴 2: Flat 레이아웃

```
my-package/
├── pyproject.toml
├── README.md
├── my_package/
│   ├── __init__.py
│   └── module.py
└── tests/
    └── test_module.py
```

**Simpler 그러나:**
- Can import 패키지 없이 installing
- Less 프로페셔널 위한 라이브러리

### 패턴 3: Multi-패키지 Project

```
project/
├── pyproject.toml
├── packages/
│   ├── package-a/
│   │   └── src/
│   │       └── package_a/
│   └── package-b/
│       └── src/
│           └── package_b/
└── tests/
```

## 완전한 pyproject.toml 예제

### 패턴 4: 완전한 기능 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-awesome-package"
version = "1.0.0"
description = "An awesome Python package"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"},
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"},
]
keywords = ["example", "package", "awesome"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "requests>=2.28.0,<3.0.0",
    "click>=8.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
docs = [
    "sphinx>=5.0.0",
    "sphinx-rtd-theme>=1.0.0",
]
all = [
    "my-awesome-package[dev,docs]",
]

[project.urls]
Homepage = "https://github.com/username/my-awesome-package"
Documentation = "https://my-awesome-package.readthedocs.io"
Repository = "https://github.com/username/my-awesome-package"
"Bug Tracker" = "https://github.com/username/my-awesome-package/issues"
Changelog = "https://github.com/username/my-awesome-package/blob/main/CHANGELOG.md"

[project.scripts]
my-cli = "my_package.cli:main"
awesome-tool = "my_package.tools:run"

[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins:plugin1"

[tool.setuptools]
package-dir = {"" = "src"}
zip-safe = false

[tool.setuptools.packages.find]
where = ["src"]
include = ["my_package*"]
exclude = ["tests*"]

[tool.setuptools.package-data]
my_package = ["py.typed", "*.pyi", "data/*.json"]

# Black configuration
[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311"]
include = '\.pyi?$'

# Ruff configuration
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

# MyPy configuration
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=my_package --cov-report=term-missing"

# Coverage configuration
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### 패턴 5: 동적 Versioning

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
dynamic = ["version"]
description = "Package with dynamic version"

[tool.setuptools.dynamic]
version = {attr = "my_package.__version__"}

# Or use setuptools-scm for git-based versioning
[tool.setuptools_scm]
write_to = "src/my_package/_version.py"
```

**에서 __init__.py:**
```python
# src/my_package/__init__.py
__version__ = "1.0.0"

# Or with setuptools-scm
from importlib.metadata import version
__version__ = version("my-package")
```

## 명령-Line 인터페이스 (CLI) 패턴

### 패턴 6: CLI 와 함께 Click

```python
# src/my_package/cli.py
import click

@click.group()
@click.version_option()
def cli():
    """My awesome CLI tool."""
    pass

@cli.command()
@click.argument("name")
@click.option("--greeting", default="Hello", help="Greeting to use")
def greet(name: str, greeting: str):
    """Greet someone."""
    click.echo(f"{greeting}, {name}!")

@cli.command()
@click.option("--count", default=1, help="Number of times to repeat")
def repeat(count: int):
    """Repeat a message."""
    for i in range(count):
        click.echo(f"Message {i + 1}")

def main():
    """Entry point for CLI."""
    cli()

if __name__ == "__main__":
    main()
```

**Register 에서 pyproject.toml:**
```toml
[project.scripts]
my-tool = "my_package.cli:main"
```

**Usage:**
```bash
pip install -e .
my-tool greet World
my-tool greet Alice --greeting="Hi"
my-tool repeat --count=3
```

### 패턴 7: CLI 와 함께 argparse

```python
# src/my_package/cli.py
import argparse
import sys

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="My awesome tool",
        prog="my-tool"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add subcommand
    process_parser = subparsers.add_parser("process", help="Process data")
    process_parser.add_argument("input_file", help="Input file path")
    process_parser.add_argument(
        "--output", "-o",
        default="output.txt",
        help="Output file path"
    )

    args = parser.parse_args()

    if args.command == "process":
        process_data(args.input_file, args.output)
    else:
        parser.print_help()
        sys.exit(1)

def process_data(input_file: str, output_file: str):
    """Process data from input to output."""
    print(f"Processing {input_file} -> {output_file}")

if __name__ == "__main__":
    main()
```

## 구축 및 게시

### 패턴 8: 빌드 패키지 Locally

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# This creates:
# dist/
#   my-package-1.0.0.tar.gz (source distribution)
#   my_package-1.0.0-py3-none-any.whl (wheel)

# Check the distribution
twine check dist/*
```

### 패턴 9: 게시 에 PyPI

```bash
# Install publishing tools
pip install twine

# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ my-package

# If all good, publish to PyPI
twine upload dist/*
```

**사용하여 API 토큰 (권장됨):**
```bash
# Create ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-...your-token...

[testpypi]
username = __token__
password = pypi-...your-test-token...
```

### 패턴 10: 자동화된 게시 와 함께 GitHub Actions

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## 고급 패턴

### 패턴 11: 포함하여 데이터 파일

```toml
[tool.setuptools.package-data]
my_package = [
    "data/*.json",
    "templates/*.html",
    "static/css/*.css",
    "py.typed",
]
```

**Accessing 데이터 파일:**
```python
# src/my_package/loader.py
from importlib.resources import files
import json

def load_config():
    """Load configuration from package data."""
    config_file = files("my_package").joinpath("data/config.json")
    with config_file.open() as f:
        return json.load(f)

# Python 3.9+
from importlib.resources import files

data = files("my_package").joinpath("data/file.txt").read_text()
```

### 패턴 12: Namespace 패키지

**위한 large projects 분할된 전반에 걸쳐 여러 repositories:**

```
# Package 1: company-core
company/
└── core/
    ├── __init__.py
    └── models.py

# Package 2: company-api
company/
└── api/
    ├── __init__.py
    └── routes.py
```

**do NOT include __init__.py 에서 the namespace 디렉터리 (회사/):**

```toml
# company-core/pyproject.toml
[project]
name = "company-core"

[tool.setuptools.packages.find]
where = ["."]
include = ["company.core*"]

# company-api/pyproject.toml
[project]
name = "company-api"

[tool.setuptools.packages.find]
where = ["."]
include = ["company.api*"]
```

**Usage:**
```python
# Both packages can be imported under same namespace
from company.core import models
from company.api import routes
```

### 패턴 13: C Extensions

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "Cython>=0.29"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
ext-modules = [
    {name = "my_package.fast_module", sources = ["src/fast_module.c"]},
]
```

**또는 와 함께 설정.py:**
```python
# setup.py
from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            "my_package.fast_module",
            sources=["src/fast_module.c"],
            include_dirs=["src/include"],
        )
    ]
)
```

## 버전 관리

### 패턴 14: Semantic Versioning

```python
# src/my_package/__init__.py
__version__ = "1.2.3"

# Semantic versioning: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features (backward compatible)
# PATCH: Bug fixes
```

**버전 constraints 에서 종속성:**
```toml
dependencies = [
    "requests>=2.28.0,<3.0.0",  # Compatible range
    "click~=8.1.0",              # Compatible release (~= 8.1.0 means >=8.1.0,<8.2.0)
    "pydantic>=2.0",             # Minimum version
    "numpy==1.24.3",             # Exact version (avoid if possible)
]
```

### 패턴 15: Git-Based Versioning

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "src/my_package/_version.py"
version_scheme = "post-release"
local_scheme = "dirty-tag"
```

**생성합니다 버전 같은:**
- `1.0.0` (에서 git tag)
- `1.0.1.dev3+g1234567` (3 commits 이후 tag)

## 테스트 Installation

### 패턴 16: Editable Install

```bash
# Install in development mode
pip install -e .

# With optional dependencies
pip install -e ".[dev]"
pip install -e ".[dev,docs]"

# Now changes to source code are immediately reflected
```

### 패턴 17: 테스트 에서 격리된 환경

```bash
# Create virtual environment
python -m venv test-env
source test-env/bin/activate  # Linux/Mac
# test-env\Scripts\activate  # Windows

# Install package
pip install dist/my_package-1.0.0-py3-none-any.whl

# Test it works
python -c "import my_package; print(my_package.__version__)"

# Test CLI
my-tool --help

# Cleanup
deactivate
rm -rf test-env
```

## 문서화

### 패턴 18: README.md 템플릿

```markdown
# My Package

[![PyPI version](https://badge.fury.io/py/my-package.svg)](https://pypi.org/project/my-package/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-package.svg)](https://pypi.org/project/my-package/)
[![Tests](https://github.com/username/my-package/workflows/Tests/badge.svg)](https://github.com/username/my-package/actions)

Brief description of your package.

## Installation

```bash
pip install my-패키지
```

## Quick Start

```python
에서 my_package import something

result = something.do_stuff()
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

Full documentation: https://my-package.readthedocs.io

## Development

```bash
git clone https://github.com/username/my-package.git
cd my-패키지
pip install -e ".[dev]"
pytest
```

## License

MIT
```

## 일반적인 패턴

### 패턴 19: Multi-아키텍처 Wheels

```yaml
# .github/workflows/wheels.yml
name: Build wheels

on: [push, pull_request]

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Build wheels
        uses: pypa/cibuildwheel@v2.16.2

      - uses: actions/upload-artifact@v3
        with:
          path: ./wheelhouse/*.whl
```

### 패턴 20: 비공개 패키지 인덱스

```bash
# Install from private index
pip install my-package --index-url https://private.pypi.org/simple/

# Or add to pip.conf
[global]
index-url = https://private.pypi.org/simple/
extra-index-url = https://pypi.org/simple/

# Upload to private index
twine upload --repository-url https://private.pypi.org/ dist/*
```

## 파일 템플릿

### .gitignore 위한 Python 패키지

```gitignore
# Build artifacts
build/
dist/
*.egg-info/
*.egg
.eggs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution
*.whl
*.tar.gz
```

### 매니페스트.에서

```
# MANIFEST.in
include README.md
include LICENSE
include pyproject.toml

recursive-include src/my_package/data *.json
recursive-include src/my_package/templates *.html
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

## Checklist 위한 게시

- [ ] 코드 is 테스트된 (pytest passing)
- [ ] 문서화 is 완전한 (README, docstrings)
- [ ] 버전 숫자 업데이트된
- [ ] CHANGELOG.md 업데이트된
- [ ] License 파일 포함된
- [ ] pyproject.toml is 완전한
- [ ] 패키지 빌드 없이 오류
- [ ] Installation 테스트된 에서 clean 환경
- [ ] CLI tools work (만약 적용 가능한)
- [ ] PyPI 메타데이터 is 올바른 (classifiers, keywords)
- [ ] GitHub 저장소 연결됨
- [ ] 테스트된 에 TestPyPI 첫 번째
- [ ] Git tag 생성된 위한 릴리스

## 리소스

- **Python 패키징 가이드**: https://packaging.python.org/
- **PyPI**: https://pypi.org/
- **TestPyPI**: https://test.pypi.org/
- **setuptools 문서화**: https://setuptools.pypa.io/
- **빌드**: https://pypa-build.readthedocs.io/
- **twine**: https://twine.readthedocs.io/

## 최선의 관행 Summary

1. **Use src/ 레이아웃** 위한 cleaner 패키지 구조
2. **Use pyproject.toml** 위한 현대적인 패키징
3. **Pin 빌드 종속성** 에서 빌드-시스템.필요합니다
4. **버전 적절하게** 와 함께 semantic versioning
5. **Include 모든 메타데이터** (classifiers, URLs, etc.)
6. **Test installation** 에서 clean 환경
7. **Use TestPyPI** 이전 게시 에 PyPI
8. **Document 철저히** 와 함께 README 및 docstrings
9. **Include LICENSE** 파일
10. **Automate 게시** 와 함께 CI/CD
