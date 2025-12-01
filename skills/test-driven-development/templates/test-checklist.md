# TDD Checklist

Use this checklist for each development task to ensure TDD compliance.

## Before Starting

- [ ] Confirmed tests are required (or have explicit authorization to skip)
- [ ] Identified test categories needed (unit / integration / e2e)
- [ ] Test file location determined (`tests/test_*.py`)

## During Development

- [ ] Written failing test defining desired functionality
- [ ] Run test - confirmed it fails as expected (RED)
- [ ] Written minimal implementation code
- [ ] Run test - confirmed it passes (GREEN)
- [ ] Refactored code while keeping tests green (REFACTOR)
- [ ] Added test for edge cases
- [ ] Added test for error conditions
- [ ] Verified test output is pristine (no warnings, no noise)

## Integration/E2E Tests

- [ ] Identified components that interact
- [ ] Written integration tests using real dependencies (no mocks)
- [ ] Written e2e tests covering complete user workflows
- [ ] Verified tests use real data and APIs

## Before Committing

- [ ] Run full test suite: `uv run pytest`
- [ ] All tests pass with pristine output
- [ ] Test coverage is comprehensive
- [ ] No test output ignored or dismissed
- [ ] Type annotations present in test code

## Test Quality Verification

- [ ] Each test has clear docstring explaining what it verifies
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Test names clearly describe what is being tested
- [ ] Expected errors are explicitly captured with `pytest.raises`
- [ ] No commented-out test code
- [ ] No skipped tests without documented reason
