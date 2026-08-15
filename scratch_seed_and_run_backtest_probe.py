import io
import logging
import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import UTC, datetime, timedelta

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

PROJECT_ROOT = r"c:\Users\hoang\Documents\Sagittarius-Engine"
BOT_ROOT = os.path.join(PROJECT_ROOT, "Sagittarius_Elite_Warrior")
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Sagittarius_Elite_Warrior.src.application.ports.i_market_data_repository import (
    IMarketDataRepository,
)
from Sagittarius_Elite_Warrior.src.config.config_keys import ConfigKeys
from Sagittarius_Elite_Warrior.src.domain.entities.market_data import MarketData
from Sagittarius_Elite_Warrior.src.domain.value_objects.timeframe import TimeFrame
from Sagittarius_Elite_Warrior.src.main import create_app
from Sagittarius_Elite_Warrior.src.presentation.ui.app_bootstrapper import _apply_font, _apply_theme
from Sagittarius_Elite_Warrior.src.presentation.ui.assets import Palette, get_icon_loader
from Sagittarius_Elite_Warrior.src.presentation.ui.main_window import MainWindow
from sagittarius_engine.extensions.pyside_mvc import configure_app_qml
from sagittarius_engine.infrastructure.config.config_manager import ConfigManager

PROJECT_ROOT = r"c:\Users\hoang\Documents\Sagittarius-Engine"
CONFIG_DIR = os.path.join(BOT_ROOT, "src", "config")
APP_CONFIG = os.path.join(CONFIG_DIR, "app_config.json")
USER_CONFIG = os.path.join(CONFIG_DIR, "user_config.json")


def make_klines(count: int = 6000) -> list[MarketData]:
    start = datetime(2026, 8, 1, tzinfo=UTC)
    rows: list[MarketData] = []
    for i in range(count):
        open_time = start + timedelta(minutes=i)
        rows.append(
            MarketData(
                symbol="BTCUSDT",
                interval="1m",
                open_time=open_time,
                open_price=10000.0 + i * 0.1,
                high_price=10003.0 + i * 0.1,
                low_price=9997.0 + i * 0.1,
                close_price=10001.0 + i * 0.1,
                volume=100.0 + i,
                close_time=open_time + timedelta(seconds=59),
                quote_asset_volume=1000.0 + i,
                number_of_trades=10 + (i % 5),
                taker_buy_base_asset_volume=50.0 + i,
                taker_buy_quote_asset_volume=500.0 + i,
            )
        )
    return rows


config_manager = ConfigManager()
config_manager.load_json(APP_CONFIG)
config_manager.load_json(USER_CONFIG, writable=True)
config_manager.load_dict({ConfigKeys.DEV_MODE.value: True})

app_engine = create_app(config_manager)
app_engine.boot()
repo = app_engine.context.container.resolve(IMarketDataRepository)
repo.save_klines(make_klines())

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


def click_and_flush(button) -> None:
    button.clicked.emit()
    for _ in range(4):
        app.processEvents()


def run_probe():
    try:
        sidebar_root = window._sidebar.quick_widget.rootObject()
        button = find_qml_item(sidebar_root, "navButton_backtest")
        if button is None:
            button = find_qml_item(sidebar_root, "navButton_Backtest Engine")
        if button is None:
            raise RuntimeError("Backtest navigation button not found")
        click_and_flush(button)

        entry = window._router._registry["backtest"]
        presenter = entry.get("presenter_instance")
        if presenter is None:
            raise RuntimeError("Backtest presenter not created")

        if presenter._view_model.selectedTimeframe != TimeFrame.ONE_MINUTE.value:
            presenter._view_model.selectedTimeframe = TimeFrame.ONE_MINUTE.value
            app.processEvents()

        root = presenter.view.top_widget.rootObject()
        if root is None:
            raise RuntimeError("Backtest toolbar root not found")

        for object_name in (
            "btnBacktestCapital",
            "btnBacktestIndicatorPicker",
            "btnBacktestBotParams",
        ):
            btn = find_qml_item(root, object_name)
            if btn is None:
                raise RuntimeError(f"Toolbar button not found: {object_name}")
            click_and_flush(btn)

        run_button = find_qml_item(root, "btnRunBacktest")
        if run_button is None:
            raise RuntimeError("Run Backtest button not found")
        click_and_flush(run_button)

        thread_manager = presenter._thread_manager
        thread_manager.shutdown(wait=True)
        for _ in range(60):
            app.processEvents()

        mode = presenter.view._chart_mode
        presenter.view.set_chart_mode(mode.EQUITY)
        for _ in range(10):
            app.processEvents()
        presenter.view.set_chart_mode(mode.BOTH)
        for _ in range(10):
            app.processEvents()
        presenter.view.set_chart_mode(mode.OHLC)
        for _ in range(10):
            app.processEvents()

        click_and_flush(find_qml_item(root, "btnBacktestCapital"))
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
combined = "\n".join(
    [
        "[STDOUT]",
        stdout_buffer.getvalue(),
        "[STDERR]",
        stderr_buffer.getvalue(),
        "[LOG]",
        logger_buffer.getvalue(),
        "[RESULT]",
        str(result),
    ]
)
print(combined)

app_engine.stop()
