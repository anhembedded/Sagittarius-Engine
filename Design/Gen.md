# design

```mernaid
flowchart TB
    Entry["Entry Point<br/>(CLI / Batch / UI)"]

    subgraph Adapters["Adapters Layer"]
        CLI["CLI Adapter"]
        subgraph UI_Adapter["UI Adapter (Qt)"]
            View["View<br/>(QMainWindow, Widgets)"]
            InputParser["Input Parser"]
            Presenter["Presenter<br/>(Gọi AppController, nhận callback)"]
            ViewModel["ViewModel / DTO"]
        end
    end

    subgraph Core["Application Core (Headless-first)"]
        AppController["IAppController<br/>(Interface)"]
        AppControllerImpl["AppControllerImpl<br/>(Điều phối command, quản lý callback)"]
        ApplicationService["ApplicationService<br/>(Use Cases / Orchestration)"]
        IStudentRepo["IStudentRepository<br/><<interface>>"]
        SSOT["In-Memory Store<br/>(Domain Data + App State)"]
    end

    subgraph Domain["Domain Layer"]
        DomainModel["Domain Model<br/>(Entities, Value Objects)"]
        DomainEvent["Domain Events"]
    end

    subgraph Infra["Infrastructure"]
        RepositoryImpl["RepositoryImpl<br/>(implements IStudentRepository)"]
        DB[("(Database)")]
    end

    %% ===== Khởi tạo =====
    Entry --> CLI
    Entry --> View

    %% ===== Luồng điều khiển (chỉ qua AppController) =====
    View -- "1. Người dùng thao tác" --> InputParser
    InputParser -- "2. Dữ liệu chuẩn hóa" --> Presenter
    Presenter -- "3. Gửi Command (kèm callback)" --> AppController
    CLI -- "3b. Gửi Command (kèm callback)" --> AppController

    AppController -- "4. Gọi Use Case tương ứng" --> ApplicationService
    ApplicationService -- "5. Thao tác Domain" --> DomainModel
    DomainModel -- "6. Tạo sự kiện" --> DomainEvent
    DomainEvent -- "7. Trả về ApplicationService" --> ApplicationService

    ApplicationService -- "8. Gọi interface lưu trữ" --> IStudentRepo
    IStudentRepo -. "9. triển khai bởi" .-> RepositoryImpl
    RepositoryImpl -- "10. Kết nối" --> DB

    ApplicationService -- "11. Cập nhật SSOT (nếu cần)" --> SSOT

    %% ===== Trả kết quả (callback) =====
    ApplicationService -- "12. Trả kết quả (Result/Data)" --> AppController
    AppController -- "13. Gọi callback cho UI" --> Presenter
    AppController -- "13b. Gọi callback cho CLI" --> CLI

    Presenter -- "14. Tạo ViewModel" --> ViewModel
    ViewModel -- "15. Cập nhật View" --> View

```