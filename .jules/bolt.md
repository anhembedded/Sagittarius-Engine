## 2024-06-25 - DictConfig constructor optimization
**Learning:** Initializing configurations key-by-key using a python loop inside application bootstrapping takes noticeable CPU time when configuration sizes grow, because each `config.set` invokes internal python dictionary operations plus loop overhead.
**Action:** When loading configurations from files (like JSON), if the underlying store supports it, inject the entire dictionary at once via constructor arguments (`DictConfig(config_data)`) to bypass per-key iteration overhead.
## 2025-02-12 - Middleware Pipeline Iteration Optimization
**Learning:** `MiddlewarePipeline` uses recursive lambdas `lambda: self.__invoke_middleware(...)` which generates closures dynamically for every request, slowing down the pipeline due to call stack depth and closure instantiation overhead.
**Action:** Replace the recursive lambda execution chain with an iterative approach using `functools.partial` processing `reversed(self.middlewares)` to build a flat execution chain, avoiding recursion depth overhead and improving performance.
## 2025-02-18 - AsyncioEventBus optimization

**Learning:** Lock-free reads and the Copy-On-Write pattern using tuples can slightly improve performance in `AsyncioEventBus.emit()` by avoiding mutable list snapshots on every emit.
**Action:** When implementing high-frequency event busses, consider storing event handlers as immutable tuples to allow lock-free, allocation-free iteration during the highly-executed emit path, pushing the minor lock and copy overhead to the less frequent on/off paths.
