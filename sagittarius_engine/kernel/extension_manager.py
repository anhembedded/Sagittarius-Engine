from typing import Any
from sagittarius_engine.interfaces.i_extension import IExtension, ExtensionDescriptor
from sagittarius_engine.interfaces.i_module import IModule
from sagittarius_engine.kernel.events import (
    ExtensionInitializing,
    ExtensionStarted,
    ExtensionStopped,
    ExtensionDisposed,
)
from sagittarius_engine.exceptions import (
    ExtensionDependencyError,
    ExtensionCircularDependencyError,
)


class ModuleExtensionAdapter(IExtension):
    """
    @brief Adapts a legacy IModule to the IExtension interface.
    """

    def __init__(self, legacy_module: Any):
        self.legacy_module = legacy_module
        deps = getattr(legacy_module, "dependencies", [])
        opt_deps = getattr(legacy_module, "optional_dependencies", [])
        prio = getattr(legacy_module, "priority", 0)
        enabled = getattr(legacy_module, "enabled", True)
        self._descriptor = ExtensionDescriptor(
            name=legacy_module.__class__.__name__,
            dependencies=deps if isinstance(deps, list) else [],
            optional_dependencies=opt_deps if isinstance(opt_deps, list) else [],
            priority=prio if isinstance(prio, int) else 0,
            enabled=enabled if isinstance(enabled, bool) else True,
        )

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._descriptor

    def register(self, context: Any) -> None:
        self.legacy_module.register(context.app)

    def boot(self, context: Any) -> None:
        self.legacy_module.boot(context.app)

    def shutdown(self, context: Any) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self.legacy_module, name)


def create_module_extension_adapter(legacy_module: Any) -> Any:
    """
    @brief Dynamically creates an adapter class that retains the original class name.
    """
    cls_name = legacy_module.__class__.__name__
    # Dynamically create subclass of ModuleExtensionAdapter named cls_name
    dynamic_cls = type(cls_name, (ModuleExtensionAdapter,), {})
    return dynamic_cls(legacy_module)


class ExtensionManager:
    """
    @brief Orchestrates the extension lifecycle with dependency awareness.
    """

    def __init__(self, context: Any) -> None:
        self.context = context
        self.registered_extensions: list[IExtension] = []
        self.sorted_extensions: list[IExtension] = []
        self.initialized_extensions: list[IExtension] = []

    def register(self, extension_or_module: IExtension | IModule | Any) -> None:
        """
        @brief Registers an extension or adapts a legacy module.
        """
        if isinstance(extension_or_module, IExtension):
            ext = extension_or_module
        elif isinstance(extension_or_module, IModule):
            ext = create_module_extension_adapter(extension_or_module)
        else:
            # support duck-typing for objects that have register and boot methods
            if hasattr(extension_or_module, "register") and hasattr(
                extension_or_module, "boot"
            ):
                ext = create_module_extension_adapter(extension_or_module)
            else:
                raise TypeError(
                    "Registered object must implement IExtension or IModule"
                )

        self.registered_extensions.append(ext)

        # Try to initialize any available extensions immediately to support instant resolution
        try:
            self._try_initialize_available()
        except Exception as e:
            self._rollback()
            raise e

    def _get_logger(self) -> Any:
        try:
            return self.context.logger
        except Exception:
            return None

    def _emit(self, event_name: str, event_data: Any) -> None:
        try:
            self.context.event_bus.emit(event_name, event_data)
        except Exception:  # nosec B110
            pass

    def _try_initialize_available(self) -> None:
        """
        @brief Scans and initializes deferred extensions whose dependencies have been registered and initialized.
        """
        initialized_names = {ext.descriptor.name for ext in self.initialized_extensions}
        enabled_exts = [
            ext for ext in self.registered_extensions if ext.descriptor.enabled
        ]

        # ⚡ Bolt: Sort by priority once outside the loop to avoid O(M * N log N) redundant sorts
        sorted_exts = sorted(
            enabled_exts, key=lambda e: e.descriptor.priority, reverse=True
        )

        while True:
            initialized_any = False
            for ext in sorted_exts:
                name = ext.descriptor.name
                if name in initialized_names:
                    continue

                # Check if all required dependencies are initialized
                deps_satisfied = True
                for dep in ext.descriptor.dependencies:
                    if dep not in initialized_names:
                        deps_satisfied = False
                        break

                # Check if registered or pending optional dependencies are initialized
                if deps_satisfied:
                    for dep in ext.descriptor.optional_dependencies:
                        if dep not in initialized_names:
                            deps_satisfied = False
                            break

                if deps_satisfied:
                    logger = self._get_logger()
                    if logger:
                        logger.info(f"Initializing extension '{name}'...")
                    self._emit("extension.initializing", ExtensionInitializing(name))
                    ext.initialize(self.context)
                    self.initialized_extensions.append(ext)
                    initialized_names.add(name)
                    initialized_any = True

            if not initialized_any:
                break

    def _build_and_sort(self) -> list[IExtension]:
        """
        @brief Topologically sorts registered and enabled extensions based on dependencies.
        """
        enabled_exts = [
            ext for ext in self.registered_extensions if ext.descriptor.enabled
        ]
        ext_by_name = {ext.descriptor.name: ext for ext in enabled_exts}

        visiting = set()
        visited = set()
        result = []

        def dfs(name: str):
            if name in visiting:
                raise ExtensionCircularDependencyError(
                    f"Circular dependency detected involving extension '{name}'"
                )
            if name in visited:
                return

            ext = ext_by_name.get(name)
            if not ext:
                return

            visiting.add(name)

            # Validate and traverse required dependencies
            for dep in ext.descriptor.dependencies:
                if dep not in ext_by_name:
                    raise ExtensionDependencyError(
                        f"Extension '{name}' requires missing dependency '{dep}'"
                    )
                dfs(dep)

            # Traverse optional dependencies
            for dep in ext.descriptor.optional_dependencies:
                if dep in ext_by_name:
                    dfs(dep)

            visiting.remove(name)
            visited.add(name)
            result.append(ext)

        # Sort by priority descending to process higher priority items first
        sorted_by_priority = sorted(
            enabled_exts, key=lambda e: e.descriptor.priority, reverse=True
        )
        for ext in sorted_by_priority:
            dfs(ext.descriptor.name)

        return result

    def initialize_and_start(self) -> None:
        """
        @brief Resolves dependencies, initializes remaining extensions, and boots them.
        @details Performs safe rollback/disposal on initialization failure.
        """
        logger = self._get_logger()
        self.sorted_extensions = self._build_and_sort()

        # 1. Initialize stage for any remaining deferred extensions
        for ext in self.sorted_extensions:
            if ext not in self.initialized_extensions:
                name = ext.descriptor.name
                if logger:
                    logger.info(f"Initializing extension '{name}'...")
                self._emit("extension.initializing", ExtensionInitializing(name))
                try:
                    ext.initialize(self.context)
                    self.initialized_extensions.append(ext)
                except Exception as e:
                    if logger:
                        logger.error(
                            f"Failed to initialize extension '{name}': {e}. Rolling back..."
                        )
                    self._rollback()
                    raise e

        # 2. Start stage
        for ext in self.sorted_extensions:
            name = ext.descriptor.name
            if logger:
                logger.info(f"Starting extension '{name}'...")
            ext.start(self.context)
            self._emit("extension.started", ExtensionStarted(name))

    def _rollback(self) -> None:
        """
        @brief Safe cleanup of initialized extensions in reverse order on failure.
        """
        logger = self._get_logger()
        for ext in reversed(self.initialized_extensions):
            name = ext.descriptor.name
            if logger:
                logger.info(f"Disposing extension '{name}' due to rollback...")
            try:
                ext.dispose(self.context)
                self._emit("extension.disposed", ExtensionDisposed(name))
            except Exception as e:
                if logger:
                    logger.error(f"Error during rollback disposal of '{name}': {e}")
        # Clear initialized list since they are now rolled back
        self.initialized_extensions.clear()

    def stop_and_dispose(self) -> None:
        """
        @brief Stops and disposes extensions in reverse dependency order.
        """
        logger = self._get_logger()
        for ext in reversed(self.sorted_extensions):
            name = ext.descriptor.name
            if logger:
                logger.info(f"Stopping extension '{name}'...")
            try:
                ext.stop(self.context)
                self._emit("extension.stopped", ExtensionStopped(name))
            except Exception as e:
                if logger:
                    logger.error(f"Error stopping extension '{name}': {e}")

            if logger:
                logger.info(f"Disposing extension '{name}'...")
            try:
                ext.dispose(self.context)
                self._emit("extension.disposed", ExtensionDisposed(name))
            except Exception as e:
                if logger:
                    logger.error(f"Error disposing extension '{name}': {e}")

        self.sorted_extensions.clear()
        self.initialized_extensions.clear()
