from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.i_kernel_context import IKernelContext


class Lifecycle:
    def __init__(self, context: "IKernelContext") -> None:
        self._state = "created"


class EngineState(Enum):
    STOPPED = "stopped"
    BOOTING = "booting"
    BOOTED = "booted"
    STOPPING = "stopping"


class EngineLifecycle:
    """Responsible for managing engine state."""

    def __init__(self, context: "IKernelContext") -> None:
        self.context = context
        self.state = EngineState.STOPPED

    def set_booting(self) -> None:
        self.state = EngineState.BOOTING

    def set_booted(self) -> None:
        self.state = EngineState.BOOTED

    def set_stopping(self) -> None:
        self.state = EngineState.STOPPING

    def set_stopped(self) -> None:
        self.state = EngineState.STOPPED

    @property
    def is_booted(self) -> bool:
        return self.state == EngineState.BOOTED

    @property
    def is_booting(self) -> bool:
        return self.state == EngineState.BOOTING

    @property
    def is_stopping(self) -> bool:
        return self.state == EngineState.STOPPING

    @property
    def is_stopped(self) -> bool:
        return self.state == EngineState.STOPPED
