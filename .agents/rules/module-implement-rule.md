---
trigger: model_decision
description: Generate new module
---

1. LAYER BOUNDARY (NO LEAKAGE):
   - Only import from inner layers (Inward Dependency Rule).
   - NEVER import from outer layers.
   - Domain Layer: Use Python Standard Library ONLY (No third-party libraries).

2. SINGLE RESPONSIBILITY BY LAYER:
   - Domain: Pure Data Models (Entities) or Abstract Interfaces. No execution logic.
   - Use Cases: Business workflows. Call interfaces, never concrete external tools.
   - Adapters: Translators (Controllers, Gateways, Presenters) between Use Cases and Infrastructure.
   - Infrastructure: Frameworks, Database configs, Exchange APIs, Logger tools, EventBus engines.

3. TYPE SAFETY & DOCS:
   - Use strict Python Type Hinting for all parameters and return types.
   - Include concise docstrings explaining the 'what' and 'why'.

4. Clean architecture concept

5. Creating module Publish must have abstract class, not only implement class