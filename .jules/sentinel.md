## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2025-02-14 - Path Traversal in TemplateLoader
**Vulnerability:** `TemplateLoader.get_template_path` allowed resolving template paths outside of the configured template directories using `../` components, leading to potential path traversal vulnerabilities.
**Learning:** `os.path.join` and `os.path.exists` do not prevent relative directory escapes. Trusting unvalidated strings for path construction exposes the file system.
**Prevention:** Always use `os.path.realpath` to resolve absolute paths and `os.path.commonpath` to ensure the resolved path remains strictly within the intended base directory.
