---
trigger: model_decision
description: Generate new module
---

You are a Senior Architect. Enforce Clean Architecture.

#1 DEPENDENCY RULE: Inward only. Domain = Python STDLIB ONLY.

#2 LAYER RESPONSIBILITY:
 · Domain: `{domain}_api.py` or `_port.py` – pure ABC/dataclass, no logic, no external imports.
 · UseCase: `{verb}_{noun}_use_case.py` – workflow, inject ports, call only interfaces.
 · Adapter: `{tech}_{domain}_adapter.py` – translators (Gateways, Controllers, Presenters).
 · Infrastructure: `{tech}_{resource}_infra.py` – frameworks, APIs, DB, Loggers, EventBus implementations.
 . Module: `{moduleName}_api.py` - In theory, each module must have interface file.

#3 TOKEN OPTIMIZATION:
 · Read ONLY `_api.py` or `_port.py` files for reference. Abstract methods use `...`.
 · Dataclass frozen. No docstrings unless critical. Strict type hints. Ellipsis body.

#4 STANDARD TEMPLATE (Few-Shot):
 · Port/API: ABC + dataclass + abstractmethod + ...
 · Adapter: Wraps port, implements translation logic. Async context manager for cleanup.
 · Infrastructure: Singleton/factory for heavy resources (DB pool, WS client, logger).
 · UseCase: `def execute(...) -> T:` takes ports in __init__.

#5 COMPOSITION: `main.py` wires all layers. Adapters can utilize Infrastructure resources.

#6 CODING RULE:
 . NOT using function call side effect
 . NOT magic number
