import pytest
from unittest.mock import Mock, call

from src.domain.crypto_stream.crypto_stream_port import CryptoStreamPort, Ticker
from src.domain.logger.Logger_api import Logger
from src.use_cases.print_price_flow.print_price_use_cases import StartPrintPriceUseCase, StopPrintPriceUseCase


@pytest.fixture
def mock_crypto_stream() -> Mock:
    return Mock(spec=CryptoStreamPort)

@pytest.fixture
def mock_logger() -> Mock:
    return Mock(spec=Logger)

def test_start_print_price_use_case(mock_crypto_stream: Mock, mock_logger: Mock) -> None:
    # Arrange
    use_case = StartPrintPriceUseCase(crypto_stream=mock_crypto_stream, logger=mock_logger)
    symbol = "ETHUSDT"

    # Act
    use_case.execute(symbol)

    # Assert
    mock_logger.info.assert_called_once_with(f"Starting price stream for {symbol}...")
    mock_crypto_stream.start_stream.assert_called_once()

    # Extract the callback passed to start_stream
    args, _ = mock_crypto_stream.start_stream.call_args
    assert args[0] == symbol
    on_tick_callback = args[1]

    # Test the callback explicitly
    test_ticker = Ticker(symbol=symbol, price=3000.5, volume=10.0)
    on_tick_callback(test_ticker)

    # Verify logger received the callback output
    mock_logger.info.assert_has_calls([
        call(f"Starting price stream for {symbol}..."),
        call(f"[{symbol}] Price: 3000.5000 | Vol: 10.00")
    ])

def test_stop_print_price_use_case(mock_crypto_stream: Mock, mock_logger: Mock) -> None:
    # Arrange
    use_case = StopPrintPriceUseCase(crypto_stream=mock_crypto_stream, logger=mock_logger)
    symbol = "ETHUSDT"

    # Act
    use_case.execute(symbol)

    # Assert
    mock_logger.info.assert_called_once_with(f"Stopping price stream for {symbol}...")
    mock_crypto_stream.stop_stream.assert_called_once_with(symbol)
