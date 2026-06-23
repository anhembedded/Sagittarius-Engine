# Kiến trúc Tổng thể (Architecture)

Framework ứng dụng nguyên lý Clean Architecture kết hợp Event-Driven (Headless-first).

## 1. Biểu đồ tổng thể

```mermaid
graph TD
    subgraph Adapters [Adapters / UI / CLI]
        CLI[CLI Adapter]
        Web[Web / Flask Adapter]
    end

    subgraph AppKernel [Application Framework / Core]
        App[App Instance]
        Container[DI Container]
        Pipeline[Middleware Pipeline]
        EventBus[Event Bus]
    end

    subgraph ApplicationLayer [Application Services / Use Cases]
        Commands[Commands]
        Queries[Queries]
    end

    subgraph DomainLayer [Domain Entities]
        Models[Entities / Value Objects]
    end

    subgraph InfrastructureLayer [Infrastructure / IO]
        DB[Database Repositories]
        Ext[External APIs]
        Logger[StdLogger]
    end

    CLI -->|Executes| App
    Web -->|Executes| App

    App -->|Resolves| Container
    App -->|Pipes through| Pipeline
    App -->|Publishes to| EventBus

    Pipeline --> Commands
    Pipeline --> Queries

    Commands --> Models
    Queries --> Models

    Commands -->|Calls| DB
    Queries -->|Calls| DB
```

## 2. Quy tắc hướng luồng
- **Hướng vào trong**: Tất cả mọi layer bên ngoài (Adapters, Infrastructure) phải phụ thuộc vào layer bên trong (Application, Domain).
- **Core.py**: Chứa toàn bộ giao diện (`ICommand`, `IEventBus`, `IContainer`...) và class trung tâm `App`. Nó độc lập và không chứa code cụ thể liên quan tới Infra (ví dụ: `print`, `logging`, `requests`).
- **Composition Root**: File `main.py` của ứng dụng đóng vai trò làm điểm lắp ráp (Composition Root). Ở đó ta gắn kết `MemoryEventBus`, `StdLibContainer` với `App`, rồi boot các `Module`.
