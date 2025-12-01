---
name: workbench:python-development
description: Expert Python development covering modern Python 3.12+, async patterns, FastAPI/Django, testing with pytest, performance optimization, and packaging. Use for production-grade Python code.
when_to_use: When writing Python code. When building APIs with FastAPI or Django. When writing async code. When optimizing performance. When packaging libraries. When writing tests with pytest.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Python Development Expert

**Announce at start:** "I'm using the python-development skill for Python expertise."

## Overview

Production-grade Python development with modern tooling, type safety, and best practices for Python 3.12+.

**Core principle:** Write readable, type-safe, well-tested code using the modern Python ecosystem.

## Quick Reference

| Task | Tool/Approach |
|------|---------------|
| Package management | `uv` (not pip/poetry) |
| Linting + formatting | `ruff` |
| Type checking | `mypy` or `pyright` |
| Testing | `pytest` |
| Web API | FastAPI (async) or Django (batteries) |

## Modern Tooling

### uv Package Manager

```bash
# Create new project
uv init myproject
cd myproject

# Add dependencies
uv add fastapi uvicorn
uv add --dev pytest ruff mypy

# Run commands
uv run python main.py
uv run pytest

# Sync from lockfile
uv sync

# Manage Python versions
uv python install 3.12
uv python pin 3.12
```

### pyproject.toml

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.100",
    "uvicorn[standard]",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio",
    "ruff",
    "mypy",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "PT"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Project Structure

```
src/
└── myproject/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   └── routes.py
    ├── services/
    │   └── __init__.py
    └── models/
        └── __init__.py
tests/
├── conftest.py
├── unit/
└── integration/
pyproject.toml
```

## Type Hints

### Basic Patterns

```python
from typing import TypeAlias
from collections.abc import Callable, Sequence

# Basic types
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times

# Collections (use lowercase in 3.12+)
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Optional (use | None in 3.10+)
def find_user(user_id: int) -> User | None:
    ...

# Callable
Handler: TypeAlias = Callable[[Request], Response]

# Generic functions
def first[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None
```

### Pydantic Models

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = []

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

class UserCreate(BaseModel):
    name: str
    email: str
```

### Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    tags: list[str] = field(default_factory=list)

@dataclass(frozen=True)  # Immutable
class Point:
    x: float
    y: float
```

## Async Patterns

### Basic async/await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Concurrent execution
async def fetch_all(urls: list[str]) -> list[dict]:
    return await asyncio.gather(*[fetch_data(url) for url in urls])

# Run from sync code
result = asyncio.run(fetch_all(urls))
```

### Semaphore Rate Limiting

```python
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

### Producer-Consumer Pattern

```python
async def producer(queue: asyncio.Queue[str], items: list[str]) -> None:
    for item in items:
        await queue.put(item)
    await queue.put(None)  # Sentinel

async def consumer(queue: asyncio.Queue[str]) -> None:
    while True:
        item = await queue.get()
        if item is None:
            break
        await process(item)
        queue.task_done()

async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=100)
    await asyncio.gather(
        producer(queue, items),
        consumer(queue),
    )
```

### Timeout and Error Handling

```python
async def fetch_with_timeout(url: str, timeout: float = 10.0) -> dict | None:
    try:
        async with asyncio.timeout(timeout):
            return await fetch_data(url)
    except asyncio.TimeoutError:
        logger.warning(f"Timeout fetching {url}")
        return None
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching {url}: {e}")
        return None
```

## FastAPI

### Basic Setup

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

### Routes with Validation

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    # Pydantic validates request body automatically
    db_user = await user_service.create(user)
    return UserResponse.model_validate(db_user)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

### Dependency Injection

```python
from typing import Annotated

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    user = await verify_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.get("/me")
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserResponse:
    return UserResponse.model_validate(current_user)
```

## Testing with pytest

### Basic Tests

```python
import pytest

def test_addition():
    assert 1 + 1 == 2

def test_exception():
    with pytest.raises(ValueError, match="invalid"):
        raise ValueError("invalid input")

class TestUserService:
    def test_create_user(self, user_service):
        user = user_service.create(name="Test", email="test@example.com")
        assert user.id is not None
        assert user.name == "Test"
```

### Fixtures

```python
# conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="Test", email="test@example.com")

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    await engine.dispose()

@pytest.fixture
def client(db_session) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_user(db_session: AsyncSession):
    user = User(name="Test", email="test@example.com")
    db_session.add(user)
    await db_session.commit()

    result = await db_session.get(User, user.id)
    assert result.name == "Test"
```

### Parameterization

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("hello world", 11),
])
def test_string_length(input: str, expected: int):
    assert len(input) == expected

@pytest.mark.parametrize("a,b,expected", [
    pytest.param(1, 2, 3, id="positive"),
    pytest.param(-1, 1, 0, id="mixed"),
    pytest.param(0, 0, 0, id="zeros"),
])
def test_add(a: int, b: int, expected: int):
    assert a + b == expected
```

### Mocking

```python
from unittest.mock import AsyncMock, patch, MagicMock

@pytest.fixture
def mock_client():
    with patch("myapp.client.httpx.AsyncClient") as mock:
        mock_instance = AsyncMock()
        mock.return_value.__aenter__.return_value = mock_instance
        yield mock_instance

async def test_api_call(mock_client):
    mock_client.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"data": "test"}
    )

    result = await fetch_data("/endpoint")

    assert result == {"data": "test"}
    mock_client.get.assert_called_once_with("/endpoint")
```

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

# Profile a function
profiler = cProfile.Profile()
profiler.enable()
result = slow_function()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)

# Line profiler (install: pip install line_profiler)
# @profile decorator, run with: kernprof -l script.py
```

### Common Optimizations

```python
# Use dict for O(1) lookup instead of list O(n)
user_set = {u.id for u in users}  # O(1) membership test
if user_id in user_set: ...

# List comprehension over loop
squares = [x**2 for x in range(1000)]  # Faster than append loop

# Generator for memory efficiency
def read_large_file(path: str):
    with open(path) as f:
        for line in f:
            yield line.strip()

# Use slots for memory efficiency
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(n: int) -> int:
    return sum(i**2 for i in range(n))
```

### Batch Database Operations

```python
# Bad: N+1 queries
for user in users:
    posts = await get_posts(user.id)

# Good: Batch query
user_ids = [u.id for u in users]
all_posts = await get_posts_batch(user_ids)
posts_by_user = {p.user_id: p for p in all_posts}
```

## Packaging

### Build and Publish

```bash
# Build
uv build

# Test on TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Publish to PyPI
uv publish
```

### CLI Entry Points

```toml
[project.scripts]
mycli = "myproject.cli:main"
```

```python
# myproject/cli.py
import click

@click.command()
@click.option("--name", default="World", help="Name to greet")
def main(name: str) -> None:
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

## Best Practices

### Do

- Use type hints everywhere
- Use `uv` for package management
- Use `ruff` for linting and formatting
- Write tests with pytest
- Use dataclasses or Pydantic for data structures
- Use async for I/O-bound operations
- Use context managers for resources
- Handle errors explicitly

### Avoid

- `pip install` (use `uv add`)
- Mutable default arguments: `def f(items=[])`
- Bare `except:` clauses
- `from module import *`
- Global mutable state
- Blocking calls in async code
- Ignoring type checker errors

## Common Patterns

| Pattern | Use Case |
|---------|----------|
| Repository | Database abstraction |
| Service layer | Business logic isolation |
| Dependency injection | Testability, loose coupling |
| Factory | Complex object creation |
| Strategy | Interchangeable algorithms |
| Context manager | Resource cleanup |
