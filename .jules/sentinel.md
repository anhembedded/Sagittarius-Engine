## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.
## 2025-02-12 - Path Traversal in TemplateLoader
**Vulnerability:** TemplateLoader's `get_template_path` did not sanitize the user-provided `template_name`, allowing path traversal (e.g. `../../../../etc`) to escape the template directories.
**Learning:** `os.path.join` does not validate whether the resulting path stays within the base directory. Checking for existence (`os.path.exists`) without bounds validation introduces both path traversal and directory existence oracle vulnerabilities.
**Prevention:** Always use `os.path.realpath` and `os.path.commonpath` to validate that a joined path remains within the intended base directory *before* performing any file existence or access operations.
