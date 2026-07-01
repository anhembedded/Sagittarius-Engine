---
type: design_doc
tags: [sagittarius, module, health]
language: python
---

# HealthModule

## Overview
The `HealthModule` provides a lightweight, built-in mechanism to check the status of the application and its core dependencies.

## Problem Statement
In modern cloud environments (like Kubernetes or Docker Swarm), orchestrators need to know if an application is running (liveness) and ready to accept traffic (readiness). Exposing a standard set of health checks simplifies monitoring and deployment strategies.

## Proposed Solution
Sagittarius includes a `HealthModule` that can be added to the application. When registered, it typically exposes a query or endpoint (depending on the bound adapter) to report application status, checking critical dependencies like the Database.

## Core API / Interface

### `class HealthModule(BaseModule)` (in `src/modules/health_module.py`)
- `def register(self, app: App) -> None`: Registers health check components.
- `def boot(self, app: App) -> None`: Hooks into the boot lifecycle.

## Dependencies
- Internal: `BaseModule`, `App`

## How to Use / Examples

```python
from src.app_kernel import App
from src.modules.health_module import HealthModule

# Assuming app is initialized
app.use(HealthModule())
```

## Implementation Notes
- The specific implementation details (e.g. returning JSON vs simple booleans) depend on how the module is extended within the user's codebase, but the baseline module provides the standard structure.

## Related Documents
- `modules.md`
