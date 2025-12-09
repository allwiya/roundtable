# Tests

Comprehensive test suite for Roundtable AI MCP Server.

## Structure

```
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests for full workflows
├── fixtures/          # Shared test fixtures and data
├── conftest.py        # Pytest configuration and fixtures
└── README.md          # This file
```

## Running Tests

### All tests
```bash
pytest
```

### Unit tests only
```bash
pytest -m unit
```

### Integration tests only
```bash
pytest -m integration
```

### With coverage
```bash
pytest --cov --cov-report=html
```

### Specific test file
```bash
pytest tests/unit/test_server_config.py
```

### Verbose output
```bash
pytest -v
```

## Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.requires_cli` - Tests requiring CLI tools

## Writing Tests

### Unit Test Example
```python
import pytest

@pytest.mark.unit
def test_something():
    assert True
```

### Async Test Example
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### Using Fixtures
```python
def test_with_fixture(mock_context, temp_project_dir):
    # Use fixtures
    assert temp_project_dir.exists()
```

## Coverage

Coverage reports are generated in:
- Terminal: Summary after test run
- HTML: `htmlcov/index.html`
- XML: `coverage.xml` (for CI/CD)

Target coverage: 80%+

## CI/CD Integration

Tests run automatically on:
- Push to any branch
- Pull requests
- Pre-commit hooks (optional)
