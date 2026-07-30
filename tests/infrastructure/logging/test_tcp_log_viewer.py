import json
import socket
import threading
import time
from sagittarius_engine.infrastructure.config.dict_config import DictConfig
from sagittarius_engine.infrastructure.logging.std_logger import StdLogger
from sagittarius_engine.infrastructure.logging.tcp_log_viewer_handler import (
    TcpLogViewerHandler,
)


class MockTcpLogServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 0) -> None:
        self.host = host
        self.received_logs: list[dict] = []
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, port))
        self.port = self._server_socket.getsockname()[1]
        self._server_socket.listen(5)
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._accept_loop, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _accept_loop(self) -> None:
        self._server_socket.settimeout(0.5)
        while not self._stop_event.is_set():
            try:
                client_sock, _ = self._server_socket.accept()
                threading.Thread(
                    target=self._handle_client, args=(client_sock,), daemon=True
                ).start()
            except socket.timeout:
                continue
            except Exception:
                break

    def _handle_client(self, client_sock: socket.socket) -> None:
        client_sock.settimeout(2.0)
        buffer = ""
        while not self._stop_event.is_set():
            try:
                data = client_sock.recv(4096).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        self.received_logs.append(json.loads(line))
            except Exception:
                break
        client_sock.close()

    def stop(self) -> None:
        self._stop_event.set()
        try:
            self._server_socket.close()
        except Exception:
            pass
        if self._thread.is_alive():
            self._thread.join(timeout=1.0)


def test_tcp_log_viewer_handler_transmission():
    server = MockTcpLogServer()
    server.start()

    try:
        handler = TcpLogViewerHandler(
            host=server.host,
            port=server.port,
            module_name="test-service",
        )

        import logging

        logger = logging.getLogger("TestTcpLogger")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        logger.info(
            "Service booted successfully", extra={"extra": {"request_id": "req-123"}}
        )

        # Give background worker thread brief time to deliver log over TCP
        time.sleep(0.5)

        assert len(server.received_logs) >= 1
        last_log = server.received_logs[-1]
        assert last_log["message"] == "Service booted successfully"
        assert last_log["module"] == "test-service"
        assert last_log["level"] == "INFO"
        assert last_log["extra"] == {"request_id": "req-123"}
    finally:
        handler.close()
        server.stop()


def test_std_logger_structured_logging():
    server = MockTcpLogServer()
    server.start()

    try:
        config = DictConfig(
            {
                "log.viewer.enabled": True,
                "log.viewer.host": server.host,
                "log.viewer.port": server.port,
                "log.viewer.module": "student-test-app",
            }
        )

        logger = StdLogger(config)
        logger.info(
            "User created",
            extra={"user_id": 99, "role": "admin", "submodule": "UserService"},
        )

        time.sleep(0.5)

        assert len(server.received_logs) >= 1
        log_data = server.received_logs[-1]
        assert log_data["message"] == "User created"
        assert log_data["module"] == "student-test-app"
        assert log_data["submodule"] == "UserService"
        assert log_data["extra"] == {"user_id": 99, "role": "admin"}
    finally:
        server.stop()
