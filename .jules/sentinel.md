## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-09 - Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` allowed arbitrary file reads via path traversal because it did not validate the `file_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** Similarly to output ports, file storage input ports (e.g. `BatchInputPort`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-12 - Fail-Open Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` implemented path traversal defenses but defaulted `base_path` to `None`, bypassing the checks completely and creating a critical fail-open vulnerability allowing unrestricted file system access.
**Learning:** Security controls must be fail-closed. Defaulting a confinement parameter to `""` securely restricts access to the current working directory, whereas bypassing checks on `None` silently disables the defense.
**Prevention:** When implementing path traversal defenses, ensure the default parameter (e.g., `base_path`) enforces a restrictive boundary (like `""`) instead of `None`, and execute validation unconditionally.

## 2026-08-12 - Insecure Bind Address in WebsocketBroadcaster
**Vulnerability:** `WebsocketBroadcaster` defaulted to binding on `0.0.0.0`, exposing telemetry broadcast endpoints to any network interface and potentially unauthorized actors.
**Learning:** Defaulting to all interfaces (`0.0.0.0`) without authentication is dangerous for services broadcasting system state or telemetry. Network listeners should bind to loopback (`127.0.0.1`) by default unless external exposure is explicitly required and secured.
**Prevention:** Default internal and unauthenticated network listeners to `127.0.0.1`. Allow configuration for users to explicitly opt into external binding.
