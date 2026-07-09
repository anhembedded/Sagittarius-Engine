from typing import Any


class EngineLifecycle:
    """Responsible for managing engine state."""

    def __init__(self, context: Any) -> None:
        self.context = context
        self.state = "stopped"

    def set_booting(self) -> None:
        self.state = "booting"

    def set_booted(self) -> None:
        self.state = "booted"

    @property
    def is_booted(self) -> bool:
        return self.state == "booted"

    @property
    def is_booting(self) -> bool:
        return self.state == "booting"

    @property
    def is_stopped(self) -> bool:
        return self.state == "stopped"
