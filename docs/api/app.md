> Applies to Sagittarius Engine v1.x

# App

The `App` class is the primary entry point and orchestrator for the Sagittarius Engine. It initializes the dependency injection container, the event bus, and coordinates the boot and shutdown phases of the application host.

## Purpose

Use `App` to configure your composition root, load extensions, attach middleware pipelines, and trigger the boot sequence.

## Related APIs

- **[EngineContext](engine_context.md)**: Coordinates operations under the hood.
- **[IEventBus](event_bus.md)**: Manages communication between components.
- **[IExtension](extension.md)**: Extend App capabilities.

---

## Reference

::: sagittarius_engine.kernel.app.App

---

> [Found an issue? Edit this page on GitHub.]()
