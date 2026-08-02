# Testing Guide

## Testing Framework & Coverage
* **Test Framework**: `pytest`
* **Test Commands**: `pytest tests/ --cov=sagittarius_engine --cov-report=term-missing`
* **Coverage Requirement**: Strict `80%` minimum branch/line coverage for CI pipelines (`--cov-fail-under=80`).

## Testing Categories

* **Unit Tests**: Fast, in-memory, zero external dependencies. Located in `tests/runtime/`, `tests/infrastructure/`, etc. Use `unittest.mock.MagicMock` to isolate system calls.
* **Integration Tests**: Tests interaction between multiple components (e.g., Container + EventBus + TaskManager). Example: `tests/extensions/test_audit_integration.py` which verifies telemetry events are propagated properly.
* **Architecture Tests**: `tests/test_architecture.py` enforces Clean Architecture bounds (e.g., Domain layer must not import from Infrastructure).

## Best Practices

* **Container Testing**: When testing services, construct a real `StdLibContainer` rather than manually injecting everything if testing component wiring.
* **EventBus Verification**: Use `MemoryEventBus` and bind listeners (`bus.on(...)`) to assert events are emitted during test flows.
* **Async Testing**: Use `pytest.mark.asyncio` when testing `AsyncRuntime` or background task logic.
* **Fixtures**: Keep fixtures in `conftest.py` if shared across multiple test files.
