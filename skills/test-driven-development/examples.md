# TDD Examples

Concrete examples of TDD workflow.

## Example 1: Adding a new function

**Task**: Implement `calculate_total(items: list[dict]) -> float` that sums item prices.

### Step 1: Write failing test

```python
"""Test suite for shopping cart calculations."""

import pytest
from shopping_cart import calculate_total


def test_calculate_total_with_multiple_items():
    """
    Verify calculate_total correctly sums prices of multiple items.
    """
    items = [
        {"name": "apple", "price": 1.50},
        {"name": "banana", "price": 0.75},
        {"name": "orange", "price": 2.00},
    ]

    result = calculate_total(items)

    assert result == 4.25


def test_calculate_total_with_empty_list():
    """
    Verify calculate_total returns 0 for empty item list.
    """
    items = []

    result = calculate_total(items)

    assert result == 0.0


def test_calculate_total_with_single_item():
    """
    Verify calculate_total works with a single item.
    """
    items = [{"name": "apple", "price": 1.50}]

    result = calculate_total(items)

    assert result == 1.50
```

### Step 2: Run test (expect failure)

```bash
uv run pytest tests/test_shopping_cart.py -v
```

**Expected output**: `ImportError` or `AttributeError` (function doesn't exist yet)

### Step 3: Write minimal implementation

```python
"""Shopping cart calculations."""


def calculate_total(items: list[dict]) -> float:
    """
    Calculate total price of items in shopping cart.

    Args:
        items: List of item dictionaries with 'price' key

    Returns:
        Total price as float
    """
    return sum(item["price"] for item in items)
```

### Step 4: Run test (expect success)

```bash
uv run pytest tests/test_shopping_cart.py -v
```

**Expected output**: All tests pass with pristine output

### Step 5: Refactor if needed

Tests are green, implementation is simple and readable. No refactoring needed.

---

## Example 2: Bug fix workflow

**Bug report**: `calculate_discount()` crashes when discount percentage is None

### Step 1: Write test reproducing the bug

```python
def test_calculate_discount_handles_none_percentage():
    """
    Verify calculate_discount gracefully handles None percentage.

    Regression test for bug where None percentage caused crash.
    """
    price = 100.0
    discount_percentage = None

    result = calculate_discount(price, discount_percentage)

    assert result == 100.0  # No discount applied
```

### Step 2: Run test (expect failure confirming bug)

```bash
uv run pytest tests/test_shopping_cart.py::test_calculate_discount_handles_none_percentage -v
```

**Expected output**: `TypeError: unsupported operand type(s)` or similar

### Step 3: Fix root cause

```python
def calculate_discount(price: float, discount_percentage: float | None) -> float:
    """
    Calculate discounted price.

    Args:
        price: Original price
        discount_percentage: Discount as percentage (0-100), or None

    Returns:
        Price after discount
    """
    if discount_percentage is None:
        return price

    return price * (1 - discount_percentage / 100)
```

### Step 4: Run test (expect success)

```bash
uv run pytest tests/test_shopping_cart.py -v
```

**Expected output**: All tests pass including the new regression test

---

## Example 3: Integration test

**Task**: Test that order processing correctly updates inventory

```python
"""Integration tests for order processing."""

import pytest
from database import Database
from order_processor import OrderProcessor


def test_order_processing_updates_inventory():
    """
    Verify order processing correctly decrements inventory quantities.

    Integration test using real database (not mocks).
    """
    # Setup: Create test database with real data
    db = Database(":memory:")  # SQLite in-memory database
    db.create_tables()
    db.add_product("apple", quantity=10, price=1.50)

    processor = OrderProcessor(db)

    # Execute: Process order
    order = {"product": "apple", "quantity": 3}
    result = processor.process_order(order)

    # Verify: Check inventory was updated
    assert result.success is True
    assert db.get_product_quantity("apple") == 7

    # Cleanup: Database automatically disposed (in-memory)
```

**Key points**:
- Uses real SQLite database (in-memory for speed)
- No mocks - tests actual database interactions
- Tests cross-component behavior
