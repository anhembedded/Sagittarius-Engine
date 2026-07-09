import importlib
import inspect
import pkgutil
from typing import TYPE_CHECKING
from sagittarius_engine.base.base_module import BaseModule
from sagittarius_engine.interfaces import IModule
if TYPE_CHECKING:
    from sagittarius_engine.kernel.app import App

class ModuleAutoDiscovery:
    """
    @brief Auto-discovers and loads Modules.

    @details Rules:
    - If it's a multi-file module (directory), the `__init__.py` file must act as the
      entry point and contain (or import) a class inheriting from `IModule`.
    - If it's a single-file module, the `.py` file itself must contain a class
      inheriting from `IModule`.

    @par Tutorial / Usage Example:
    @code
    # Automatically scans the "sagittarius_engine.extensions" package and registers all found IModules
    ModuleAutoDiscovery.discover("sagittarius_engine.extensions", app)
    @endcode
    """

    @staticmethod
    def discover(modules_package_str_path: str, app: 'App') -> None:
        """
        @brief Scans the specified package and loads the IModules.

        @param modules_package The string path to the modules package.
        @param app The current application instance.
        """
        try:
            package = importlib.import_module(modules_package_str_path)
        except ImportError as e:
            logger = app._get_logger()
            if logger:
                logger.warning(f'Could not discover package {modules_package_str_path}: {e}')
            return
        if not hasattr(package, '__path__'):
            return
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__):
            full_module_name = f'{modules_package_str_path}.{name}'
            try:
                sub_package = importlib.import_module(full_module_name)
                for _, obj in inspect.getmembers(sub_package, inspect.isclass):
                    if issubclass(obj, IModule) and obj is not IModule and (obj is not BaseModule):
                        app.use(obj())
            except Exception as e:
                logger = app._get_logger()
                if logger:
                    logger.error(f'Failed to load module {full_module_name}: {e}')
