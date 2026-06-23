from PySide6.QtWidgets import QApplication
from EntryPoint.ApplicationBase import BaseApplication
from LazyFrameWork.ui.presenters.presenter_factory import PresenterFactory
from ApplicationCore.EventBus import IEventBus, GeneralEventBus
from ApplicationCore.ApplicationService import ApplicationService
from ApplicationCore.AppController import AppController
from UI.MainView import MainView
from UI.MainPresenter import MainPresenter
from sys import argv


class GUIApplication(BaseApplication):
    def __init__(self):
        super().__init__()

    def run(self):
        self.QT_APP = QApplication(argv)
        self._bootstrap_core()
        self._bootstrap_ui()
        self.QT_APP.exec()

    def _bootstrap_core(self):
        """Khởi tạo Application Core: EventBus, Service, Controller."""
        self.eventbus: IEventBus = GeneralEventBus()
        self.app_service = ApplicationService()
        self.app_controller = AppController(self.eventbus, self.app_service)

    def _bootstrap_ui(self):
        """Khởi tạo UI: View và Presenter, liên kết với AppController."""
        self.main_view = MainView()
        self.main_view.show()

        self.main_presenter = MainPresenter(self.app_controller)
        self.main_presenter.bind(self.main_view)