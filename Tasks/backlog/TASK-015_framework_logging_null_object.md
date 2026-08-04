# TASK-015: Framework Logging & Null Object Pattern

## Description
We have introduced a `NullLogger` (Null Object Pattern) to eliminate pervasive null checks (`if logger:`) throughout the engine. The fallback is configured in `EngineContext`. The logging statements in `app.py`'s `use`, `use_middleware`, and `boot` methods were recently removed by the user and need to be restored cleanly.

## Requirements
1. **Remove Null Checks:** Scan the framework (especially `sagittarius_engine/kernel/app.py` and any related services) and remove any remaining `if logger:` null checks.
2. **Restore Logging:** Add structured, informative logging back to the engine's core lifecycle and registration methods (e.g., `use`, `use_middleware`, `boot`).
3. **Use Safe Logger:** Rely directly on `_get_logger()` or `context.logger` knowing it will return a valid `ILogger` implementation (either a real logger or a `NullLogger`).
