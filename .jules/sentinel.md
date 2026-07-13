## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2024-07-13 - Path Traversal in TemplateLoader
**Vulnerability:** TemplateLoader used `os.path.join` with untrusted template names without verifying the resulting path.
**Learning:** File generation tools resolving paths from user input must ensure the final resolved path does not traverse outside the intended sandbox. Dummy test files must not be left behind.
**Prevention:** Use `os.path.realpath` to resolve both the base and target paths, and enforce boundaries using `os.path.commonpath`. Always clean up generated files and carefully verify test changes.
