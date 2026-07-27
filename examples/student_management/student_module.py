# Clean Architecture - Sagittarius BaseModule Integration
from sagittarius_engine import App
from sagittarius_engine.base import BaseModule

from examples.student_management.application.contracts.student_repository import IStudentRepository
from examples.student_management.infrastructure.sqlite_student_repo import SqliteStudentRepository
from examples.student_management.application.use_cases.add_student_use_case import AddStudentUseCase
from examples.student_management.application.use_cases.update_student_use_case import UpdateStudentUseCase
from examples.student_management.application.use_cases.delete_student_use_case import DeleteStudentUseCase
from examples.student_management.application.use_cases.list_students_use_case import ListStudentsUseCase
from examples.student_management.application.use_cases.search_students_use_case import SearchStudentsUseCase
from examples.student_management.application.use_cases.get_student_use_case import GetStudentUseCase
from examples.student_management.application.use_cases.generate_report_use_case import GenerateReportUseCase


class StudentModule(BaseModule):
    """
    Sagittarius Application Module for Student Management.
    Registers repositories & use cases in the DI container.
    """

    def register(self, app: App) -> None:
        # Register Repository
        app.container.singleton(IStudentRepository, lambda c: c.resolve(SqliteStudentRepository))

        # Register UseCase Handlers
        app.container.bind(AddStudentUseCase, AddStudentUseCase)
        app.container.bind(UpdateStudentUseCase, UpdateStudentUseCase)
        app.container.bind(DeleteStudentUseCase, DeleteStudentUseCase)
        app.container.bind(ListStudentsUseCase, ListStudentsUseCase)
        app.container.bind(SearchStudentsUseCase, SearchStudentsUseCase)
        app.container.bind(GetStudentUseCase, GetStudentUseCase)
        app.container.bind(GenerateReportUseCase, GenerateReportUseCase)

    def boot(self, app: App) -> None:
        pass
