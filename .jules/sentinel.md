## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2024-05-18 - [Fix Path Traversal in TemplateLoader]
**Vulnerability:** Path Traversal vulnerability found in `TemplateLoader.get_template_path()` where an attacker could provide an arbitrary path via `template_name` escaping the expected directory (e.g., `../../etc`).
**Learning:** `os.path.join` natively allows directory traversal sequences if absolute paths or parent directories (`..`) are supplied, leaving dynamically loaded components (such as project templates) vulnerable.
**Prevention:** Always validate that `os.path.commonpath([base_directory, requested_path])` equates to the `base_directory` after resolving absolute locations using `os.path.realpath()`.
