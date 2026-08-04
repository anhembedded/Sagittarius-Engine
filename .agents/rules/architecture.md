---
name: Architecture Rules
description: Module boundaries, dependency guidelines, and strict 4-layer Clean Architecture rules for the Sagittarius Engine and application layers.
trigger: model_decision
---

# Rules: Architecture

Module boundaries, dependency guidelines, and layout rules.

## IEngineContext — God Object Prevention

`IEngineContext` must ONLY be used during the engine's Bootstrap and Extension lifecycle phase.

### ✅ Valid Usage
- Inside `IExtension.register()`, `boot()`, `shutdown()`, `boot_async()`, `shutdown_async()`.
- Inside `IHostedService.start()` and `stop()`.
- Inside Kernel orchestrators: `Bootstrap`, `AppRunner`, `ExtensionManager`.

### ❌ Invalid Usage
- Inside `domain/` layer (entities, value objects, domain services).
- Inside `application/` layer (use cases, command/query handlers, application services).
- As a constructor parameter (`__init__`) of any non-extension class.

### Correct Pattern
Register dependencies in `IExtension.register()` using `context.container`, then inject them
into use cases / handlers via the DI Container — never pass `IEngineContext` itself:

```python
# ✅ Correct
class MyExtension(IExtension):
    def register(self, context: IEngineContext) -> None:
        context.container.singleton(IMyRepo, ConcreteRepo)

class MyUseCase:  # Gets IMyRepo injected by container — NOT IEngineContext
    def __init__(self, repo: IMyRepo) -> None:
        self._repo = repo

# ❌ Wrong
class MyUseCase:
    def __init__(self, context: IEngineContext) -> None:  # God Object anti-pattern!
        self._context = context
```

## Module Boundaries

- `sagittarius_engine/interfaces/` — Pure abstractions only. No concrete imports.
- `sagittarius_engine/kernel/` — Internal orchestration. Uses `IKernelContext` not `IEngineContext`.
- `sagittarius_engine/extensions/` — Feature extensions. Depend on `IEngineContext` only.
- `sagittarius_engine/infrastructure/` — Adapters and implementations. No domain imports.

## Clean Architecture Layers (The 4 Layers)

The system is strictly divided into 4 layers following Clean Architecture principles:

### Layer 1 & 2: The Core (Lõi hệ thống)
**Responsibility:** Contains the business rules.
- **Layer 1 - Domain (Enterprise Business Rules):** Contains Entities and Value Objects (e.g., `MarketData`, `TimeFrame`). Must be **100% pure Python**. Must know absolutely nothing about the app, bot, framework (`sagittarius_engine`), or database.
- **Layer 2 - Application (Application Business Rules):** Contains Use Cases (e.g., `sync_market_data.py`, `manage_live_stream.py`) and Contracts/Ports (e.g., `IExchangeClient`, `IMarketDataRepository`, `ILiveStreamService`). Must NOT contain any API connection, framework lifecycle, or SQL logic.

### Layer 3: Interface Adapters (Tầng Giao tiếp / Chuyển đổi)
**Responsibility:** Acts as the "translator" between the Core and the Outside World.
- Transforms data from formats convenient for Use Cases to formats convenient for Database/UI, and vice versa.
- **Example (Binace_Bot):** The `src/presentation/cli/` directory. It takes raw text from the user, translates it into DTOs (e.g., `StartLiveStreamCommand`), and dispatches it to the Engine. It also takes results and prints them.
- **Note:** If a UI (e.g., PySide/Qt) is added later, all UI code belongs here. The Application layer must remain completely unaware of whether it is driven by CLI or a GUI.

### Layer 4: Infrastructure & Frameworks (Tầng Cơ sở hạ tầng)
**Responsibility:** Where the system touches hardware, network, databases, and frameworks.
- This layer contains "dirty" code full of external libraries, SDKs, and network connections. It plugs Adapters into the Ports defined by Layer 2.
- **Examples (Binace_Bot):** `src/infrastructure/` and `src/main.py`.
- **External Libraries:** `binance-python` (for API), `sqlalchemy` (for DB), and `sagittarius_engine` (for framework).
- **Concrete Adapters:**
  - `PythonBinanceClient`: Uses `binance` to satisfy `IExchangeClient`.
  - `BinanceWebsocketService`: Uses `BinanceSocketManager` to satisfy `ILiveStreamService`.
  - `SQLAlchemyMarketDataRepository`: Uses `sqlalchemy` to satisfy `IMarketDataRepository`.
- **Composition Root:** `main.py` is the "dirtiest" place where everything is imported, the DI Container is initialized, all pieces are wired together, and the system is booted.
