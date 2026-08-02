## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-09 - Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` allowed arbitrary file reads via path traversal because it did not validate the `file_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** Similarly to output ports, file storage input ports (e.g. `BatchInputPort`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.
## 2024-08-02 - Defaulting Base Path to Empty String for Path Traversal Defense
**Vulnerability:** BatchInputPort had a path traversal vulnerability because `base_path` defaulted to `None` and the confinement check was bypassed when `base_path` was `None`. This allowed unconfined arbitrary file read access (e.g., `../../etc/passwd`).
**Learning:** In path traversal defenses using `os.path.commonpath`, defaulting the `base_path` parameter to `None` and conditionally applying the check creates a critical fail-open vulnerability.
**Prevention:** Default `base_path` to `""` (empty string) instead of `None` to provide a secure, fail-closed model (confined to the Current Working Directory) and apply the confinement check unconditionally.
