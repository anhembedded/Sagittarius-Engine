# Task: Implement `BackgroundService` Pattern for Hosted Services

## 🎯 Goal
Simplify long-running `IHostedService` implementations (such as `TerminalMenu`, background queue workers, and polling services) by introducing an abstract `BackgroundService` class in `sagittarius_engine.runtime`.

---

## 🏛️ Background & Motivation
Currently, any `IHostedService` that needs to run a background loop (e.g., `TerminalMenu`) must manually:
1. Instantiate its own `CancellationToken`.
2. Call `context.tasks.spawn(...)` inside `start()`.
3. Manage its own `self.task` handle and `wait_for_exit()`.
4. Manually cancel the token inside `stop()`.

This causes boilerplate duplication across every long-running service and violates the Single Responsibility Principle.

---

## 📐 Proposed Design

### 1. Abstract `BackgroundService` Class
Path: `sagittarius_engine/runtime/hosted/background_service.py`

```python
from abc import abstractmethod
from typing import Any
from sagittarius_engine.interfaces import IEngineContext
from sagittarius_engine.runtime.hosted.hosted_service import IHostedService
from sagittarius_engine.runtime.tasks.cancellation_token import CancellationToken


class BackgroundService(IHostedService):
    """
    @brief Base class for long-running background Hosted Services.
    @details Handles thread spawning, cancellation token lifecycle, and safe shutdown automatically.
    """

    def __init__(self) -> None:
        self.token = CancellationToken()
        self._task: Any = None

    def start(self, context: IEngineContext) -> None:
        self._task = context.tasks.spawn(
            self._run_wrapper, name=self.__class__.__name__, token=self.token
        )

    def _run_wrapper(self, token: CancellationToken) -> None:
        self.run(token)

    @abstractmethod
    def run(self, token: CancellationToken) -> None:
        """
        @brief Subclasses override this method to write their execution loop.
        """
        pass

    def stop(self, context: IEngineContext) -> None:
        self.token.cancel()
```

### 2. Export in `sagittarius_engine/runtime/hosted/__init__.py` & `sagittarius_engine/runtime/__init__.py`

```python
from .background_service import BackgroundService
```

### 3. Refactor `TerminalMenu` Example
Path: `examples/student_management/presentation/cli/terminal_menu.py`

```python
class TerminalMenu(BackgroundService):
    def __init__(self, app: App) -> None:
        super().__init__()
        self.app = app

    def run(self, token: CancellationToken) -> None:
        while not token.is_cancelled():
            self._print_header()
            ...
```

---

## 📋 Implementation Checklist
- [ ] Create `sagittarius_engine/runtime/hosted/background_service.py`
- [ ] Export `BackgroundService` in `sagittarius_engine/runtime/__init__.py`
- [ ] Add unit tests in `tests/test_background_service.py`
- [ ] Refactor `TerminalMenu` in `examples/student_management/presentation/cli/terminal_menu.py`
- [ ] Verify using `ruff check .`, `mypy sagittarius_engine`, and `pytest`
