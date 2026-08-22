# EPIC-001C — Widget Kit Expansion

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** 🟡 **In Progress — data table + gallery delivered (2026-08-22); anti-raw-primitive
test and Field/Modal coverage not yet done.** See §4 below before treating this as closed.
**Category:** UI Engine / Component Library
**Priority:** P1
**Depends on:** EPIC-001B ✅ (the kit renders tokens; the vocabulary must exist first)

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

- [x] Gallery renders every shipped component in a representative state with zero QML
      warnings — `test_gallery_loads_with_no_qml_errors`, and visually confirmed via
      `scripts/render_gallery_snapshot.py`'s PNG output.
- [x] Table header and row delegates provably read the same column definition — both derive
      width from the identical `root.columns` array and `_weightSum()` formula, not two
      independently maintained copies; `test_app_data_table_renders_every_row_from_its_model`
      covers the data-wiring half, visual alignment confirmed in the rendered snapshot.
- [ ] **Not done.** Static test flags raw visual primitives (`Rectangle`, bare `Button`)
      authored outside the kit. `find_literal_colors` (EPIC-001B) only catches colour
      literals, not primitive authorship — a screen could still hand-roll a styled
      `Rectangle` using correct tokens and this wouldn't catch it. Needed before this epic
      can claim screens are structurally prevented from bypassing the kit.
- [x] Kit components resolve all visual values through tokens; none carry literals except
      the sanctioned compatibility fallbacks — **and this was not already true**: running
      the EPIC-001B guard against `QmlShared/` on first use found **8 real pre-existing
      violations** (see §4). `test_widget_kit_source_has_zero_literal_colours` now holds the
      kit itself to zero, permanently.

## 📝 Implementation Notes — what was actually delivered

**Delivered:**

- **`AppDataTable.qml`** — schema-driven table. `columns` is declarative data (`key`,
  `title`, `weight`, `align`, optional `formatter`); header and every row delegate compute
  width from the identical array via `root._weightSum()` — a shared function, not a copied
  formula. Cell text is `Text.PlainText` per the security rule. Real bug caught building
  this, not hypothetical: a delegate using Qt6's `required property` pattern loses QML's
  *implicit* `index`/`model` context properties too — `index` had to be declared
  `required property int index` explicitly, or it silently resolved to `undefined` at
  runtime (caught rendering the gallery snapshot, not by static analysis).
- **`Gallery.qml`** — one runnable page covering `StatefulButton` (idle/active/disabled),
  `FieldBackground`+`StyledCheck`, `TimeRangeCard`, `LogPanel`, and `AppDataTable` with
  sample trading-flavoured data, entirely token-driven. Registered as a loadable document
  (not a qmldir type — it's a page, not a reusable component).
- **`scripts/render_gallery_snapshot.py`** — boots the engine offscreen with the reference
  consumer's real palette, loads the Gallery, grabs a PNG. Not a test; a tool for actually
  *seeing* the kit, per ui-architecture.md §6.2's reasoning that a design system with no way
  to view everything in one place isn't verifiable in practice, only on paper.
- **8 real literal-colour violations found and resolved in `QmlShared/` itself**
  (`DateTimePicker.qml` ×6, `FieldBackground.qml` ×2, `TimeRangeCard.qml` ×1 — one file had
  both real bugs and legitimate exemptions): 3 were genuine drift with a matching token
  already available (`Theme.stateHoverBg`/`Theme.stateIdleBg`) and were fixed outright; 2 in
  `FieldBackground.qml` are the sanctioned `Theme`-unavailable compatibility fallback
  ui-architecture.md §2.2 explicitly permits, now marked `// token-exempt` so they're
  visible instead of indistinguishable from drift; 3 in `DateTimePicker.qml` (an idle-state
  background shade and two day-grid text contrast colours) have no matching semantic token
  today — tokenizing them to the nearest existing value would have silently changed the
  visual, so they're marked `// token-exempt` with the reason inline rather than force-fit,
  per the escape-hatch policy `EPIC-001A` recorded. `FieldBackground.qml`'s `radius: 6` was
  also switched to `Theme.radiusMd` (exact value match, zero visual change) while already in
  the file.
- **3 new tests**, `484 passed, 7 skipped` total (up from 481), `mypy`/`ruff` clean.

**Not delivered — remaining scope for a follow-up pass:**

- Anti-raw-primitive static test (§ above).
- Broader coverage: no `AppModal`/dialog-shell component yet (screens still build modals
  from `Popup`/`ModalDialogCard`-equivalent by hand outside this kit); `StatefulButton` is
  the only button primitive — no distinct icon-only/toolbar-button variant if one turns out
  to be needed once a real screen migrates.
- The gallery does not yet demonstrate hover/pressed states (no synthetic pointer input is
  driven in the offscreen snapshot) — only structurally distinct states (`isActive`,
  `enabled: false`) are visible in the rendered image.
