# EPIC-001C — Widget Kit Expansion

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** 🔵 Backlog
**Category:** UI Engine / Component Library
**Priority:** P1
**Depends on:** EPIC-001B (the kit renders tokens; the vocabulary must exist first)

---

## 🎯 Summary & Objectives

Grow `QmlShared` from seven ad-hoc components into a widget kit complete enough that a
consuming screen never needs to author a visual primitive of its own.

`StatefulButton`, `BaseCard`, `FieldBackground`, `StyledCheck`, `DateTimePicker`,
`TimeRangeCard` and `LogPanel` already exist and already prove the model — `StatefulButton`
was promoted precisely because the same background recipe had been reimplemented seven-plus
times with disabled-opacity constants that disagreed with each other. The gap is coverage,
not concept.

### Objectives

1. Close the coverage gaps that force screens back to raw primitives — the data table is
   the largest and most valuable one.
2. Give every component an explicit, documented property contract, so behaviour is uniform
   across the kit rather than per-component folklore.
3. Ship a runnable **gallery**: every component, every state, in one place. A design system
   without a gallery is a design system nobody can verify.
4. Add the static test that keeps screens off raw primitives once the kit can replace them.

---

## 📐 Scope Notes

- **Data table first.** It is the single biggest source of hand-rolled duplication in the
  consuming app, and centralised column definitions are already a written requirement
  (`qml-rule.md` §2.3) that nothing currently enforces. Column spec should be declarative
  data — id, title, width weight, alignment, formatter, sortable — bound by both header and
  row delegates, so alignment is structural rather than a promise.
- Components must not accumulate a flat, universal property set. What is universal
  (identity, enabled/active, layout hint) belongs to a shared base; what is specific
  (columns, series, placeholder) belongs to the component. A base that grows a property per
  new component type has become a union, not an abstraction.
- No fixed pixel geometry in component contracts. Size is the region's decision; components
  express intent, not numbers.

## 🧪 Verification & Test Coverage

- Gallery renders every component in every documented state with zero QML warnings.
- Table header and row delegates provably read the same column definition — asserted, not
  eyeballed.
- Static test flags raw visual primitives authored outside the kit.
- Kit components resolve all visual values through tokens; none carry literals except the
  sanctioned compatibility fallbacks.
