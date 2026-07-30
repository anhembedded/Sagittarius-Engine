from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class SystemHealth:
    status: str            # "healthy", "unhealthy"
    components: Dict[str, str] # {"database": "ok", "container": "ok"}

@dataclass(frozen=True)
class EnvironmentMetrics:
    hostname: str
    os_name: str
    python_version: str
    memory_usage_mb: float
    cpu_cores: int

@dataclass(frozen=True)
class TaskDetail:
    id: str
    name: str
    status: str            # "PENDING", "RUNNING", "DONE"
    cancelled: bool
    progress: float
    progress_message: str

@dataclass(frozen=True)
class ExtensionInfo:
    name: str
    is_active: bool

# Entity Root - Gom tất cả mọi thứ lại
@dataclass(frozen=True)
class EngineTelemetry:
    uptime_seconds: float
    health: SystemHealth
    environment: EnvironmentMetrics
    active_tasks: List[TaskDetail]
    loaded_extensions: List[ExtensionInfo]
    recent_events: List[str]
