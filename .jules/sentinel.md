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

## 2025-02-13 - Denial of Service (DoS) in IPC Event Bus Components
**Vulnerability:** IPC components (`IPCQueueEventBus` and `IPCBroker`) were vulnerable to Denial of Service (DoS) crashes caused by placing unpicklable objects into a `multiprocessing.Queue`. This causes the internal background `_feed` thread to permanently crash.
**Learning:** When using `multiprocessing.Queue` in concurrent or IPC scenarios, inserting non-serializable data does not fail synchronously on `put()`. Instead, it causes a silent background thread crash, permanently halting IPC communication for the entire process.
**Prevention:** To prevent DoS crashes in `multiprocessing.Queue`'s background `_feed` thread caused by unpicklable data, IPC components must synchronously validate data serializability using `pickle.dumps()` within a try-except block before calling `queue.put()`.
