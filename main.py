import os
import cmd2
import argparse

from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from src.infrastructure.logger.logger_factory import LoggerFactory

from src.domain.app_manager.app_manager import AppManager
from src.adapters.crypto_stream.binance_crypto_stream_adapter import BinanceCryptoStreamAdapter
from src.use_cases.print_price_flow.print_price_use_cases import StartPrintPriceUseCase, StopPrintPriceUseCase


class CryptoTradingBotCLI(cmd2.Cmd):
    """Interactive CLI for Crypto Trading Bot"""

    def __init__(self, app_manager: AppManager):
        super().__init__()
        self.app_manager = app_manager
        self.prompt = "(crypto-bot) "
        self.intro = "Welcome to Crypto Trading Bot. Type 'help' to list commands."

    start_parser = argparse.ArgumentParser()
    start_parser.add_argument('-s', '--symbol', type=str, default='ETHUSDT', help="Crypto symbol to track (e.g. ETHUSDT)")

    @cmd2.with_argparser(start_parser)
    def do_start_price(self, args: argparse.Namespace) -> None:
        """Start streaming crypto price"""
        try:
            self.app_manager.execute_command("start_price", args.symbol)
        except Exception as e:
            self.perror(f"Error starting stream: {e}")

    stop_parser = argparse.ArgumentParser()
    stop_parser.add_argument('-s', '--symbol', type=str, default='ETHUSDT', help="Crypto symbol to stop tracking")

    @cmd2.with_argparser(stop_parser)
    def do_stop_price(self, args: argparse.Namespace) -> None:
        """Stop streaming crypto price"""
        try:
            self.app_manager.execute_command("stop_price", args.symbol)
        except Exception as e:
            self.perror(f"Error stopping stream: {e}")

    def do_quit(self, arg: str) -> bool:
        """Exit the application"""
        self.poutput("Shutting down...")
        # Automatically stop any hardcoded cleanup if needed (for simplicity, we let thread daemon or manual stop handle it)
        try:
            self.app_manager.execute_command("stop_price", "ETHUSDT")
        except:
            pass
        return True


def main() -> None:
    # 1. Initialize Configuration Infra & Adapter
    json_infra = JsonFileInfra()
    config_adapter = LocalConfigAdapter(json_infra)

    # 2. Init App Manager (Domain Layer)
    app_manager = AppManager(
        config_adapter=config_adapter,
        logger_factory=LoggerFactory.create
    )

    # Bootstrap application (Loads config and initializes logger)
    app_manager.Bootstrap()
    logger = app_manager.logger
    logger.info(f"Application bootstrapped in {app_manager.config.mode} mode.")

    # 3. Initialize Infrastructure & Adapters
    crypto_stream_adapter = BinanceCryptoStreamAdapter()

    # 4. Initialize Use Cases
    start_price_uc = StartPrintPriceUseCase(crypto_stream_adapter, logger)
    stop_price_uc = StopPrintPriceUseCase(crypto_stream_adapter, logger)

    # 5. Wire up Commands in App Manager
    app_manager.register_command("start_price", start_price_uc.execute)
    app_manager.register_command("stop_price", stop_price_uc.execute)

    # 6. Start UI/CLI Layer
    cli = CryptoTradingBotCLI(app_manager)
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user.")
    finally:
        # Cleanup
        try:
            crypto_stream_adapter.stop_stream("ETHUSDT")
        except:
            pass
        logger.info("Application stopped.")


if __name__ == "__main__":
    main()
