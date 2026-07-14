## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2026-07-14 - Fix Path Traversal in TemplateLoader
**Vulnerability:** A path traversal vulnerability existed in `TemplateLoader` due to inadequate path validation using only `os.path.join`, allowing templates to be loaded from outside the designated directories (e.g., using `../`).
**Learning:** `os.path.join` does not prevent resolving paths outside the root directory when `../` is used.
**Prevention:** Always use `os.path.realpath` and verify the resolved path remains within the base directory using `os.path.commonpath` when loading files dynamically based on input.
