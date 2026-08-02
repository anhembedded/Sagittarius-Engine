# Skill: Investigate and Fix Bug

> Context: Use user-provided context. Prioritize correctness, minimal impact, and long-term maintainability.

## 1. Tracking (Complex Tasks Only)

**Assess complexity first.** Only create a tracking file if the task meets the complexity threshold.
Refer to `../rules/task-tracking.md` for the full complexity gate criteria.

Typical triggers for this skill: systemic bug across 3+ modules, user RCA approval required before fix, non-deterministic issue needing multi-session investigation.

If tracking is needed:
```
.ai/tracking/investigate-fix-bug_<YYYYMMDD_HHMM>.md
```
Update phase status at the START and END of each phase.

## 2. Workflow

* **Phase 1 — Understand:** Collect error messages, stack traces, logs, and repro steps. Never assume the cause. → *Update tracking: 🔄 → ✅*
* **Phase 2 — Investigate:** Identify the origin module. Trace execution. Determine if the issue is deterministic. → *Update tracking*
* **Phase 3 — Root Cause Analysis (RCA):** Determine *why* it happened, *why* the code allowed it, and *why* tests missed it. Report RCA to the user before proceeding. → *Update tracking. Stop if BLOCKED by user approval.*
* **Phase 4 — Design:** Evaluate options. Choose the simplest, backward-compatible fix. Ask the user if multiple viable options exist. → *Update tracking*
* **Phase 5 — Implement:** Apply the smallest correct fix. (Refer: `.ai\rules\coding-style.md`) → *Update tracking*
* **Phase 6 — Validate:** Confirm fix, verify build passes, no regressions. (Refer: `.ai\context\testing.md`) → *Update tracking: mark task DONE*

## 3. Testing Strategy

* **Rule:** Never alter tests just to pass. Tests must validate intended behavior.
* **Regression & Expansion:** Add tests that fail before the fix and pass after. Expand coverage to include boundaries, null/invalid inputs, edge cases, and concurrency.
* **Quality:** New tests must be independent, fast, deterministic, and readable. Document any coverage gaps identified during RCA.

## 4. Systemic Investigation & Architecture

* **Pattern Matching:** Search for similar logic, copy-pasted code, or shared utilities across the codebase. If systemic, fix all occurrences and expand tests.
* **Architecture Strictness:** Never introduce circular dependencies, break layering, leak infrastructure details, or bypass DI.

## 5. Documentation

* Update docs (docs/, FAQ, Architecture Notes, CHANGELOG) ONLY IF behavior, API, config, or troubleshooting steps change. Skip updates for internal refactoring unless it affects maintainers.

## 6. Deliverables & Exit Criteria

Bug is considered fixed ONLY when the following are delivered in your response:

* **Problem & Root Cause:** Clear summary.
* **Solution & Files Modified:** Explanation of the minimal fix.
* **Validation:** Build/Test status, including new regression tests added.
* **Documentation:** What was updated (or explicitly state why updates weren't needed).

## 7. Golden Rule

When faced with uncertainty: Prefer asking one precise question over making one incorrect assumption. Incorrect code is worse than incomplete code.
