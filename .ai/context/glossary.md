# Glossary & Terms

Definitions of project-specific terms, acronyms, and variables.

## Glossary

This document defines project-specific terminology.

AI assistants MUST use these definitions instead of assuming common industry meanings.

---

## Engine

The central runtime responsible for hosting applications.

Responsibilities:

- Dependency Injection
- Event Bus
- Runtime
- Lifecycle
- Module Loading

The Engine does NOT contain business logic.

---

## Application

A user-built software that runs on top of the Engine.

Examples:

- Trading Bot
- Desktop Application
- REST API

Applications consume Engine services.

---

## Module

A self-contained feature that can be registered into the Engine.

A Module may provide:

- Services
- Configuration
- Commands
- Events
- Background Tasks

A Module owns its own lifecycle.

A Module is NOT a Python package.

---

## Extension

An optional capability that extends the Engine.

Examples:

- CQRS
- Scheduler
- Metrics
- Plugin Loader

Extensions should not depend on Applications.

---

## Plugin

A dynamically loaded package discovered at runtime.

Plugins are optional.

Plugins should communicate through public extension points.

Plugins should never access Engine internals directly.

---

## Dispatcher

The component responsible for dispatching requests.

Examples:

- Commands
- Queries
- Events

The Dispatcher does not contain business logic.

---

# Event

A notification describing something that has already happened.

Events are immutable.

Events may have multiple subscribers.

Events should not return values.

---

# Command

A request asking the system to perform an action.

Commands modify system state.

Commands have exactly one handler.

---

# Query

A request asking for information.

Queries do not modify state.

Queries should be side-effect free.

---

# Service

A reusable component providing functionality.

Services are resolved through Dependency Injection.

Services should not create other services manually.

---

# Hosted Service

A long-running background process managed by the Runtime.

Examples:

- Scheduler
- MQTT Listener
- Health Monitor

Hosted Services start and stop with the application lifecycle.

---

# Runtime

The execution environment responsible for:

- Startup
- Shutdown
- Hosted Services
- Background Tasks

---

# Lifecycle

The ordered sequence of application states.

Typical lifecycle:

Initialize

↓

Configure

↓

Start

↓

Running

↓

Stopping

↓

Stopped

---

# Context

A shared object containing runtime resources.

Typical resources include:

- Container
- Logger
- Configuration
- Dispatcher

Context is not business data.

---

# Adapter

A bridge between the Engine and an external system.

Examples:

- Database
- MQTT
- REST API
- File System

Adapters isolate infrastructure concerns.

---

# Repository

An abstraction over data persistence.

Repositories belong to the application layer.

The Engine does not provide repositories.

---

# Public API

Any API intended for external consumers.

Public APIs should remain stable.

Breaking changes require documentation updates.

---

# Internal API

Implementation details not intended for consumers.

Internal APIs may change without notice.

Applications should never depend on them.
