## 2024-06-25 - DictConfig constructor optimization
**Learning:** Initializing configurations key-by-key using a python loop inside application bootstrapping takes noticeable CPU time when configuration sizes grow, because each `config.set` invokes internal python dictionary operations plus loop overhead.
**Action:** When loading configurations from files (like JSON), if the underlying store supports it, inject the entire dictionary at once via constructor arguments (`DictConfig(config_data)`) to bypass per-key iteration overhead.
## 2025-02-12 - Middleware Pipeline Iteration Optimization
**Learning:** `MiddlewarePipeline` uses recursive lambdas `lambda: self.__invoke_middleware(...)` which generates closures dynamically for every request, slowing down the pipeline due to call stack depth and closure instantiation overhead.
**Action:** Replace the recursive lambda execution chain with an iterative approach using `functools.partial` processing `reversed(self.middlewares)` to build a flat execution chain, avoiding recursion depth overhead and improving performance.
## 2025-02-12 - COW Tuples for Lock-Free Event Emissions
**Learning:** Using lists for event handlers requires obtaining a lock during `emit()` to safely copy or iterate, causing lock contention in high-throughput event buses.
**Action:** Use a Copy-On-Write (COW) pattern by storing handlers in immutable `tuple`s (`dict[str, tuple[Callable, ...]]`). This allows `emit()` to perform lock-free reads, significantly improving throughput for frequent event emissions.
