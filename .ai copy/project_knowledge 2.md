==================================================
Project Knowledge Base
==================================================

Sagittarius Engine is a lightweight, modular Application Engine for Python.

It is NOT:

- a web framework
- an MVC framework
- a Clean Architecture framework
- an ORM
- a dependency injection library only
- a CQRS framework

Sagittarius Engine is an application runtime host.

Its purpose is to provide reusable runtime capabilities while remaining completely architecture-agnostic.

Applications built on Sagittarius Engine are free to use any architecture:

- Clean Architecture
- DDD
- MVC
- Layered
- Event-Driven
- Hexagonal
- Custom architectures

The engine never enforces any of them.

==================================================
Core Philosophy
==================================================

Applications choose architecture.

Kernel provides capabilities.

Runtime orchestrates execution.

Extensions integrate technologies.

SDK accelerates development.

==================================================
Current Architecture
==================================================

Sagittarius consists of five layers.

Layer 1

Kernel

Responsible for:

- Application host
- EngineContext
- Dispatcher
- Lifecycle
- Bootstrapping

Layer 2

Runtime

Responsible for:

- Hosted Services
- Scheduler
- Task Manager
- Async Runtime
- Cancellation Tokens

Layer 3

Extensions

Responsible for integrating technologies.

Examples:

- SQLAlchemy
- CQRS
- Persistence
- Logging
- Metrics
- Health Checks

Extensions are optional.

Kernel never depends on them.

Layer 4

SDK

Responsible for:

- Project Templates
- Project Generator
- Placeholder Rendering

SDK is a developer productivity tool.

It is not part of the runtime.

Layer 5

Applications

Applications own:

- business logic
- domain
- services
- repositories
- controllers
- UI

The engine never owns business code.

==================================================
Public API Philosophy
==================================================

Documentation must describe only the public API.

Public API examples should use:

from sagittarius_engine import ...

Do not import internal packages.

Never expose implementation details.

Never describe private classes.

Never rely on deprecated APIs unless writing migration guides.

==================================================
Runtime Capabilities
==================================================

Sagittarius currently provides:

- Dependency Injection Container
- Dispatcher
- Event Bus
- Middleware Pipeline
- Extension Runtime
- Hosted Services
- Scheduler
- Background Task Manager
- Async Runtime
- Cancellation Tokens
- Configuration
- Logging
- Metrics
- Storage
- Persistence Adapters

==================================================
Extension Model
==================================================

Extensions are first-class runtime components.

Each extension participates in a lifecycle:

initialize()

↓

start()

↓

stop()

↓

dispose()

Extensions may declare:

- dependencies
- optional dependencies
- priority

The engine resolves dependency order automatically using topological sorting.

==================================================
Runtime Lifecycle
==================================================

Application startup sequence:

Container

↓

Runtime

↓

Extensions

↓

Hosted Services

↓

Scheduler

↓

Ready

Shutdown sequence:

Scheduler

↓

Hosted Services

↓

Extensions

↓

Task Manager

↓

Async Runtime

↓

Stopped

==================================================
Design Goals
==================================================

Sagittarius prioritizes:

- simplicity
- modularity
- composability
- testability
- deterministic lifecycle
- dependency inversion
- runtime safety
- graceful shutdown

It intentionally avoids:

- magic
- hidden globals
- architecture lock-in
- business abstractions
- framework-specific patterns

==================================================
Target Applications
==================================================

Sagittarius is designed for:

✓ Trading Bots

✓ Desktop Applications

✓ Background Workers

✓ Automation

✓ ETL Pipelines

✓ Long-running Services

✓ Plugin-based Applications

✓ CLI Applications

==================================================
Non Goals
==================================================

Sagittarius is NOT intended to be:

- Django
- FastAPI
- Flask
- SQLAlchemy
- Celery
- APScheduler
- PySide

Instead, it integrates with them through Extensions.

==================================================
Writing Guidelines
==================================================

Whenever explaining a feature:

1. Explain the concept first.

2. Explain why it exists.

3. Explain when to use it.

4. Explain when not to use it.

5. Show diagrams if they improve understanding.

6. Show runnable examples.

7. Mention related engine capabilities.

8. Avoid implementation details.

Always assume the reader is building a real application on top of Sagittarius Engine.