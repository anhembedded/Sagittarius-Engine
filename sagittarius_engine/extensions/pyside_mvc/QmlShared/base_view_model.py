from PySide6.QtCore import Property, QObject, Signal


class BaseQmlViewModel(QObject):
    """
    @brief Base for every QML screen's ViewModel: carries the FSM-driven
    `uiMode` property QML binds its enabled/visible states to.

    @details
    QmlHostView.apply_ui_mode() (fed by BasePresenter's FSM binding) calls
    `set_ui_mode()` here; QML reads `viewModel.uiMode` — e.g.
    `enabled: viewModel.uiMode !== "LOCKED"`. This replaces the
    reflection-over-ui_matrix.json mechanism (UIMatrixMixin) used by the
    QtWidgets screens: QML binds declaratively, so a JSON matrix mapping
    widget-attribute names to booleans has nothing to drive.
    """

    uiModeChanged = Signal()
    controlsEnabledChanged = Signal()

    #: Which `uiMode` string values should disable this screen's controls —
    #: subclasses override to opt in (e.g. `frozenset({"LOCKED", "LIVE"})`).
    #: Empty by default: the engine has no opinion on which of an app's
    #: modes are "busy" states, mirroring BaseStateMachine's own genericity
    #: over "any Enum" — a subclass that never sets this keeps today's
    #: behavior (`controlsEnabled` always True) unchanged.
    DISABLED_UI_MODES: frozenset[str] = frozenset()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._ui_mode = "IDLE"
        self._controls_enabled = "IDLE" not in self.DISABLED_UI_MODES

    def _get_ui_mode(self) -> str:
        return self._ui_mode

    uiMode = Property(str, _get_ui_mode, notify=uiModeChanged)

    def _get_controls_enabled(self) -> bool:
        return self._controls_enabled

    #: Derived from `uiMode`/`DISABLED_UI_MODES` — screens bind
    #: `enabled: viewModel.controlsEnabled` instead of hand-rolling their own
    #: `uiMode === "IDLE" || uiMode === "ERROR"`-style string comparison,
    #: which is where screens have drifted into inconsistent (and once,
    #: behaviorally different) ad hoc conditions in the past.
    controlsEnabled = Property(
        bool, _get_controls_enabled, notify=controlsEnabledChanged
    )

    def set_ui_mode(self, mode: str) -> None:
        if mode == self._ui_mode:
            return
        self._ui_mode = mode
        self.uiModeChanged.emit()

        enabled = mode not in self.DISABLED_UI_MODES
        if enabled != self._controls_enabled:
            self._controls_enabled = enabled
            self.controlsEnabledChanged.emit()
