# EPIC-001A — Architecture Rule Rewrite & Ownership Boundary

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** ✅ **Completed (2026-08-22)**
**Category:** Governance / UI Architecture
**Started:** 2026-08-22
**Unblocks:** EPIC-001B / EPIC-001C / EPIC-001D may now start.

---

## 🎯 Summary & Objectives

The engine is adopting a **UI Engine** direction: `extensions/pyside_mvc` grows into a
three-layer, opinionated UI framework (design tokens → widget kit → UI runtime), and
`Sagittarius_Elite_Warrior` migrates onto it screen by screen afterwards.

This task writes **no product code**. It exists because the governance document for that
exact area is currently wrong, and shipping a QML UI engine underneath a rule that mandates
QtWidgets would hand every future contributor (human or AI) two contradictory sets of
instructions.

### The concrete problem

`.agents/rules/ui-architecture.md` still describes the pre-QML world:

| Line in the current rule | Why it is now wrong |
| :--- | :--- |
| "All cards MUST inherit from `BaseCard` (which is a `QFrame`)" | The shipped `BaseCard` is a QML `Rectangle`-rooted component, not a `QFrame`. |
| "ALL styling must be moved to `src/presentation/ui/qss/style.qss`" | Styling flows through the `Theme` bridge into QML. QSS covers only the residual QtWidgets shell. |
| "`MainWindow` will load this file dynamically at startup" | Describes app startup behaviour, from inside the engine repo. |
| "Use `RouterManager` to initialize them on demand" | The shipped type is `PresenterManager`; no `RouterManager` exists in this repo. |
| Path reference `src/presentation/ui/qss/style.qss` | An **application** path leaking into an **engine** rule — the engine has no `src/presentation/`. |

The file also has no notion of the ownership boundary the UI Engine depends on, so there
is currently nothing that would stop a consumer app from writing raw colours again — which
is the failure mode this whole direction exists to prevent.

**Reference material, not a template to copy verbatim:** `Sagittarius_Elite_Warrior/.agents/rules/qml-rule.md`
is the app repo's current, accurate QML standard (theme tokens, component modularization,
responsive sizing, model-view patterns, testing). It describes an **application's** QML —
this task adapts its structure and rigor to describe an **engine's** contract instead: no
screen names, no trading vocabulary, no assumption that any particular consuming app exists.

### Objectives

1. Replace `.agents/rules/ui-architecture.md` with a rule that describes the QML reality.
2. Codify the **three-layer ownership boundary** as an enforceable rule, not a suggestion.
3. Remove every application-specific path and behaviour from the engine's rule.
4. Record the escape-hatch mechanism (resolved below — see §3).
5. Record the target structure of `pyside_mvc` so EPIC-001B/C/D have a fixed destination.

---

## 📐 Implementation Plan / Overview

### 1. The ownership boundary to codify

The engine holds three monopolies; the consuming app holds domain vocabulary and
composition, and nothing else.

| Layer | Engine owns | App may |
| :--- | :--- | :--- |
| **Tokens** | Every visual value: colour, spacing, radius, typography, motion | Supply its own palette **dict** once, at bootstrap, filling the engine's fixed semantic vocabulary. Never a literal at point of use. |
| **Widget Kit** | The QML components that render those tokens | Compose them. Never author a raw visual primitive — except via the escape hatch in §3. |
| **Runtime** | Shell, regions, navigation, lifecycle (`mount`/`unmount`/`ui_mode`) | Declare what it contributes. Never hand-build layout geometry. |

The rule must state the boundary in terms a static test can later check, because
EPIC-001B/C will add exactly those tests. Vague wording here produces unenforceable tests
later.

### 2. Target structure for `pyside_mvc`

Decided 2026-08-22: **grow `pyside_mvc` in place**, do not create a parallel UI extension.
A second UI extension would split the theme bridge and `OverlayHost` across two homes and
reproduce the very drift this direction is meant to end.

The rule records this target so later tasks converge rather than improvise:

```
extensions/pyside_mvc/
├── tokens/     design-token contract + theme bridge      (EPIC-001B)
├── kit/        QML widget kit                            (EPIC-001C)
├── runtime/    shell, regions, registry, lifecycle       (EPIC-001D)
└── (existing)  base_presenter, base_view, thread_affinity, ui_watchdog, ...
```

Existing public imports from `sagittarius_engine.extensions.pyside_mvc` must keep working
throughout; re-export from the package root so the consuming app is never forced into a
flag-day change.

### 3. Escape hatch — resolved 2026-08-22

**Decision:** escapes are permitted, but only through **single-level inheritance from the
matching engine base primitive** (e.g. `BaseCard`, a future `BaseField`) — never by
authoring a bare `Rectangle`/`Item` from scratch. A derived component overrides only the
behaviour it genuinely needs; everything visual (background, border, spacing, disabled/
active tinting) is already token-driven on the base and is inherited, not re-specified.

This keeps the boundary intact under escape: what is "freed" is behaviour/logic, never a
visual value. `BaseCard` in `QmlShared` already works this way today (`setActive()`/
`setDisabled()` are no-op hooks meant to be overridden) — this formalizes an existing
pattern rather than inventing a new one.

Each escape must be named and justified at the call site (a one-line comment stating why
no kit component fits). A repeated escape for the same need is a signal to promote it into
the kit proper (EPIC-001C), not to keep re-deriving it ad hoc.

### 4. Token vocabulary ownership — resolved 2026-08-22

**Decision:** the engine defines a **fixed semantic token vocabulary** (`accent`, `danger`,
`spaceMd`, `radiusMd`, …); the consuming app fills values, it does not invent names. This
reverses today's design, where `get_theme_bridge()` accepts an arbitrary dict with no
engine-side opinion on keys.

This is what makes engine-side validation possible: at bootstrap, the engine can check the
app's palette against its own required vocabulary and fail loudly and specifically on a
missing token, instead of silently rendering with an undefined value. EPIC-001B implements
the vocabulary and the completeness check; this task only records the decision so it is not
re-litigated.

### 5. What this rule must NOT contain

- No application paths, screen names, or trading concepts.
- No QtWidgets-era doctrine except where it accurately describes the residual shell.
- No instructions that assume a specific consuming application exists.

### 6. Cross-repo note

Migration of `Sagittarius_Elite_Warrior` onto this UI engine is tracked **separately**, on
that repository's own board (`Tasks/ROADMAP.md`, `EPIC-005`). Per `.agents/ONBOARDING.md` §9
of the app repo, the two task boards must not be mixed. Nothing in this task changes app
code.

**Operational prerequisite for that migration** (recorded here so it is not rediscovered
later): the app currently installs the engine **non-editable from GitHub** — its
`direct_url.json` pins commit `8c36411`. Until that is switched to the local editable
install (`install-rule.md` Option 2), no engine change is visible to the app without a
push-and-reinstall cycle.

---

## 🧪 Verification & Test Coverage

This is a documentation/governance task; verification is consistency-based rather than
test-based.

- [x] `.agents/rules/ui-architecture.md` contains no `src/presentation/` path, and no
      reference to `RouterManager`, `QStackedWidget`, or `setStyleSheet` as the sanctioned
      styling mechanism. Verified by grep — clean.
- [x] Every type the rule names actually exists in this repository — verified by grep, not
      by assumption: `BaseCard`, `BasePresenter`, `BaseView`, `thread_affinity`,
      `safe_ui_action`, `UIWatchdog`, `QmlShared`, `with_state_token_defaults` all resolve
      to real files (the old file failed this exact check on `RouterManager`).
- [x] The rule states the escape-hatch mechanism (§1.1) and the fixed token vocabulary
      decision (§2.1) explicitly — both are now settled, not open questions.
- [x] `.agents/manifest.yml` still lists `ui-architecture.md` and the entry resolves to a
      real file.
- [x] `PLAYBOOK.md` rule-routing table reaches the rewritten file for UI work — **found
      broken during verification** (the old routing table had no row for
      `ui-architecture.md` at all, despite `manifest.yml` listing it; a UI task would never
      have been told to load it). Fixed by adding a `UI / QML (pyside_mvc)` row.
- [x] No engine source file changes in this task — `git status --short` touches only
      `.agents/` (`PLAYBOOK.md`, `rules/task-tracking.md`, `rules/ui-architecture.md`) and
      `Tasks/` (this epic's own restructuring). No file under `sagittarius_engine/` changed.

## 📝 Implementation Notes

- Rewrote `.agents/rules/ui-architecture.md` in full: ownership boundary (§1), escape hatch
  (§1.1), token discipline (§2), widget kit composition rules (§3), runtime contract (§4),
  security/quality baseline (§5), testing requirements (§6, including the gallery and
  conformance-suite requirements EPIC-001C/D must deliver), naming (§7), consumption model
  (§8). Structure and rigor adapted from `Sagittarius_Elite_Warrior/.agents/rules/qml-rule.md`
  per the user's explicit direction to use it as reference material, generalized to an
  engine contract with zero application-specific content.
- Also restructured `Tasks/` per user request: this program now lives at
  `Tasks/epics/EPIC-001_ui_engine_foundation/`, convention ported from
  `Sagittarius_Elite_Warrior/Tasks/epics/`. `Tasks/README.md` and `.agents/rules/task-tracking.md`
  updated to document and link the new convention.
