## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.## 2024-07-20 - [Path Traversal in TemplateLoader]
**Vulnerability:** The `TemplateLoader.get_template_path` method dynamically resolved paths by joining the directory with `template_name` without verifying if the resulting path escaped the base directory, allowing a malicious path string (e.g., `"../../../../etc"`) to perform an arbitrary file read.
**Learning:** This existed because `os.path.join` natively allows directory traversal sequences if absolute validation isn't independently performed.
**Prevention:** Always use `os.path.realpath` to resolve both base and requested paths, then validate confinement via `os.path.commonpath([base_path, requested_path]) == base_path` before checking if the file exists or returning it.
## 2024-05-18 - [Path Traversal in BatchOutputPort]
**Vulnerability:** BatchOutputPort accepted relative paths like `../` and passed them directly to `open()` without validation.
**Learning:** File paths passed dynamically to I/O ports or file storage components must always be constrained to an intended directory. The fact that the directory is created if missing (`os.makedirs`) actively exacerbates the issue by creating unexpected directories outside the sandbox.
**Prevention:** Always require an explicit `allowed_dir` parameter for file operations, resolve both the allowed dir and the target file via `os.path.realpath()`, and enforce confinement using `os.path.commonpath()`. Do not rely on input sanitization (like removing `../`); always use absolute path resolution and prefix validation.
## 2025-02-09 - Path Traversal in BatchOutputPort
**Vulnerability:** `BatchOutputPort` allowed arbitrary file writes via path traversal because it did not validate the `output_path` parameter, passing user-controlled paths directly to `open()`.
**Learning:** File storage ports (e.g. `BatchOutputPort`, `LocalFileStorage`) must actively validate that the resolved path is confined within a safe `base_path`. A default behavior of lacking a `base_path` fails open, creating critical risks.
**Prevention:** Require a `base_path` parameter with a safe default (or explicitly pass it from callers), resolve all paths with `os.path.realpath`, and use `os.path.commonpath` to ensure the final path resides within the base directory. If an attempt to escape is detected, raise `PathTraversalError`.
