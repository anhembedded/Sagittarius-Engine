import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from zoneinfo import ZoneInfo
from src.infrastructure.crypto_api.crypto_api import TickerData, BinanceManager

class TestTickerData(unittest.TestCase):
    def test_ticker_data_parsing(self):
        raw_data = {
            "s": "ETHUSDT",
            "c": "2000.50",
            "o": "1950.00",
            "h": "2050.00",
            "l": "1900.00",
            "p": "50.50",
            "P": "2.5",
            "w": "1980.00",
            "v": "100.0",
            "q": "198000.0",
            "b": "2000.00",
            "a": "2001.00",
            "n": 500,
            "E": 1625097600000 # Timestamp in milliseconds
        }
        timezone = ZoneInfo("UTC")
        ticker = TickerData(raw_data, timezone)

        self.assertEqual(ticker.symbol, "ETHUSDT")
        self.assertEqual(ticker.last_price, 2000.50)
        self.assertEqual(ticker.open_price, 1950.00)
        self.assertEqual(ticker.high_price, 2050.00)
        self.assertEqual(ticker.low_price, 1900.00)
        self.assertEqual(ticker.price_change, 50.50)
        self.assertEqual(ticker.price_change_pct, 2.5)
        self.assertEqual(ticker.weighted_avg_price, 1980.00)
        self.assertEqual(ticker.volume, 100.0)
        self.assertEqual(ticker.quote_volume, 198000.0)
        self.assertEqual(ticker.best_bid, 2000.00)
        self.assertEqual(ticker.best_ask, 2001.00)
        self.assertEqual(ticker.trade_count, 500)
        self.assertEqual(ticker.event_time, datetime.fromtimestamp(1625097600.0, tz=timezone))


class TestBinanceManager(unittest.TestCase):

    @patch('src.infrastructure.crypto_api.crypto_api.ThreadedWebsocketManager')
    def test_start_stop(self, MockTWM):
        mock_twm_instance = MockTWM.return_value
        manager = BinanceManager(symbol="BTCUSDT", timezone="UTC")

        manager.start()

        MockTWM.assert_called_once_with(api_key=None, api_secret=None)
        mock_twm_instance.start.assert_called_once()
        mock_twm_instance.start_symbol_ticker_socket.assert_called_once_with(
            callback=manager._handle_socket_message,
            symbol="BTCUSDT"
        )

        manager.stop()
        mock_twm_instance.stop.assert_called_once()
        self.assertIsNone(manager._twm)

    def test_handle_socket_message_error(self):
        manager = BinanceManager()
        # Should not raise any error or dispatch
        with patch.object(manager, '_dispatch') as mock_dispatch:
            manager._handle_socket_message({"e": "error", "m": "test error"})
            mock_dispatch.assert_not_called()

    def test_dispatch(self):
        mock_callback = MagicMock()
        manager = BinanceManager(on_tick=mock_callback)

        raw_data = {
            "s": "ETHUSDT", "c": "2000.50", "o": "1950.00", "h": "2050.00",
            "l": "1900.00", "p": "50.50", "P": "2.5", "w": "1980.00",
            "v": "100.0", "q": "198000.0", "b": "2000.00", "a": "2001.00",
            "n": 500, "E": 1625097600000
        }
        manager._handle_socket_message(raw_data)

        mock_callback.assert_called_once()
        ticker = mock_callback.call_args[0][0]
        self.assertIsInstance(ticker, TickerData)
        self.assertEqual(ticker.symbol, "ETHUSDT")

if __name__ == '__main__':
    unittest.main()
