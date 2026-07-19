## 2024-06-25 - DictConfig constructor optimization
**Learning:** Initializing configurations key-by-key using a python loop inside application bootstrapping takes noticeable CPU time when configuration sizes grow, because each `config.set` invokes internal python dictionary operations plus loop overhead.
**Action:** When loading configurations from files (like JSON), if the underlying store supports it, inject the entire dictionary at once via constructor arguments (`DictConfig(config_data)`) to bypass per-key iteration overhead.
## 2025-02-12 - Middleware Pipeline Iteration Optimization
**Learning:** `MiddlewarePipeline` uses recursive lambdas `lambda: self.__invoke_middleware(...)` which generates closures dynamically for every request, slowing down the pipeline due to call stack depth and closure instantiation overhead.
**Action:** Replace the recursive lambda execution chain with an iterative approach using `functools.partial` processing `reversed(self.middlewares)` to build a flat execution chain, avoiding recursion depth overhead and improving performance.
## 2025-02-13 - Event Bus Copy-On-Write Optimization
**Learning:** Frequent event emissions that require acquiring a thread lock in `emit()` to snapshot handlers can cause severe thread contention under high load.
**Action:** Use a Copy-On-Write (COW) pattern for Event Buses by storing handlers in an immutable `tuple` (e.g., `dict[str, tuple]`). This allows `emit()` to read the handlers completely lock-free, pushing the synchronization cost solely to the less frequent `on()` and `off()` registration methods.
