## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-09 - Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` allowed arbitrary file reads via path traversal because it did not validate the `file_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** Similarly to output ports, file storage input ports (e.g. `BatchInputPort`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-09 - Missing Authentication on WebSocket Telemetry Broadcaster
**Vulnerability:** The `WebsocketBroadcaster` (part of the `AuditService`) defaulted to listening on `0.0.0.0` and exposed sensitive engine system states without any authentication check.
**Learning:** Background daemon services exposing internal states over the network (e.g., WebSockets, HTTP) must not bind globally (`0.0.0.0`) by default and must always implement some form of authentication (even if basic, like token-based).
**Prevention:** Change the default bind address to local (`127.0.0.1`), accept a token via URL parameters (e.g. `/?token=XYZ`), and securely retrieve standard default credentials from the environment variables (e.g. `os.getenv("AUDIT_WEBSOCKET_TOKEN")`) with a fallback to secure dynamically generated tokens `secrets.token_urlsafe(32)` if absent.
