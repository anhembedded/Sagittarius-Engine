from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, Union, Optional, TYPE_CHECKING
import inspect

if TYPE_CHECKING:
    from src.app_kernel import App
import pkgutil
import importlib

from src.interfaces.i_module import IModule

class BaseModule(IModule):
    """
    @brief Base class for Modules.
    @details Provides an empty implementation (pass) for register/boot methods.
    This allows child modules to skip defining both methods if they are not needed.
    """

    def register(self, app: 'App') -> None:
        pass

    def boot(self, app: 'App') -> None:
        pass
