# EPIC-001D — Runtime, Regions & Slot Registry

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** 🔵 Backlog
**Category:** UI Engine / Composition Runtime
**Priority:** P2 — highest value ceiling, highest design risk; deliberately sequenced last
**Depends on:** EPIC-001B, EPIC-001C

---

## 🎯 Summary & Objectives

Give the UI Engine a composition runtime: a shell that owns named regions, a registry that
screens contribute into, and a uniform screen lifecycle — so assembling a screen stops
being bespoke layout code.

### Why this is sequenced last

This layer is the most speculative of the three. It must assume which widgets exist, which
regions matter, and which surfaces are genuinely dynamic — none of which is reliably known
until EPIC-001B and EPIC-001C have landed and real screens have been built against them.
Choosing these abstractions early means choosing them with the least information, and a
wrong abstraction with live consumers is far more expensive to correct than duplicated code.

### Objectives

1. A shell owning window chrome, navigation, overlay host and named regions.
2. A registry screens contribute into, rather than a layout each screen hand-builds.
3. A uniform screen lifecycle — mount, unmount, ui_mode, shutdown — with one conformance
   test suite every screen must pass, including screens not yet written.
4. Navigation derived from screen self-description, not wired by hand.

---

## 📐 Design Constraints

Carried forward from the architecture review, to be honoured rather than rediscovered:

- **Python describes, QML renders.** A registered contribution is a *specification* —
  identity, kind, state, layout hint, action — not a visual object. Visual authority stays
  in the kit. Building visual objects in Python reintroduces imperative UI construction and
  forfeits bindings, previews and hot reload.
- **Registry state is exposed as models, not as dynamically-named context properties.** A
  per-slot model gives ordering, multiple contributions per slot, and real reactivity;
  string-concatenated context properties give one item per slot, no tooling visibility, and
  silent nulls on typos.
- **Registry is for genuinely dynamic surfaces.** Where composition is static, direct
  declaration is shorter and clearer than registration. Forcing every surface through the
  registry trades layout code for registration code without reducing either.
- **The runtime must not know the consuming application.** Contributions are fed by the
  app's own presenters/view models. A data source reaching from the domain into the UI
  runtime would collapse the separation this extension exists to provide.
- **Regions decide geometry.** A contribution expresses intent; the region resolves size
  and placement.

## 🧪 Verification & Test Coverage

- One conformance suite, applied to every registered screen: mount/unmount repeatedly
  without leaking; shutdown cleanly while background work is in flight; respond correctly
  to every ui_mode; declare complete metadata.
- Contributions render into the correct region, in declared order, and survive
  add/remove/reorder.
- Navigation reflects registered screens with no hand-written wiring.
- A screen that violates the contract fails the suite rather than failing at runtime.
