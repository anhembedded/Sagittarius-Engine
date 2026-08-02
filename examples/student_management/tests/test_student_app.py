from typing import Generator
import os
import pytest

from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.interfaces import IConfig, IEventBus
from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from sagittarius_engine.extensions.logger.logger_module import LoggerExtension
from examples.student_management.student_module import StudentModule

from examples.student_management.domain.events import ReportCompletedEvent
from sagittarius_engine.runtime.tasks.events import TaskProgressUpdated
from examples.student_management.domain.student import (
    Student,
    EmptyNameError,
    InvalidAgeError,
    InvalidGPAError,
    DuplicateStudentIDError,
    StudentNotFoundError,
)

# Application Layer Contracts & UseCases
from examples.student_management.application.contracts.use_case_ports import (
    IAddStudentUseCase,
    IUpdateStudentUseCase,
    IDeleteStudentUseCase,
    IListStudentsUseCase,
    ISearchStudentsUseCase,
    IGetStudentUseCase,
    IGenerateReportUseCase,
)
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


@pytest.fixture
def app() -> Generator[App, None, None]:
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

    app.use(LoggerExtension())
    app.use(StudentModule())

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
    # Track events
    added_events = []
    app.event_bus.on("student.added", lambda s: added_events.append(s))

    # 1. Successful Add
    cmd = AddStudentCommand("STD001", "John Doe", 20, "Male", "CS", 3.5)
    student = app.dispatch(IAddStudentUseCase, cmd)

    assert student.student_id == "STD001"
    assert student.full_name == "John Doe"
    assert len(added_events) == 1
    event_student = (
        added_events[0].student
        if hasattr(added_events[0], "student")
        else added_events[0]
    )
    assert event_student.student_id == "STD001"

    # 2. Duplicate Student ID
    with pytest.raises(DuplicateStudentIDError):
        app.dispatch(IAddStudentUseCase, cmd)


def test_query_and_search_workflows(app: App) -> None:
    # Add initial dataset
    s1 = app.dispatch(
        IAddStudentUseCase,
        AddStudentCommand("STD001", "Alice Smith", 21, "Female", "CS", 3.8),
    )
    app.dispatch(
        IAddStudentUseCase,
        AddStudentCommand("STD002", "Bob Johnson", 22, "Male", "EE", 3.2),
    )

    # 1. List All Students
    all_students = app.dispatch(IListStudentsUseCase, ListStudentsQuery())
    assert len(all_students) == 2

    # 2. Get Student by internal ID
    student = app.dispatch(IGetStudentUseCase, GetStudentQuery(s1.id))
    assert student.full_name == "Alice Smith"

    # 3. Get Non-existent Student
    with pytest.raises(StudentNotFoundError):
        app.dispatch(IGetStudentUseCase, GetStudentQuery("non-existent-uuid"))

    # 4. Search by Name / Major
    results = app.dispatch(ISearchStudentsUseCase, SearchStudentsQuery("Alice"))
    assert len(results) == 1
    assert results[0].student_id == "STD001"

    results_ee = app.dispatch(ISearchStudentsUseCase, SearchStudentsQuery("EE"))
    assert len(results_ee) == 1
    assert results_ee[0].student_id == "STD002"


def test_update_and_delete_workflows(app: App) -> None:
    updated_events = []
    deleted_events = []
    app.event_bus.on("student.updated", lambda s: updated_events.append(s))
    app.event_bus.on("student.deleted", lambda sid: deleted_events.append(sid))

    student = app.dispatch(
        IAddStudentUseCase,
        AddStudentCommand("STD001", "Charlie Brown", 20, "Male", "CS", 3.0),
    )

    # 1. Update Student
    update_cmd = UpdateStudentCommand(
        student.id, "STD001", "Charlie B.", 21, "Male", "Software Eng", 3.7
    )
    updated = app.dispatch(IUpdateStudentUseCase, update_cmd)

    assert updated.full_name == "Charlie B."
    assert updated.gpa == 3.7
    assert len(updated_events) == 1

    # 2. Delete Student
    del_cmd = DeleteStudentCommand(student.id)
    app.dispatch(IDeleteStudentUseCase, del_cmd)
    assert len(deleted_events) == 1
    deleted_payload = (
        deleted_events[0].student_id
        if hasattr(deleted_events[0], "student_id")
        else deleted_events[0]
    )
    assert deleted_payload == student.id

    # Verify student is gone
    with pytest.raises(StudentNotFoundError):
        app.dispatch(IGetStudentUseCase, GetStudentQuery(student.id))


def test_async_report_generation(app: App) -> None:
    import time

    completed_reports = []
    progress_updates = []

    app.event_bus.on(
        ReportCompletedEvent,
        lambda e: completed_reports.append(e.report_content),
    )
    app.event_bus.on(TaskProgressUpdated, lambda e: progress_updates.append(e.progress))

    app.dispatch(
        IAddStudentUseCase,
        AddStudentCommand("STD001", "Student A", 20, "Male", "CS", 4.0),
    )

    # Trigger Async Report Generation Task
    result = app.dispatch(IGenerateReportUseCase, GenerateReportCommand())
    assert "report generation started" in result.lower()

    # Wait for background task to complete
    timeout = 5.0
    start = time.time()
    while len(completed_reports) == 0 and (time.time() - start) < timeout:
        time.sleep(0.05)

    assert len(completed_reports) == 1
    assert "Report Summary" in completed_reports[0]
    assert len(progress_updates) > 0


def test_persistence_across_app_lifecycle() -> None:
    db_file = "test_lifecycle_students.db"
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
    app1.use(LoggerExtension())
    app1.use(StudentModule())

    app1.boot()

    app1.dispatch(
        IAddStudentUseCase,
        AddStudentCommand("STD777", "Alice Persistent", 20, "Female", "CS", 3.9),
    )
    app1.stop()

    # 2. Setup second app session with same database file, retrieve and verify
    container2 = StdLibContainer()
    event_bus2 = MemoryEventBus()
    app2 = App(container2, event_bus2)
    container2.singleton(IConfig, DictConfig(initial_data={"database.path": db_file}))
    container2.singleton(IEventBus, event_bus2)
    app2.use(LoggerExtension())
    app2.use(StudentModule())

    app2.boot()

    students = app2.dispatch(IListStudentsUseCase, ListStudentsQuery())
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
