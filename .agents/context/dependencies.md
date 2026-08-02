# Dependencies

Sagittarius Engine intentionally limits dependencies to remain a lightweight "Kernel".

## Core Dependencies (`requirements.txt`)
- **`pydantic`**: Used for data validation, configuration parsing, and Data Transfer Objects (DTOs).
- **`websockets`**: Used for the Engine telemetry streaming (AuditExtension).
- *(Note: `PySide6` is NOT a core dependency, it is strictly used in downstream tool apps like `audit_dashboard`)*.

## Development & Test Dependencies (`requirements-dev.txt`)
- **`pytest` & `pytest-cov`**: For unit and integration testing.
- **`pytest-asyncio`**: For testing async tasks in the runtime.
- **`mypy`**: Static type checking.
- **`ruff`**: Extremely fast Python linter and formatter.
- **`bandit`**: Security vulnerability scanner.
- **`pip-audit`**: Dependency vulnerability scanner.
- **`build` & `twine`**: Packaging and distribution.
