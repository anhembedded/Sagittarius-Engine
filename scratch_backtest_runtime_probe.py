import io
import logging
import os
import sys
from contextlib import redirect_stderr, redirect_stdout

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

PROJECT_ROOT = r"c:\Users\hoang\Documents\Sagittarius-Engine"
BOT_ROOT = os.path.join(PROJECT_ROOT, "Sagittarius_Elite_Warrior")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Sagittarius_Elite_Warrior.src.config.config_keys import ConfigKeys
from Sagittarius_Elite_Warrior.src.main import create_app
from Sagittarius_Elite_Warrior.src.presentation.ui.app_bootstrapper import _apply_font, _apply_theme
from Sagittarius_Elite_Warrior.src.presentation.ui.assets import Palette, get_icon_loader
from Sagittarius_Elite_Warrior.src.presentation.ui.main_window import MainWindow
from sagittarius_engine.extensions.pyside_mvc import configure_app_qml
from sagittarius_engine.infrastructure.config.config_manager import ConfigManager

CONFIG_DIR = os.path.join(BOT_ROOT, "src", "config")
APP_CONFIG = os.path.join(CONFIG_DIR, "app_config.json")
USER_CONFIG = os.path.join(CONFIG_DIR, "user_config.json")

config_manager = ConfigManager()
config_manager.load_json(APP_CONFIG)
config_manager.load_json(USER_CONFIG, writable=True)
config_manager.load_dict({ConfigKeys.DEV_MODE.value: True})

app_engine = create_app(config_manager)
app_engine.boot()
app = QApplication(sys.argv)
_apply_font(app, config_manager)
_apply_theme(app, config_manager)
configure_app_qml(Palette.as_ui_dict(), get_icon_loader(), Palette.as_icon_dict())
window = MainWindow(app_engine)
window.show()

stdout_buffer = io.StringIO()
stderr_buffer = io.StringIO()
logger_buffer = io.StringIO()
handler = logging.StreamHandler(logger_buffer)
handler.setLevel(logging.INFO)
root_logger = logging.getLogger()
root_logger.addHandler(handler)

from Sagittarius_Elite_Warrior.tests.conftest import find_qml_item

result = {"ok": False, "error": None}

def run_probe():
    try:
        sidebar_root = window._sidebar.quick_widget.rootObject()
        button = find_qml_item(sidebar_root, "navButton_backtest")
        if button is None:
            button = find_qml_item(sidebar_root, "navButton_Backtest Engine")
        if button is None:
            raise RuntimeError("Backtest navigation button not found")
        button.clicked.emit()
        app.processEvents()
        app.processEvents()

        entry = window._router._registry["backtest"]
        presenter = entry.get("presenter_instance")
        if presenter is None:
            raise RuntimeError("Backtest presenter not created")
        root = presenter.view.top_widget.rootObject()
        run_button = find_qml_item(root, "btnRunBacktest")
        if run_button is None:
            raise RuntimeError("Run Backtest button not found")
        run_button.clicked.emit()
        app.processEvents()
        app.processEvents()

        thread_manager = presenter._thread_manager
        thread_manager.shutdown(wait=True)
        for _ in range(20):
            app.processEvents()
        result["ok"] = True
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        QTimer.singleShot(0, app.quit)

QTimer.singleShot(0, run_probe)
with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
    app.exec()

root_logger.removeHandler(handler)
handler.flush()
combined = "\n".join([
    "[STDOUT]",
    stdout_buffer.getvalue(),
    "[STDERR]",
    stderr_buffer.getvalue(),
    "[LOG]",
    logger_buffer.getvalue(),
    "[RESULT]",
    str(result),
])
print(combined)

app_engine.stop()
