> Applies to Sagittarius Engine v1.x

# Dispatcher

The `Dispatcher` is responsible for routing command and query requests through the application's registered middleware pipeline before invoking the final request handler.

## Purpose

Use the `Dispatcher` (via `App.dispatch`) to execute commands and queries. This decouples request senders from their handlers.

## Related APIs

- **[App](app.md)**: Exposes the `dispatch` method directly.
- **[EngineContext](engine_context.md)**: Owns the dispatcher instance.

---

## Reference

::: sagittarius_engine.kernel.dispatcher.Dispatcher

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/api/dispatcher.md)
