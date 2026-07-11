> Applies to Sagittarius Engine v1.x

# TaskManager

The `TaskManager` coordinates spawning, executing, tracking, and canceling synchronous threads and asynchronous tasks.

## Purpose

Use the `TaskManager` to spawn long-running parallel tasks, fire-and-forget operations, or safe cooperative async loops.

## Related APIs

- **[CancellationToken](cancellation_token.md)**: Pass tokens to support graceful cancellation.
- **[Scheduler](scheduler.md)**: Coordinates time-based execution.

---

## Reference

::: sagittarius_engine.runtime.tasks.task_manager.TaskManager

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/api/task_manager.md)
