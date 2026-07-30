## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.
## 2024-05-24 - [Fix Path Traversal in BatchInputPort]
**Vulnerability:** Found a Path Traversal vulnerability in `BatchInputPort` when passing a file path that is joined with `base_path` but not validated properly.
**Learning:** Even internal adapter tools (like batch input ports) require robust path traversal defense to ensure inputs cannot escape the intended directory, as they could be abused if dynamic.
**Prevention:** Always use `os.path.realpath` and `os.path.commonpath` to validate bounded file operations inside constrained paths when joining variables. Default `base_path` to `None` to prevent inadvertently changing relative file loading behavior.
