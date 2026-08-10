from unittest.mock import MagicMock
from sagittarius_engine.extensions.audit.audit_service import AuditService

def test_audit_service_task_leak():
    """
    [Unit Test]
    Verifies that get_all_tasks_details does not leak the raw exception
    to the returned dictionary.
    """
    context = MagicMock()
    context.tasks = MagicMock()

    # Mocking a task that failed with an error
    class MockTask:
        def __init__(self):
            self.id = "123"
            self.name = "Test Task"
            self.status = "Failed"
            self.progress = 0.0
            self.start_time = None
            self.error = ValueError("Database connection failed: password incorrect")

    context.tasks.tasks = {"123": MockTask()}

    audit_service = AuditService(context)
    audit_service._logger = MagicMock()

    details = audit_service.get_all_tasks_details()

    assert len(details) == 1

    # The external facing details should not contain the exact error string
    assert details[0]["error"] == "An internal error occurred."

    # Verify the actual error was logged internally
    audit_service._logger.error.assert_called_once()
    assert "Database connection failed" in audit_service._logger.error.call_args[0][0]

def test_audit_service_task_exception_leak():
    """
    [Unit Test]
    Verifies that get_all_tasks_details does not leak the raw exception
    to the returned dictionary when using exception instead of error.
    """
    context = MagicMock()
    context.tasks = MagicMock()

    # Mocking a task that failed with an exception
    class MockTask:
        def __init__(self):
            self.id = "123"
            self.name = "Test Task"
            self.status = "Failed"
            self.progress = 0.0
            self.start_time = None
            self.exception = ValueError("Secret API Key invalid")

    context.tasks.tasks = {"123": MockTask()}

    audit_service = AuditService(context)
    audit_service._logger = MagicMock()

    details = audit_service.get_all_tasks_details()

    assert len(details) == 1

    # The external facing details should not contain the exact error string
    assert details[0]["error"] == "An internal error occurred."

    # Verify the actual exception was logged internally
    audit_service._logger.error.assert_called_once()
    assert "Secret API Key invalid" in audit_service._logger.error.call_args[0][0]
