# PROJECT CONTEXT

**Roots:**
- `C:\Users\hoang\Documents\Sagittarius_ForkBoy\examples`

**Pattern:** `*.py`
**Generated:** 2026-07-21 21:51:07

## Directory Tree: C:\Users\hoang\Documents\Sagittarius_ForkBoy\examples

```
examples
├── desktop
│   └── main.py
├── my_app
│   ├── controllers
│   │   └── __init__.py
│   ├── main.py
│   ├── models
│   │   └── __init__.py
│   └── views
│       └── __init__.py
├── my_bot
│   └── main.py
├── my_service
│   ├── adapters
│   │   └── __init__.py
│   ├── application
│   │   └── __init__.py
│   ├── domain
│   │   └── __init__.py
│   ├── infrastructure
│   │   └── __init__.py
│   ├── main.py
│   └── modules
│       └── __init__.py
├── plugin_system
│   └── main.py
├── rest_api
│   └── main.py
├── trading_bot
│   ├── app
│   │   ├── __init__.py
│   │   ├── exchanges
│   │   │   └── mock_exchange.py
│   │   └── strategies
│   │       └── mean_reversion.py
│   └── main.py
├── websocket
│   └── main.py
└── worker
    └── main.py
```

---

# FILE: desktop\main.py

```python
import time
from sagittarius_engine import App

class MockDesktopWindow:

def __init__(self, app: App) -> None:
        self.app = app
        self.logger = app.context.logger
        self.status_text = "Idle"

self.app.event_bus.on("ui.update_status", self.on_status_updated)

    def on_status_updated(self, event) -> None:
        self.status_text = event.text
        self.logger.info(f"[UI Thread] UI Label updated: {self.status_text}")

    def simulate_button_click(self) -> None:
        self.logger.info("[UI Thread] Button clicked! Spawning background work...")

        self.app.context.tasks.spawn(self.perform_heavy_calc, name="HeavyCalc")

    def perform_heavy_calc(self) -> None:
        self.logger.info("[Worker Thread] Starting heavy calculations...")
        time.sleep(0.05)
        self.logger.info("[Worker Thread] Calculations finished. Notifying UI...")

        class UIEvent:
            def __init__(self, text: str) -> None:
                self.text = text

        self.app.event_bus.emit("ui.update_status", UIEvent("Task Complete!"))

def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

app.use(LoggerModule())

app.boot()

window = MockDesktopWindow(app)

window.simulate_button_click()

time.sleep(0.1)

app.stop()

if __name__ == "__main__":
    main()
``````

# FILE: my_app\controllers\__init__.py

```python

``````

# FILE: my_app\main.py

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("MVC App 'my_app' booted successfully by Developer!")

if __name__ == "__main__":
    main()
``````

# FILE: my_app\models\__init__.py

```python

``````

# FILE: my_app\views\__init__.py

```python

``````

# FILE: my_bot\main.py

```python
from sagittarius_engine.infrastructure.container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot()
    print("Minimal App 'my_bot' booted successfully by Developer!")

if __name__ == "__main__":
    main()
``````

# FILE: my_service\adapters\__init__.py

```python

``````

# FILE: my_service\application\__init__.py

```python

``````

# FILE: my_service\domain\__init__.py

```python

``````

# FILE: my_service\infrastructure\__init__.py

```python

``````

# FILE: my_service\main.py

```python
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus
from sagittarius_engine.kernel import App

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    app.boot(auto_discover="modules")
    print(
        "Clean Architecture App 'my_service' booted successfully by Developer!"
    )

if __name__ == "__main__":
    main()
``````

# FILE: my_service\modules\__init__.py

```python

``````

# FILE: plugin_system\main.py

```python
import time
from sagittarius_engine import App, IExtension, ExtensionDescriptor

class MetricsPlugin(IExtension):
    def __init__(self) -> None:
        self._desc = ExtensionDescriptor(name="MetricsPlugin", priority=10)
        self.initialized = False

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._desc

    def register(self, context) -> None:
        self.initialized = True
        context.logger.info("[MetricsPlugin] Registered.")

    def boot(self, context) -> None:
        context.logger.info("[MetricsPlugin] Started.")

    def shutdown(self, context) -> None:
        context.logger.info("[MetricsPlugin] Stopped.")

    def dispose(self, context) -> None:
        context.logger.info("[MetricsPlugin] Disposed.")

class TradingPlugin(IExtension):
    def __init__(self) -> None:
        self._desc = ExtensionDescriptor(
            name="TradingPlugin", dependencies=["MetricsPlugin"], priority=5
        )
        self.initialized = False

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._desc

    def register(self, context) -> None:
        self.initialized = True
        context.logger.info("[TradingPlugin] Registered.")

    def boot(self, context) -> None:
        context.logger.info("[TradingPlugin] Started.")

    def shutdown(self, context) -> None:
        context.logger.info("[TradingPlugin] Stopped.")

    def dispose(self, context) -> None:
        context.logger.info("[TradingPlugin] Disposed.")

class DashboardPlugin(IExtension):
    def __init__(self) -> None:
        self._desc = ExtensionDescriptor(
            name="DashboardPlugin", dependencies=["TradingPlugin"], priority=0
        )
        self.initialized = False

    @property
    def descriptor(self) -> ExtensionDescriptor:
        return self._desc

    def register(self, context) -> None:
        self.initialized = True
        context.logger.info("[DashboardPlugin] Registered.")

    def boot(self, context) -> None:
        context.logger.info("[DashboardPlugin] Started.")

    def shutdown(self, context) -> None:
        context.logger.info("[DashboardPlugin] Stopped.")

    def dispose(self, context) -> None:
        context.logger.info("[DashboardPlugin] Disposed.")

def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

app.use(LoggerModule())

app.use(DashboardPlugin())
    app.use(TradingPlugin())
    app.use(MetricsPlugin())

app.boot()

time.sleep(0.05)

app.stop()

if __name__ == "__main__":
    main()
``````

# FILE: rest_api\main.py

```python
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService

class CreateUserCommand:

def execute(self, dto: dict) -> dict:
        return {"id": 1, "name": dto.get("name", "Unknown"), "status": "created"}

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):

        self.app = server.app
        super().__init__(request, client_address, server)

    def log_message(self, format, *args):

        self.app.context.logger.info(f"[HTTP Server] {format % args}")

    def do_POST(self) -> None:
        if self.path == "/users":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
            except ValueError:
                data = {}

result = self.app.dispatch(CreateUserCommand, data)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

class HttpHostedService(IHostedService):

def __init__(self, app: App, port: int = 8080) -> None:
        self.app = app
        self.port = port
        self.server = None
        self._thread = None

    def start(self, context) -> None:
        self.server = HTTPServer(("127.0.0.1", self.port), RequestHandler)
        self.server.app = self.app
        self._thread = threading.Thread(
            target=self.server.serve_forever, name="HttpServerThread", daemon=True
        )
        self._thread.start()
        context.logger.info(
            f"HTTP Server started on http://127.0.0.1:{self.port}"
        )

    def stop(self, context) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            context.logger.info("HTTP Server stopped.")
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

container.bind(CreateUserCommand, CreateUserCommand)

app.use(LoggerModule())

http_service = HttpHostedService(app, port=9090)
    app.context.hosted_services.register(http_service)

app.boot()

time.sleep(0.2)

app.stop()

if __name__ == "__main__":
    main()
``````

# FILE: trading_bot\app\__init__.py

```python

``````

# FILE: trading_bot\app\exchanges\mock_exchange.py

```python
import time
import random
from sagittarius_engine.runtime import IHostedService

class MockExchange(IHostedService):

def __init__(self) -> None:
        self.price = 100.0
        self.started = False

    def start(self, context) -> None:
        self.started = True
        context.logger.info("MockExchange connected. Price stream ready.")

    def stop(self, context) -> None:
        self.started = False
        context.logger.info("MockExchange disconnected.")

    def get_latest_price(self) -> float:
        self.price += random.uniform(-1.0, 1.0)
        return self.price

    def place_order(self, symbol: str, side: str, amount: float) -> str:
        time.sleep(0.05)
        return f"ORDER_ID_{random.randint(1000, 9999)}"
``````

# FILE: trading_bot\app\strategies\mean_reversion.py

```python
from sagittarius_engine import App
from examples.trading_bot.app.exchanges.mock_exchange import MockExchange

class TradingStrategy:

def __init__(self, app: App, exchange: MockExchange) -> None:
        self.app = app
        self.exchange = exchange
        self.logger = app.context.logger

    def check_market(self) -> None:
        price = self.exchange.get_latest_price()
        self.logger.info(f"[Strategy] Checked price: {price:.2f}")

        if price < 99.0:
            self.logger.info(
                f"[Strategy] Price {price:.2f} is cheap! Spawning BUY order task..."
            )
            self.app.context.tasks.spawn(self.buy)
        elif price > 101.0:
            self.logger.info(
                f"[Strategy] Price {price:.2f} is high! Spawning SELL order task..."
            )
            self.app.context.tasks.spawn(self.sell)

    def buy(self) -> None:
        self.logger.info("[OrderExecution] Connecting to exchange to BUY...")
        order_id = self.exchange.place_order("BTCUSDT", "BUY", 0.01)
        self.logger.info(f"[OrderExecution] BUY Order completed: {order_id}")

    def sell(self) -> None:
        self.logger.info("[OrderExecution] Connecting to exchange to SELL...")
        order_id = self.exchange.place_order("BTCUSDT", "SELL", 0.01)
        self.logger.info(f"[OrderExecution] SELL Order completed: {order_id}")
``````

# FILE: trading_bot\main.py

```python
import time
from sagittarius_engine import App
from examples.trading_bot.app.exchanges.mock_exchange import MockExchange
from examples.trading_bot.app.strategies.mean_reversion import TradingStrategy

def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

app.use(LoggerModule())

exchange = MockExchange()
    app.context.hosted_services.register(exchange)

app.boot()

strategy = TradingStrategy(app, exchange)

app.context.scheduler.every(seconds=0.1).do(strategy.check_market)

time.sleep(0.5)

app.stop()

if __name__ == "__main__":
    main()
``````

# FILE: websocket\main.py

```python
import asyncio
import logging
import time
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService, CancellationToken

class MockWebSocketClient(IHostedService):

def __init__(self, app: App) -> None:
        self.app = app
        self.logger = app.context.logger
        self.token = CancellationToken()
        self._main_task = None

    def start(self, context) -> None:

        self._main_task = self.app.context.tasks.spawn(
            self.connect_and_listen, name="WebSocketClient", token=self.token
        )
        self.logger.info("WebSocket Hosted Service started.")

    def stop(self, context) -> None:

        self.token.cancel()
        self.logger.info("WebSocket Hosted Service stopping...")
        if self._main_task and self._main_task.future:
            try:
                self._main_task.future.result(timeout=2.0)
            except Exception:
                pass
        self.logger.info("WebSocket Hosted Service stopped.")

    async def connect_and_listen(self, token: CancellationToken) -> None:
        backoff = 0.01
        while not token.is_cancelled():
            try:
                self.logger.info("[WebSocket] Attempting connection...")

                await asyncio.sleep(0.01)

                self.logger.info("[WebSocket] Connected! Starting heartbeat...")
                backoff = 0.01

heartbeat = asyncio.create_task(self.heartbeat_loop(token))

while not token.is_cancelled():

                    await asyncio.sleep(0.05)
                    self.logger.info("[WebSocket] Received price tick update.")

self.logger.warning("[WebSocket] Connection dropped by peer!")
                    break

                heartbeat.cancel()
                try:
                    await heartbeat
                except asyncio.CancelledError:
                    pass

            except Exception as e:
                self.logger.error(f"[WebSocket] Connection error: {e}")

            if not token.is_cancelled():
                self.logger.info(
                    f"[WebSocket] Reconnecting in {backoff}s..."
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 0.5)

    async def heartbeat_loop(self, token: CancellationToken) -> None:
        while not token.is_cancelled():
            try:
                await asyncio.sleep(0.03)
                self.logger.info("[WebSocket] Heartbeat PING sent.")
            except asyncio.CancelledError:
                break

def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

app.use(LoggerModule())

client = MockWebSocketClient(app)
    app.context.hosted_services.register(client)

    app.boot()

time.sleep(0.2)

app.stop()

if __name__ == "__main__":
    main()
``````

# FILE: worker\main.py

```python
import time
import queue
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService, CancellationToken

class QueueWorkerService(IHostedService):

def __init__(self, app: App) -> None:
        self.app = app
        self.logger = app.context.logger
        self.job_queue = queue.Queue()
        self.token = CancellationToken()
        self.task = None

    def start(self, context) -> None:

        self.task = self.app.context.tasks.spawn(
            self.consume_loop, name="QueueConsumer", token=self.token
        )
        self.logger.info("Queue worker started.")

    def stop(self, context) -> None:

        self.token.cancel()
        self.logger.info("Cancellation signalled to queue worker.")

if self.task and self.task.future:
            try:
                self.task.future.result(timeout=2.0)
            except Exception:
                pass
        self.logger.info("Queue worker stopped.")

    def add_job(self, data: str) -> None:
        self.job_queue.put(data)
        self.logger.info(f"[Producer] Queued job: '{data}'")

    def consume_loop(self, token: CancellationToken) -> None:
        while not token.is_cancelled():
            try:

                job = self.job_queue.get(timeout=0.02)
                self.logger.info(f"[Consumer] Processing job: '{job}'...")
                time.sleep(0.05)
                self.logger.info(f"[Consumer] Completed job: '{job}'")
                self.job_queue.task_done()
            except queue.Empty:
                continue

def main():
    from sagittarius_engine.infrastructure.container.std_container import (
        StdLibContainer,
    )
    from sagittarius_engine.infrastructure.event_bus.memory_event_bus import (
        MemoryEventBus,
    )
    from sagittarius_engine.extensions.logger_module import LoggerModule

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

app.use(LoggerModule())

worker = QueueWorkerService(app)
    app.context.hosted_services.register(worker)

    app.boot()

worker.add_job("Import Transactions")
    worker.add_job("Generate Reports")
    worker.add_job("Send Email Notifications")

time.sleep(0.2)

app.stop()

if __name__ == "__main__":
    main()
``````

