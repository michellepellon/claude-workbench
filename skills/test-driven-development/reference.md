# TDD Reference Guide

Detailed guidance for test-driven development.

## Testing Philosophy

**Root Principle**: Tests define behavior. Implementation follows tests.

- Tests are **specifications** that happen to be executable
- Write tests to clarify thinking, not just verify correctness
- Test output is CRITICAL information - never ignore it
- Pristine test output is non-negotiable

## Python Testing Stack

### Required Tools

- **pytest**: Test framework (`uv add --dev pytest`)
- **pytest-cov**: Coverage reporting (`uv add --dev pytest-cov`)
- **pytest-xdist**: Parallel test execution (`uv add --dev pytest-xdist`)

### Optional but Recommended

- **hypothesis**: Property-based testing (`uv add --dev hypothesis`)
- **pytest-timeout**: Prevent hanging tests (`uv add --dev pytest-timeout`)

## Test Organization

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── __init__.py
│   ├── test_module.py           # Unit tests
│   ├── integration/
│   │   └── test_workflow.py     # Integration tests
│   └── e2e/
│       └── test_user_flow.py    # End-to-end tests
├── pyproject.toml
└── pytest.ini
```

## pytest Configuration

**pytest.ini**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (moderate speed, real dependencies)
    e2e: End-to-end tests (slow, full stack)
```

## Running Tests

### Basic execution
```bash
uv run pytest                    # Run all tests
uv run pytest tests/test_module.py    # Run specific file
uv run pytest -k "test_name"     # Run tests matching pattern
```

### With markers
```bash
uv run pytest -m unit            # Run only unit tests
uv run pytest -m "not e2e"       # Skip slow e2e tests
```

### With coverage
```bash
uv run pytest --cov=src --cov-report=html
```

### Parallel execution
```bash
uv run pytest -n auto            # Use all CPU cores
```

## Test Naming Conventions

### Test Files
- `test_*.py` - Test file for corresponding module
- Location: `tests/test_module.py` for `src/mypackage/module.py`

### Test Functions
- `test_function_name_behavior()` - Descriptive name
- Good: `test_calculate_total_returns_zero_for_empty_cart()`
- Bad: `test_1()`, `test_calc()`

### Test Classes (optional, for grouping)
- `TestClassName` - Group related tests
- Good: `TestOrderProcessor`, `TestUserAuthentication`

## Assertion Best Practices

### Use specific assertions
```python
# Good
assert result == 42
assert "error" in response.text
assert len(items) == 3

# Avoid
assert result  # Vague - what are we checking?
```

### Test exceptions explicitly
```python
# Good
with pytest.raises(ValueError, match="Invalid input"):
    function_with_bad_input()

# Avoid
try:
    function_with_bad_input()
    assert False, "Should have raised"
except ValueError:
    pass  # Swallows details
```

### Use pytest helpers
```python
# Floating point comparison
assert result == pytest.approx(3.14159, rel=1e-5)

# Multiple assertions with detailed output
def test_user_creation():
    user = create_user("alice", "alice@example.com")

    assert user.name == "alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None
    # If any fail, pytest shows which specific assertion failed
```

## Fixture Usage

Fixtures provide reusable test setup:

```python
import pytest


@pytest.fixture
def sample_database():
    """Provide in-memory database for tests."""
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()


@pytest.fixture
def sample_user(sample_database):
    """Provide test user in database."""
    user = sample_database.create_user("test@example.com")
    return user


def test_user_can_create_order(sample_user, sample_database):
    """Verify user can successfully create an order."""
    order = sample_database.create_order(sample_user.id, items=[])

    assert order.user_id == sample_user.id
    assert order.status == "pending"
```

## No Mocks Policy

**Principle**: Tests should use real implementations, not mocks.

### Instead of mocks, use:

1. **In-memory databases** (SQLite `:memory:`)
2. **Test servers** (temporary HTTP servers)
3. **Filesystem fixtures** (temporary directories)
4. **Real objects with test configuration**

### Example: Testing with real database

```python
# Good: Real database, fast execution
@pytest.fixture
def test_db():
    db = Database(":memory:")  # SQLite in-memory
    db.create_tables()
    yield db


def test_order_creation(test_db):
    order = test_db.create_order(user_id=1, items=[])
    assert test_db.get_order(order.id) is not None
```

```python
# Avoid: Mock database
@pytest.fixture
def mock_db():
    db = Mock(spec=Database)
    db.create_order.return_value = Mock(id=1)
    return db

# This doesn't test real database behavior!
```

### When external APIs are necessary

Use test instances or sandboxes:
- Test API keys for real services
- Sandbox environments (Stripe test mode, etc.)
- Local service containers (Docker)

## Test Categories

### Unit Tests
- Test single function/class in isolation
- Fast execution (< 100ms per test)
- No external dependencies
- Mark with `@pytest.mark.unit`

### Integration Tests
- Test interactions between components
- Moderate speed (< 1s per test)
- Use real dependencies (databases, file system)
- Mark with `@pytest.mark.integration`

### End-to-End Tests
- Test complete user workflows
- Slower execution (seconds per test)
- Exercise full application stack
- Mark with `@pytest.mark.e2e`

## Debugging Test Failures

When tests fail:

1. **Read the output carefully** - pytest provides detailed information
2. **Use `-v` for verbose output** to see exactly what failed
3. **Use `--tb=long`** for full tracebacks
4. **Use `pytest --pdb`** to drop into debugger on failure
5. **Check fixtures** - ensure test setup is correct
6. **Verify assumptions** - what did you expect vs what happened?

## Common Patterns

### Parameterized tests
```python
@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (5, 120),
])
def test_factorial(input, expected):
    """Verify factorial calculation for various inputs."""
    assert factorial(input) == expected
```

### Testing async code
```python
import pytest


@pytest.mark.asyncio
async def test_async_function():
    """Verify async function behavior."""
    result = await async_function()
    assert result is not None
```

### Temporary files
```python
def test_file_processing(tmp_path):
    """Verify file processing with temporary file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    result = process_file(test_file)

    assert result.success is True
```

## Continuous Integration

Tests should run automatically on every commit:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4  # Optional: upload coverage
```

## Test Coverage Goals

- **Minimum**: 80% line coverage
- **Target**: 90%+ line coverage
- **Focus**: High coverage of critical paths

Check coverage:
```bash
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Anti-Patterns to Avoid

❌ **Skipping tests without justification**
```python
@pytest.mark.skip  # Why? Document reason!
def test_something():
    pass
```

❌ **Ignoring test output warnings**
```
tests/test_module.py::test_function
  /path/to/code.py:42: DeprecationWarning: ...
-- Docs: https://docs.pytest.org/
```

❌ **Tests that don't test anything**
```python
def test_function():
    function()  # No assertions!
```

❌ **Tests dependent on execution order**
```python
# Bad: test_b depends on test_a running first
def test_a():
    global state
    state = "ready"

def test_b():
    assert state == "ready"  # Fragile!
```

❌ **Overly complex test setup**
```python
# If setup is this complex, consider breaking into smaller tests
def test_complex_scenario():
    # 50 lines of setup...
    # What are we actually testing?
    assert result == expected
```

## Summary

**Remember**:
1. Tests define behavior - write them first
2. Use real implementations, not mocks
3. Test output is critical - read it carefully
4. Pristine output is required
5. Comprehensive coverage is non-negotiable

For questions or exceptions, STOP and get explicit authorization from the user.
