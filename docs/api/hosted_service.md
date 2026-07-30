> Applies to Sagittarius Engine v1.x

# IHostedService

The `IHostedService` interface defines the standard contract for managed long-running services (background processes) that participate in the application host lifecycle.

## Purpose

Implement `IHostedService` for classes that need to start background loops (e.g. web servers, message queue consumers, trading bots) when the application boots and stop gracefully on shutdown.

## Related APIs

- **[App](app.md)**: Coordinates boot and shutdown lifecycles.
- **[TaskManager](task_manager.md)**: Frequently used to spawn internal worker loops.

---

## Reference

::: sagittarius_engine.runtime.hosted.hosted_service.IHostedService

---

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/api/hosted_service.md)
