# Skill: Implement Module

> Context: You are a Principal Software Engineer designing a production-ready module.
> Critical Rule: A module is not just isolated code; it is a citizen of a larger ecosystem.

## 1. AI Blind Spots to Actively Avoid

Before writing any implementation, you MUST address these common AI oversights:

* **Reinventing the Wheel:** Scan the codebase for existing utilities (Loggers, Config parsers, Event Buses, DI containers). DO NOT build custom versions of existing shared logic.
* **Lifecycle Neglect:** If your module allocates resources (memory, sockets, file handles, hardware states), you MUST provide explicit and deterministic teardown/cleanup mechanisms.
* **Concurrency & State:** Assume the module will be called in a multi-threaded environment. Avoid mutable global/static state. Ensure operations are thread-safe or strictly isolated.
* **Silent Failures:** Do not use empty `catch` blocks or generic error swallowing. Fail fast on invalid configurations, and gracefully degrade on runtime anomalies.

## 2. Design & Architecture Boundaries

* **Contract First:** Always define the public Interface/API (the "What") before implementing the details (the "How"). Hide all implementation details behind boundaries.
* **Strict OOP & Dependency Injection:** Dependencies must be injected, not instantiated internally. Avoid tight coupling to concrete infrastructure.
* **Idempotency:** Ensure that calling start, stop, or processing functions multiple times does not corrupt the system state or cause side effects.

## 3. Tracking (Complex Tasks Only)

**Assess complexity first.** Only create a tracking file if the task meets the complexity threshold.
Refer to `../rules/task-tracking.md` for the full complexity gate criteria.

Typical triggers for this skill: module integrates with 3+ systems, lifecycle management is non-trivial, user approval needed before integration wiring.

If tracking is needed:
```
.ai/tracking/implement_<YYYYMMDD_HHMM>.md
```
Update phase status at the START and END of each phase.

## 4. Implementation Workflow

1. **Scope Alignment:** State the exact scope. Explicitly list what is OUT of scope to prevent hallucinated features. → *Update tracking: 🔄 → ✅*
2. **Integration Points:** Identify how this module registers with the system (e.g., DI bindings, startup hooks, routing tables). → *Update tracking*
3. **Observability:** Implement structured logging, tracing context, and telemetry. → *Update tracking*
4. **Static Analysis Compliance:** Ensure code conforms to typing, static analysis rules, and naming conventions. → *Update tracking: mark task DONE after validation*

## 5. Deliverables & Exit Criteria

When implementing a module, your output must include:

* **Public API / Interface:** The strict contract exposed to the system.
* **Implementation:** Clean, minimal, and fully documented internal logic.
* **Lifecycle Management:** Explicit initialization and destruction logic.
* **Integration Instructions:** How to wire this module into the existing DI container or orchestration layer.
* **Testing Strategy:** Unit tests for both the "happy path" and specifically for failure modes, resource cleanup, and invalid inputs.

## 6. Golden Rule

If the requirements are ambiguous regarding how the module should handle edge cases (e.g., network timeout, memory constraints), STOP and ask the user. Never silently assume default behaviors.

Refer:
    - [Coding Rule](../rules/coding-style.md)
    - [repo tree](../context/repository.md)
    - [test](../context/testing.md)