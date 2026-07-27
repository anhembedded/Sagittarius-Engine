import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from sagittarius_engine import App
from sagittarius_engine.runtime import IHostedService


class CreateUserCommand:
    """
    @brief Simulates a command to create a user.
    """

    def execute(self, dto: dict) -> dict:
        return {"id": 1, "name": dto.get("name", "Unknown"), "status": "created"}


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        # Store context/app reference from server instance
        self.app = server.app
        super().__init__(request, client_address, server)

    def log_message(self, format, *args):
        # Forward HTTP server logging to engine logger
        self.app.context.logger.info(f"[HTTP Server] {format % args}")

    def do_POST(self) -> None:
        if self.path == "/users":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
            except ValueError:
                data = {}

            # Execute command via unified engine dispatch
            result = self.app.dispatch(CreateUserCommand, data)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class HttpHostedService(IHostedService):
    """
    @brief Exposes HTTP Server as an engine hosted service.
    """

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
        context.logger.info(f"HTTP Server started on http://127.0.0.1:{self.port}")

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
    from sagittarius_engine.extensions.logger_module import LoggerExtension

    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Register command in container
    container.bind(CreateUserCommand, CreateUserCommand)

    # Register logger
    app.use(LoggerExtension())

    # Create and register HttpHostedService on custom port
    http_service = HttpHostedService(app, port=9090)
    app.context.hosted_services.register(http_service)

    # Boot the application
    app.boot()

    # Let the server run briefly
    time.sleep(0.2)

    # Stop the application gracefully
    app.stop()


if __name__ == "__main__":
    main()
