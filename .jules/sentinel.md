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

## 2025-02-23 - Information Disclosure in AuditService Health Check
**Vulnerability:** `AuditService.get_system_health` caught exceptions during health checks and directly embedded the raw exception string (`str(e)`) in the returned dictionary, causing an information disclosure vulnerability.
**Learning:** Returning raw exception messages to callers (like a UI or API endpoint) can leak sensitive internals, such as stack traces, database schema details, or underlying code logic, especially when it originates from deeply nested calls like CQRS dispatchers.
**Prevention:** Never expose raw exception strings (`str(e)`) in external-facing or state-reporting methods. Instead, securely log the raw exception (e.g., `self._logger.error(f"Error: {e}")`) and return a generic error message (e.g., `"message": "An internal error occurred"`) to the caller.
## 2024-05-24 - Information Disclosure in Task Telemetry
**Vulnerability:** Raw exception strings (str(t.error)) were exposed in telemetry endpoints for background tasks.
**Learning:** Generic handlers in diagnostic or telemetry APIs often inadvertently expose internal logic and potential secrets via raw exception strings.
**Prevention:** Never directly assign exception string representations to output payload properties. Instead, securely log the raw error and substitute it with a generic, safe message like 'An internal error occurred'.
