# Test Suite for Introspection & Ontogenesis

This directory contains the test suite for the introspection and ontogenesis frameworks.

## Test Files

- **test_core_functionality.py** - Core functionality tests that validate the main APIs (9 tests passing)
- **test_introspection.py** - Comprehensive introspection tests (33 test cases, API alignment in progress)
- **test_ontogenesis.py** - Comprehensive ontogenesis tests (39 test cases, API alignment in progress)
- **test_operators.py** - Differential operator tests (18 test cases, API alignment in progress)
- **test_integration.py** - Integration tests (25 test cases, API alignment in progress)

## Running Tests

### Run all passing tests:
```bash
pytest tests/test_core_functionality.py -v
```

### Run with coverage:
```bash
pytest tests/test_core_functionality.py --cov=introspection --cov=ontogenesis --cov-report=html
```

### Run specific test class:
```bash
pytest tests/test_core_functionality.py::TestIntrospectionCore -v
```

### Run specific test:
```bash
pytest tests/test_core_functionality.py::TestIntrospectionCore::test_copilot_initialization -v
```

## Test Status

### ✅ Passing Tests (9/115)
- Copilot initialization
- Basic introspection
- Recursive introspection
- Self-optimization
- Ontogenetic state tracking
- Domain-specific kernel creation
- Example reproduction tests

### 🔄 In Progress (106/115)
- API signature mismatches being resolved
- Additional test cases being aligned with actual implementation

## Continuous Integration

Tests run automatically on:
- Every push to main, develop, or copilot/** branches
- Every pull request
- Manual workflow dispatch

See `.github/workflows/test-introspection-ontogenesis.yml` for CI configuration.

## Test Coverage Goal

Target: 70%+ code coverage for introspection and ontogenesis modules.

## Adding New Tests

1. Create tests that match the actual API (see `test_core_functionality.py` for examples)
2. Use descriptive test names: `test_<what_is_being_tested>`
3. Include docstrings explaining what the test validates
4. Mark slow tests with `@pytest.mark.slow` decorator
5. Mark integration tests with `@pytest.mark.integration` decorator

## Example Tests

All examples in `examples/` directory serve as functional tests:
- `examples/introspection/basic_introspection.py`
- `examples/ontogenesis/self_generation.py`
- `examples/ontogenesis/evolution_example.py`

These run successfully and validate the frameworks work as designed.

## Dependencies

```bash
pip install pytest pytest-cov numpy
```

Or install all development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Future Work

- [ ] Complete API alignment for all 115 test cases
- [ ] Increase code coverage to 70%+
- [ ] Add performance benchmarks
- [ ] Add property-based testing with Hypothesis
- [ ] Add mutation testing with mutmut
