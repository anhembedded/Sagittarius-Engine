> Applies to Sagittarius Engine v1.x

# CancellationToken

The `CancellationToken` class provides a cooperative cancellation model that allows long-running tasks or loops to be stopped gracefully when requested.

## Purpose

Pass a `CancellationToken` to long-running task loops or operations, and periodically call `check_cancelled()` or inspect `is_cancelled` to terminate execution.

## Related APIs

- **[TaskManager](task_manager.md)**: Integrates with tokens to monitor execution states.
- **[Scheduler](scheduler.md)**: Uses cancellation tokens internally to manage jobs.

---

## Reference

::: sagittarius_engine.runtime.tasks.cancellation_token.CancellationToken

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/api/cancellation_token.md)
