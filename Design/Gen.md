# design

```mernaid
flowchart TD
    subgraph Adapters["🖥️ Adapters Layer (Bên ngoài cùng)"]
        direction TB
        CLI["CLI Adapter"]
        UI["UI Adapter (Qt)"]
        Presenter["Presenter<br/>(gọi AppController, nhận callback)"]
        InputParser["Input Parser"]
        View["View<br/>(QMainWindow, Widgets)"]
        ViewModel["ViewModel / DTO"]
        UI --> View
        UI --> Presenter
        UI --> InputParser
        UI --> ViewModel
    end

    subgraph Core["⚙️ Application Core (Headless-first)"]
        direction TB
        IAppController["IAppController<br/><<interface>>"]
        AppControllerImpl["AppControllerImpl<br/>(Command Bus + Callback Manager)"]
        ApplicationService["ApplicationService<br/>(Use Cases / Orchestration)"]
        IStudentRepo["IStudentRepository<br/><<interface>>"]
        SSOT["In-Memory Store<br/>(Domain Data + App State)"]
        IAppController --> AppControllerImpl
        IAppController --> ApplicationService
        IAppController --> SSOT
        AppControllerImpl --> ApplicationService
        ApplicationService --> IStudentRepo
        ApplicationService --> SSOT
    end

    subgraph Domain["🏛️ Domain Layer (Trong cùng)"]
        DomainModel["Domain Model<br/>(Entities, Value Objects)"]
        DomainEvent["Domain Events"]
    end

    subgraph Infra["💾 Infrastructure Layer"]
        RepositoryImpl["RepositoryImpl<br/>(implements IStudentRepository)"]
        DB[("(Database)")]
        RepositoryImpl --> DB
    end

    %% Dependency arrows (lớp ngoài phụ thuộc vào lớp trong)
    Adapters --> Core
    Core --> Domain

    %% Infrastructure phụ thuộc vào interface của Core
    Infra --> IStudentRepo

    %% Ghi chú hướng phụ thuộc
    note1[["⬅ Mọi phụ thuộc đều hướng vào trong. Lớp bên trong không biết lớp bên ngoài."]]

```