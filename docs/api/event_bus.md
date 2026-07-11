> Applies to Sagittarius Engine v1.x

# IEventBus

The `IEventBus` interface defines the contract for decoupled event publishing and subscription (Pub/Sub pattern) within the engine runtime.

## Purpose

Use `IEventBus` to notify other subsystems of occurrences (e.g., domain events or system lifecycle notifications) without coupling components together.

## Related APIs

- **[App](app.md)**: Exposes the primary event bus.
- **[EngineContext](engine_context.md)**: Exposes and registers the active event bus.

---

## Reference

::: sagittarius_engine.interfaces.i_event_bus.IEventBus

---

> [Found an issue? Edit this page on GitHub.]()
