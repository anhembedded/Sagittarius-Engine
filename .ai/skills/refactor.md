# Skill: Refactor

> Context: Refactoring improves structure without changing observable behavior.
> The risk is high: you must change code without breaking anything. Every step must be verifiable.

## 1. AI Blind Spots to Actively Address

* **Behavioral Equivalence is Non-Negotiable:** AI agents often refactor and subtly change behavior. Before starting, define the exact observable behavior that must be preserved (outputs, errors, side effects, event order, timing).
* **Test Coverage Gap:** If tests do not cover the code being refactored, write characterization tests *first* before changing anything. Refactoring without a safety net is rewriting.
* **Rename Propagation:** Renaming a symbol (class, method, constant) must be propagated to ALL references: code, tests, docs, configuration, serialized data, API contracts. AI often misses non-code references.
* **Refactor ≠ Redesign:** Refactoring is structural improvement, not feature addition or architectural redesign. If the scope expands during refactoring, stop and ask the user.
* **Incremental Commits:** One logical change per commit. Never bundle multiple refactoring types (e.g., extract + rename + move) in a single commit. This makes rollback impossible.
* **Public API Freeze:** During refactoring, the public API must remain unchanged. If an API must change, that is a separate, explicitly approved task.

## 2. Tracking (Complex Tasks Only)

**Assess complexity first.** Only create a tracking file if the task meets the complexity threshold.
Refer to `../rules/task-tracking.md` for the full complexity gate criteria.

Typical triggers for this skill: rename propagation across 3+ modules, no existing test coverage (safety net phase required), multi-session execution.

If tracking is needed:
```
.ai/tracking/refactor_<YYYYMMDD_HHMM>.md
```
Update phase status at the START and END of each phase.

## 3. Workflow

* **Phase 1 — Audit:** Identify *why* this code needs refactoring. Name the smell: God Class, Feature Envy, Long Method, Shotgun Surgery, Primitive Obsession, etc. → *Update tracking: 🔄 → ✅*
* **Phase 2 — Safety Net:** Verify test coverage for all paths being touched. If coverage is insufficient, add characterization tests first. → *Update tracking*
* **Phase 3 — Plan:** Define the exact sequence of atomic refactoring steps. Each step must leave the code in a buildable, testable state. → *Update tracking*
* **Phase 4 — Execute Incrementally:** Apply one step at a time. Build and run tests after each step. → *Update tracking*
* **Phase 5 — Cross-Reference Sweep:** After renaming or moving any symbol, scan: code, tests, docs, configs, comments, serialization schemas. → *Update tracking*
* **Phase 6 — Validate:** All tests pass. No regressions. No dead code introduced. Lint clean. → *Update tracking: mark task DONE*

## 4. Refactoring Catalog (Common Patterns)

Apply the appropriate technique for each smell:

| Smell | Technique |
|-------|-----------|
| Long Method | Extract Method |
| God Class | Extract Class / Move Method |
| Duplicate Code | Extract Function / Template Method |
| Primitive Obsession | Introduce Value Object |
| Feature Envy | Move Method to correct owner |
| Inappropriate Intimacy | Introduce Interface / Facade |
| Shotgun Surgery | Move related logic together |
| Data Clumps | Introduce Parameter Object |

## 5. Forbidden Actions

* Never change business logic during refactoring.
* Never remove tests to simplify refactoring.
* Never introduce new dependencies.
* Never change public interfaces without explicit user approval.
* Never mix bug fixes with refactoring in the same commit.

## 6. Deliverables

* **Smell Identified:** What was wrong and why.
* **Technique Applied:** What pattern was used.
* **Behavior Proof:** Test results before and after (both must pass).
* **Regression Check:** Full test suite status.

## 7. Golden Rule

If you are unsure whether a change preserves behavior — stop. Run the tests first, then decide.

Refer:
  - [Coding Style](../rules/coding-style.md)
  - [Architecture](../rules/architecture.md)
  - [Testing](../context/testing.md)
