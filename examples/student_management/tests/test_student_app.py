import pytest
import threading
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.interfaces import IConfig, IEventBus
from sagittarius_engine.infrastructure.config.dict_config import DictConfig

# Domain Models & Exceptions
from examples.student_management.domain.student import (
    Student,
    EmptyNameError,
    InvalidAgeError,
    InvalidGPAError,
    DuplicateStudentIDError,
    StudentNotFoundError,
)

# Application Layer Contracts & UseCases
from examples.student_management.application.contracts.student_repository import IStudentRepository
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
from examples.student_management.application.use_cases.add_student_use_case import AddStudentUseCase
from examples.student_management.application.use_cases.update_student_use_case import UpdateStudentUseCase
from examples.student_management.application.use_cases.delete_student_use_case import DeleteStudentUseCase
from examples.student_management.application.use_cases.list_students_use_case import ListStudentsUseCase
from examples.student_management.application.use_cases.search_students_use_case import SearchStudentsUseCase
from examples.student_management.application.use_cases.get_student_use_case import GetStudentUseCase
from examples.student_management.application.use_cases.generate_report_use_case import GenerateReportUseCase

# Infrastructure Adapters
from examples.student_management.infrastructure.sqlite_student_repo import SqliteStudentRepository


from typing import Generator


@pytest.fixture
def app() -> Generator[App, None, None]:
    import os

    db_file = "test_students.db"
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except OSError:
            pass

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IConfig, DictConfig(initial_data={"database.path": db_file}))
    container.singleton(IEventBus, event_bus)
    container.singleton(IStudentRepository, lambda c: c.resolve(SqliteStudentRepository))

    container.bind(AddStudentUseCase, AddStudentUseCase)
    container.bind(UpdateStudentUseCase, UpdateStudentUseCase)
    container.bind(DeleteStudentUseCase, DeleteStudentUseCase)
    container.bind(ListStudentsUseCase, ListStudentsUseCase)
    container.bind(SearchStudentsUseCase, SearchStudentsUseCase)
    container.bind(GetStudentUseCase, GetStudentUseCase)
    container.bind(GenerateReportUseCase, GenerateReportUseCase)

    app.boot()
    yield app
    app.stop()

    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except OSError:
            pass


def test_domain_model_validations() -> None:
    # 1. Invalid Name
    with pytest.raises(EmptyNameError):
        Student("1", "STD001", " ", 20, "Male", "CS", 3.5)

    # 2. Invalid Age
    with pytest.raises(InvalidAgeError):
        Student("2", "STD002", "John Doe", -5, "Male", "CS", 3.5)
    with pytest.raises(InvalidAgeError):
        Student("2", "STD002", "John Doe", 200, "Male", "CS", 3.5)

    # 3. Invalid GPA
    with pytest.raises(InvalidGPAError):
        Student("3", "STD003", "John Doe", 20, "Male", "CS", -0.5)
    with pytest.raises(InvalidGPAError):
        Student("3", "STD003", "John Doe", 20, "Male", "CS", 4.5)


def test_add_student_workflow(app: App) -> None:
    cmd = AddStudentCommand(
        student_id="STD001",
        full_name="Alice Smith",
        age=21,
        gender="Female",
        major="Computer Science",
        gpa=3.8,
    )
    student = app.dispatch(AddStudentUseCase, cmd)

    assert student.id is not None
    assert student.student_id == "STD001"
    assert student.full_name == "Alice Smith"
    assert student.age == 21
    assert student.gpa == 3.8

    # Assert duplicate student ID exception
    with pytest.raises(DuplicateStudentIDError):
        app.dispatch(AddStudentUseCase, cmd)


def test_query_and_search_workflows(app: App) -> None:
    # Add two students
    app.dispatch(
        AddStudentUseCase,
        AddStudentCommand("STD001", "Alice Smith", 21, "Female", "CS", 3.8),
    )
    bob = app.dispatch(
        AddStudentUseCase,
        AddStudentCommand("STD002", "Bob Johnson", 22, "Male", "Math", 3.2),
    )

    # 1. List Students
    students = app.dispatch(ListStudentsUseCase, ListStudentsQuery())
    assert len(students) == 2

    # 2. Get Student by UUID
    retrieved = app.dispatch(GetStudentUseCase, GetStudentQuery(id=bob.id))
    assert retrieved.student_id == "STD002"
    assert retrieved.full_name == "Bob Johnson"

    # 3. Search by Name (Substring)
    matches = app.dispatch(SearchStudentsUseCase, SearchStudentsQuery(term="alice"))
    assert len(matches) == 1
    assert matches[0].student_id == "STD001"

    # 4. Search by Student ID (Exact match)
    matches_id = app.dispatch(SearchStudentsUseCase, SearchStudentsQuery(term="STD002"))
    assert len(matches_id) == 1
    assert matches_id[0].full_name == "Bob Johnson"


def test_update_and_delete_workflows(app: App) -> None:
    alice = app.dispatch(
        AddStudentUseCase,
        AddStudentCommand("STD001", "Alice Smith", 21, "Female", "CS", 3.8),
    )

    # 1. Update Student
    update_cmd = UpdateStudentCommand(
        id=alice.id,
        student_id="STD001",
        full_name="Alice A. Smith",
        age=22,
        gender="Female",
        major="Data Science",
        gpa=3.9,
    )
    updated = app.dispatch(UpdateStudentUseCase, update_cmd)
    assert updated.full_name == "Alice A. Smith"
    assert updated.age == 22
    assert updated.major == "Data Science"
    assert updated.gpa == 3.9

    # 2. Delete Student
    app.dispatch(DeleteStudentUseCase, DeleteStudentCommand(id=alice.id))

    # Verify student is removed
    students = app.dispatch(ListStudentsUseCase, ListStudentsQuery())
    assert len(students) == 0

    # Getting student should now throw NotFound
    with pytest.raises(StudentNotFoundError):
        app.dispatch(GetStudentUseCase, GetStudentQuery(id=alice.id))


def test_async_report_generation(app: App) -> None:
    # Add a student to calculate GPA average
    app.dispatch(
        AddStudentUseCase,
        AddStudentCommand("STD001", "Alice Smith", 21, "Female", "CS", 4.0),
    )

    report_result = None
    event_received = threading.Event()

    def on_report_completed(report_content: str) -> None:
        nonlocal report_result
        report_result = report_content
        event_received.set()

    # Register listener on EventBus
    app.event_bus.on("report.completed", on_report_completed)

    # Dispatch GenerateReportCommand (returns immediately)
    msg = app.dispatch(GenerateReportUseCase, GenerateReportCommand())
    assert msg == "Async GPA report generation started."

    # Wait for background task to complete (timeout 6.0s since we sleep 4.0s)
    success = event_received.wait(timeout=6.0)
    assert success, "Async report generation timed out"
    assert report_result is not None and "Average GPA = 4.00" in report_result


def test_persistence_across_app_lifecycle() -> None:
    db_file = "test_lifecycle_students.db"
    import os
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except OSError:
            pass

    # 1. Setup first app session, add a student, and shutdown
    container1 = StdLibContainer()
    event_bus1 = MemoryEventBus()
    app1 = App(container1, event_bus1)
    container1.singleton(IConfig, DictConfig(initial_data={"database.path": db_file}))
    container1.singleton(IEventBus, event_bus1)
    container1.singleton(IStudentRepository, lambda c: c.resolve(SqliteStudentRepository))
    container1.bind(AddStudentUseCase, AddStudentUseCase)

    app1.boot()
    
    app1.dispatch(
        AddStudentUseCase,
        AddStudentCommand("STD777", "Alice Persistent", 20, "Female", "CS", 3.9)
    )
    app1.stop()

    # 2. Setup second app session with same database file, retrieve and verify
    container2 = StdLibContainer()
    event_bus2 = MemoryEventBus()
    app2 = App(container2, event_bus2)
    container2.singleton(IConfig, DictConfig(initial_data={"database.path": db_file}))
    container2.singleton(IEventBus, event_bus2)
    container2.singleton(IStudentRepository, lambda c: c.resolve(SqliteStudentRepository))
    container2.bind(ListStudentsUseCase, ListStudentsUseCase)

    app2.boot()
    
    students = app2.dispatch(ListStudentsUseCase, ListStudentsQuery())
    assert len(students) == 1
    assert students[0].student_id == "STD777"
    assert students[0].full_name == "Alice Persistent"
    app2.stop()

    # Clean up test DB file
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except OSError:
            pass
