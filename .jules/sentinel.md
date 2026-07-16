## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2026-07-16 - Path Traversal Vulnerability in TemplateLoader
**Vulnerability:** The `TemplateLoader.get_template_path` method was vulnerable to path traversal because it did not validate that the requested template name (`template_name`) resolved to a location inside the allowed template directories, allowing paths like `../../../../etc` to escape confinement.
**Learning:** Utilities that load file paths using raw string combinations (`os.path.join`) without absolute path validation (`os.path.realpath`) and root confinement checks (`os.path.commonpath`) are highly vulnerable to path traversal.
**Prevention:** Always resolve arbitrary file paths using `os.path.realpath` and enforce path confinement constraints with `os.path.commonpath` before checking for path existence.
