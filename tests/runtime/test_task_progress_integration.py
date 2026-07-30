from sagittarius_engine.kernel.app import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.extensions.audit.audit_service import AuditService


def test_integration_task_progress_and_audit():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()

    # Instantiate AuditService
    audit_service = AuditService(context=app.context, port=0)

    # A background task that updates progress
    def long_running_task(token):
        # We need the task handle to update progress
        pass

    # Wait, we need the background_task instance to call update_progress.
    # Usually tasks would get it from context.tasks...
    # For integration test, we can just spawn it and get the handle.
    task_handle = app.context.tasks.spawn(long_running_task, name="UploadFile")

    # Update progress
    task_handle.update_progress(45.5, "Uploading chunk 2")

    # Query AuditService
    tasks_details = audit_service.get_all_tasks_details()

    # Verify AuditService sees the progress
    found = False
    for t in tasks_details:
        if t["id"] == task_handle.id:
            assert t["progress"] == 45.5
            assert t["status"] in ("running", "completed")
            found = True

    assert found, "Task should be in AuditService output"
