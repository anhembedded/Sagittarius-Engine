# Skill: Optimize Performance

> Context: You are optimizing a production system. The goal is to fix a measured, real problem — not to make code "look faster."
> The risk of premature or incorrect optimization is higher than the cost of the original slowness.

## 1. AI Blind Spots to Actively Address

* **Measure Before Touching:** AI agents often optimize by intuition. Every optimization MUST start with a profiling report or concrete metric. Never optimize code you haven't measured.
* **Benchmark or It Didn't Happen:** Changes must be validated with a before/after benchmark. "It should be faster" is not acceptable. State the actual measured improvement.
* **Algorithmic vs. Micro-Optimization:** AI frequently optimizes at the micro level (e.g., list comprehension vs. loop) while missing O(n²) algorithms or N+1 query problems that dominate cost by orders of magnitude. Fix algorithmic complexity first.
* **Cache Invalidation is the Hard Part:** When introducing caches, AI rarely implements invalidation. Define the exact invalidation strategy before caching anything: TTL, event-driven, manual, or none.
* **Concurrency Footgun:** Introducing parallelism or async to improve throughput often introduces deadlocks, race conditions, or resource exhaustion under load. These bugs are non-deterministic and catastrophic. Analyze thread safety before introducing concurrency.
* **Readability Cost:** Every optimization has a maintenance cost. If the code becomes significantly harder to read, document *why* the optimization exists and link to the benchmark that justifies it.

## 2. Tracking (Complex Tasks Only)

**Assess complexity first.** Only create a tracking file if the task meets the complexity threshold.
Refer to `../rules/task-tracking.md` for the full complexity gate criteria.

Typical triggers for this skill: benchmark required across multiple phases, concurrency changes with thread safety risk, multi-layer I/O optimization.

If tracking is needed:
```
.ai/tracking/optimize_<YYYYMMDD_HHMM>.md
```
Update phase status at the START and END of each phase.

## 3. Workflow

* **Phase 1 — Profile:** Gather evidence. Use profiling tools, APM data, or query analyzers. Identify the actual bottleneck, not the assumed one. → *Update tracking: 🔄 → ✅*
* **Phase 2 — Categorize:** Classify the bottleneck (Algorithmic / I/O / CPU / Memory / Concurrency). → *Update tracking*
* **Phase 3 — Hypothesize:** Propose a fix. Explain the expected improvement and the mechanism. → *Update tracking*
* **Phase 4 — Implement Minimally:** Apply the smallest possible change. → *Update tracking*
* **Phase 5 — Benchmark:** Measure before/after under realistic load. → *Update tracking*
* **Phase 6 — Validate Correctness:** Run full test suite. Performance changes must not alter behavior. → *Update tracking*
* **Phase 7 — Document:** Add comment explaining *why* the optimization exists and link to benchmark data. → *Update tracking: mark task DONE*

## 4. Optimization Priority Order

Apply fixes in this order — highest ROI first:

1. **Algorithm** — Replace O(n²) with O(n log n) or O(n).
2. **Query** — Eliminate N+1 queries, add indexes, use projections.
3. **I/O** — Batch operations, connection pooling, reduce round-trips.
4. **Concurrency** — Parallelize independent work, use async I/O.
5. **Caching** — Cache computed or fetched data with a defined invalidation strategy.
6. **Memory** — Reduce allocations, pool objects, avoid large intermediate copies.
7. **Micro** — Inline loops, avoid redundant method calls (only after all above are exhausted).

## 5. Forbidden Actions

* Never optimize without a measured baseline.
* Never introduce a cache without an invalidation strategy.
* Never parallelize code without analyzing thread safety first.
* Never sacrifice correctness for speed.
* Never remove or weaken tests as part of optimization.

## 6. Deliverables

* **Bottleneck Report:** Evidence of the problem (profile data, query plan, metric).
* **Optimization Applied:** What changed and why.
* **Benchmark Result:** Measured before/after comparison.
* **Correctness Proof:** Test suite passes with no regressions.
* **Inline Documentation:** Comment justifying the optimization with a link to the benchmark.

## 7. Golden Rule

If you cannot measure the improvement, you cannot claim the optimization worked.

Refer:
  - [Runtime Context](../context/runtime.md)
  - [Coding Style](../rules/coding-style.md)
  - [Testing](../context/testing.md)
