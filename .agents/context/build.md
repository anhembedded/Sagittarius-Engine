# Build & CI/CD Pipeline

The project uses modern Python packaging (`pyproject.toml` + `setup.py`) and standard tools.

## Development Commands

* **Install Dependencies**: 
  ```bash
  pip install -r requirements.txt
  pip install -r requirements-dev.txt
  ```
* **Install Project locally (Editable mode)**: 
  ```bash
  pip install -e .
  ```
* **Linting & Formatting (Ruff)**: 
  ```bash
  ruff check sagittarius_engine tests
  ruff format sagittarius_engine tests
  ```
* **Type Checking (Mypy)**: 
  ```bash
  mypy sagittarius_engine tests --ignore-missing-imports --follow-imports=skip
  ```
* **Run Tests & Coverage (Pytest)**: 
  ```bash
  pytest tests/ --cov=sagittarius_engine --cov-report=term-missing --cov-fail-under=80
  ```

## CI/CD Workflow (GitHub Actions)

Defined in `.github/workflows/ci.yml`. It runs automatically on PRs and merges to `main` / `develop`.

### Pipeline Jobs:
1. **Lint & Type Check**: Fails fast if Ruff or Mypy catches issues.
2. **Test Matrix**: Runs Pytest on multiple OSs (Linux, Windows) and Python versions (including 3.14-dev). Minimum 80% coverage enforced.
3. **Architecture Guard**: Runs `tests/test_architecture.py` to ensure core boundaries aren't violated.
4. **Example Integration**: Runs tests against `examples/` to ensure the framework doesn't break user-space apps.
5. **Security Audit**: Uses `bandit` (SAST scan) and `pip-audit` (Vulnerability check).
6. **Package Build Check**: Runs `python -m build` and `twine check` to validate distribution metadata.
