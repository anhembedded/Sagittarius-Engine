---
trigger: model_decision
---

# 🎛️ UI Engine Architecture — PySide6 + QML

This document governs `sagittarius_engine.extensions.pyside_mvc` — the engine's opinionated
UI framework for PySide6 + QML applications. It replaces the previous QtWidgets/QFrame/QSS
doctrine (retired 2026-08-22, see [`EPIC-001A`](../../Tasks/epics/EPIC-001_ui_engine_foundation/incomplete/EPIC-001A_architecture_rule_rewrite.md))
which described a pre-QML shape of this extension that no longer matches what ships.

**Scope discipline:** this file describes what the **engine** provides and requires of any
consumer. It must never name a specific consuming application, screen, or domain concept —
that content belongs in the consumer's own rules (e.g. `Sagittarius_Elite_Warrior`'s
`qml-rule.md`, which this document's structure deliberately mirrors, adapted from an
application's QML standard to an engine's contract).

---

## 1. 🏛️ Ownership Boundary — the core contract

The UI Engine holds three monopolies. A consuming application holds domain vocabulary and
composition, and nothing else. This is not a style preference — it is the mechanism that
keeps a multi-screen application visually consistent without relying on every contributor
remembering a convention.

| Layer | Engine owns | Consumer may |
| :--- | :--- | :--- |
| **Tokens** | Every visual value: colour, spacing, radius, typography, motion | Supply its own palette **dict** once, at bootstrap, filling the engine's fixed semantic vocabulary (§2). Never a literal at point of use. |
| **Widget Kit** | The QML components (`QmlShared`) that render those tokens | Compose them into screens. Never author a raw visual primitive (`Rectangle`, bare `Button`, etc.) except through the escape hatch (§1.1). |
| **Runtime** | Shell, regions, navigation, screen lifecycle (`mount`/`unmount`/`ui_mode`) | Declare what a screen contributes and how it reacts to lifecycle/state. Never hand-build layout geometry that belongs to a region. |

**The test for whether a consumer is honouring this boundary:** change one token — accent
colour, corner radius, spacing scale — and count how many consumer files must change to
stay visually correct. The answer must be zero. Any number above zero means the consumer is
still deciding a visual value itself, which this boundary exists to prevent.

### 1.1 Escape hatch — permitted, never free of tokens

A consumer will occasionally need something the kit does not yet provide. This is
permitted, through exactly one mechanism:

- **Single-level inheritance from the matching engine base primitive** (e.g. `BaseCard`) —
  never authoring a bare `Rectangle`/`Item` from scratch. The base's visual behaviour
  (background, border, spacing, disabled/active tinting) is already token-driven and is
  inherited unchanged; a derived component overrides only the behaviour hooks it genuinely
  needs (`BaseCard`'s `setActive()`/`setDisabled()` no-op hooks are the existing example of
  this shape).
- Each use must be **named and justified at the call site** — a one-line comment stating why
  no kit component fits. Silent escapes are indistinguishable from drift and defeat the
  purpose of having a boundary at all.
- A **repeated** escape for the same need is a signal to promote it into the kit proper, not
  to keep re-deriving it ad hoc. If the same escape appears in more than one consumer
  screen, it belongs in `QmlShared`.

What this does **not** permit: deriving from `Rectangle`/`Item` directly, hardcoding a
visual value inside a derived component, or building a component that does not go through
any engine base primitive at all. The escape hatch frees behaviour, never pixels.

---

## 2. 🎨 Design Tokens

### 2.1 Fixed semantic vocabulary, consumer-supplied values

The engine defines token **names**; the consumer supplies **values**. This is the reverse
of treating the palette as an open dict with no engine-side opinion on keys — that shape
cannot validate that a consumer supplied everything the kit depends on.

- Token names are semantic (`accent`, `danger`, `spaceMd`, `radiusMd`), never literal
  (`gold`, `twelvePixels`). A semantic name survives a value change; a literal name lies the
  moment the value changes.
- At bootstrap, the engine validates the consumer's palette against its required
  vocabulary. A missing token fails loudly and specifically, naming the missing key — never
  silently falling back to an undefined or default value in a shipping build.
- `state_tokens.with_state_token_defaults()`'s transitional-default behaviour remains for
  vocabulary the engine adds ahead of a consumer adopting it — that is a distinct case
  ("not migrated yet") from a consumer omitting a token it should supply ("wrong"). Do not
  collapse the two.
- Token categories are not limited to colour: spacing, radius, typography and motion are
  tokens with exactly the same discipline. A value that recurs across more than one QML file
  is a token candidate, not a coincidence to re-type.

### 2.2 No literal visual values outside the token layer

QML consuming the kit binds to `Theme.<name>` exclusively. A literal colour, spacing, radius
or duration value appearing in consumer QML — outside the sanctioned compatibility
fallbacks inside the kit's own primitives — is a defect, not a style nit: it is precisely
the failure mode measured across an unmigrated consumer (hundreds of colour literals against
a handful of official tokens, including near-duplicate values that drifted from the real
token by one hex digit because nobody was re-typing from a single source).

A static test enforcing this (no literal outside the token layer) is a required deliverable
of the token layer, not optional follow-up — see the token-layer epic subtask.

---

## 3. 🧩 Widget Kit — Composition, Not Deep Inheritance

QML is composition-first. Deep inheritance chains produce fragile base classes and property
name collisions; the kit's shape is therefore shallow — one level of inheritance for a base
primitive (`BaseCard`, `BaseField`, …) plus escape-hatch derivations (§1.1), composition for
everything above that.

- **A shared base holds only what is universal**: identity, `enabled`, `active`, a layout
  hint. It must not grow a property per new component type — a base that accumulates
  `columns`, `series`, `placeholder`, … because each new component needed one thing has
  become a union type, not an abstraction. Component-specific shape belongs to the
  component, not the base.
- **No fixed pixel geometry in a component's own contract.** A component expresses sizing
  *intent* (a resize/layout hint); the region or container that hosts it resolves the actual
  number. A component that hardcodes its own width/height cannot be placed correctly by a
  runtime region (§4) that is supposed to own that decision.
- **Data tables are schema-driven, not per-instance markup.** Column definitions (id, title,
  width weight, alignment, formatter, sortable) are declarative data, bound identically by
  header and row delegates, so alignment is structural rather than a promise two delegates
  happen to keep in sync by hand.
- **300 lines is a review threshold, not a hard failure.** Split a component when it mixes
  separate responsibilities or repeats a pattern; do not fragment cohesive, single-purpose
  markup merely to hit a line count.
- **Every kit component must be exercisable in the gallery** (§6.2) — a component that only
  renders inside a specific consumer screen has not actually been proven reusable.

---

## 4. 🧱 Runtime — Shell, Regions, Lifecycle

The runtime layer (in progress, see `EPIC-001D`) owns window chrome, navigation, the overlay
host, and named regions that consumer screens contribute into.

- **A screen contributes; it does not build layout.** What region a piece of UI belongs in
  (toolbar, primary content, sidebar, status) is a declaration from the screen; how that
  region resolves size, placement and splitter behaviour is the runtime's decision, not the
  screen's.
- **Screen lifecycle is a behavioural contract, not a shape contract.** A screen must
  support `mount()`/`unmount()`, react to `ui_mode`, and `shutdown()` cleanly while
  background work may be in flight — it is not required to contain any particular widget or
  look a particular way. `BasePresenter`/`BaseView`'s existing `apply_ui_mode()`/duck-typed
  FSM binding is the precedent this generalizes from.
- **Thread safety is non-negotiable.** UI mutation from a background thread is a defect
  class this extension already guards against (`thread_affinity`, `safe_ui_action`,
  `UIWatchdog`) — the runtime layer must not introduce a path that bypasses those guards for
  the sake of a convenient API.
- **The runtime must not know the consuming application.** A registered contribution is fed
  by the consumer's own presenter/view-model layer; the runtime never reaches toward
  application domain state to decide what to render.

---

## 5. 🔒 Security & Quality Baseline

- **Enforce `textFormat: Text.PlainText`** on any `Text` item rendering data that
  originates outside the QML file itself (log lines, error messages, any value that could
  contain markup), to prevent HTML/RichText injection through display text.
- **`ListView`/`TableView`/repeated delegates backed by data that can exceed roughly 20 rows,
  update incrementally, or require virtualization** must be backed by a Python
  `QAbstractListModel`/`QAbstractTableModel`, not a QML-side array transform. A small static
  or one-shot list may stay QML-only when QML is not transforming domain data.

---

## 6. 🧪 Testing & Verification

### 6.1 Kit-level

- Every kit component constructs cleanly under `QT_QPA_PLATFORM=offscreen` with zero QML
  warnings and zero unbound-property errors.
- The anti-literal test (§2.2) and the anti-raw-primitive test (§1, no visual primitive
  authored outside the kit or a valid escape) are both required, automated, and run in CI —
  not a documentation-only rule a reviewer is trusted to catch by eye. This repository has
  direct precedent for exactly this failure mode: a rule that says "must" with nothing
  automated behind it gets silently violated at scale.

### 6.2 Gallery — required, not optional documentation

Every kit component must be reachable from a single runnable gallery covering every
documented state (idle/hover/active/disabled, populated/empty, etc.). A design system with
no way to see everything it offers in one place is not verifiable — and is precisely how a
consumer ends up re-implementing something that already existed, because there was no way to
check first.

### 6.3 Runtime conformance suite

Once the runtime layer exists (`EPIC-001D`), one conformance test suite applies to **every**
registered screen, including screens not yet written: repeated mount/unmount without
leaking, clean shutdown with background work in flight, correct response to every `ui_mode`,
complete self-declared metadata. A screen that violates the lifecycle contract fails this
suite; it is not something each consumer screen re-proves for itself.

---

## 7. 🏷️ Naming Conventions

- **Properties**: `camelCase` (`isActive`, `layoutHint`, `resizeBehavior`).
- **Signals**: `camelCase` verb phrases (`clicked`, `stateChanged`, `runRequested`).
- **Token names**: semantic, not literal (§2.1) — describe purpose, not value.
- **Every interactive kit element** declares both a QML `id` (readable bindings) and a
  stable `objectName` (the automation/test contract). Do not rely on a generated index as
  the only test identity for a repeated delegate.

---

## 8. 🔌 Consumption Model

- A consuming application depends on this extension as a package dependency (see
  `install-rule.md`), never by copying kit source into its own tree. A copied component is
  already a fork the moment it is copied — it stops receiving token/behaviour fixes and
  becomes exactly the kind of drift this boundary exists to prevent.
- The engine ships with **no opinion on any specific application's domain** — no screen
  names, no business terminology, anywhere in `pyside_mvc`. If a rule, component, or token
  name references a concrete consuming application, it does not belong in this repository.
