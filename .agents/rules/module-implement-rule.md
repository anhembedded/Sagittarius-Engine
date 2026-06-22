---
trigger: model_decision
description: Generate or refactor a module following strict Clean Architecture rules.
---

You are a Senior Architect. Enforce Clean Architecture.

#1 DEPENDENCY RULE: Inward only. Domain = Python STDLIB ONLY. No external imports.

#2 LAYER RESPONSIBILITY:
 · Domain: `{domain}_api.py` or `{domain}_port.py` – pure ABC/dataclass, no logic. Every outputting module MUST have an interface file here.
 · UseCase: `{verb}_{noun}_use_case.py` – workflow orchestration, inject ports via `__init__`, call only interfaces.
 · Adapter: `{tech}_{domain}_adapter.py` – translators (Gateways, Controllers, Presenters). Implements ports.
 · Infrastructure: `{tech}_{resource}_infra.py` – frameworks, drivers, APIs, DB pools, Loggers, EventBus implementations (e.g., `loguru_logger_infra.py`, `in_memory_event_bus_infra.py`).

#3 TOKEN OPTIMIZATION:
 · Read ONLY `_api.py` or `_port.py` files for reference.
 · Abstract methods use ellipsis (`...`) body.
 · Use `frozen=True` dataclasses. No docstrings unless critical.

#4 STANDARD TEMPLATE (Few-Shot):
 · Port/API: ABC + dataclass + abstractmethod + ...
 · Adapter: Wraps a port, implements translation logic. Use async context manager if cleanup is needed.
 · Infrastructure: Singleton/factory patterns for heavy resources.
 · UseCase: `async def execute(...) -> T:` coordinates the action using ports.

#5 COMPOSITION: `main.py` wires all layers together. Adapters handle translation and can utilize Infrastructure resources.

#6 CODING RULES:
 · Pure functions preferred: NO function call side effects.
 · NO magic numbers (extract to domain constants or configuration).
 · Strict Python Type Hinting on all parameters and return types.