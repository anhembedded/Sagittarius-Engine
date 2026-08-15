from enum import Enum


class UIMode(str, Enum):
    IDLE = "IDLE"
    LIVE = "LIVE"
    LOCKED = "LOCKED"
    ERROR = "ERROR"


mode = UIMode.IDLE
print("type mode:", type(mode))
print("mode.value:", getattr(mode, "value", "NO_VALUE"))
print("hasattr value:", hasattr(mode, "value"))
print("dict:", {"IDLE": 123}.get(mode.value))
