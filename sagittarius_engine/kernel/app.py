from typing import Any
from sagittarius_engine.exceptions import ModuleRegistrationError
from sagittarius_engine.kernel.context import EngineContext
from sagittarius_engine.interfaces import (
    ICommand,
    IContainer,
    IEventBus,
    ILogger,
    IMiddleware,
    IModule,
    IQuery,
)


class App:
    """
    @brief The public façade of the Sagittarius Engine.

    @details App delegates runtime operations to EngineContext.
    """

    def __init__(self, container: IContainer, event_bus: IEventBus) -> None:
        """
        @brief Initializes the application with the core ports.

        @param container The dependency injection container.
        @param event_bus The event bus.
        """
        self.context = EngineContext(self, container, event_bus)

    @property
    def container(self) -> IContainer:
        return self.context.container

    @property
    def event_bus(self) -> IEventBus:
        return self.context.event_bus

    @property
    def modules(self) -> list[Any]:
        return self.context.modules

    @property
    def pipeline(self) -> Any:
        return self.context.middleware_pipeline

    @property
    def lifecycle(self) -> Any:
        return self.context.lifecycle

    def use(self, extension_or_module: Any) -> None:
        """
        @brief Manually adds an Extension or Module to the App.
        """
        try:
            self.context.extension_manager.register(extension_or_module)
        except TypeError as e:
            raise ModuleRegistrationError(str(e)) from e

    def use_middleware(self, middleware_instance: IMiddleware) -> None:
        """
        @brief Registers a Middleware for the application.
        @param middleware_instance The middleware instance.
        """
        self.context.middleware_pipeline.add(middleware_instance)

    def _get_logger(self) -> ILogger | None:
        return self.context.logger

    def boot(self, auto_discover: str | None = None) -> None:
        """
        @brief Boots the application.
        """
        self.context.bootstrap.boot(auto_discover)

    def dispatch(self, handler_class: type, input_dto: Any = None) -> Any:
        """
        @brief Dispatches a command or query through the Middleware Pipeline.
        """
        return self.context.dispatcher.dispatch(handler_class, input_dto)

    def execute(self, command_class: type, input_dto: Any = None) -> Any:
        """
        @brief Deprecated. Use dispatch instead.
        """
        import warnings

        warnings.warn(
            "App.execute is deprecated. Use App.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(command_class, input_dto)

    def query(self, query_class: type, input_dto: Any = None) -> Any:
        """
        @brief Deprecated. Use dispatch instead.
        """
        import warnings

        warnings.warn(
            "App.query is deprecated. Use App.dispatch instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.dispatch(query_class, input_dto)

    def stop(self) -> None:
        """
        @brief Shuts down the application gracefully.
        @details Stops the scheduler, hosted services, extensions, task manager, and async runtime in reverse order.
        """
        print("[DEBUG] [app.py] App.stop() called.", flush=True)
        if self.context.lifecycle.is_stopping or self.context.lifecycle.is_stopped:
            print("[DEBUG] [app.py] App.stop() skipped (already stopping/stopped).", flush=True)
            return

        logger = self._get_logger()
        if logger:
            logger.info("App is stopping gracefully...")

        self.context.lifecycle.set_stopping()

        # 1. Stop Scheduler
        try:
            print("[DEBUG] [app.py] Step 1: Stopping scheduler...", flush=True)
            self.context.scheduler.stop()
            print("[DEBUG] [app.py] Step 1: Scheduler stopped.", flush=True)
        except Exception as e:
            print(f"[DEBUG] [app.py] Step 1 Error: {e}", flush=True)

        # 2. Stop Hosted Services
        try:
            print("[DEBUG] [app.py] Step 2: Stopping hosted services...", flush=True)
            self.context.hosted_services.stop()
            print("[DEBUG] [app.py] Step 2: Hosted services stopped.", flush=True)
        except Exception as e:
            print(f"[DEBUG] [app.py] Step 2 Error: {e}", flush=True)

        # 3. Stop Extensions
        try:
            print("[DEBUG] [app.py] Step 3: Stopping extensions...", flush=True)
            self.context.extension_manager.stop_and_dispose()
            print("[DEBUG] [app.py] Step 3: Extensions stopped.", flush=True)
        except Exception as e:
            print(f"[DEBUG] [app.py] Step 3 Error: {e}", flush=True)

        # 4. Shutdown Task Manager
        try:
            print("[DEBUG] [app.py] Step 4: Shutting down task manager...", flush=True)
            self.context.tasks.shutdown()
            print("[DEBUG] [app.py] Step 4: Task manager shut down.", flush=True)
        except Exception as e:
            print(f"[DEBUG] [app.py] Step 4 Error: {e}", flush=True)

        # 5. Stop Async Runtime
        try:
            print("[DEBUG] [app.py] Step 5: Stopping async runtime...", flush=True)
            self.context.async_runtime.stop()
            print("[DEBUG] [app.py] Step 5: Async runtime stopped.", flush=True)
        except Exception as e:
            print(f"[DEBUG] [app.py] Step 5 Error: {e}", flush=True)

        self.context.lifecycle.set_stopped()
        print("[DEBUG] [app.py] App.stop() finished cleanly.", flush=True)


