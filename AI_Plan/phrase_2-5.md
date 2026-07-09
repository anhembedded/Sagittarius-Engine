**Phase 2.5 là bước quan trọng nhất trong toàn bộ roadmap**. Sau bước này, Sagittarius sẽ có kiến trúc của một **Engine** thay vì một framework.

Mục tiêu duy nhất là:

> **App không còn sở hữu bất kỳ service nào. App chỉ là entry point của Engine.**

Tất cả service sẽ nằm trong **EngineContext** hoặc **EngineServices**.

Mình khuyên dùng **EngineContext** vì sau này có thể chứa cả runtime state, metadata, lifecycle...

---

```text
# ROLE

You are a senior software architect performing Phase 2.5 of the Sagittarius Engine refactoring.

Phase 1 renamed the project into an Application Engine.

Phase 2 decomposed the App class into smaller kernel services.

This phase introduces a central EngineContext that owns every runtime service.

DO NOT change behaviors.

DO NOT redesign public APIs.

DO NOT introduce new features.

Everything must remain backward compatible.

--------------------------------------------------
# OBJECTIVE

Currently App still directly owns several runtime components.

For example:

- Container
- EventBus
- Logger
- Configuration
- Middleware
- Dispatcher
- ModuleLoader

This tightly couples App to every engine subsystem.

Instead the engine should own these services through a dedicated EngineContext.

App becomes only the public entry point.

--------------------------------------------------
# TARGET ARCHITECTURE

kernel/

    app.py

    bootstrap.py

    dispatcher.py

    lifecycle.py

    module_loader.py

    context.py

--------------------------------------------------
# CREATE EngineContext

Create a new class:

EngineContext

Its responsibility is to own every runtime service.

Example:

class EngineContext:

    container

    event_bus

    logger

    config

    dispatcher

    middleware_pipeline

    lifecycle

    module_loader

Do not add business objects.

Only engine infrastructure.

--------------------------------------------------
# APP RESPONSIBILITY

App should no longer directly create or own services.

Instead:

class App:

    def __init__(...):

        self.context = EngineContext(...)

App delegates everything through context.

Example:

self.context.dispatcher.execute(...)

instead of

self.dispatcher.execute(...)

--------------------------------------------------
# ENGINE SERVICES

Every runtime service should live inside EngineContext.

Examples:

context.container

context.event_bus

context.logger

context.config

context.dispatcher

context.middleware_pipeline

context.module_loader

context.lifecycle

--------------------------------------------------
# SINGLE SOURCE OF TRUTH

Every service instance must exist only once.

Avoid duplicated references.

Bad:

App.container

Bootstrap.container

Dispatcher.container

Good:

EngineContext.container

Everyone receives EngineContext
or receives only the dependency they need.

--------------------------------------------------
# DEPENDENCY FLOW

Desired dependency graph:

                 App
                  │
                  ▼
           EngineContext
          /      |      \
         /       |       \
 Bootstrap Dispatcher Lifecycle
         \       |       /
          \      |      /
           Container
           EventBus
           Logger
           Config

App should never coordinate individual services.

--------------------------------------------------
# BOOTSTRAP

Bootstrap receives EngineContext.

It initializes:

container

extensions

logger

configuration

event bus

App.boot()

simply calls

context.bootstrap.boot()

--------------------------------------------------
# DISPATCHER

Dispatcher receives EngineContext.

It uses:

context.container

context.middleware_pipeline

context.event_bus

Do not pass App into Dispatcher.

--------------------------------------------------
# MODULE LOADER

ModuleLoader receives EngineContext.

It can register services using:

context.container

It can publish events using:

context.event_bus

--------------------------------------------------
# LIFECYCLE

Lifecycle receives EngineContext.

Future startup/shutdown events should live here.

No implementation changes.

--------------------------------------------------
# DO NOT CHANGE

Do NOT modify:

Dependency Injection behavior

Middleware behavior

EventBus behavior

Logging

Configuration

Storage

Persistence

CQRS

Repositories

Interfaces

Adapters

Extensions

Only ownership changes.

--------------------------------------------------
# PUBLIC API

The following code must continue working.

app = App(...)

app.boot()

app.execute(...)

app.query(...)

app.use(...)

app.use_middleware(...)

There must be zero breaking API changes.

--------------------------------------------------
# DESIGN PRINCIPLES

Favor composition.

Avoid global singletons.

Avoid service locator anti-pattern.

EngineContext is NOT a DI container.

It is merely the owner of runtime services.

Business code should still receive dependencies via constructor injection.

--------------------------------------------------
# CODE QUALITY

Each runtime service should have one owner.

Avoid duplicated references.

Avoid circular imports.

Avoid hidden global state.

Prefer explicit dependency injection.

--------------------------------------------------
# DOCUMENTATION

Update architecture documentation.

Describe EngineContext as:

"The runtime composition root of the Sagittarius Engine.

It owns every engine service and coordinates communication between engine subsystems.

It does not contain application or business logic."

Update App documentation.

Describe App as:

"The public façade of the Sagittarius Engine.

App delegates runtime operations to EngineContext."

--------------------------------------------------
# ACCEPTANCE CRITERIA

✓ App no longer owns runtime services

✓ EngineContext owns all runtime services

✓ Bootstrap uses EngineContext

✓ Dispatcher uses EngineContext

✓ ModuleLoader uses EngineContext

✓ Lifecycle uses EngineContext

✓ No duplicated service ownership

✓ Public API unchanged

✓ No behavioral changes

✓ All existing tests continue passing

--------------------------------------------------
# OUTPUT

Provide:

1. New EngineContext implementation

2. Updated dependency diagram

3. List of moved responsibilities

4. List of files changed

5. Compatibility report

Do not implement Phase 3.

Do not redesign CQRS.

Do not remove existing APIs.

Only centralize runtime ownership through EngineContext.
```

---

## Mình còn đề xuất thêm một cải tiến nhỏ cho Phase 2.5

Thay vì `EngineContext` chỉ là một "túi chứa service", hãy thiết kế nó như **Composition Root** của engine:

```python
class EngineContext:
    def __init__(
        self,
        container: IContainer,
        event_bus: IEventBus,
        logger: ILogger,
        config: IConfig,
        middleware_pipeline: MiddlewarePipeline,
        dispatcher: Dispatcher,
        lifecycle: EngineLifecycle,
        module_loader: ModuleLoader,
    ):
        ...
```

Điều này có hai lợi ích:

1. **Không biến `EngineContext` thành Service Locator**. Mỗi service vẫn nhận đúng dependency qua constructor thay vì tự đi lấy từ context.
2. **Dễ kiểm thử**. Bạn có thể thay từng service bằng mock hoặc fake trong unit test mà không ảnh hưởng đến phần còn lại.

Đó cũng là cách nhiều engine và framework hiện đại tổ chức phần "kernel" của mình: `App` → `EngineContext` → các service chuyên trách, trong khi business code vẫn hoàn toàn sử dụng dependency injection thông thường.
