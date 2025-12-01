---
name: workbench:test-driven-development
description: Enforce strict TDD workflow for all development tasks. Use when implementing new features, fixing bugs, or refactoring code. Ensures comprehensive test coverage (unit, integration, e2e) before writing implementation code. Activates automatically for all coding tasks unless explicitly authorized to skip testing.
when_to_use: When implementing new features. When fixing bugs. When refactoring code. For ALL coding tasks unless explicitly authorized to skip. Always write tests before implementation code.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Test-Driven Development

Enforce strict TDD workflow with comprehensive test coverage.

**Announce at start:** "I'm using the test-driven-development skill to ensure test-first implementation."

## Core TDD Cycle

For EVERY feature, bug fix, or refactoring task:

1. **Write failing test** defining desired functionality
2. **Run test** to confirm it fails as expected
3. **Write ONLY enough code** to make test pass
4. **Run test** to confirm success
5. **Refactor** while ensuring tests remain green
6. **Repeat** for next requirement

## Test Requirements

ALL projects require:
- **Unit tests**: Test individual functions/classes in isolation
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete user workflows

## Python Test Standards

- Use `pytest` as test framework
- Use `uv run pytest` to execute tests
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*`
- 4-space indentation, 80-char line length
- Type annotations for test parameters
- **NEVER use mocks** - always use real data and APIs

## Test Quality Standards

- Test output MUST BE PRISTINE to pass
- NEVER ignore test output - it contains CRITICAL information
- Expected errors MUST be captured and tested explicitly
- Tests MUST comprehensively cover ALL functionality
- Add docstrings explaining what each test verifies

## Authorization Check

The ONLY way to skip tests is explicit authorization:

> "I AUTHORIZE YOU TO SKIP WRITING TESTS THIS TIME."

If this phrase is not present, tests are MANDATORY.

## Workflow

1. **Before starting**: Check if tests are required (default: YES)
2. **During development**: Write tests BEFORE implementation
3. **After changes**: Run full test suite to verify no regressions
4. **Before committing**: Ensure all tests pass with pristine output

## See Also

- [examples.md](./examples.md) - Concrete TDD workflow examples
- [templates/pytest-test.py](./templates/pytest-test.py) - Test template
- [templates/test-checklist.md](./templates/test-checklist.md) - TDD checklist
- [reference.md](./reference.md) - Detailed testing guidance
