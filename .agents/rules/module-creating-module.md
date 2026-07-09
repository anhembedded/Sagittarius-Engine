---
trigger: always_on
description: Generate or refactor a module following strict Clean Architecture rules.
---

# Sagittarius Framework – Knowledge Base for AI Agent

## 1. Overview

Sagittarius is a lightweight Python application framework adhering to **Clean Architecture**, using only Python standard library (except for some optional dependencies like `pydantic`, `sqlalchemy`, `boto3`, etc.). The framework provides core components out of the box: DI Container, EventBus (synchronous, thread-pool, asyncio), Middleware Pipeline, Module System (auto‑discovery), Config, Logging, BaseEvent, Testing Helpers, and many extension modules.

**Philosophy:**
- Program to interfaces (contracts), not implementations.
- Dependency Rule: Domain → Application → Infrastructure → Presentation.
- Everything is a module that can be enabled/disabled flexibly.
- No mandatory async/await – supports both synchronous and asynchronous flows.

## 2. Framework directory structure

```
Sagittarius_ForkBoy/
├── src/                     # Framework source code
│   ├── interfaces/          # Core interfaces (ports)
│   │   ├── i_command.py
│   │   ├── i_query.py
│   │   ├── i_module.py
│   │   ├── i_event_bus.py
│   │   ├── i_async_event_bus.py
│   │   ├── i_container.py
│   │   ├── i_middleware.py
│   │   ├── i_logger.py
│   │   ├── i_config.py
│   │   ├── i_file_storage.py
│   │   ├── i_metrics.py
│   │   └── __init__.py      # Exports all interfaces
│   ├── app_kernel.py        # App, MiddlewarePipeline, ModuleAutoDiscovery
│   ├── base_module.py       # BaseModule (convenience class)
│   ├── base_event.py        # BaseEvent (event metadata)
│   ├── base_repository.py   # BaseRepository (generic CRUD)
│   ├── exceptions.py        # DependencyResolutionError, ModuleRegistrationError
│   ├── scaffold.py          # New project generator
│   ├── infra/               # Infrastructure implementations
│   │   ├── std_container.py
│   │   ├── memory_event_bus.py
│   │   ├── thread_pool_event_bus.py
│   │   ├── asyncio_event_bus.py
│   │   ├── resilient_event_bus.py
│   │   ├── std_logger.py
│   │   ├── config_manager.py
│   │   ├── dict_config.py
│   │   ├── local_file_storage.py
│   │   ├── s3_file_storage.py
│   │   ├── azure_blob_storage.py
│   │   └── log_metrics.py
│   ├── middleware/           # Sample middleware
│   │   ├── logging_middleware.py
│   │   ├── timing_middleware.py
│   │   ├── validation_middleware.py
│   │   └── pydantic_validation_middleware.py
│   └── modules/              # Built-in modules
│       ├── logger_module.py
│       ├── database_module.py
│       └── health_module.py
├── tests/                    # Framework tests
├── example/                  # Sample applications
└── docs/                     # Documentation
```

## 3. Core concepts

### 3.1 Interfaces (Ports)
All interfaces reside in `src/interfaces/`. When writing app code, you should only depend on these interfaces, never import a concrete implementation directly.

```python
from src.interfaces import ICommand, IEventBus, IContainer, ...
```

### 3.2 App Kernel
`App` is the central orchestrator. It receives `IContainer` and `IEventBus` through its constructor (Composition Root).

```python
from sagittarius_engine.infrastructure.std_container import StdLibContainer
from sagittarius_engine.infrastructure.memory_event_bus import MemoryEventBus
from src.app_kernel import App

container = StdLibContainer()
event_bus = MemoryEventBus()
app = App(container, event_bus)
container.singleton(IContainer, container)
container.singleton(IEventBus, event_bus)
```

Key methods:
- `use(module)`: registers a module.
- `boot(auto_discover="sagittarius_engine.extensions")`: boots the app, auto-discovers if a package name is provided.
- `execute(CommandClass, data_transfer_obj)`, `query(QueryClass, data_transfer_obj)`: runs a use case through the middleware pipeline.

### 3.3 Container (Dependency Injection)
`StdLibContainer` (implements `IContainer`) automatically resolves constructor dependencies based on type hints.

- `bind(interface, concrete)`: registers a transient binding (new instance each resolution).
- `singleton(interface, instance_or_factory)`: registers a singleton.
- `resolve(SomeClass)`: returns an instance, injecting dependencies automatically.

**Note:** The container will not resolve abstract classes unless they have been bound or registered as a singleton.

### 3.4 EventBus
There are four types, all implementing `IEventBus`:

- **MemoryEventBus**: synchronous, thread‑safe, runs handlers on the calling thread.
- **ThreadPoolEventBus**: uses `ThreadPoolExecutor` to run handlers concurrently.
- **AsyncioEventBus**: runs on the asyncio event loop, supports both async and sync handlers.
- **ResilientEventBus**: decorator around another bus, adding retry + dead letter queue.

**Usage:**
```python
event_bus.on("user.created", lambda event: print(event.user.name))
event_bus.emit("user.created", UserCreated(user))
```

### 3.5 Middleware Pipeline
`MiddlewarePipeline` manages a chain of `IMiddleware`. When `app.execute(...)` is called, the request passes through all middleware before reaching the final handler.

Sample middleware: `LoggingMiddleware`, `TimingMiddleware`, `ValidationMiddleware`, `PydanticValidationMiddleware`.

### 3.6 Module System & Auto‑Discovery
Each module implements `IModule` (or extends `BaseModule`). A module has two methods:
- `register(app)`: binds classes into the container.
- `boot(app)`: registers event handlers, initializes resources.

Place modules in the app’s `modules/` directory and call `app.boot(auto_discover="sagittarius_engine.extensions")` to load them automatically.

Modules can be a single file (`modules/my_module.py`) or a package (`modules/my_module/__init__.py`).

### 3.7 Configuration
`IConfig` provides `get(key, default)` and `set(key, value)`. Implementations: `DictConfig`, `ConfigManager` (supports multiple sources: Dict, Env, JSON, Dotenv). Later sources override earlier ones.

### 3.8 Logging
`ILogger` with `info`, `warning`, `error`, `debug`. `StdLogger` uses the standard `logging` module, reads configuration from `IConfig` (level, file). `LoggerModule` automatically registers `ILogger` in the container.

### 3.9 BaseEvent
`BaseEvent` class provides `event_id` (UUID) and `occurred_on` (UTC). Inheritance is optional but recommended for metadata.

### 3.10 Testing Helpers
`tests/conftest.py` provides `container`, `event_bus`, `app` fixtures. `tests/helpers.py` contains `AppTestCase` and `assert_event_emitted`. When writing tests, only test through the public API (black‑box); do not test implementation details.

### 3.11 Extension modules
- `DatabaseModule`: connects SQLAlchemy, reads `database.url` from config, provides `ISession` singleton.
- `HealthModule`: registers `HealthCheckQuery` that checks container, event bus, database status.
- `PydanticValidationMiddleware`: validates DTO using a Pydantic model.
- `FileStorage`: interface `IFileStorage`, adapters `LocalFileStorage`, `S3FileStorage`, `AzureBlobStorage`.
- `Metrics`: interface `IMetrics`, implementation `LogMetrics`.

## 4. How to build an application with the framework

### 4.1 Create a new project
```bash
python sagittarius_engine/tools/scaffold.py my_app
cd my_app
```
Generated structure:
```
my_app/
├── domain/          # Entities, Domain Events, Domain Services
├── application/     # Commands, Queries, Contracts (interfaces)
├── infrastructure/  # Repositories, External services
├── adapters/        # CLI, Web, Batch
├── modules/         # Packaged modules (auto‑discover)
├── config.json
└── main.py
```

### 4.2 Write the Domain
```python
# domain/user.py
class User:
    def __init__(self, user_id: int, name: str):
        self.id = user_id
        self.name = name

# domain/events.py
from src.base_event import BaseEvent

class UserCreated(BaseEvent):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
```

### 4.3 Define a Port (Repository Interface)
```python
# application/contracts/user_repo.py
from abc import ABC, abstractmethod
from my_app.domain.user import User

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...
    @abstractmethod
    def get_all(self) -> list[User]: ...
```

### 4.4 Write Use Cases (Command/Query)
```python
# application/commands/create_user.py
from src.interfaces import ICommand, IEventBus
from my_app.application.contracts.user_repo import IUserRepository
from my_app.domain.user import User
from my_app.domain.events import UserCreated

class CreateUserCommand(ICommand):
    def __init__(self, repo: IUserRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus

    def execute(self, data_transfer_obj: dict) -> User:
        user = User(user_id=data_transfer_obj['id'], name=data_transfer_obj['name'])
        self.repo.add(user)
        self.event_bus.emit('user.created', UserCreated(user))
        return user
```

### 4.5 Implement Infrastructure (Repository)
```python
# infrastructure/memory_user_repo.py
from my_app.application.contracts.user_repo import IUserRepository
from my_app.domain.user import User

class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users = []
    def add(self, user: User): self._users.append(user)
    def get_all(self): return self._users
```

### 4.6 Package into a Module
```python
# modules/user_module/__init__.py
from src.base_module import BaseModule
from src.app_kernel import App
from my_app.application.contracts.user_repo import IUserRepository
from my_app.infrastructure.memory_user_repo import InMemoryUserRepository
from my_app.application.commands.create_user import CreateUserCommand

class UserModule(BaseModule):
    def register(self, app: App):
        app.container.singleton(IUserRepository, InMemoryUserRepository())
        app.container.bind(CreateUserCommand, CreateUserCommand)

    def boot(self, app: App):
        app.event_bus.on('user.created', lambda event: print(f"New user: {event.user.name}"))
```

### 4.7 Composition Root (main.py)
```python
from sagittarius_engine.infrastructure.std_container import StdLibContainer
from sagittarius_engine.infrastructure.memory_event_bus import MemoryEventBus
from src.app_kernel import App
from src.interfaces import IContainer, IEventBus
from sagittarius_engine.extensions.logger_module import LoggerModule

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    app.use(LoggerModule())  # optional

    app.boot(auto_discover="sagittarius_engine.extensions")

    # CLI or other startup logic
    # e.g.:
    # from my_app.adapters.cli import UserCLI
    # UserCLI(app).run()

if __name__ == "__main__":
    main()
```

### 4.8 Run the application
```bash
PYTHONPATH=. python main.py
```

## 5. Important development rules

- **Never import infrastructure from application/domain** – only import interfaces.
- **Always program to interfaces**, never depend on concrete classes.
- **Use type hints** so the container can resolve automatically.
- **Event handlers must be registered in `boot()`, not `register()`**.
- **Do not test implementation details** – only test the public API.
- **Optional dependencies**: always wrap external library imports in try/except and provide a fallback.
- **Use `IConfig` for all configuration**, avoid hardcoding.
- **Use `BaseEvent` for domain events** to include metadata.

## 6. Quick examples of common tasks

### Attach middleware
```python
from sagittarius_engine.middleware.logging_middleware import LoggingMiddleware
app.use_middleware(LoggingMiddleware(container))
```

### Use ResilientEventBus instead of MemoryEventBus
```python
from sagittarius_engine.infrastructure.resilient_event_bus import ResilientEventBus
event_bus = ResilientEventBus(MemoryEventBus(), max_retries=3)
```

### Validate a DTO with Pydantic
```python
from pydantic import BaseModel
from sagittarius_engine.middleware.pydantic_validation_middleware import PydanticValidationMiddleware

class CreateUserDTO(BaseModel):
    name: str
    age: int

app.use_middleware(PydanticValidationMiddleware(CreateUserDTO))
```

### Check application health
```python
from sagittarius_engine.extensions.health_module import HealthCheckQuery
health = app.query(HealthCheckQuery)
print(health)
```

### Create an event inheriting from BaseEvent
```python
from src.base_event import BaseEvent

class OrderPlaced(BaseEvent):
    def __init__(self, order):
        super().__init__()
        self.order = order
```

## 7. Testing Notes

When writing tests for an app using the framework, you can use the fixtures from the framework’s `tests/conftest.py` (if importable) or create your own container, event bus, app in your own fixtures. Always test through `App.execute`, `App.query`, `EventBus.emit/on`; do not invoke internal functions directly.

```python
def test_create_user(app):
    from my_app.application.commands.create_user import CreateUserCommand
    user = app.execute(CreateUserCommand, {'id': 1, 'name': 'Alice'})
    assert user.name == 'Alice'
```

---

**Framework version:** 1.0.0 (2026-06-25)
