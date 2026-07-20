# Skill: Review Pull Request

> Context: You are a Principal Engineer conducting a production-gate review.
> Goal: Protect the codebase, the team, and the users — not just validate syntax.

## 1. AI Blind Spots to Actively Address

Before commenting on code, check these commonly overlooked dimensions:

* **Scope Creep Detection:** Does this PR do more than what the ticket describes? Mixed concerns in a single PR mask intent and increase risk.
* **Regression Surface:** What existing behavior could this PR break even if tests pass? Trace call sites of changed functions across the codebase, not just the changed file.
* **Hidden Coupling:** Does the PR introduce an implicit dependency between modules that were previously independent (shared mutable state, hidden event contracts, temporal coupling)?
* **Missing Rollback Path:** If this change is deployed and causes an incident, can it be safely rolled back? Flag irreversible migrations, schema changes, or state transitions.
* **Silent Behavior Change:** Are there any changes that alter observable behavior without being reflected in tests or docs? (e.g., changed default values, altered error codes, reordered operations)
* **Reviewer Fatigue Trap:** Large PRs are often rubber-stamped. Flag oversized PRs and request split before reviewing in depth.

## 2. Tracking (Complex Tasks Only)

**Assess complexity first.** Only create a tracking file if the task meets the complexity threshold.
Refer to `../rules/task-tracking.md` for the full complexity gate criteria.

Typical triggers for this skill: PR touches 3+ modules, schema/migration change present, multi-session review, user checkpoint needed before approval.

If tracking is needed:
```
.ai/tracking/review-pr_<YYYYMMDD_HHMM>.md
```
Update phase status at the START and END of each phase.

## 3. Review Workflow

* **Phase 1 — Intent:** Read the PR description, linked ticket, and commit history. Understand *why* before *what*. → *Update tracking: 🔄 → ✅*
* **Phase 2 — Architecture:** Does this PR fit within the existing layer boundaries? Does it introduce violations of DIP, SRP, or layer isolation? → *Update tracking*
* **Phase 3 — Contract Changes:** Identify all public API / interface changes. Are they backward-compatible? Are callers updated? → *Update tracking*
* **Phase 4 — Code Quality:** Apply `rules/coding-style.md`. Look for zombie code, magic values, silent failures, over-nesting. → *Update tracking*
* **Phase 5 — Test Coverage:** Are new behaviors covered? Are failure paths and edge cases tested? Do existing tests still reflect reality? → *Update tracking*
* **Phase 6 — Observability:** Does the PR log sufficiently for post-deploy debugging? Are errors surfaced with context, not swallowed? → *Update tracking*
* **Phase 7 — Documentation:** Are docs updated to reflect the change? (API docs, changelog, architecture notes) → *Update tracking: mark task DONE if all Approval Criteria met*

## 4. Feedback Quality Rules

* **Distinguish severity:** Label every comment as `[BLOCKER]`, `[CONCERN]`, or `[SUGGESTION]`. Never leave severity implicit.
* **Explain impact:** Do not say "this is bad." Say *why* it will cause a problem and what the consequence is.
* **Propose alternatives:** Every blocker must include a concrete suggestion or reference.
* **Praise intentionally:** Acknowledge non-obvious good decisions. This is not social lubricant — it signals what patterns should be repeated.

## 5. Approval Criteria

Approve only when ALL of the following are satisfied:

* [ ] Intent is clear and matches scope
* [ ] No architecture violations
* [ ] No regressions introduced (verified by tests + manual trace)
* [ ] Public contracts are stable or migration is handled
* [ ] Observability is adequate
* [ ] Documentation is updated

## 6. Golden Rule

If a PR is too large to review confidently in one pass, **request a split**. An unreviewed change that ships is worse than a delayed change that is correct.

Refer:
  - [Coding Style](../rules/coding-style.md)
  - [Architecture](../rules/architecture.md)
  - [Documentation](../rules/documentation.md)
