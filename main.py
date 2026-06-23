import os
import time

from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from src.infrastructure.logger.logger_factory import LoggerFactory
from src.infrastructure.event_bus.InMemory_EventBus_infra import InMemoryEventBusInfra

from application.app_manager.app_manager import AppManager
from src.adapters.crypto_stream.binance_crypto_stream_adapter import BinanceCryptoStreamAdapter

from src.use_cases.print_price_flow.print_price_use_cases import StartPrintPriceUseCase, StopPrintPriceUseCase
from src.use_cases.app_controller.AppControllerImpl import AppControllerImpl

from src.adapters.cli_adapter.cli_presenter import CLIPresenter
from src.adapters.cli_adapter.cli_view import CryptoTradingBotCLI

def main() -> None:
    # 1. Initialize Configuration Infra & Adapter
    json_infra = JsonFileInfra()
    config_adapter = LocalConfigAdapter(json_infra)

    # 2. Init App Manager (Domain Layer) to bootstrap config and logger
    app_manager = AppManager(
        config_adapter=config_adapter,
        logger_factory=LoggerFactory.create
    )
    app_manager.Bootstrap()
    logger = app_manager.logger
    logger.info(f"Application bootstrapped in {app_manager.config.mode} mode.")

    # 3. Initialize Core Infrastructure & Adapters
    event_bus = InMemoryEventBusInfra(logger=logger)
    crypto_stream_adapter = BinanceCryptoStreamAdapter()

    # 4. Initialize Use Cases (Application Services)
    start_price_uc = StartPrintPriceUseCase(crypto_stream_adapter, logger, event_bus)
    stop_price_uc = StopPrintPriceUseCase(crypto_stream_adapter, logger)

    # 5. Initialize Application Controller (Headless-first core orchestration)
    app_controller = AppControllerImpl(
        event_bus=event_bus,
        start_price_uc=start_price_uc,
        stop_price_uc=stop_price_uc,
        logger=logger
    )
    app_controller.start() # Subscribes to Command Events

    # 6. Initialize CLI (Adapters Layer)
    cli_presenter = CLIPresenter(event_bus)
    cli = CryptoTradingBotCLI(cli_presenter)

    # 7. Start CLI loop in the main thread
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")
    finally:
        # Cleanup
        app_controller.stop()
        crypto_stream_adapter.stop_stream("ETHUSDT") # Force cleanup fallback
        logger.info("Application stopped gracefully.")


if __name__ == "__main__":
    main()
