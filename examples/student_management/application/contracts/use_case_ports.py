# Clean Architecture - Application Layer Use Case Ports (Pure ABCs)
# These interfaces define the contract for each use case.
# Presentation and Infrastructure layers depend ONLY on these, never on concrete classes.
from abc import abstractmethod
from typing import Sequence

from examples.student_management.application.dtos.commands import (
    AddStudentCommand,
    UpdateStudentCommand,
    DeleteStudentCommand,
    GenerateReportCommand,
)
from examples.student_management.application.dtos.queries import (
    ListStudentsQuery,
    SearchStudentsQuery,
    GetStudentQuery,
)
from examples.student_management.domain.student import Student
from sagittarius_engine.extensions.cqrs import ICommand, IQuery


class IAddStudentUseCase(ICommand[AddStudentCommand, Student]):
    @abstractmethod
    def execute(self, command: AddStudentCommand) -> Student: ...


class IUpdateStudentUseCase(ICommand[UpdateStudentCommand, Student]):
    @abstractmethod
    def execute(self, command: UpdateStudentCommand) -> Student: ...


class IDeleteStudentUseCase(ICommand[DeleteStudentCommand, None]):
    @abstractmethod
    def execute(self, command: DeleteStudentCommand) -> None: ...


class IListStudentsUseCase(IQuery[ListStudentsQuery, Sequence[Student]]):
    @abstractmethod
    def execute(self, query: ListStudentsQuery) -> Sequence[Student]: ...


class ISearchStudentsUseCase(IQuery[SearchStudentsQuery, Sequence[Student]]):
    @abstractmethod
    def execute(self, query: SearchStudentsQuery) -> Sequence[Student]: ...


class IGetStudentUseCase(IQuery[GetStudentQuery, Student]):
    @abstractmethod
    def execute(self, query: GetStudentQuery) -> Student: ...


class IGenerateReportUseCase(ICommand[GenerateReportCommand, str]):
    @abstractmethod
    def execute(self, command: GenerateReportCommand) -> str: ...
