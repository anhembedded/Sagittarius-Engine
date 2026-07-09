# ROLE

You are a senior software architect performing Phase 2 of the Sagittarius Engine refactoring.

Phase 1 has already renamed the project into an Application Engine.

This phase focuses ONLY on separating responsibilities inside the Engine.

DO NOT redesign public APIs.
DO NOT change behaviors.
DO NOT introduce new features.

Everything must remain backward compatible.

--------------------------------------------------
# OBJECTIVE

The current App class has become a God Object.

It currently manages:

- application lifecycle
- dependency container
- middleware pipeline
- module loading
- event bus
- command execution
- query execution
- logging

This violates the Single Responsibility Principle.

Refactor the internals so that App becomes a lightweight façade over dedicated engine services.

--------------------------------------------------
# TARGET ARCHITECTURE

Create a dedicated kernel layer.

kernel/

    app.py                # Public facade
    bootstrap.py          # Bootstrapping process
    lifecycle.py          # Engine lifecycle management
    dispatcher.py         # Execution dispatcher
    module_loader.py      # Module/extension discovery

The exact filenames may differ slightly if needed,
but responsibilities must be clearly separated.

--------------------------------------------------
# RESPONSIBILITIES

App should become extremely small.

It should mainly expose:

class App:

    boot()

    execute()

    query()

    use()

    use_middleware()

Internally it should delegate to dedicated classes.

--------------------------------------------------
# BOOTSTRAP

Move everything related to startup into Bootstrap.

Responsibilities:

- initialize engine
- auto discovery
- register extensions
- initialize services

App.boot() should simply call Bootstrap.boot().

--------------------------------------------------
# MODULE LOADER

Move module discovery logic into ModuleLoader.

Responsibilities:

- discover extensions
- load extensions
- instantiate extensions
- register extensions

App should never scan packages directly.

--------------------------------------------------
# LIFECYCLE

Create an EngineLifecycle component.

Responsibilities:

- boot state
- started state
- stopped state
- future lifecycle hooks

Do not implement stop() yet.

Only prepare the architecture.

--------------------------------------------------
# DISPATCHER

Create Dispatcher.

Responsibilities:

- resolve handlers
- execute middleware pipeline
- invoke executable

App.execute()

should delegate to Dispatcher.execute()

App.query()

should delegate to Dispatcher.query()

No behavioral changes.

--------------------------------------------------
# APP

The final App should mostly coordinate components.

Pseudo example:

class App:

    def boot(...):
        self.bootstrap.boot(...)

    def execute(...):
        return self.dispatcher.execute(...)

    def query(...):
        return self.dispatcher.query(...)

Very little logic should remain inside App.

--------------------------------------------------
# DO NOT CHANGE

Do NOT rename:

App

ApplicationRunner

MiddlewarePipeline

StdLibContainer

MemoryEventBus

ILogger

IContainer

IEventBus

Do NOT modify interfaces.

Do NOT modify middleware.

Do NOT modify event bus.

Do NOT modify DI container.

Do NOT modify tests except imports if required.

--------------------------------------------------
# KEEP API STABLE

The following code must continue working without modification.

app = App(container, event_bus)

app.use(...)

app.use_middleware(...)

app.boot()

app.execute(...)

app.query(...)

Behavior must remain identical.

--------------------------------------------------
# CODE QUALITY

Favor composition over inheritance.

Each class should have one responsibility.

Avoid circular imports.

Avoid duplicated logic.

Prefer dependency injection between kernel services.

--------------------------------------------------
# TESTS

All existing tests must continue passing.

If a test breaks because of an internal move,
fix imports instead of changing behavior.

--------------------------------------------------
# DOCUMENTATION

Update class docstrings to reflect the new engine architecture.

App should now be documented as:

"The public façade of the Sagittarius Engine."

Bootstrap:

"Responsible for bootstrapping the engine."

Dispatcher:

"Responsible for executing handlers through the middleware pipeline."

Lifecycle:

"Responsible for managing engine state."

ModuleLoader:

"Responsible for discovering and loading engine extensions."

--------------------------------------------------
# OUTPUT

Provide:

1. New kernel architecture

2. Responsibility of every new class

3. Before/After dependency diagram

4. Files moved

5. Any compatibility concerns

Do not implement Phase 3.

Do not redesign the framework.

Do not remove existing APIs.

Only separate responsibilities inside the engine kernel.