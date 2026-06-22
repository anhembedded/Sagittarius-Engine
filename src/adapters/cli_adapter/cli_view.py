import cmd2
import argparse
import threading

from src.adapters.cli_adapter.cli_presenter import CLIPresenter

class CryptoTradingBotCLI(cmd2.Cmd):
    """
    View / Input parser for CLI. Deals with the user input and display.
    Delegates to the Presenter to trigger domain events.
    """
    def __init__(self, presenter: CLIPresenter):
        super().__init__()
        self._presenter = presenter
        self.prompt = "(crypto-bot) "
        self.intro = "Welcome to Crypto Trading Bot. Type 'help' to list commands."

    start_parser = argparse.ArgumentParser()
    start_parser.add_argument('-s', '--symbol', type=str, default='ETHUSDT', help="Crypto symbol to track (e.g. ETHUSDT)")

    @cmd2.with_argparser(start_parser)
    def do_start_price(self, args: argparse.Namespace) -> None:
        """Start streaming crypto price"""
        try:
            self._presenter.publish_start_price(args.symbol)
        except Exception as e:
            self.perror(f"Error starting stream: {e}")

    stop_parser = argparse.ArgumentParser()
    stop_parser.add_argument('-s', '--symbol', type=str, default='ETHUSDT', help="Crypto symbol to stop tracking")

    @cmd2.with_argparser(stop_parser)
    def do_stop_price(self, args: argparse.Namespace) -> None:
        """Stop streaming crypto price"""
        try:
            self._presenter.publish_stop_price(args.symbol)
        except Exception as e:
            self.perror(f"Error stopping stream: {e}")

    def do_quit(self, arg: str) -> bool:
        """Exit the application"""
        self.poutput("Shutting down CLI...")
        try:
            self._presenter.publish_quit()
        except:
            pass
        return True


class CLIThread(threading.Thread):
    def __init__(self, presenter: CLIPresenter):
        super().__init__(daemon=True) # Run as daemon so it dies if main thread dies
        self._cli = CryptoTradingBotCLI(presenter)

    def run(self):
        self._cli.cmdloop()
