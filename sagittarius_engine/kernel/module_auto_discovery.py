from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sagittarius_engine.kernel.app import App


class ModuleAutoDiscovery:
    """
    @brief Auto-discovers and loads Modules.

    @details Re-delegates discovery logic to ModuleLoader for backwards compatibility.
    """

    @staticmethod
    def discover(modules_package_str_path: str, app: "App") -> None:
        """
        @brief Scans the specified package and loads the IModules.

        @param modules_package_str_path The string path to the modules package.
        @param app The current application instance.
        """
        from sagittarius_engine.kernel.module_loader import ModuleLoader

        loader = ModuleLoader(app)
        loader.discover_and_load(modules_package_str_path)
