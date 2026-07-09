Theo mình thì **Phase 3 mới là lúc Sagittarius thực sự trở thành Engine**.

Sau Phase 2.5, engine đã có Kernel hoàn chỉnh. Nhưng nó vẫn còn **rất nhiều khái niệm của Clean Architecture** như:

* `ICommand`
* `IQuery`
* `BaseRepository`
* `BaseModule`
* `ApplicationService`
* ...

Đây đều là **opinionated patterns**, không nên nằm trong Engine.

Engine chỉ nên cung cấp **capabilities**, còn CQRS, DDD, Repository... phải là **extensions**.

Đây là prompt mình sẽ dùng.

---

```text
# ROLE

You are a principal software architect performing Phase 3 of the Sagittarius Engine evolution.

Previous phases have transformed Sagittarius from a Clean Architecture project
into an Application Engine.

The kernel is now stable.

This phase removes opinionated application architecture concepts from the kernel
and converts them into optional extensions.

DO NOT redesign the engine.

DO NOT break public APIs.

DO NOT introduce new runtime behavior.

This is an architectural separation only.

--------------------------------------------------
# OBJECTIVE

The engine must become architecture-agnostic.

It should no longer assume the user is building a Clean Architecture project.

Instead it should provide reusable runtime capabilities.

Patterns such as CQRS, Repository, DDD, and Modules must become optional extensions.

--------------------------------------------------
# ENGINE PRINCIPLE

The kernel must only contain engine capabilities.

Examples:

- Dependency Injection
- Middleware
- Event Bus
- Configuration
- Logging
- Lifecycle
- Dispatcher
- Module Loading
- Threading
- Scheduling
- Storage Abstractions

The kernel must NOT know:

- Command
- Query
- Aggregate
- Repository
- Entity
- Domain
- UseCase
- ValueObject

--------------------------------------------------
# MOVE CQRS OUT OF KERNEL

Anything specifically related to CQRS must be moved.

Examples:

ICommand

IQuery

CommandHandler

QueryHandler

CommandDispatcher (if any)

QueryDispatcher (if any)

Move them into:

extensions/cqrs/

Suggested structure:

extensions/

    cqrs/

        commands.py

        queries.py

        handlers.py

        dispatcher.py

        __init__.py

--------------------------------------------------
# MOVE REPOSITORY ABSTRACTIONS

Repository abstractions are application patterns.

Move them out of the kernel.

Suggested destination:

extensions/persistence/

or

extensions/sqlalchemy/

depending on current implementation.

Examples:

BaseRepository

Repository interfaces

Repository helpers

Unit of Work (future)

--------------------------------------------------
# MODULES

If there are classes representing business modules
instead of engine extensions,
move them into extensions.

Engine kernel should only know:

ExtensionLoader

ExtensionMetadata

ExtensionLifecycle

It should not know business modules.

--------------------------------------------------
# KERNEL RESPONSIBILITIES

After this phase the kernel should contain only:

kernel/

    app.py

    bootstrap.py

    context.py

    dispatcher.py

    lifecycle.py

    module_loader.py

container/

middleware/

interfaces/

events/

config/

logging/

threading/

storage/

adapters/

tools/

No CQRS.

No Repository.

No Domain concepts.

--------------------------------------------------
# EXTENSION PRINCIPLE

Extensions may depend on the kernel.

The kernel must NEVER depend on extensions.

Dependency direction:

Extensions
        ↓
Kernel

Never:

Kernel
      ↓
Extensions

--------------------------------------------------
# PUBLIC API

Maintain backward compatibility.

Legacy imports should continue working if possible.

Example:

from sagittarius_engine.application import ICommand

may internally re-export:

extensions.cqrs.ICommand

Mark legacy imports as deprecated.

Do not remove them.

--------------------------------------------------
# IMPORT RULES

Kernel imports must never reference:

extensions.cqrs

extensions.persistence

extensions.ddd

extensions.sqlalchemy

Kernel must remain independent.

--------------------------------------------------
# DOCUMENTATION

Rewrite documentation.

Describe CQRS as:

"An optional Sagittarius Extension."

Describe Repository support as:

"An optional persistence extension."

Remove any wording implying they are mandatory.

--------------------------------------------------
# DO NOT CHANGE

Do NOT modify:

DI container

Middleware pipeline

Event Bus

Configuration

Logging

EngineContext

Lifecycle

Dispatcher

Storage

Threading

Adapters

Behavior

Only relocate architecture-specific concepts.

--------------------------------------------------
# TESTS

Update imports where necessary.

Do not rewrite test logic.

All tests must continue passing.

--------------------------------------------------
# CODE QUALITY

Favor loose coupling.

No circular dependencies.

No duplicated implementations.

No hidden compatibility layers beyond import re-exports.

Minimize breaking changes.

--------------------------------------------------
# ACCEPTANCE CRITERIA

✓ Kernel contains only engine infrastructure.

✓ CQRS is an extension.

✓ Repository abstractions are extensions.

✓ Kernel has zero dependency on CQRS.

✓ Kernel has zero dependency on Repository.

✓ Public API remains compatible.

✓ Legacy imports are deprecated but functional.

✓ Existing tests pass.

--------------------------------------------------
# OUTPUT

Provide:

1. New package tree.

2. Every class that was moved.

3. Compatibility shims created.

4. Dependency graph before/after.

5. Remaining Clean Architecture concepts still inside the kernel.

Do not implement future DDD features.

Do not redesign APIs.

Only separate engine infrastructure from optional architectural extensions.
```

---

# Tuy nhiên, mình sẽ **thay đổi roadmap của bạn một chút**.

Sau khi xem Sagittarius, mình thấy **CQRS chưa phải vấn đề lớn nhất**. Vấn đề lớn hơn là **engine vẫn bị "framework hóa"**.

Thay vì Phase 3 như trên, mình sẽ chia thành hai bước nhỏ:

### Phase 3A – Engine Decoupling (nên làm trước)

Tách mọi thứ còn "opinionated" khỏi kernel:

* CQRS
* Repository
* SQLAlchemy
* Health
* Metrics
* Validation
* Pydantic

=> Tất cả chuyển thành `extensions/`.

### Phase 3B – Extension Manifest (rất đáng làm)

Định nghĩa một chuẩn cho extension, ví dụ:

```python
class IExtension(Protocol):
    def register(self, context: EngineContext) -> None:
        ...

    def boot(self, context: EngineContext) -> None:
        ...

    def shutdown(self, context: EngineContext) -> None:
        ...
```

Lúc đó người dùng chỉ cần:

```python
app.use(SqlAlchemyExtension())
app.use(CQRSExtension())
app.use(MetricsExtension())
```

Đây mới là cảm giác của một **Engine** thực sự, giống như ASP.NET Core, Unreal Engine hay VS Code Extension Host: kernel chỉ biết "extension", còn CQRS, persistence, metrics... đều là plugin. Theo mình, đây sẽ là điểm khác biệt lớn nhất của Sagittarius so với các framework Python khác.
