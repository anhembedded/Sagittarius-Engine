> Applies to Sagittarius Engine v1.x

# IExtension & ExtensionDescriptor

The `IExtension` interface defines the standard plugin contract for extending the Sagittarius Engine runtime capability. The `ExtensionDescriptor` specifies metadata, dependencies, and execution priority.

## Purpose

Implement `IExtension` to register concrete adapters, configure services in the container, and register event bus handlers.

## Related APIs

- **[App](app.md)**: Exposes the `.use()` method to load extensions.
- **[EngineContext](engine_context.md)**: Coordinates extension initialization.

---

## ExtensionDescriptor Reference

::: sagittarius_engine.interfaces.i_extension.ExtensionDescriptor

---

## IExtension Reference

::: sagittarius_engine.interfaces.i_extension.IExtension

---

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/api/extension.md)
