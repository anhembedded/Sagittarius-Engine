## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2025-02-09 - Path Traversal in BatchInputPort
**Vulnerability:** `BatchInputPort` allowed arbitrary file reads via path traversal because it did not validate the `file_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** Similarly to output ports, file storage input ports (e.g. `BatchInputPort`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.

## 2026-08-06 - Path Traversal in ProjectGenerator
**Vulnerability:** `ProjectGenerator.generate` allowed arbitrary file writes via path traversal because it did not validate the `project_name` parameter or dynamically rendered template directory paths (`rendered_rel_dir`) and file paths (`rendered_file_name`) before using them as destination paths.
**Learning:** File/Project generation tools must actively validate that all resolved output paths (including those derived from templates and user inputs) are confined within the safe `output_dir` (base path).
**Prevention:** Validate all resolved destination paths by comparing their `os.path.realpath` with the `os.path.realpath` of the base directory using `os.path.commonpath`. If they do not match, raise a `PathTraversalError`.
