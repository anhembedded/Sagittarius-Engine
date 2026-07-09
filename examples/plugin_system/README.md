# Plugin System Reference Application

This reference application validates dynamic extension loading, topological dependency sorting, and correct lifecycle phases execution.

## Key Patterns
- **Topological Sorting**: We register `AddonPlugin` before `CorePlugin` in `main.py`, but the engine correctly resolves the dependency graph and boots `CorePlugin` first.
- **Unified Lifecycles**: Validates that plugins receive `initialize()`, `start()`, `stop()`, and `dispose()` triggers in the correct sequence.
