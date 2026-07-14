## 2024-06-25 - DictConfig constructor optimization
**Learning:** Initializing configurations key-by-key using a python loop inside application bootstrapping takes noticeable CPU time when configuration sizes grow, because each `config.set` invokes internal python dictionary operations plus loop overhead.
**Action:** When loading configurations from files (like JSON), if the underlying store supports it, inject the entire dictionary at once via constructor arguments (`DictConfig(config_data)`) to bypass per-key iteration overhead.
## 2025-02-12 - Middleware Pipeline Iteration Optimization
**Learning:** `MiddlewarePipeline` uses recursive lambdas `lambda: self.__invoke_middleware(...)` which generates closures dynamically for every request, slowing down the pipeline due to call stack depth and closure instantiation overhead.
**Action:** Replace the recursive lambda execution chain with an iterative approach using `functools.partial` processing `reversed(self.middlewares)` to build a flat execution chain, avoiding recursion depth overhead and improving performance.
## 2024-07-14 - EventBus Lock-free Emit Optimization
**Learning:** Using `threading.Lock()` for reading `_handlers` dictionaries containing `list`s in `EventBus` implementations creates severe lock contention during high-frequency event emissions.
**Action:** Replace `list` with a `tuple` (Copy-On-Write) for handlers. This allows removing the read lock inside the `emit()` method because tuples are immutable, providing a massive performance boost (e.g. from ~32s to ~0.2s for 1M events). Write operations (`on`, `off`) still use the lock and replace the tuple.
