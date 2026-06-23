# Python Clean Architecture Framework

A minimalist, headless-first, event-driven framework designed to help you build applications using strict Clean Architecture and Domain-Driven Design (DDD) principles.

## Features
- **Decoupled Architecture:** Core library (Domain/App) is independent of infrastructure and adapters.
- **Event-Driven:** Built-in MemoryEventBus and ResilientEventBus.
- **Dependency Injection:** Automatic resolving of type-hinted dependencies using a minimalist DI container.
- **Middleware Support:** Inject cross-cutting concerns like logging or validation via a Middleware Pipeline.
- **Modular:** Extend application functionality seamlessly via `IModule`.

## Documentation
- [Hướng dẫn sử dụng](docs/huong_dan_su_dung.md)
- [Kiến trúc tổng thể](docs/architecture.md)

## Getting Started

### 1. Scaffolding a new project
Use the built-in scaffolding tool to generate a new clean architecture application:
```bash
python -m src.scaffold my_new_app
```

### 2. Examples
Check out the `example/` directory for sample applications demonstrating core features:
- **`example/CLI_smallApp/`**: A standard interactive CLI application.
- **`example/batch_csv/`**: Shows how to handle batch processing of CSV files.
- **`example/simple_ui/`**: A simple Flask web application adapter acting over the framework core.
- **`example/multi_module/`**: Demonstrates inter-module communication using EventBus.

## Running Tests
Run the entire test suite using `pytest`:
```bash
python -m pytest tests/ --cov=src
```

## Architecture Summary
The framework strongly enforces the **Dependency Rule**. The domain layer has no external dependencies. The core interacts with outer layers strictly via Ports (interfaces). Infrastructure elements (Loggers, EventBus, Config) are injected via the Container.

*See `docs/architecture.md` for a deeper breakdown.*
