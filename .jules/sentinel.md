## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.
