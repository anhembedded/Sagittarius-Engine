import pytest
import threading
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


# Models and exceptions
from examples.student_management.app.models.student import (
    Student,
    EmptyNameError,
    InvalidAgeError,
    InvalidGPAError,
    DuplicateStudentIDError,
    StudentNotFoundError,
)

# Repository
from examples.student_management.app.contracts.student_repository import IStudentRepository
from examples.student_management.app.infrastructure.in_memory_student_repo import InMemoryStudentRepository

# Commands & Queries
from examples.student_management.app.commands.add_student import AddStudentCommand
from examples.student_management.app.commands.update_student import UpdateStudentCommand
from examples.student_management.app.commands.delete_student import DeleteStudentCommand
from examples.student_management.app.queries.list_students import ListStudentsQuery
from examples.student_management.app.queries.search_students import SearchStudentsQuery
from examples.student_management.app.queries.get_student import GetStudentQuery

# Handlers
from examples.student_management.app.handlers.add_student_handler import AddStudentCommandHandler
from examples.student_management.app.handlers.update_student_handler import UpdateStudentCommandHandler
from examples.student_management.app.handlers.delete_student_handler import DeleteStudentCommandHandler
from examples.student_management.app.handlers.list_students_handler import ListStudentsHandler
from examples.student_management.app.handlers.search_students_handler import SearchStudentsHandler
from examples.student_management.app.handlers.get_student_handler import GetStudentHandler
from examples.student_management.app.commands.generate_report import GenerateReportCommand
from examples.student_management.app.handlers.generate_report_handler import GenerateReportCommandHandler



from sagittarius_engine.interfaces import IConfig, IEventBus
from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from examples.student_management.app.infrastructure.sqlite_student_repo import SqliteStudentRepository


@pytest.fixture
def app() -> App:
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


    container.bind(AddStudentCommandHandler, AddStudentCommandHandler)
    container.bind(UpdateStudentCommandHandler, UpdateStudentCommandHandler)
    container.bind(DeleteStudentCommandHandler, DeleteStudentCommandHandler)
    container.bind(ListStudentsHandler, ListStudentsHandler)
    container.bind(SearchStudentsHandler, SearchStudentsHandler)
    container.bind(GetStudentHandler, GetStudentHandler)
    container.bind(GenerateReportCommandHandler, GenerateReportCommandHandler)

    app.boot()
    yield app
    app.stop()

    # Cleanup test DB file
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
    student = app.dispatch(AddStudentCommandHandler, cmd)

    assert student.id is not None
    assert student.student_id == "STD001"
    assert student.full_name == "Alice Smith"
    assert student.age == 21
    assert student.gpa == 3.8

    # Assert duplicate student ID exception
    with pytest.raises(DuplicateStudentIDError):
        app.dispatch(AddStudentCommandHandler, cmd)


def test_query_and_search_workflows(app: App) -> None:
    # Add two students
    app.dispatch(
        AddStudentCommandHandler,
        AddStudentCommand("STD001", "Alice Smith", 21, "Female", "CS", 3.8),
    )
    bob = app.dispatch(
        AddStudentCommandHandler,
        AddStudentCommand("STD002", "Bob Johnson", 22, "Male", "Math", 3.2),
    )

    # 1. List Students
    students = app.dispatch(ListStudentsHandler, ListStudentsQuery())
    assert len(students) == 2

    # 2. Get Student by UUID
    retrieved = app.dispatch(GetStudentHandler, GetStudentQuery(id=bob.id))
    assert retrieved.student_id == "STD002"
    assert retrieved.full_name == "Bob Johnson"

    # 3. Search by Name (Substring)
    matches = app.dispatch(SearchStudentsHandler, SearchStudentsQuery(term="alice"))
    assert len(matches) == 1
    assert matches[0].student_id == "STD001"

    # 4. Search by Student ID (Exact match)
    matches_id = app.dispatch(SearchStudentsHandler, SearchStudentsQuery(term="STD002"))
    assert len(matches_id) == 1
    assert matches_id[0].full_name == "Bob Johnson"


def test_update_and_delete_workflows(app: App) -> None:
    alice = app.dispatch(
        AddStudentCommandHandler,
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
    updated = app.dispatch(UpdateStudentCommandHandler, update_cmd)
    assert updated.full_name == "Alice A. Smith"
    assert updated.age == 22
    assert updated.major == "Data Science"
    assert updated.gpa == 3.9

    # 2. Delete Student
    app.dispatch(DeleteStudentCommandHandler, DeleteStudentCommand(id=alice.id))

    # Verify student is removed
    students = app.dispatch(ListStudentsHandler, ListStudentsQuery())
    assert len(students) == 0

    # Getting student should now throw NotFound
    with pytest.raises(StudentNotFoundError):
        app.dispatch(GetStudentHandler, GetStudentQuery(id=alice.id))


def test_async_report_generation(app: App) -> None:
    # Add a student to calculate GPA average
    app.dispatch(
        AddStudentCommandHandler,
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
    msg = app.dispatch(GenerateReportCommandHandler, GenerateReportCommand())
    assert msg == "Async GPA report generation started."

    # Wait for background task to complete (timeout 6.0s since we sleep 4.0s)
    success = event_received.wait(timeout=6.0)
    assert success, "Async report generation timed out"
    assert "Average GPA = 4.00" in report_result


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
    container1.bind(AddStudentCommandHandler, AddStudentCommandHandler)

    app1.boot()
    
    app1.dispatch(
        AddStudentCommandHandler,
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
    container2.bind(ListStudentsHandler, ListStudentsHandler)

    app2.boot()
    
    students = app2.dispatch(ListStudentsHandler, ListStudentsQuery())
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



