# Trading Bot Reference Application

This reference application demonstrates how to use the Sagittarius Engine to build long-running applications requiring:

- Connection lifecycles (`IHostedService`)
- Automated background tasks (`TaskManager`)
- Tick schedule loop (`Scheduler`)

## Architecture

- **`MockExchange`** (`IHostedService`): Manages simulated connection states.
- **`TradingStrategy`**: Reads prices and executes trades inside independent non-blocking task workers.
