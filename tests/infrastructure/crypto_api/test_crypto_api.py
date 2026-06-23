import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.crypto_api.crypto_api import BinanceManager, TickerData
from zoneinfo import ZoneInfo
from datetime import datetime

def get_sample_raw_ticker():
    return {
        "s": "ETHUSDT",
        "c": "2000.50",
        "o": "1900.00",
        "h": "2050.00",
        "l": "1890.00",
        "p": "100.50",
        "P": "5.28",
        "w": "1980.00",
        "v": "10000.00",
        "q": "19800000.00",
        "b": "2000.00",
        "a": "2001.00",
        "n": 50000,
        "E": 1672531200000  # Jan 1, 2023 UTC
    }

def test_ticker_data_parsing():
    raw = get_sample_raw_ticker()
    timezone = ZoneInfo("UTC")

    ticker = TickerData(raw, timezone)

    assert ticker.symbol == "ETHUSDT"
    assert ticker.last_price == 2000.50
    assert ticker.open_price == 1900.00
    assert ticker.price_change_pct == 5.28
    assert ticker.event_time.year == 2023

def test_ticker_data_repr():
    raw = get_sample_raw_ticker()
    timezone = ZoneInfo("UTC")
    ticker = TickerData(raw, timezone)

    rep = repr(ticker)
    assert "ETHUSDT" in rep
    assert "2000.5000" in rep

@patch("src.infrastructure.crypto_api.crypto_api.ThreadedWebsocketManager")
def test_binance_manager_start_stop(mock_twm_class):
    mock_twm = MagicMock()
    mock_twm_class.return_value = mock_twm

    manager = BinanceManager(symbol="ETHUSDT", timezone="UTC")

    manager.start()
    mock_twm_class.assert_called_once()
    mock_twm.start.assert_called_once()
    mock_twm.start_symbol_ticker_socket.assert_called_once_with(
        callback=manager._handle_socket_message,
        symbol="ETHUSDT"
    )

    manager.stop()
    mock_twm.stop.assert_called_once()
    assert manager._twm is None

def test_binance_manager_handle_socket_message_error():
    manager = BinanceManager()

    # Should not crash and not call dispatch
    with patch.object(manager, "_dispatch") as mock_dispatch:
        manager._handle_socket_message({"e": "error", "m": "Some error"})
        mock_dispatch.assert_not_called()

def test_binance_manager_handle_socket_message_success():
    mock_callback = MagicMock()
    manager = BinanceManager(on_tick=mock_callback)

    raw = get_sample_raw_ticker()
    manager._handle_socket_message(raw)

    mock_callback.assert_called_once()
    args, _ = mock_callback.call_args
    ticker = args[0]

    assert isinstance(ticker, TickerData)
    assert ticker.symbol == "ETHUSDT"

@patch("src.infrastructure.crypto_api.crypto_api.ThreadedWebsocketManager")
def test_binance_manager_join(mock_twm_class):
    mock_twm = MagicMock()
    mock_twm_class.return_value = mock_twm

    manager = BinanceManager()
    manager.start()

    manager.join()
    mock_twm.join.assert_called_once()
