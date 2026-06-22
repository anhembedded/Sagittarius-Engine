import pytest
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import MagicMock, patch

from src.infrastructure.crypto_api.crypto_api import TickerData, BinanceManager

def test_ticker_data_parsing():
    raw_msg = {
        "s": "ETHUSDT",
        "c": "2000.50",
        "o": "1950.00",
        "h": "2050.00",
        "l": "1900.00",
        "p": "50.50",
        "P": "2.5",
        "w": "1980.00",
        "v": "1000.5",
        "q": "2000000.0",
        "b": "2000.00",
        "a": "2001.00",
        "n": 500,
        "E": 1672531200000
    }
    tz = ZoneInfo("UTC")

    ticker = TickerData(raw_msg, tz)

    assert ticker.symbol == "ETHUSDT"
    assert ticker.last_price == 2000.50
    assert ticker.open_price == 1950.00
    assert ticker.high_price == 2050.00
    assert ticker.low_price == 1900.00
    assert ticker.price_change == 50.50
    assert ticker.price_change_pct == 2.5
    assert ticker.weighted_avg_price == 1980.00
    assert ticker.volume == 1000.5
    assert ticker.quote_volume == 2000000.0
    assert ticker.best_bid == 2000.00
    assert ticker.best_ask == 2001.00
    assert ticker.trade_count == 500
    assert ticker.event_time.timestamp() == 1672531200.0

    repr_str = repr(ticker)
    assert "ETHUSDT" in repr_str
    assert "2000.50" in repr_str

@patch("src.infrastructure.crypto_api.crypto_api.ThreadedWebsocketManager")
def test_binance_manager_lifecycle(mock_twm_class):
    mock_twm_instance = MagicMock()
    mock_twm_class.return_value = mock_twm_instance

    callback_called = False
    def on_tick(ticker):
        nonlocal callback_called
        callback_called = True

    manager = BinanceManager(symbol="BTCUSDT", timezone="UTC", on_tick=on_tick)

    # Start
    manager.start()
    mock_twm_class.assert_called_once()
    mock_twm_instance.start.assert_called_once()
    mock_twm_instance.start_symbol_ticker_socket.assert_called_once_with(
        callback=manager._handle_socket_message,
        symbol="BTCUSDT"
    )

    # Handle message
    raw_msg = {
        "s": "BTCUSDT", "c": "2", "o": "1", "h": "3", "l": "1",
        "p": "1", "P": "100", "w": "2", "v": "1", "q": "2",
        "b": "1.9", "a": "2.1", "n": 1, "E": 1000000
    }
    manager._handle_socket_message(raw_msg)
    assert callback_called

    # Stop
    manager.stop()
    mock_twm_instance.stop.assert_called_once()
    assert manager._twm is None

def test_binance_manager_error_message(caplog):
    manager = BinanceManager(symbol="BTCUSDT", timezone="UTC")
    err_msg = {"e": "error", "m": "Test Error"}
    manager._handle_socket_message(err_msg)
    assert "WebSocket error: Test Error" in caplog.text
