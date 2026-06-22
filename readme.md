# PROJECT PROFILE: Crypto Trading Bot (Python)
- **IDE:** Google Antigravity IDE
- **Architecture:** Strict Clean Architecture (Inward dependency rule).

# LAYER CONFIGURATION & NAMING CONVENTIONS:
1. 🌐 Domain: `{domain}_api.py` or `_port.py`
   - Content: Pure ABCs, frozen dataclasses, strict type hints, no logic.
   - Constraint: Python STDLIB ONLY (no external imports). Methods use `...`.
2. ⚙️ UseCase: `{verb}_{noun}_use_case.py`
   - Content: Orchestrates workflow via injected ports in `__init__`.
   - Entry point: `async def execute(...) -> T:`
3. 🔌 Adapter: `{tech}_{domain}_adapter.py`
   - Content: Translators (Gateways/Controllers). Implements ports, handles async cleanup.
4. 🏗️ Infrastructure: `{tech}_{resource}_infra.py`
   - Content: Heavy resources (WS clients, DB pools, Loggers), singletons/factories.

# RULES FOR AGENT:
- Read ONLY `_api.py` or `_port.py` files for structural references.
- Maintain maximum token efficiency: No redundant docstrings, use ellipsis (`...`) for abstract bodies.
- Composition happens strictly in `main.py`.
