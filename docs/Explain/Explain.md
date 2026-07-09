Great, you've shared the complete framework codebase. This is the perfect starting point. Let's walk through learning Sagittarius step by step, using the actual files you now have.

I'll guide you from the big picture down to building your first small app. By the end, you'll understand every piece and be able to create trading bots, web apps, or any other system.

---

## 1. The Big Picture – Clean Architecture in Sagittarius

The framework enforces a clear separation of concerns. Everything flows inward:

```
Presentation (adapters)  →  Application (use cases)  →  Domain (entities)
                                 ↑
                          Infrastructure (DI, DB, FS)
```

**Key rule:** Code in inner layers never imports from outer layers. All dependencies point inward.

Your `src/` folder implements the **Application & Infrastructure** of the framework itself. Your own app will sit outside `src/`, using `src/` as a library.

---

## 2. Start with the Contracts – the Interfaces

Everything in Sagittarius is built around **interfaces** (Python ABCs). These are the "ports" you plug into. Open `src/interfaces/` and glance at these core ones:

- **`ICommand`** – for write operations.
- **`IQuery`** – for read-only operations.
- **`IModule`** – a pluggable module that registers services and event handlers.
- **`IEventBus`** – publish/subscribe events.
- **`IContainer`** – dependency injection container.
- **`IMiddleware`** – interceptors that wrap command/query execution.
- **`ILogger`**, **`IConfig`** – logging and configuration.

All of these are re‑exported from `src/interfaces/__init__.py`. You will **never** import a concrete class from `src/infra/` in your app code – only interfaces.

---

## 3. The Heart of the Framework – `App` Kernel

Open `src/app_kernel.py`. This file contains:

- **`App`** – the central orchestrator.
- **`MiddlewarePipeline`** – executes a chain of middlewares around commands/queries.
- **`ModuleAutoDiscovery`** – scans a package for `IModule` classes and loads them automatically.

### A Minimal App Bootstrap

```python
from sagittarius_engine.infrastructure.std_container import StdLibContainer
from sagittarius_engine.infrastructure.memory_event_bus import MemoryEventBus
from src.app_kernel import App
from src.interfaces import IContainer, IEventBus

container = StdLibContainer()
event_bus = MemoryEventBus()
app = App(container, event_bus)

# The container must know about itself
container.singleton(IContainer, container)
container.singleton(IEventBus, event_bus)

# Boot (and auto‑load modules from 'modules' package if you have one)
app.boot(auto_discover="sagittarius_engine.extensions")
```

After this, your app is alive, and you can call `app.execute(SomeCommand, data_transfer_obj)` or `app.query(SomeQuery, data_transfer_obj)`.

---

## 4. Dependency Injection – `StdLibContainer`

Open `src/infra/std_container.py`. This container **auto‑wires** objects by inspecting `__init__` type hints. You only need to register bindings for interfaces.

### Key Methods

- `bind(interface, concrete_class)` – transient (new instance every time).
- `singleton(interface, instance_or_factory)` – shared instance.
- `resolve(SomeClass)` – get an instance (with all dependencies automatically injected).

### Example

```python
class IRepository(ABC):
    @abstractmethod
    def save(self, user): ...

class InMemoryRepo(IRepository):
    def save(self, user): pass

container.bind(IRepository, InMemoryRepo)

class CreateUserCmd(ICommand):
    def __init__(self, repo: IRepository, event_bus: IEventBus):
        self.repo = repo
        self.event_bus = event_bus
    def execute(self, data_transfer_obj):
        # ...
        pass

# The container automatically provides InMemoryRepo and the event bus
cmd = container.resolve(CreateUserCmd)
```

You almost never call `resolve` directly – `app.execute()` does it for you.

---

## 5. Event Bus – The Communication Backbone

Open `src/interfaces/i_event_bus.py`. There are several implementations:

- `MemoryEventBus` (`src/infra/memory_event_bus.py`) – synchronous, in‑memory, thread‑safe.
- `ThreadPoolEventBus` (`src/infra/thread_pool_event_bus.py`) – runs handlers in a thread pool.
- `ResilientEventBus` (`src/infra/resilient_event_bus.py`) – adds retry + dead letter queue on top of another bus.
- `AsyncioEventBus` (`src/infra/asyncio_event_bus.py`) – for `asyncio` workflows.

### Basic Usage

```python
event_bus = MemoryEventBus()

def handler(data):
    print("Event received:", data)

event_bus.on("user.created", handler)
event_bus.emit("user.created", {"name": "Alice"})
```

The `App` automatically uses the `event_bus` you give it. Modules register their handlers in the `boot()` method.

---

## 6. Modules – Your App's Feature Containers

A module is a class implementing `IModule` (or extending `BaseModule` from `src/base_module.py`). It has two lifecycle methods:

- `register(app)` – bind your classes into the container.
- `boot(app)` – register event listeners, start background tasks.

### Example Module

```python
# modules/user_module/__init__.py
from src.base_module import BaseModule
from src.app_kernel import App
from my_app.application.commands.create_user import CreateUserCommand
from my_app.infrastructure.repos import InMemoryUserRepo

class UserModule(BaseModule):
    def register(self, app: App):
        app.container.singleton(IUserRepository, InMemoryUserRepo())
        app.container.bind(CreateUserCommand, CreateUserCommand)

    def boot(self, app: App):
        app.event_bus.on('user.created', lambda event: print("User created!"))
```

Place this file in your app's `modules/` directory, and `app.boot(auto_discover="sagittarius_engine.extensions")` will load it automatically.

---

## 7. Middleware – Cross‑Cutting Concerns

Middleware wraps every command/query execution. Open `src/interfaces/i_middleware.py` and the examples in `src/middleware/`.

### Using Built‑in Middleware

```python
from sagittarius_engine.middleware.logging_middleware import LoggingMiddleware
from sagittarius_engine.middleware.timing_middleware import TimingMiddleware

app.use_middleware(LoggingMiddleware(container))   # automatically logs start/end
app.use_middleware(TimingMiddleware())             # prints execution time
```

### Writing Your Own

```python
class MyMiddleware(IMiddleware):
    def process(self, cmd_or_query, data_transfer_obj, next_handler):
        # do something before
        result = next_handler()      # continue to next middleware / final handler
        # do something after
        return result
```

---

## 8. Configuration & Logging

**Configuration** uses `IConfig` (see `src/interfaces/i_config.py`). Implementations: `DictConfig` (in‑memory) and `ConfigManager` (multi‑source). You can load JSON, environment variables, and `.env` files.

**Logging** is provided via `ILogger` and `StdLogger` (reads `log.level` and `log.file` from config). The `LoggerModule` (`src/modules/logger_module.py`) registers a singleton `ILogger` automatically.

In your `main.py`, simply add:

```python
from sagittarius_engine.extensions.logger_module import LoggerModule
app.use(LoggerModule())
```

Now `app.execute(...)` and `EventBus` will log automatically.

---

## 9. Putting It All Together – Your First App

Let's build a tiny "User Creator" app using the scaffold. Run:

```bash
python sagittarius_engine/tools/scaffold.py my_first_app
cd my_first_app
```

This creates a standard Clean Architecture directory structure and a `main.py` that already includes logging, database, health modules, and auto‑discovery.

Now add a simple module:

1. **Domain** (`domain/user.py`):
   ```python
   class User:
       def __init__(self, id, name): self.id = id; self.name = name
   ```

2. **Port** (`application/contracts/user_repo.py`):
   ```python
   from abc import ABC, abstractmethod
   from my_first_app.domain.user import User
   class IUserRepository(ABC):
       @abstractmethod
       def add(self, user: User): ...
       @abstractmethod
       def all(self): ...
   ```

3. **Command** (`application/commands/create_user.py`):
   ```python
   from src.interfaces import ICommand, IEventBus
   from my_first_app.application.contracts.user_repo import IUserRepository
   from my_first_app.domain.user import User

   class CreateUserCommand(ICommand):
       def __init__(self, repo: IUserRepository, event_bus: IEventBus):
           self.repo = repo; self.event_bus = event_bus
       def execute(self, data_transfer_obj):
           user = User(data_transfer_obj['id'], data_transfer_obj['name'])
           self.repo.add(user)
           self.event_bus.emit('user.created', user)
           return user
   ```

4. **Infrastructure** (`infrastructure/memory_user_repo.py`):
   ```python
   from my_first_app.application.contracts.user_repo import IUserRepository
   class InMemoryUserRepo(IUserRepository):
       def __init__(self): self._users = []
       def add(self, user): self._users.append(user)
       def all(self): return self._users
   ```

5. **Module** (`modules/user_module/__init__.py`):
   ```python
   from src.base_module import BaseModule
   from my_first_app.application.commands.create_user import CreateUserCommand
   from my_first_app.infrastructure.memory_user_repo import InMemoryUserRepo
   from my_first_app.application.contracts.user_repo import IUserRepository

   class UserModule(BaseModule):
       def register(self, app):
           app.container.singleton(IUserRepository, InMemoryUserRepo())
           app.container.bind(CreateUserCommand, CreateUserCommand)
       def boot(self, app):
           app.event_bus.on('user.created', lambda u: print(f"Welcome {u.name}"))
   ```

6. **Run** – The scaffold's `main.py` already auto‑discovers `modules/`. Just execute:
   ```bash
   PYTHONPATH=. python main.py
   ```
   Then you can quickly test with a simple CLI adapter or just call `app.execute(...)` from a script.

---

## 10. Testing – Built‑in Helpers

The framework provides pytest fixtures and helpers (if you have `tests/conftest.py` and `tests/helpers.py`). You can write tests like:

```python
def test_create_user(app, event_bus):
    app.use(UserModule())
    app.boot()
    user = app.execute(CreateUserCommand, {'id': 1, 'name': 'Alice'})
    assert user.name == 'Alice'
    # assert events were emitted using provided helpers
```

---

## Where to Go Next

- **Explore the remaining interfaces** (`IFileStorage`, `IMetrics`, `ISession`, `IAsyncEventBus`) to see what else the framework supports.
- **Check the built‑in modules** (`health_module`, `database_module`) – they show you how to integrate real databases.
- **Read the docstrings** inside each file – they are very detailed and give you usage examples.
- **Start building your trading bot** – you already have all the pieces.

You now have a complete mental model of the framework. The code you shared is your ultimate reference; keep it open as you build. Once you feel comfortable with the basic flow, we can dive into any specific component or start sketching your Binance ETH bot architecture.