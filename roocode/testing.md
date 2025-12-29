# Testing Guide for Agentic Development

**Last Updated:** 2025-12-29
**Purpose:** Define testing philosophy and practices for AI agents writing code

---

## Philosophy

### Tests as Executable Documentation

Tests should tell the story of what your code does:

```python
def test_layering_pattern_detection_identifies_three_hop_chain():
    """
    Given: A sequence of transfers A -> B -> C -> D within 1 hour
    When: Analyzing for layering patterns with min_layers=3
    Then: Should detect one layering pattern with path A -> B -> C -> D
    """
    transfers = create_transfer_chain(
        addresses=["A", "B", "C", "D"],
        time_spacing_minutes=10,
        amount=1000
    )
    
    patterns = detect_layering_pattern(transfers, min_layers=3)
    
    assert len(patterns) == 1
    assert patterns[0].path == ["A", "B", "C", "D"]
    assert patterns[0].confidence > 0.8
```

---

## When to Write Tests

### ✓ ALWAYS Test

**1. Bug Fixes (Regression Tests)**
```python
def test_transfer_amount_precision_preserved():
    """
    Regression test for bug #123: decimal precision lost in transfers.
    
    Previously: Amount 1.123456789 was truncated to 1.12
    Now: Full precision is preserved
    """
    transfer = Transfer(amount="1.123456789")
    stored = repository.save(transfer)
    retrieved = repository.get(stored.id)
    
    assert str(retrieved.amount) == "1.123456789"
```

**2. Integration Points**
```python
def test_clickhouse_stores_and_retrieves_transfers():
    """Integration test: ClickHouse repository"""
    transfer = create_sample_transfer()
    
    repository.insert(transfer)
    retrieved = repository.get_by_id(transfer.id)
    
    assert retrieved.from_address == transfer.from_address
    assert retrieved.to_address == transfer.to_address
    assert retrieved.amount == transfer.amount
```

**3. Critical Business Logic**
```python
def test_risk_score_calculation_for_high_velocity_transfers():
    """
    Critical: Risk scoring must correctly identify high-velocity patterns
    """
    # Create 50 transfers in 5 minutes (high velocity)
    transfers = create_high_velocity_transfers(
        count=50,
        time_window_minutes=5
    )
    
    risk_score = calculate_risk_score(transfers)
    
    assert risk_score > 0.7  # High risk threshold
    assert "high_velocity" in risk_score.factors
```

**4. Complex Algorithms**
```python
def test_cycle_detection_in_complex_graph():
    """
    Test cycle detection with multiple overlapping cycles
    """
    # Create graph with 3 cycles
    graph = create_test_graph([
        ("A", "B", "C", "A"),  # Cycle 1
        ("B", "D", "E", "B"),  # Cycle 2
        ("C", "F", "G", "C"),  # Cycle 3
    ])
    
    cycles = detect_cycles(graph)
    
    assert len(cycles) == 3
    assert set(cycles[0]) == {"A", "B", "C"}
```

### ✗ SKIP Tests

**1. Simple CRUD Operations**
```python
# ❌ Don't test simple getters
def test_transfer_get_from_address():
    transfer = Transfer(from_address="0x123")
    assert transfer.from_address == "0x123"

# ❌ Don't test basic database operations
def test_repository_insert():
    repository.insert(transfer)
    # This is testing the framework, not your code
```

**2. One-Time Scripts**
```python
# ❌ Don't test migration scripts
# scripts/migrate_legacy_data.py
def migrate_legacy_transfers():
    """One-time migration, run once and verify manually"""
    pass
```

**3. Prototypes**
```python
# ❌ Don't test exploratory code
# experiments/test_new_algorithm.py
def experimental_pattern_detection():
    """Still exploring, will test when settled"""
    pass
```

---

## Test Types

### Integration Tests (Recommended)

Test real interactions with actual dependencies:

```python
import pytest
from libs.observability import setup_logger
from libs.db import create_client

@pytest.fixture
def clickhouse_client():
    """Provide real ClickHouse client for tests"""
    logger = setup_logger("test")
    client = create_client(
        host="localhost",
        port=9000,
        database="test_db"
    )
    yield client
    client.close()


def test_transfer_repository_with_real_database(clickhouse_client):
    """Integration test with actual ClickHouse instance"""
    repository = TransferRepository(clickhouse_client)
    
    transfer = create_sample_transfer()
    repository.insert(transfer)
    
    retrieved = repository.get_by_id(transfer.id)
    assert retrieved is not None
    
    # Cleanup
    repository.delete(transfer.id)
```

### Unit Tests (When Appropriate)

Test isolated logic without external dependencies:

```python
def test_address_validation():
    """Unit test: pure function, no dependencies"""
    assert is_valid_ethereum_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb")
    assert not is_valid_ethereum_address("invalid")
    assert not is_valid_ethereum_address("")


def test_amount_formatting():
    """Unit test: pure transformation"""
    assert format_amount("1.23456789", decimals=2) == "1.23"
    assert format_amount("1000.5", decimals=0) == "1001"
```

### End-to-End Tests (Sparingly)

Test complete workflows:

```python
@pytest.mark.e2e
def test_complete_indexing_pipeline():
    """
    E2E test: Complete flow from blockchain to database
    
    This is slow and requires full infrastructure, so we mark it
    and run it separately from unit tests.
    """
    # Start indexer
    indexer = BlockIndexer(network="test-network")
    
    # Index blocks
    indexer.index_block_range(start=1, end=10)
    
    # Verify data in database
    transfers = repository.get_transfers_in_range(block_start=1, block_end=10)
    assert len(transfers) > 0
    
    # Verify labels applied
    assert all(t.labels is not None for t in transfers)
```

---

## BDD Approach

Use Given-When-Then structure:

```python
def test_burst_pattern_detection_with_volume_threshold():
    """
    Scenario: Detect burst pattern when transfer count exceeds threshold
    
    Given: A time window of 5 minutes
      And: A volume threshold of 20 transfers
      And: A sequence of 25 transfers in 5 minutes
    When: Analyzing for burst patterns
    Then: Should detect one burst pattern
      And: Burst should have 25 transfers
      And: Burst time window should be approximately 5 minutes
    """
    # Given
    time_window_minutes = 5
    threshold = 20
    transfers = create_burst_transfers(
        count=25,
        time_window_minutes=time_window_minutes
    )
    
    # When
    patterns = detect_burst_pattern(
        transfers,
        time_window_minutes=time_window_minutes,
        threshold=threshold
    )
    
    # Then
    assert len(patterns) == 1
    assert len(patterns[0].transfers) == 25
    assert patterns[0].duration_minutes <= time_window_minutes + 1
```

---

## Agentic Testing Workflow

### 1. Read Existing Tests First

Before writing new tests, understand the existing test patterns:

```bash
# Look at similar tests
ls tests/test_patterns/
cat tests/test_patterns/test_cycle_detection.py
```

### 2. Create Fixtures

Reuse test data setup:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_transfer():
    """Provide a standard test transfer"""
    return Transfer(
        id="test-123",
        from_address="0xabc",
        to_address="0xdef",
        amount="1000.0",
        timestamp="2024-01-01T00:00:00Z",
        network="ethereum"
    )


@pytest.fixture
def transfer_chain():
    """Provide a chain of connected transfers"""
    return create_transfer_chain(
        addresses=["A", "B", "C", "D"],
        amount=1000
    )
```

### 3. Write Descriptive Test Names

Test names should describe the scenario:

```python
# ❌ Bad
def test_pattern():
    pass

def test_detection():
    pass

# ✓ Good
def test_layering_pattern_not_detected_when_time_gap_exceeds_threshold():
    pass

def test_cycle_detection_ignores_single_address_self_transfer():
    pass
```

### 4. Use Assertions with Messages

Make failures informative:

```python
# ❌ Bad
assert len(patterns) == 1

# ✓ Good
assert len(patterns) == 1, \
    f"Expected 1 layering pattern, found {len(patterns)}"

# ✓ Better
expected_pattern_count = 1
actual_pattern_count = len(patterns)
assert actual_pattern_count == expected_pattern_count, \
    f"Expected {expected_pattern_count} pattern(s), found {actual_pattern_count}. " \
    f"Patterns: {[p.path for p in patterns]}"
```

---

## Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── integration/             # Integration tests
│   ├── test_clickhouse_repository.py
│   ├── test_postgres_repository.py
│   └── test_api_endpoints.py
├── unit/                    # Unit tests
│   ├── test_validators.py
│   ├── test_formatters.py
│   └── test_calculations.py
└── e2e/                     # End-to-end tests
    └── test_indexing_pipeline.py
```

### Test File Naming

- Unit tests: `test_{module_name}.py`
- Integration tests: `test_{integration_point}.py`
- E2E tests: `test_{workflow_name}.py`

---

## Anti-Patterns

### ❌ Testing Implementation Details

```python
# ❌ Bad - testing internal method
def test_internal_cache_clearing():
    detector = PatternDetector()
    detector._clear_cache()
    assert detector._cache == {}

# ✓ Good - testing behavior
def test_pattern_detection_returns_fresh_results_after_data_update():
    detector = PatternDetector()
    
    first_result = detector.detect(data_v1)
    detector.update_data(data_v2)
    second_result = detector.detect(data_v2)
    
    assert first_result != second_result
```

### ❌ Over-Mocking

```python
# ❌ Bad - mocking everything
@patch('package.module.ClickHouseClient')
@patch('package.module.Logger')
@patch('package.module.MetricsRegistry')
def test_with_too_many_mocks(mock_metrics, mock_logger, mock_client):
    # Test is fragile and doesn't test real behavior
    pass

# ✓ Good - use real objects when possible
def test_with_real_dependencies(clickhouse_client):
    # Test actual behavior with real database
    repository = TransferRepository(clickhouse_client)
    # Test realistic scenarios
```

### ❌ Unclear Test Setup

```python
# ❌ Bad - magic test data
def test_detection():
    data = [1, 2, 3, 4, 5]
    result = detect(data)
    assert result == True

# ✓ Good - clear test data
def test_cycle_detection_finds_three_node_cycle():
    # Create explicit cycle: A -> B -> C -> A
    transfers = [
        Transfer(from_addr="A", to_addr="B"),
        Transfer(from_addr="B", to_addr="C"),
        Transfer(from_addr="C", to_addr="A"),
    ]
    
    cycles = detect_cycles(transfers)
    
    assert len(cycles) == 1
    assert set(cycles[0]) == {"A", "B", "C"}
```

---

## Best Practices

### 1. Test One Thing

```python
# ❌ Bad - testing multiple things
def test_pattern_detection():
    patterns = detect_all_patterns(transfers)
    assert len(patterns) > 0
    assert patterns[0].type == "layering"
    assert patterns[0].confidence > 0.5
    assert patterns[1].type == "cycle"

# ✓ Good - focused tests
def test_layering_pattern_detection():
    patterns = detect_layering_pattern(transfers)
    assert len(patterns) == 1

def test_cycle_pattern_detection():
    patterns = detect_cycle_pattern(transfers)
    assert len(patterns) == 1
```

### 2. Make Tests Readable

```python
# ✓ Good - readable test
def test_high_risk_score_for_suspicious_pattern():
    # Arrange - Create suspicious pattern
    transfers = create_layering_pattern(
        layers=5,
        amount_per_hop=10000,
        time_between_hops_minutes=5
    )
    
    # Act - Calculate risk
    risk = calculate_risk_score(transfers)
    
    # Assert - Verify high risk
    assert risk.score > 0.8
    assert "layering" in risk.detected_patterns
```

### 3. Use Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("address,expected", [
    ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", True),
    ("0xinvalid", False),
    ("", False),
    (None, False),
])
def test_ethereum_address_validation(address, expected):
    assert is_valid_ethereum_address(address) == expected
```

---

## Running Tests

### With Docker (Recommended)

```bash
# Run all tests
docker compose -f docker-compose.dev.yml run --rm dev pytest

# Run specific test file
docker compose -f docker-compose.dev.yml run --rm dev pytest tests/test_patterns/test_cycle.py

# Run with coverage
docker compose -f docker-compose.dev.yml run --rm dev pytest --cov=src --cov-report=html

# Run integration tests only
docker compose -f docker-compose.dev.yml run --rm dev pytest tests/integration/

# Run with verbose output
docker compose -f docker-compose.dev.yml run --rm dev pytest -v -s
```

### Marks for Test Selection

```python
import pytest

@pytest.mark.unit
def test_pure_function():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

@pytest.mark.slow
def test_expensive_operation():
    pass

@pytest.mark.e2e
def test_complete_workflow():
    pass
```

```bash
# Run only unit tests
pytest -m unit

# Run everything except slow tests
pytest -m "not slow"

# Run integration and e2e
pytest -m "integration or e2e"
```

---

## Related Documentation

- [`coding-standards.md`](coding-standards.md) - Code quality standards
- [`automode.md`](automode.md) - Script execution patterns
- [`rules.md`](rules.md) - General development rules
