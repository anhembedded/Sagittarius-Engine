# Student Management Architecture
```text
examples/student_management/
├── domain/                                      # Pure Python STDLIB Layer
│   ├── student.py                               # Student Entity & Domain Exceptions
│   └── events.py                                # Domain Events (inheriting BaseEvent)
│
├── application/                                 # Use Cases, Ports & DTOs
│   ├── contracts/
│   │   ├── student_repository.py                # IStudentRepository (Persistence Port)
│   │   └── student_monitor_view.py              # IStudentMonitorView (MVP View Port)
│   ├── dtos/
│   │   ├── commands.py                          # Add/Update/Delete/GenerateReport Commands
│   │   └── queries.py                           # List/Search/Get Queries
│   └── use_cases/
│       ├── add_student_use_case.py              # AddStudentUseCase
│       ├── update_student_use_case.py           # UpdateStudentUseCase
│       ├── delete_student_use_case.py           # DeleteStudentUseCase
│       ├── list_students_use_case.py            # ListStudentsUseCase
│       ├── search_students_use_case.py          # SearchStudentsUseCase
│       ├── get_student_use_case.py              # GetStudentUseCase
│       └── generate_report_use_case.py          # GenerateReportUseCase
│
├── infrastructure/                              # Technical Adapters
│   ├── sqlite_student_repo.py                   # SqliteStudentRepository
│   └── in_memory_student_repo.py                # InMemoryStudentRepository
│
├── presentation/                                # MVP Presentation Layer
│   ├── presenters/
│   │   └── student_monitor_presenter.py         # StudentMonitorPresenter (MVP Mediator)
│   ├── ui/
│   │   ├── event_bridge.py                      # Qt Signal Bridge
│   │   └── desktop_window.py                    # Passive View (MainWindow implementing IStudentMonitorView)
│   └── cli/
│       └── terminal_menu.py                     # CLI Hosted Service Interface
│
├── student_module.py                            # BaseModule DI Configuration
├── main.py                                      # Composition Root
└── tests/
    └── test_student_app.py                      # Application Unit & Lifecycle Tests
```