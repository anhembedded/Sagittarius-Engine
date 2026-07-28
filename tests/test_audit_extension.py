import pytest
from unittest.mock import Mock, MagicMock
from sagittarius_engine.extensions.audit.audit_service import AuditService
from sagittarius_engine.extensions.audit.audit_extension import AuditExtension
from sagittarius_engine.interfaces import IEngineContext


def test_audit_service_telemetry_collection():
    """
    [Unit Test - UT]
    Verifies AuditService securely extracts telemetry from duck-typed context properties.
    """
    # Mock the context heavily
    mock_context = MagicMock(spec=IEngineContext)
    
    # Mock extension manager
    mock_ext_manager = MagicMock()
    mock_ext1 = MagicMock()
    mock_ext1.descriptor.name = "TestExtension"
    mock_ext1.descriptor.version = "1.2.3"
    mock_ext1.descriptor.enabled = True
    mock_ext_manager.registered_extensions = [mock_ext1]
    mock_context.extension_manager = mock_ext_manager
    
    # Mock hosted services
    mock_hs_manager = MagicMock()
    mock_hs1 = MagicMock()
    mock_hs1.__class__.__name__ = "TestService"
    mock_hs_manager.started_services = [mock_hs1]
    mock_context.hosted_services = mock_hs_manager
    
    # Init service
    service = AuditService(mock_context)
    
    assert service.get_uptime_seconds() >= 0
    
    exts = service.get_loaded_extensions()
    assert len(exts) == 1
    assert exts[0]["name"] == "TestExtension"
    assert exts[0]["enabled"] is True
    
    srvs = service.get_running_hosted_services()
    assert len(srvs) == 1
    assert srvs[0] == "TestService"

def test_audit_service_active_tasks_and_config():
    """
    [Unit Test - UT]
    Verifies AuditService properly queries TaskManager and Config/EventBus.
    """
    mock_context = MagicMock(spec=IEngineContext)
    
    # Mock Task Manager
    from datetime import datetime, timezone, timedelta
    mock_task = MagicMock()
    mock_task.name = "MyTestTask"
    mock_task.status = "running"
    mock_task.start_time = datetime.now(timezone.utc) - timedelta(seconds=5)
    mock_task.end_time = None
    
    mock_tasks = MagicMock()
    mock_tasks.tasks = {"test-id-123": mock_task}
    mock_context.tasks = mock_tasks
    
    # Mock EventBus & Config
    mock_eb = MagicMock()
    mock_eb._handlers = {"user.created": [lambda: None, lambda: None], "order.placed": [lambda: None]}
    mock_context.event_bus = mock_eb
    
    mock_config = MagicMock()
    mock_config._config = {"app.name": "Test", "debug": True}
    
    def resolve_mock(interface):
        if interface.__name__ == "IConfig":
            return mock_config
        return None
    mock_context.container.resolve.side_effect = resolve_mock
    
    service = AuditService(mock_context)
    
    tasks = service.get_active_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == "test-id-"
    assert tasks[0]["name"] == "MyTestTask"
    assert "5." in tasks[0]["runtime"]
    
    info = service.get_config_and_event_bus_info()
    assert info["event_bus_handlers"]["user.created"] == 2
    assert "app.name" in info["config_keys"]


def test_audit_extension_registration():
    """
    [Unit Test - UT]
    Verifies AuditExtension correctly injects its services into the EngineContext.
    """
    mock_context = MagicMock()
    
    ext = AuditExtension(enable_dashboard=True)
    ext.register(mock_context)
    
    # Should register AuditService as singleton
    mock_context.container.singleton.assert_called_once()
    args, _ = mock_context.container.singleton.call_args
    assert args[0] == AuditService
    
    # Mock resolve to return a mock AuditService
    mock_audit_service = MagicMock()
    mock_context.container.resolve.return_value = mock_audit_service
    
    # Start should call start_server
    ext.boot(mock_context)
    mock_audit_service.start_server.assert_called_once()
    
    # Shutdown should call stop_server
    ext.shutdown(mock_context)
    mock_audit_service.stop_server.assert_called_once()
