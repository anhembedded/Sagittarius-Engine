# Dependency Injection Container

The Dependency Injection (DI) Container is a central pillar of the Sagittarius Engine, responsible for the automatic instantiation, wiring, and lifecycle management of all system components.

---

## 1. Overview

In a Clean Architecture system, high-level modules should depend on abstractions (interfaces) rather than concrete implementations. However, *something* in the application has to know how to instantiate the concrete classes and pass them in. This is the DI Container's job.

Instead of writing tightly-coupled code like:

```python
controller = UserController(SqliteRepository())
```

You simply register your implementations with the `IContainer`, and it automatically parses the dependency graph and wires everything together.

---

## 2. Terminology

Before diving deeper, let's establish the common vocabulary used when interacting with the DI Container:

- **Transient**: An object whose lifecycle is very short. Every time it is resolved or injected, a *brand new instance* is created.
- **Singleton**: An object whose lifecycle is bound to the container. The first time it is resolved, it is cached and shared for all future requests.
- **Binding**: The configuration rule that maps an interface/abstract class to a concrete implementation.
- **Resolution**: The act of the Container recursively traversing the dependency graph, instantiating classes, and returning the fully constructed object.
- **Factory**: A function or lambda that returns an instance, allowing for custom initialization logic when the container's auto-wiring isn't enough.

---

## 3. Use Cases

The DI Container is designed to solve specific architectural problems:

1. **Decoupling Business Logic from Infrastructure**: When your Domain Use Cases need to talk to a database, you bind `IUserRepository` to `SqliteUserRepository`. The Use Case only knows about the interface, allowing you to swap the database later without touching the business logic.
2. **Shared Infrastructure State (Singletons)**: When your entire application needs to communicate over a single message bus, or read from the same configuration file, you bind `IEventBus` and `IConfig` as singletons.
3. **Lazy/Deferred Initialization**: When a component is heavy (e.g., establishing a database connection), you can use the container to delay its creation until a controller actually requests it at runtime.

---

## 4. How it works

The default engine implementation is the `StdLibContainer` (located in `sagittarius_engine.infrastructure.container.std_container`).

- **Automatic Type Resolution**: The container uses Python's standard `inspect` and `typing.get_type_hints` modules to examine the `__init__` method of the requested class. It recursively resolves all required parameters based on their type annotations.
- **High Performance (Caching)**: Reflection in Python can be slow. To solve this, `StdLibContainer` uses a lock-free `_resolution_cache`. The signature and type hints of a class are parsed exactly **once** and cached, making subsequent resolutions extremely fast.
- **Thread Safety**: The container uses `threading.RLock` and a "Double-checked locking" pattern to ensure that Singletons are only instantiated exactly once, even if multiple threads request them simultaneously.
- **Circular Dependency Detection**: While recursively building the dependency tree, it tracks the stack of currently-resolving classes in a `set`. If it sees a class twice in the same resolution chain, it immediately throws a `DependencyResolutionError`.

---

## 5. Components & API

### Interfaces

- **`IContainer`**: The core port interface all engine components rely on.

### Implementations

- **`StdLibContainer`**: The built-in concrete implementation relying on the standard library.

### Core Methods

- **`bind(abstract: type, concrete: type)`**: Registers a **Transient** binding. Every time `abstract` is requested, a *brand new instance* of `concrete` will be created.
- **`singleton(abstract: type, instance_or_factory: Any)`**: Registers a **Singleton** binding. The container ensures that only *one* shared instance is ever created. You can pass:
  - An already initialized object (`MemoryEventBus()`)
  - A concrete type to be lazy-loaded on first request (`SqliteUserRepository`)
  - A factory lambda function (`lambda c: build_complex_thing()`)
- **`resolve(abstract: type)`**: Instructs the container to fetch or build an instance of the requested type, automatically resolving all of its nested dependencies.

---

## 6. Code Examples & Usage Guide

### Use Case 1: Shared Infrastructure State (Singleton Binding)

When you need exactly one instance shared across the entire app.

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus

container = StdLibContainer()

# Register a singleton (Created lazily on first use, or immediately if passing an instance)
container.singleton(IEventBus, MemoryEventBus)

# Every time you resolve IEventBus, you get the EXACT same object in memory
bus1 = container.resolve(IEventBus)
bus2 = container.resolve(IEventBus)
assert bus1 is bus2  # True
```

### Use Case 2: Decoupling Business Logic (Transient Binding)

When you want a new instance for every request, and want to hide the concrete implementation.

```python
# Register a transient binding (Created new every time)
container.bind(IUserRepository, PostgresUserRepository)

# If your UserController's __init__ requires IUserRepository,
# it is automatically injected here:
controller = container.resolve(UserController)
```

### Use Case 3: Factory Initialization

If an object requires complex setup that the container can't guess (like database credentials), use a factory function:

```python
def make_database(c: IContainer) -> DatabaseConnection:
    config = c.resolve(IConfig)
    return DatabaseConnection(host=config.get("DB_HOST"), port=config.get("DB_PORT"))


container.singleton(DatabaseConnection, make_database)
```

---

## 7. Common Misconceptions (Module & Use Cases)

### ❌ Misconception 1: "Reflection is too slow, so a Python DI Container is bad for performance."

✅ **Truth**: While `inspect.signature` is slow, `StdLibContainer` utilizes a `_resolution_cache`. The reflection happens exactly *once* per class type. Every subsequent resolve reads directly from the cache dictionary, which is extremely fast in CPython.

### ❌ Misconception 2: `container.bind()` shares the same instance across the app

✅ **Truth**: `bind()` is transient! Every single time you call `resolve()` (or whenever a class requires it as a dependency), a brand new instance is instantiated. If you want state to be shared (like a Database connection or an Event Bus), you **must** use `singleton()`.

### ❌ Misconception 3: You need special `@inject` decorators to use the Container

✅ **Truth**: You do not need any decorators at all! The `StdLibContainer` relies purely on standard Python 3 type hints. As long as your `__init__` parameters are properly annotated (e.g., `def __init__(self, repo: IUserRepository):`), the container will figure it out automatically.

### ❌ Misconception 4: "I should register everything, including Data Transfer Objects (DTOs) and Entities, into the DI Container."

✅ **Truth**: The DI Container is strictly for resolving **Services**, **Repositories**, and **Behaviors**. You should *never* use the DI Container to resolve simple data classes, Domain Entities, or DTOs. Those should be instantiated directly in your code (e.g., `user = User(name="John")`).
