## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2025-03-09 - Path Traversal Vulnerability in TemplateLoader
**Vulnerability:** The `TemplateLoader` implementation allowed escaping the template base directory by accepting paths containing `../` via the template name resolution, potentially leading to arbitrary file read.
**Learning:** This existed because `os.path.join()` doesn't inherently prevent traversal when concatenated with user-provided directory components if they are not explicitly validated against a confined base directory.
**Prevention:** Always use `os.path.realpath` to resolve both base and final paths and verify that the base path remains a common prefix of the final path using `os.path.commonpath`.
