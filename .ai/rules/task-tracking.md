# Rules: Task Tracking

> Context: Task tracking is a tool for complex, multi-phase tasks — not a mandatory ritual.
> Use judgment. Tracking costs tokens. Only use it when the benefit outweighs the cost.

---

## When to Use Tracking (Complexity Gate)

**Create a tracking file ONLY when the task meets one or more of these criteria:**

* **Multi-session:** Task is likely to span multiple interactions or conversations.
* **High phase count:** 4 or more phases with non-trivial dependencies between them.
* **High rollback risk:** A failure mid-task would be difficult to undo (schema changes, data migrations, large refactors).
* **User checkpoint required:** One or more phases require user approval before proceeding (e.g., RCA sign-off, design review).
* **Cross-cutting impact:** Changes touch 3 or more modules, layers, or subsystems simultaneously.
* **Unclear scope:** Scope may expand during execution and must be bounded in writing.

**Do NOT create tracking files when:**

* The task is a single focused change (one file, one function, one concept).
* All phases can be completed in a single continuous response.
* The task is purely investigative (read-only analysis, answering a question).
* There is no risk of partial completion causing system breakage.

**When uncertain:** Default to NO tracking. Add tracking only if the task turns out to be more complex than expected.

---

## File Naming & Location

```
.ai/tracking/<task-type>_<YYYYMMDD_HHMM>.md
```

Examples:
```
refactor_20260718_2130.md
implement_20260718_0900.md
optimize_20260719_1045.md
review-pr_20260719_1400.md
```

---

## File Format

```markdown
# Task: [Type] — [Short Description]

**Started:** YYYY-MM-DD HH:MM
**Skill:** [skill name]
**Status:** IN PROGRESS | BLOCKED | DONE | FAILED

---

## Scope

[What is in scope. What is explicitly out of scope.]

---

## Phases

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| 1 | [Name] | ⬜ TODO | |
| 2 | [Name] | ⬜ TODO | |
| N | [Name] | ⬜ TODO | |

---

## Phase Details

### Phase 1 — [Name]
**Status:** 🔄 IN PROGRESS
**Started:** HH:MM

[What was done. Key decisions. Artifacts produced.]

**Exit Criteria:** [What must be true to consider this phase done]
**Result:** [Outcome when completed]

---

## Blockers

[None | Description of blocker and what is needed to unblock]

---

## Artifacts

[Links or paths to files created/modified during this task]

---

## Exit Criteria (Task-Level)

[What must be true for the entire task to be considered DONE]
```

---

## Update Rules

* Update phase status **immediately** when a phase starts or ends.
* Update the top-level `Status` field whenever any phase changes.
* If a phase is BLOCKED, record the blocker and stop — do not proceed to the next phase.
* Do NOT mark a phase ✅ DONE until its Exit Criteria are satisfied.
* Do NOT delete tracking files. They are the audit trail.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | TODO — not started |
| 🔄 | IN PROGRESS — actively being worked |
| ✅ | DONE — exit criteria met |
| ❌ | FAILED — could not complete, requires user decision |
| ⏸ | BLOCKED — waiting on information or approval |
