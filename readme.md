# Sagittarius Framework

**A lightning-fast, minimalist, headless-first, event-driven Python framework designed to help you build applications using strict Clean Architecture and Domain-Driven Design (DDD) principles.**

---

## What is Sagittarius?

Sagittarius is not just another web framework. It is an **Application Core Framework**. Its primary goal is to isolate your core business logic (Domain and Application Use Cases) from external infrastructure, databases, and UI frameworks.

Whether you are building a CLI, a background worker, or an API using Flask/FastAPI, your core application remains the same. Sagittarius achieves this by strictly enforcing the Dependency Rule using a minimalist native Dependency Injection container.

**Key Highlights:**
- **Zero External Dependencies in Core:** Built entirely using the Python Standard Library.
- **Decoupled Architecture:** Core library (Domain/App) is completely independent of infrastructure and adapters.
- **Event-Driven:** Built-in sync (`MemoryEventBus`), background (`ThreadPoolEventBus`), and async (`AsyncioEventBus`) Event Buses for modular communication.
- **Dependency Injection:** Automatic resolution of type-hinted dependencies.
- **Middleware Pipeline:** Inject cross-cutting concerns like logging or validation effortlessly.
- **Modular Design:** Extend application functionality seamlessly via `IModule`.

## Documentation

- [Hướng dẫn sử dụng (Vietnamese)](docs/huong_dan_su_dung.md)
- [Kiến trúc tổng thể (Architecture Details)](docs/architecture.md)

## Quick Start

### 1. Installation

To install the framework in editable mode for development:

```bash
pip install -e .
```

### 2. Scaffold a new project

Use the built-in scaffolding tool to generate a new clean architecture application:

```bash
python -m sagittarius_engine.tools.scaffold my_new_app
```

### 3. Examples

Check out the `example/` directory for sample applications demonstrating core features. These examples are designed to be run from the root of the project:

- **`example/CLI_smallApp/`**: A standard interactive CLI application.
- **`example/batch_csv/`**: Shows how to handle batch processing of CSV files.
- **`example/simple_ui/`**: A simple Flask web application adapter acting over the framework core.
- **`example/multi_module/`**: Demonstrates inter-module communication using EventBus.

For example, to run the Multi-Module example:
```bash
python example/multi_module/main.py
```

## Running Tests

The framework comes with a full suite of tests. Run them using `pytest` to ensure everything is working correctly:

```bash
python -m pytest tests/ --cov=sagittarius_engine
```
