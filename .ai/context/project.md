# Sagittarius Engine

## Overview

Sagittarius Engine is a lightweight, modular application runtime for Python.

It is **not**:
- Web framework
- MVC framework
- Clean Architecture framework
- ORM
- DI library
- CQRS framework

Applications own architecture.
Sagittarius provides runtime capabilities only.

Supported architectures include:
- Clean Architecture
- DDD
- MVC
- Layered
- Event Driven
- Hexagonal
- Custom

---

## Philosophy

- Applications choose architecture
- Kernel provides capabilities
- Runtime orchestrates execution
- Extensions integrate technologies
- SDK accelerates development

---

## Architecture

| Layer | Responsibility |
|--------|----------------|
| Kernel | Host, Context, Dispatcher, Lifecycle, Bootstrap |
| Runtime | Hosted Services, Scheduler, Tasks, Async, Cancellation |
| Extensions | SQLAlchemy, CQRS, Persistence, Logging, Metrics |
| SDK | Templates, Generator |
| Application | Business Logic, Domain, UI |

---

## Public API Rules

Documentation must:

- use `from sagittarius_engine import ...`
- avoid internal imports
- avoid private APIs
- avoid implementation details
- avoid deprecated APIs

---

## Runtime Capabilities

- DI Container
- Dispatcher
- Event Bus
- Middleware
- Extension Runtime
- Hosted Services
- Scheduler
- Task Manager
- Async Runtime
- Cancellation Tokens
- Configuration
- Logging
- Metrics
- Storage
- Persistence

---

## Extension Lifecycle

```
initialize
    ↓
start
    ↓
stop
    ↓
dispose
```

Extension metadata:

- dependencies
- optional dependencies
- priority

Dependency order is resolved automatically.

---

## Runtime Lifecycle

Startup

```
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
```

Shutdown

```
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
```

---

## Design Goals

Prioritize

- Simplicity
- Modularity
- Composability
- Testability
- Deterministic lifecycle
- Dependency inversion
- Runtime safety
- Graceful shutdown

Avoid

- Magic
- Hidden globals
- Architecture lock-in
- Business abstractions
- Framework-specific patterns

---

## Target Applications

- Trading Bots
- Desktop Apps
- Background Workers
- Automation
- ETL
- Long-running Services
- Plugin Systems
- CLI

---

## Non Goals

Sagittarius is not intended to replace:

- Django
- FastAPI
- Flask
- SQLAlchemy
- Celery
- APScheduler
- PySide

Instead, it integrates with them through Extensions.

---

## Documentation Rules

For every feature:

1. Explain the concept
2. Explain why it exists
3. Explain when to use it
4. Explain when not to use it
5. Add diagrams when useful
6. Provide runnable examples
7. Mention related capabilities
8. Hide implementation details

Always write from the perspective of an application developer.