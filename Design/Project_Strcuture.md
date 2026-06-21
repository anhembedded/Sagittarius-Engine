Sagitarius_ForkBoy/
│
├── src/
│   ├── domain/             # Core entities & interface definitions (Pure Python)
│   │   ├── __init__.py
│   │   └── models.py       # Price, Signal, Order structures
│   │
│   ├── use_cases/          # Business rules & application logic
│   │   ├── __init__.py
│   │   ├── trading_flow.py # Coordinates data -> strategy -> execution
│   │   └── print_price_flow.py # Prints the current price to terminal
│   │
│   ├── entities/           #
│   │   ├── __init__.py
│   │   ├── price.py        # Price, Signal, Order structures
│   │   ├── strategy.py
│   │   ├── account.py
│   │   └── transaction.py
│   │
│   ├── adapters/           # Bridges between core and infrastructure
│   │   ├── __init__.py
│   │   ├── cli.py          # Command-line interface controller
│   │   └── gateways.py     # Interfaces for external APIs
│   │
│   └── infrastructure/     # Concrete implementations (Frameworks & Tools)
│       ├── __init__.py
│       ├── crypto_api.py   # Real exchange connection (e.g., Binance, Coinbase)
│       └── logger.py       # Real-time logging setup
│
└── main.py                 # Application entry point (The "Wirer")