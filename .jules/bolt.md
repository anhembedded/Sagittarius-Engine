## 2024-06-25 - DictConfig constructor optimization
**Learning:** Initializing configurations key-by-key using a python loop inside application bootstrapping takes noticeable CPU time when configuration sizes grow, because each `config.set` invokes internal python dictionary operations plus loop overhead.
**Action:** When loading configurations from files (like JSON), if the underlying store supports it, inject the entire dictionary at once via constructor arguments (`DictConfig(config_data)`) to bypass per-key iteration overhead.
## 2025-02-12 - Middleware Pipeline Iteration Optimization
**Learning:** `MiddlewarePipeline` uses recursive lambdas `lambda: self.__invoke_middleware(...)` which generates closures dynamically for every request, slowing down the pipeline due to call stack depth and closure instantiation overhead.
**Action:** Replace the recursive lambda execution chain with an iterative approach using `functools.partial` processing `reversed(self.middlewares)` to build a flat execution chain, avoiding recursion depth overhead and improving performance.
## 2024-05-19 - Template Rendering Optimization
**Learning:** Recompiling regular expressions inside loops is a common source of performance degradation in text processing utilities. In `TemplateRenderer`, iterating over a dictionary and compiling a new regex for every single placeholder key caused performance to scale negatively with the number of placeholders (`O(K * N)`). Using a single, generic pre-compiled regex with a matching function dramatically improves speed (measured a 61% reduction in execution time in benchmarks) and prevents unintended nested substitution bugs.
**Action:** Always prefer single-pass generic regex matching (`re.sub` with a callable) over multiple dynamic compilations when performing bulk text substitutions based on key-value mappings.

## $(date +%Y-%m-%d) - O(N^2) UI table update optimization
**Learning:** In PySide6 UI applications utilizing a `QTableWidget`, manually iterating through table rows to find and update existing items based on identifiers scales at O(N^2) complexity, quickly causing blocking behavior when tables grow large (e.g. hundreds or thousands of rows).
**Action:** When working with large sets of items in a UI table, cache unique identifiers to their corresponding `QTableWidgetItem` objects in a dictionary. This allows O(1) row updates by calling `.row()` on the item, dropping the overall complexity to O(N).
## 2025-03-09 - Lock Contention in High-Throughput EventBus
**Learning:** Using locks around mutable dictionaries (`_handlers`) during event emission causes significant thread contention when handlers are frequently invoked, crippling throughput in concurrent environments.
**Action:** Use a Copy-On-Write (COW) pattern for the `_handlers` registry. By storing handlers in immutable tuples (`tuple[Callable, ...]`), event emission (`emit()`) can perform a lock-free read `self._handlers.get(event_name, ())`, eliminating contention while moving the synchronization cost to the less frequent `on()` and `off()` operations.
## 2025-05-18 - Lock Contention in DI Container Resolution
**Learning:** Using locks around thread-safe dictionary reads (like `dict.get()`) during dependency resolution (`StdLibContainer._resolve`) causes unnecessary thread contention. In CPython, dictionary read operations are atomic and thread-safe due to the Global Interpreter Lock (GIL).
**Action:** Perform read-only dictionary lookups (e.g., `_factories.get`, `_resolution_cache.get`) lock-free outside of `threading.RLock()` blocks. Only acquire the lock when performing modifications or when executing logic that isn't inherently thread-safe (using double-checked locking).
## 2025-05-24 - Extension Initialization Sorting Overhead
**Learning:** Re-sorting a list (`sorted_exts = sorted(...)`) inside a `while` loop during extension initialization causes redundant O(N log N) operations for every iteration when the underlying list being sorted (`enabled_exts`) does not change.
**Action:** Ensure invariant operations such as sorting lists are hoisted outside of while or for loops to prevent redundant computational overhead.

## 2025-10-24 - Extension Initialization Iteration Optimization
**Learning:** During extension initialization resolution (`ExtensionManager._try_initialize_available`), repeatedly iterating over the full list of registered extensions to find pending ones causes redundant loop overhead, even if already initialized extensions are skipped via a quick `continue`. This results in O(N^2) worst-case performance when resolving deep dependency chains.
**Action:** Optimize iterative resolution loops by filtering out completed items into a new list (e.g., `pending_exts`) and re-assigning the iterator source (`sorted_exts = pending_exts`) at the end of each pass. This shrinks the search space progressively, eliminating redundant iterations.
