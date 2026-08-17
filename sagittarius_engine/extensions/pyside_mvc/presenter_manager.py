from collections.abc import Callable

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QStackedWidget

from sagittarius_engine.interfaces.i_container import IContainer
from sagittarius_engine.interfaces.i_logger import ILogger


class PresenterManager(QObject):
    """
    @brief True Lazy-Loading Router for PySide6 Views and Presenters.

    @details
    Unlike eager routers that pre-instantiate UI components, this manager uses Factory functions
    to guarantee zero RAM allocation for screens until they are explicitly navigated to.
    This also handles safe transitions by deferring `addWidget` to `QStackedWidget` until runtime.
    """

    # Signal emitted when navigation completes: (screen_name, presenter_instance)
    sig_screen_changed = Signal(str, object)

    def __init__(self, container: IContainer, stacked_widget: QStackedWidget):
        """
        @brief Initialize the Router.
        @param container The Dependency Injection Container.
        @param stacked_widget The QStackedWidget acting as the visual container.
        """
        super().__init__()
        self.container = container
        self.stacked_widget = stacked_widget

        self._registry: dict[str, dict] = {}
        self._current_screen_name: str | None = None
        self._is_shutdown = False
        self.logger = self.container.resolve(ILogger)

    def register(
        self, name: str, presenter_class: type, view_factory: Callable
    ) -> None:
        """
        @brief Register a screen without instantiating it.

        @param name The unique route name.
        @param presenter_class The class of the Presenter.
        @param view_factory A lambda/function that returns the View instance when called.
        """
        self._registry[name] = {
            "presenter_class": presenter_class,
            "view_factory": view_factory,
            "view_instance": None,
            "presenter_instance": None,
            "stacked_index": -1,
        }

    def navigate_to(self, name: str) -> None:
        """
        @brief Navigate to a screen, safely lazy-loading it if necessary.
        @param name The registered route name.
        """

        if self._is_shutdown:
            raise RuntimeError("PresenterManager is already shut down")
        if name not in self._registry:
            self.logger.error(f"[PresenterManager] Route '{name}' is not registered!")
            raise ValueError(f"[PresenterManager] Route '{name}' is not registered!")

        config = self._registry[name]

        # --- BƯỚC 1: TRUE LAZY INITIALIZATION ---
        if config["presenter_instance"] is None:
            self.logger.debug(f"[PresenterManager] Lazy Loading Screen: {name}")
            # 1.1 Create the View
            view = config["view_factory"]()
            config["view_instance"] = view

            # 1.2 Create the Presenter (injecting View and Container)
            presenter = config["presenter_class"](view, self.container)
            config["presenter_instance"] = presenter

            # 1.3 Add to QStackedWidget (doing this lazily prevents UI boot bottleneck)
            index = self.stacked_widget.addWidget(view)
            config["stacked_index"] = index
            self.logger.debug(
                f"[PresenterManager] Successfully booted {name} (True Lazy Load)"
            )

        # --- BƯỚC 2: SWAP VIEW ---
        self.logger.debug(f"[PresenterManager] Navigating to {name}")
        self.stacked_widget.setCurrentIndex(config["stacked_index"])
        self._current_screen_name = name

        # --- BƯỚC 3: NOTIFY ---
        self.sig_screen_changed.emit(name, config["presenter_instance"])

    def get_current_presenter(self) -> object | None:
        """
        @brief Returns the currently active Presenter.
        """
        if not self._current_screen_name:
            return None
        return self._registry[self._current_screen_name]["presenter_instance"]

    def shutdown(self) -> None:
        """Requests cooperative shutdown from every instantiated presenter."""
        if self._is_shutdown:
            return
        self._is_shutdown = True
        for config in reversed(tuple(self._registry.values())):
            presenter = config["presenter_instance"]
            shutdown = getattr(presenter, "shutdown", None)
            if callable(shutdown):
                try:
                    shutdown()
                except Exception:
                    self.logger.exception(
                        "[PresenterManager] Presenter shutdown failed: %s",
                        type(presenter).__name__,
                    )
