# Student Management Application

A complete, production-grade console and desktop management application demonstrating the capabilities of the **Sagittarius Engine** framework.

This application adheres strictly to **Clean Architecture** and uses a dual-UI presentation system: an interactive terminal menu and a PySide6 GUI monitor running in a single process.

---

## 📖 Architecture & Design Patterns

The project is structured according to Clean Architecture guidelines to isolate core business rules (Domain) from frameworks, user interfaces, and databases.

```
                      ┌─────────────────────────────────────────┐
                      │              Presentation               │
                      │   (TerminalMenu UI / PySide6 Window)    │
                      └────────────────────┬────────────────────┘
                                           │ (Dispatches DTOs)
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │            Application Layer            │
                      │     (Commands, Queries, Handlers)       │
                      └────────────────────┬────────────────────┘
                                           │ (Injects Interfaces)
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │              Domain Layer               │
                      │    (Student Model, Validation Rules)    │
                      └─────────────────────────────────────────┘
                                           ▲
                                           │ (Implements Ports)
                      ┌────────────────────┴────────────────────┐
                      │          Infrastructure Layer           │
                      │ (SQLite / In-Memory Repos, MockSession) │
                      └─────────────────────────────────────────┘
```

### Applied Design Patterns

* **Mediator Pattern / CQRS**: Commands and Queries are separated (Write vs. Read) and dispatched through the central `app.dispatch()` mediator.
* **Repository Pattern**: Business logic interacts with students via the abstract `IStudentRepository` interface, decoupling the database adapter from handlers.
* **Hosted Service Pattern**: The Terminal CLI loop is wrapped as an `IHostedService` spawned as a background task.
* **Observer Pattern**: The `IEventBus` handles asynchronous communications (e.g., student mutations, progress reports, health updates) between worker threads and UI listeners.
* **Thread-Safe Signal Bridge**: An `EventBridge` uses Qt Signals & Slots to safely marshal background multi-threaded EventBus notifications to PySide6's main GUI thread.
* **Decorator / Interceptor Pattern**: Overrides `MemoryEventBus.emit` to universally log and print every application event to the GUI.

### 🧩 Component Diagram

```mermaid
graph TB
    subgraph Presentation [Presentation Layer]
        TUI[Terminal Menu CLI]
        GUI[PySide6 Monitor GUI]
        Bridge[EventBridge Signal Router]
    end

    subgraph AppCore [Application Core]
        Kernel[App Kernel Facade]
        Bus[Memory Event Bus]
        DI[StdLib DI Container]
        Pipeline[Middleware Pipeline]
    end

    subgraph Infrastructure [Infrastructure Layer]
        Repo[SqliteStudentRepository]
        Session[MockSession Adapter]
        DB[(SQLite File: students.db)]
    end

    TUI -->|Queries/Commands| Kernel
    Kernel -->|Resolves deps| DI
    Kernel -->|Invokes pipeline| Pipeline
    Pipeline -->|Mutates state| Repo
    Repo -->|Uses transaction| Session
    Repo -->|Reads/Writes| DB
    
    Kernel -->|Publishes| Bus
    Bus -->|Raw Events| Bridge
    Bridge -->|Qt Signals| GUI
```

### 👥 Class Relationships

```mermaid
classDiagram
    direction TB
    class Student {
        +str id
        +str student_id
        +str full_name
        +int age
        +str gender
        +str major
        +float gpa
    }

    class IStudentRepository {
        <<interface>>
        +add(student: Student) void
        +update(student: Student) void
        +delete(uuid: str) void
        +get_by_id(uuid: str) Student
        +get_all() list~Student~
    }

    class SqliteStudentRepository {
        -str db_path
        +add(student: Student) void
        +update(student: Student) void
    }

    class InMemoryStudentRepository {
        -dict students
        +add(student: Student) void
    }

    IStudentRepository <|.. SqliteStudentRepository : implements
    IStudentRepository <|.. InMemoryStudentRepository : implements
    SqliteStudentRepository ..> Student : manages
    InMemoryStudentRepository ..> Student : manages

    class AddStudentCommandHandler {
        -IStudentRepository repo
        -IEventBus event_bus
        +execute(cmd: AddStudentCommand) Student
    }
    
    AddStudentCommandHandler --> IStudentRepository : depends on
    AddStudentCommandHandler ..> Student : instantiates

    class MainWindow {
        -App app
        -EventBridge bridge
        -IStudentRepository repo
        +on_student_added(student) void
    }

    MainWindow --> IStudentRepository : queries
    MainWindow --> EventBridge : listens
```

### 🌐 Deployment Topology

```mermaid
graph TB
    subgraph Host [Host Machine OS Environment]
        subgraph Process [Python Process: python.exe]
            subgraph Thread1 [Main GUI Thread]
                QtApp[QApplication Event Loop]
                GUIWindow[PySide6 Monitor Window]
            end

            subgraph Thread2 [Background Worker Thread]
                TUI_Loop[TerminalMenu CLI Loop]
            end

            subgraph Thread3 [Scheduler Thread]
                Sched[Sagittarius Scheduler Loop]
            end

            subgraph Thread4 [Asyncio Loop Thread]
                AsyncLoop[Asyncio Event Loop]
            end
        end

        subgraph Storage [Filesystem Storage]
            SqliteDB[(SQLite File: students.db)]
        end
    end

    QtApp -.-> GUIWindow
    TUI_Loop -.->|Standard I/O| OS_Console(Terminal Console stdin/stdout)
    Process -->|SQLite Protocol| SqliteDB
```

### 🧵 Module-to-Thread Mapping

The following table and diagram detail which thread runs each application module and how events are dispatched:

| Module / Extension | Thread Context | Concurrency Model & Lifecycle |
| :--- | :--- | :--- |
| **PySide6 Monitor GUI** | **Main Thread** (`MainThread`) | UI thread running the blocking `QApplication.exec()` loop. |
| **TerminalMenu UI** | **`SagittariusTask-X`** (Worker Pool Thread) | Spawned via `TaskManager` as a background hosted service to await standard input. |
| **Scheduler Module** | **`SagittariusScheduler`** (Daemon Thread) | Dedicated scheduler loop waking up on a Condition variable to trigger events. |
| **AsyncRuntime Module** | **`AsyncRuntimeLoop`** (Daemon Thread) | Event loop thread running `asyncio.run_forever()` for asyncio handlers. |
| **HealthExtension Diagnostics** | Dynamic (runs on caller's thread) | Runs synchronously on whichever thread invokes the query (TUI thread or Scheduler thread). |
| **MemoryEventBus** | Dynamic (runs on publisher's thread) | Executes handlers and maps callback loops synchronously on the publishing thread. |

```mermaid
graph TD
    subgraph Process [Python Process: python.exe]
        subgraph MainThread [Main GUI Thread]
            GUI[PySide6 Monitor Window]:::mainThread
            QtApp[QApplication Loop]:::mainThread
        end

        subgraph WorkerPool [TaskManager Thread Pool]
            TUI[TerminalMenu Hosted Loop]:::tuiThread
            ReportJob[GenerateReport Job]:::tuiThread
        end

        subgraph SchedThread [Scheduler Thread]
            Sched[Scheduler Daemon Loop]:::schedThread
            HealthJob[Health Check Job]:::schedThread
        end

        subgraph AsyncThread [Async Runtime Thread]
            Async[Asyncio Event Loop]:::asyncThread
        end
    end

    classDef mainThread fill:#e06c75,stroke:#333,stroke-width:1px,color:#000;
    classDef tuiThread fill:#98c379,stroke:#333,stroke-width:1px,color:#000;
    classDef schedThread fill:#e5c07b,stroke:#333,stroke-width:1px,color:#000;
    classDef asyncThread fill:#61afef,stroke:#333,stroke-width:1px,color:#000;
```

---



## 🛠️ Key Features

1. **Full Student CRUD**: Add, Edit, Delete, List, and Search students with validation constraints (Name length, Age, GPA limits).
2. **Persistent Storage**: Utilizes SQLite database storage (`students.db`), reading target paths through the framework's `IConfig` provider.
3. **Middleware Pipeline**: Requests pass through a 5-layer pipeline:
   - `LoggingMiddleware`
   - `TimingMiddleware`
   - `ValidationMiddleware`
   - `TransactionMiddleware` (commits mock transactions on success, rolls back on exceptions)
   - `StudentValidationMiddleware` (Pydantic validation schemas)
4. **Asynchronous Reporting**: Select option **7** to compile GPA Analytics on a background worker. It pushes progress steps (`0%` -> `25%` -> `50%` -> `75%` -> `100%`) separated by 1-second intervals.
5. **System Diagnostics**: Native `HealthExtension` monitors container resolution, EventBus integrity, and SQLite database connectivity status.
6. **Task Scheduler**: Automatically triggers periodic diagnostics check every 10 seconds.
7. **Universal Event Logging**: Captures all application lifecycle events and logs them in real-time in the PySide6 panel.

---

## 🧬 Event-Driven Data Flow

This Mermaid diagram illustrates how background actions, scheduler events, and terminal choices sync onto the GUI thread:

```mermaid
sequenceDiagram
    autonumber
    actor User as User CLI
    participant TUI as Terminal UI Thread
    participant App as Sagittarius Engine
    participant DB as SQLite DB
    participant EB as Memory EventBus
    participant Bridge as Qt EventBridge (Signals)
    participant GUI as PySide6 MainWindow (Main Thread)
    
    User->>TUI: Option 2: Add Student (name, age, gpa)
    TUI->>App: dispatch(AddStudentCommand)
    activate App
    App->>DB: INSERT INTO students
    App->>EB: emit("student.added", student)
    App-->>TUI: Student added successfully
    deactivate App
    
    Note over EB, Bridge: Interceptor catches event
    EB->>Bridge: all_events_logged.emit(event_name, data)
    activate Bridge
    Bridge-->>GUI: Slot: on_all_events_logged()
    deactivate Bridge
    GUI->>GUI: Append to event log list widget
    
    loop Every 10 Seconds (Scheduler)
        participant Scheduler as Scheduler Thread
        Scheduler->>App: query(HealthCheckQuery)
        App->>DB: Execute SELECT 1
        App-->>Scheduler: {status: HEALTHY}
        Scheduler->>EB: emit("health.updated", status)
        EB->>Bridge: health_updated.emit(status)
        Bridge-->>GUI: Slot: on_health_updated()
        GUI->>GUI: Update Footer Status Indicator
    end
```

---

## 📂 Directory Layout

```
examples/student_management/
├── app/
│   ├── commands/             # Write DTOs (Add, Edit, Delete, Report)
│   ├── contracts/            # IStudentRepository port
│   ├── handlers/             # CQRS command/query executors
│   ├── infrastructure/       # Persistence (SQLite, MockSession, Pydantic middlewares)
│   ├── models/               # Domain Entity (Student) and validation exceptions
│   ├── queries/              # Read DTOs (List, Search, Get)
│   └── ui/                   # UI Presentation (TerminalMenu, PySide6 GUI Monitor)
├── main.py                   # Composition Root and application startup entry
├── README.md                 # Documentation
└── tests/
    └── test_student_app.py   # Complete Unit and Integration suite
```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have installed the required virtual environment dependencies:
```powershell
pip install PySide6 pydantic sqlalchemy
```

### Running the Application

Launch the application directly from the root workspace directory:
```powershell
python examples/student_management/main.py
```

* This starts the **Interactive Terminal Menu** in your terminal window and spawns the **PySide6 Monitor GUI** on the desktop simultaneously.
* Type options (1 to 9) in the terminal to view, insert, update, or remove database entries. The Desktop monitor table, logs, and footer health status indicators will update immediately in the background.

---

## 🧪 Testing

To run the verification suite:
```powershell
pytest examples/student_management/tests/test_student_app.py
```

The test suite covers:
* Strict domain validation rules (empty fields, age, or GPA limits).
* Integrity constraints (duplicate Student ID checks).
* Use-case handling (CRUD operations dispatched through `app.dispatch`).
* Multi-threaded asynchronous report generation.
* Configuration injection and cross-lifecycle persistence.
