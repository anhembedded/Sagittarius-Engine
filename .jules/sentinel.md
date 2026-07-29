## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.
## 2025-02-09 - Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` allowed arbitrary file reads via path traversal because it did not validate the `file_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** Adding a `base_path` parameter with a default of `""` to an input port causes severe functional regressions because `""` resolves to the Current Working Directory, inadvertently rejecting valid absolute paths if the parameter is omitted.
**Prevention:** Make `base_path` an `Optional[str] = None` and only enforce the `os.path.commonpath` boundary check if it is explicitly provided. This safely patches the traversal vector while fully preserving backward compatibility for callers using absolute paths.
