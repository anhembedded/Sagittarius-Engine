import importlib
import inspect
import pkgutil
from typing import Any
from sagittarius_engine.base.base_module import BaseModule
from sagittarius_engine.interfaces import IModule, ILogger

class ModuleLoader:
    """Responsible for discovering and loading engine extensions."""

    def __init__(self, app: Any) -> None:
        self.app = app

    def _get_logger(self) -> ILogger | None:
        try:
            from sagittarius_engine.interfaces import ILogger
            return self.app.container.resolve(ILogger)
        except Exception:
            return None

    def discover_and_load(self, package_path: str) -> None:
        """
        @brief Scans the specified package, instantiates, and registers IModules.
        """
        logger = self._get_logger()
        try:
            package = importlib.import_module(package_path)
        except ImportError as e:
            if logger:
                logger.warning(f"Could not discover package {package_path}: {e}")
            return

        if not hasattr(package, "__path__"):
            return

        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_module_name = f"{package_path}.{name}"
            try:
                sub_package = importlib.import_module(full_module_name)
                for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                    if (
                        issubclass(obj, IModule)
                        and obj is not IModule
                        and obj is not BaseModule
                    ):
                        self.app.use(obj())
            except Exception as e:
                if logger:
                    logger.error(f"Failed to load module {full_module_name}: {e}")
