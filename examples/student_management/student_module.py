# Clean Architecture - Sagittarius BaseModule Integration
from sagittarius_engine import App
from sagittarius_engine.base import BaseModule

from examples.student_management.application.contracts.student_repository import (
    IStudentRepository,
)
from examples.student_management.infrastructure.sqlite_student_repo import (
    SqliteStudentRepository,
)

# Use Case Ports (interfaces) — Presentation/Infrastructure depend only on these
from examples.student_management.application.contracts.use_case_ports import (
    IAddStudentUseCase,
    IUpdateStudentUseCase,
    IDeleteStudentUseCase,
    IListStudentsUseCase,
    ISearchStudentsUseCase,
    IGetStudentUseCase,
    IGenerateReportUseCase,
)

# Concrete Implementations — only imported here at the Composition Root
from examples.student_management.application.use_cases.add_student_use_case import (
    AddStudentUseCase,
)
from examples.student_management.application.use_cases.update_student_use_case import (
    UpdateStudentUseCase,
)
from examples.student_management.application.use_cases.delete_student_use_case import (
    DeleteStudentUseCase,
)
from examples.student_management.application.use_cases.list_students_use_case import (
    ListStudentsUseCase,
)
from examples.student_management.application.use_cases.search_students_use_case import (
    SearchStudentsUseCase,
)
from examples.student_management.application.use_cases.get_student_use_case import (
    GetStudentUseCase,
)
from examples.student_management.application.use_cases.generate_report_use_case import (
    GenerateReportUseCase,
)


class StudentModule(BaseModule):
    """
    Sagittarius Application Module for Student Management.
    Registers repositories & use cases in the DI container.
    Concrete classes are hidden behind their port interfaces — callers
    never import the implementation directly.
    """

    def register(self, app: App) -> None:
        # Register Repository
        app.container.singleton(IStudentRepository, SqliteStudentRepository)

        # Bind UseCase Ports → Concrete Implementations
        # Callers dispatch via interface (e.g. app.dispatch(IAddStudentUseCase, cmd))
        # The container resolves the interface to the concrete class with all deps injected.
        app.container.bind(IAddStudentUseCase, AddStudentUseCase)
        app.container.bind(IUpdateStudentUseCase, UpdateStudentUseCase)
        app.container.bind(IDeleteStudentUseCase, DeleteStudentUseCase)
        app.container.bind(IListStudentsUseCase, ListStudentsUseCase)
        app.container.bind(ISearchStudentsUseCase, SearchStudentsUseCase)
        app.container.bind(IGetStudentUseCase, GetStudentUseCase)
        app.container.bind(IGenerateReportUseCase, GenerateReportUseCase)

    def boot(self, app: App) -> None:
        pass
