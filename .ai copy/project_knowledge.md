==================================================
Project Knowledge Base
==================================================

Project Name

Sagittarius Engine

Current Version

v1.x (Architecture Frozen)

Project Type

Lightweight Modular Python Application Engine

The architecture has already been stabilized.

Do NOT redesign the architecture.

Assume all public APIs are finalized.

--------------------------------------------------
Project Vision
--------------------------------------------------

Sagittarius Engine is NOT:

- a Clean Architecture framework
- an MVC framework
- a DDD framework
- an ORM
- a web framework

Sagittarius Engine IS:

A lightweight runtime host that provides reusable application capabilities.

Applications decide their own architecture.

The engine only provides runtime infrastructure.

--------------------------------------------------
Core Philosophy
--------------------------------------------------

Applications choose architecture.

Kernel provides capabilities.

Runtime orchestrates execution.

Extensions integrate technologies.

SDK accelerates development.

--------------------------------------------------
Core Responsibilities
--------------------------------------------------

Kernel provides:

• Dependency Injection
• Dispatcher
• Event Bus
• Middleware Pipeline
• Extension Lifecycle
• Configuration
• Logging
• Runtime Host
• Hosted Services
• Scheduler
• Background Tasks
• Async Runtime
• Thread Management

Kernel intentionally DOES NOT provide:

• Domain Models
• Entities
• Use Cases
• Repositories
• CQRS
• Business Rules

Those belong to applications or extensions.

--------------------------------------------------
Current Architecture
--------------------------------------------------

                Application

                     │

                     ▼

              Public API (App)

                     │

                     ▼

            EngineContext

                     │

     ┌───────────────┼───────────────┐
     ▼               ▼               ▼

 Dispatcher      Event Bus      Middleware

                     │

                     ▼

         Runtime Infrastructure

     ┌──────────┬──────────┬──────────┐
     ▼          ▼          ▼          ▼

Hosted     Scheduler   TaskMgr   AsyncRuntime
Services

                     │

                     ▼

             Extension System

                     │

                     ▼

            Application Extensions

--------------------------------------------------
Major Components
--------------------------------------------------

App

Public façade.

Responsible for:

• boot()
• stop()
• dispatch()
• use()

Nothing more.

--------------------------------------------------

EngineContext

Shared runtime context.

Provides access to:

• container
• dispatcher
• event_bus
• logger
• config
• middleware
• runtime
• extensions

--------------------------------------------------

Dispatcher

Unified request dispatcher.

Applications dispatch requests.

Extensions may register handlers.

--------------------------------------------------

Runtime

Provides:

Hosted Services

Task Manager

Scheduler

Async Runtime

Cancellation Tokens

--------------------------------------------------

Extensions

First-class runtime plugins.

Lifecycle

initialize()

start()

stop()

dispose()

Extensions may declare:

dependencies

optional_dependencies

priority

--------------------------------------------------
Runtime Boot Sequence
--------------------------------------------------

Container

↓

Async Runtime

↓

Extensions

↓

Hosted Services

↓

Scheduler

↓

Application Ready

--------------------------------------------------
Runtime Shutdown Sequence
--------------------------------------------------

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

Application Stopped

--------------------------------------------------
Extension Dependency Resolution
--------------------------------------------------

Extensions are started using:

Topological Sorting

Rules:

Required dependencies first

Optional dependencies respected

Priority breaks ties

Cycles are rejected

Rollback occurs automatically on failures.

--------------------------------------------------
SDK
--------------------------------------------------

The SDK generates projects.

Supported templates:

minimal

clean

ddd

mvc

Generated projects are runnable immediately.

The SDK is NOT part of runtime execution.

--------------------------------------------------
Reference Applications
--------------------------------------------------

Current examples include:

Trading Bot

Desktop Application

Plugin System

These examples represent recommended architecture.

They are reference implementations,
not framework requirements.

--------------------------------------------------
Stable Public API
--------------------------------------------------

Public imports always come from:

from sagittarius_engine import ...

Avoid importing internal packages.

Never document private modules.

Never document implementation details.

--------------------------------------------------
Deprecated APIs
--------------------------------------------------

Legacy execute()

Legacy query()

Remain available only for backwards compatibility.

Documentation should prefer:

dispatch()

--------------------------------------------------
Target Use Cases
--------------------------------------------------

Sagittarius Engine is designed for:

✓ Trading Bots

✓ Desktop Applications

✓ Long-running Services

✓ Background Workers

✓ Automation

✓ CLI Applications

✓ Event-driven Systems

Not optimized for:

✗ Tiny one-file scripts

✗ Simple CRUD web apps

✗ ORM replacement

✗ Framework-specific architectures

--------------------------------------------------
Documentation Audience
--------------------------------------------------

Assume readers are experienced Python developers.

Avoid explaining basic Python syntax.

Focus on:

concepts

design rationale

best practices

runtime behavior

practical usage

--------------------------------------------------
Documentation Constraints
--------------------------------------------------

Never expose:

internal packages

private classes

kernel internals

implementation details

Always document:

public APIs

runtime behavior

extension contracts

application development

Use Mermaid diagrams whenever they improve understanding.

Code examples must be runnable.

Only import from public APIs.

Documentation should describe HOW TO USE the engine,
not HOW the engine is implemented.