Below you’ll find a complete design of the `App` module using **Mermaid diagrams**.  
The design covers the static class structure, the boot sequence, and the command/query execution flow.

---

## 1. Class Diagram – Static Structure

```mermaid
classDiagram
    class App {
        +IContainer container
        +IEventBus event_bus
        +list~IModule~ modules
        +MiddlewarePipeline pipeline
        +use(module: IModule) None
        +use_middleware(middleware: IMiddleware) None
        +boot(auto_discover: Optional~str~) None
        +execute(command_class: type~ICommand~, input_dto: Any) Any
        +query(query_class: type~IQuery~, input_dto: Any) Any
        -_get_logger() Optional~ILogger~
    }

    class MiddlewarePipeline {
        +list~IMiddleware~ middlewares
        +add(middleware: IMiddleware) None
        +execute(cmd_or_query: Any, data_transfer_obj: Any, final_handler: Callable) Any
    }

    class ModuleAutoDiscovery {
        +static discover(modules_package: str, app: App) None
    }

    class IModule {
        <<interface>>
        +register(app: App) None
        +boot(app: App) None
    }

    class BaseModule {
        <<abstract>>
        +register(app: App) None
        +boot(app: App) None
    }

    class IContainer {
        <<interface>>
        +resolve(type_: type) Any
    }

    class IEventBus {
        <<interface>>
        +emit(event_name: str, payload: Any) None
    }

    class IMiddleware {
        <<interface>>
        +process(cmd_or_query: Any, data_transfer_obj: Any, next_handler: Callable) Any
    }

    class ICommand {
        <<interface>>
        +execute(input_dto: Any) Any
    }

    class IQuery {
        <<interface>>
        +execute(input_dto: Any) Any
    }

    class ILogger {
        <<interface>>
    }

    class ModuleRegistrationError
    class DependencyResolutionError

    App ..|> App : uses
    App *-- MiddlewarePipeline : pipeline
    App o-- IContainer : container
    App o-- IEventBus : event_bus
    App o-- "0..*" IModule : modules
    App --> IMiddleware : uses via pipeline
    App ..> ICommand : executes
    App ..> IQuery : queries
    App ..> ILogger : resolves optionally
    MiddlewarePipeline o-- "0..*" IMiddleware : middlewares
    ModuleAutoDiscovery ..> App : references
    ModuleAutoDiscovery ..> IModule : discovers
    IModule <|.. BaseModule : implements
    App ..> ModuleRegistrationError : raises
    App ..> DependencyResolutionError : catches
```

**Key relationships explained:**
- `App` **owns** the `MiddlewarePipeline`, the list of modules, and holds references to the `IContainer` and `IEventBus`.
- `MiddlewarePipeline` maintains an ordered list of `IMiddleware` instances.
- `ModuleAutoDiscovery` scans packages and instantiates concrete `IModule` implementations (often `BaseModule` subclasses).
- The execution methods (`execute`, `query`) work with `ICommand` / `IQuery` interfaces, resolved through the container.

---

## 2. Sequence Diagram – Application Boot

```mermaid
sequenceDiagram
    participant Client
    participant App
    participant ModuleAutoDiscovery
    participant ModulePackage
    participant ConcreteModule
    participant IContainer
    participant IEventBus
    participant ILogger

    Client->>App: boot(auto_discover="src.modules")
    activate App
        App->>App: _get_logger()
        opt logger available
            App->>ILogger: info("App is booting...")
        end

        alt auto_discover provided
            App->>ModuleAutoDiscovery: discover("src.modules", self)
            activate ModuleAutoDiscovery
                ModuleAutoDiscovery->>ModulePackage: importlib.import_module("src.modules")
                ModuleAutoDiscovery->>ModulePackage: pkgutil.iter_modules(...)
                loop for each sub‑package
                    ModuleAutoDiscovery->>ModulePackage: importlib.import_module(sub_package)
                    ModuleAutoDiscovery->>ModulePackage: inspect.getmembers(...)
                    alt found IModule subclass (not BaseModule)
                        ModuleAutoDiscovery->>ConcreteModule: instantiate()
                        ModuleAutoDiscovery->>App: use(module_instance)
                        activate App
                            App->>App: modules.append(module)
                            App->>ConcreteModule: register(self)
                        deactivate App
                    end
                end
            deactivate ModuleAutoDiscovery
        end

        loop for each module in modules
            App->>ConcreteModule: boot(self)
        end

        opt logger available
            App->>ILogger: info("App booted successfully...")
        end
        App->>IEventBus: emit("app.booted", self)
    deactivate App
```

**Flow highlights:**
- If `auto_discover` is given, `ModuleAutoDiscovery` scans the package, creates every valid `IModule` and calls `app.use()`, which immediately invokes `module.register()`.
- After discovery, all modules are booted (`module.boot(app)`).
- Finally an `app.booted` event is published.

---

## 3. Sequence Diagram – Command Execution

```mermaid
sequenceDiagram
    participant Client
    participant App
    participant IContainer
    participant MiddlewarePipeline
    participant Middleware1
    participant MiddlewareN
    participant Command

    Client->>App: execute(CreateUserCommand, CreateUserDTO(name="Alice"))
    activate App
        App->>App: _get_logger() -> info(...)
        App->>IContainer: resolve(CreateUserCommand)
        IContainer-->>App: command_instance
        note right of App: Build final handler
        App->>App: final = lambda: command.execute(data_transfer_obj)
        App->>MiddlewarePipeline: execute(command, data_transfer_obj, final)
        activate MiddlewarePipeline
            MiddlewarePipeline->>MiddlewarePipeline: build_chain(0)
            note over MiddlewarePipeline: Recursively wraps middleware<br/>around the final handler
            loop for each middleware
                MiddlewarePipeline->>Middleware1: process(command, data_transfer_obj, next_handler)
                Middleware1->>MiddlewareN: process(command, data_transfer_obj, next_handler)
                MiddlewareN->>Command: execute(data_transfer_obj)   (final handler)
                Command-->>MiddlewareN: result
                MiddlewareN-->>Middleware1: result
                Middleware1-->>MiddlewarePipeline: result
            end
        deactivate MiddlewarePipeline
        MiddlewarePipeline-->>App: result
    deactivate App
    App-->>Client: result
```

**Execution pattern:**
1. The command is resolved from the container (dependency injection).
2. A `final` callable is created that calls `command.execute(data_transfer_obj)`.
3. The `MiddlewarePipeline` builds a chain of onion‑like handlers, each `IMiddleware` can run logic before/after forwarding to the next handler.
4. The innermost handler is the command itself.
5. The result bubbles back through all middlewares and is returned to the client.

---

## Summary

- **Class diagram** captures all major classes, interfaces, and their dependencies.
- **Boot sequence** shows the auto‑discovery and module initialisation order.
- **Command execution** illustrates the middleware pipeline onion pattern.

These Mermaid diagrams fully describe the design of the `App` module as implemented in the provided code.