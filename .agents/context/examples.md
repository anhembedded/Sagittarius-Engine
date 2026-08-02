# Examples

The `examples/` directory provides runnable references on how to structure a Sagittarius Engine application.

## 1. Student Management (`examples/student_management/`)

A robust example showcasing **Clean Architecture** and **CQRS**.

### Key Patterns Demonstrated:
- **CQRS**: Separates write operations (`AddStudentCommand`) from read operations (`GenerateReportQuery`). Handled by `AddStudentUseCase` and `GenerateReportUseCase`.
- **Domain Events**: Uses the `EventBus` to emit events like `StudentAddedEvent` and `ReportGeneratedEvent`.
- **BackgroundService**: The `TerminalMenu` is implemented as an `IHostedService` (specifically a `BackgroundService`), allowing the user CLI loop to run on a background daemon thread non-blockingly while the Engine runtime manages the lifecycle.
- **Dependency Injection**: Maps interfaces like `IStudentRepository` to `InMemoryStudentRepository` within `StudentModule.register()`.

### How to Run:
```bash
python examples/student_management/main.py
```
