## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.## 2024-07-20 - [Path Traversal in TemplateLoader]
**Vulnerability:** The `TemplateLoader.get_template_path` method dynamically resolved paths by joining the directory with `template_name` without verifying if the resulting path escaped the base directory, allowing a malicious path string (e.g., `"../../../../etc"`) to perform an arbitrary file read.
**Learning:** This existed because `os.path.join` natively allows directory traversal sequences if absolute validation isn't independently performed.
**Prevention:** Always use `os.path.realpath` to resolve both base and requested paths, then validate confinement via `os.path.commonpath([base_path, requested_path]) == base_path` before checking if the file exists or returning it.

## 2024-05-28 - [Path Traversal in BatchInputPort]
**Vulnerability:** BatchInputPort accepted a `file_path` and passed it directly to `open()` without verifying if the path escaped the intended boundaries, leading to arbitrary file read.
**Learning:** File input adapters in CLI or Batch contexts are just as vulnerable to Path Traversal as web endpoints. When fixing these issues, new security parameters (like `base_path`) must be appended to the end of the argument list to avoid breaking existing code using positional arguments.
**Prevention:** Always use `os.path.realpath` and `os.path.commonpath` to enforce boundary restrictions on user-provided file paths before interacting with the file system. Ensure signature modifications are backward compatible.
