> Applies to Sagittarius Engine v1.x

# EngineContext

The `EngineContext` class acts as the shared composition root of the Sagittarius Engine. It maintains references to every internal subsystem, the dependency injection container, the event bus, and the extension manager.

## Purpose

`EngineContext` is passed to extensions during their lifecycle methods (`initialize`, `start`, `stop`, `dispose`) so they can resolve dependencies or interact with the engine.

## Related APIs

- **[App](app.md)**: Exposes the primary facade.
- **[IExtension](extension.md)**: Interacts with the context.
- **[Dispatcher](dispatcher.md)**: Dispatches requests using container services.

---

## Reference

::: sagittarius_engine.kernel.context.EngineContext

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/api/engine_context.md)
