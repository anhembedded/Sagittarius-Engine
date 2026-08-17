from unittest.mock import Mock

import pytest

from sagittarius_engine.extensions.pyside_mvc.presenter_manager import PresenterManager


class _ShutdownPresenter:
    def __init__(self, _view, _container) -> None:
        self.shutdown_calls = 0

    def shutdown(self) -> None:
        self.shutdown_calls += 1


def test_presenter_manager_shutdown_notifies_loaded_presenters_once():
    container = Mock()
    container.resolve.return_value = Mock()
    stacked_widget = Mock()
    stacked_widget.addWidget.return_value = 0
    manager = PresenterManager(container, stacked_widget)
    manager.register("backtest", _ShutdownPresenter, Mock(return_value=Mock()))
    manager.navigate_to("backtest")
    presenter = manager.get_current_presenter()

    manager.shutdown()
    manager.shutdown()

    assert presenter.shutdown_calls == 1


def test_presenter_manager_rejects_navigation_after_shutdown():
    container = Mock()
    container.resolve.return_value = Mock()
    manager = PresenterManager(container, Mock())
    manager.register("backtest", _ShutdownPresenter, Mock(return_value=Mock()))
    manager.shutdown()

    with pytest.raises(RuntimeError, match="already shut down"):
        manager.navigate_to("backtest")
