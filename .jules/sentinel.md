## 2024-07-09 - Information Disclosure in Health Check
**Vulnerability:** HealthCheckQuery exposed raw exception strings (`str(e)`) in its response status.
**Learning:** Exposing raw exceptions can leak sensitive internal implementation details or stack traces to unauthorized parties.
**Prevention:** Always catch exceptions and return generic, safe error messages in health checks or API responses.