## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-09 - Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` allowed arbitrary file reads via path traversal because it did not validate the `file_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** Similarly to output ports, file storage input ports (e.g. `BatchInputPort`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2024-08-03 - Path Traversal bypass with default `None` base_path in BatchInputPort
**Vulnerability:** BatchInputPort's `base_path` default was set to `None`, effectively bypassing `os.path.commonpath` confinement checks unless a base path was explicitly provided. This allowed path traversal to any file (e.g., `/etc/passwd`).
**Learning:** Defaulting confinement root directories to `None` creates a critical fail-open vulnerability allowing unrestricted file system access, rather than a fail-closed secure state.
**Prevention:** Always default `base_path` to `""` (empty string) to safely confine paths to the Current Working Directory. The condition checking if `base_path is not None` must be removed so confinement is applied in all scenarios.
