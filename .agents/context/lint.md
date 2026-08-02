# Code Quality (Linting & Formatting)

Sagittarius enforces extremely strict code quality and type safety rules to ensure Kernel reliability.

## Tools
* **Linter & Formatter**: `ruff`
* **Type Checker**: `mypy`

## Ruff Configuration
- Managed in `pyproject.toml` (under `[tool.ruff]`).
- Automatically checks for unused imports, module-level import position (E402), PEP8 naming, and complex logic.
- Run `ruff check .` to lint and `ruff format .` to format.

## Mypy (Strong Typing)
- **Rule**: Every function signature, argument, and return type MUST be explicitly typed.
- **Rule**: Do NOT use `Any` unless absolutely necessary (e.g. dynamic reflection). Use `Optional`, `Union`, `TypeVar`, or `Generics`.
- Run `mypy sagittarius_engine tests --ignore-missing-imports --follow-imports=skip`.

## Python Best Practices
- **Data Structures**: Use `dataclasses` (with `frozen=True` preferred) or `Pydantic` models instead of raw dictionaries.
- **Side Effects**: Avoid mutable default arguments (`def f(items=[]):`).
- **Dependencies**: Never hard-code class instantiation in domain logic. Always use Dependency Injection abstractions.
