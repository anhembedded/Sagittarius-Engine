## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.## 2024-07-20 - [Path Traversal in TemplateLoader]
**Vulnerability:** The `TemplateLoader.get_template_path` method dynamically resolved paths by joining the directory with `template_name` without verifying if the resulting path escaped the base directory, allowing a malicious path string (e.g., `"../../../../etc"`) to perform an arbitrary file read.
**Learning:** This existed because `os.path.join` natively allows directory traversal sequences if absolute validation isn't independently performed.
**Prevention:** Always use `os.path.realpath` to resolve both base and requested paths, then validate confinement via `os.path.commonpath([base_path, requested_path]) == base_path` before checking if the file exists or returning it.
