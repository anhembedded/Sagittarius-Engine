from abc import abstractmethod
from abc import ABC
import os
from enum import Enum

class OS_Type(Enum):
    WINDOWS = "Windows"
    LINUX_MAC = "Linux/Mac"

class IHelper(ABC):
    @abstractmethod
    def get_what_os() -> OS_Type:
        pass

class Helper(IHelper):
    @staticmethod
    def get_what_os() -> OS_Type:
        if os.name == "nt":
            return OS_Type.WINDOWS
        elif os.name == "posix":
            return OS_Type.LINUX_MAC
        else:
            raise ValueError("Unknown OS")


