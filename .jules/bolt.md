## 2024-06-25 - DictConfig constructor optimization
**Learning:** Initializing configurations key-by-key using a python loop inside application bootstrapping takes noticeable CPU time when configuration sizes grow, because each `config.set` invokes internal python dictionary operations plus loop overhead.
**Action:** When loading configurations from files (like JSON), if the underlying store supports it, inject the entire dictionary at once via constructor arguments (`DictConfig(config_data)`) to bypass per-key iteration overhead.
## 2025-02-12 - Middleware Pipeline Iteration Optimization
**Learning:** `MiddlewarePipeline` uses recursive lambdas `lambda: self.__invoke_middleware(...)` which generates closures dynamically for every request, slowing down the pipeline due to call stack depth and closure instantiation overhead.
**Action:** Replace the recursive lambda execution chain with an iterative approach using `functools.partial` processing `reversed(self.middlewares)` to build a flat execution chain, avoiding recursion depth overhead and improving performance.
## 2024-07-16 - EventBus Handler Array Optimization
**Learning:** Frequent events emitting to an `EventBus` encounter significant lock contention overhead if reading handlers requires a thread lock.
**Action:** Use a Copy-On-Write (COW) optimization. Store handlers in an immutable tuple (`self._handlers: dict[str, tuple[Callable, ...]]`). Modify `on` and `off` to copy and replace the tuple under a lock. This allows `emit` to perform a lock-free snapshot fetch `self._handlers.get(event_name, ())`, completely eliminating read locks during broadcast and significantly improving throughput.
