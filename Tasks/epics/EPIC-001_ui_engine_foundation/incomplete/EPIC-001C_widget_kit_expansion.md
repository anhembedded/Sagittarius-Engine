# EPIC-001C — Widget Kit Expansion

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** 🟡 **In Progress — data table, gallery, anti-raw-primitive test, and AppModal all
delivered (2026-08-22). Only the Rectangle-as-styled-card detection gap remains open (§4).**
See §4 below before treating this as closed.
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
- [x] Static test flags raw visual primitives authored outside the kit —
      `find_raw_primitives()` (new `extensions/pyside_mvc/kit/` package), scoped to `Button`/
      `CheckBox` (the two controls the kit already has a direct replacement for; `Rectangle`
      is deliberately not covered — see Implementation Notes). 8 tests, all passing.
      **Scope note carried forward, not closed by this test:** this guard checks
      *authorship* (no raw controls), not layout/geometry — a screen could still hand-roll a
      correctly-token-coloured `Rectangle` standing in for a card, which neither this guard
      nor the colour guard would catch. Full "screens structurally cannot bypass the kit" is
      not yet true; "screens cannot instantiate the two most common bypassed controls
      directly" is.
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
  `FieldBackground`+`StyledCheck`, `TimeRangeCard`, `LogPanel`, `AppDataTable`, and (added in
  a follow-up pass) `AppModal`, with sample trading-flavoured data, entirely token-driven.
  Registered as a loadable document (not a qmldir type — it's a page, not a reusable
  component).
- **`AppModal.qml`** — reusable modal dialog shell: token-driven header (title + close
  button) / scrollable body / right-aligned action footer, wrapping a QML `Popup`. Composes
  directly with the existing `OverlayHost.qml`/`overlay_host.py` full-window overlay
  (`BOT-087`) rather than introducing a second modal-hosting mechanism — a document loaded
  through `OverlayHost.load_content()` declares `readonly property bool hasOpenModal:
  myModal.opened` exactly as it already had to for a hand-rolled `Popup`. Sizing is fully
  dynamic per `qml-rule.md` §2.2: `width` targets `maxWidth` (480 default) but yields to a
  small `Overlay.overlay`; `height` follows real content up to `maxHeightFraction` (0.85) of
  the overlay's bounds — never a bare fixed number. Directly replaces the independently
  duplicated `Popup`+background recipe already seen in `DateTimePicker.qml`'s own calendar
  popup (that recipe is left as-is there, not retrofitted onto `AppModal` in this pass — see
  §4). `default property alias bodyData` lets a consumer declare ordinary children as the
  body (idiomatic QML), `property alias actions` takes a list of pre-built buttons (typically
  `StatefulButton`) right-aligned in the footer via a permanent spacer `Item` declared ahead
  of the alias target. Verified end-to-end: `test_app_modal_opens_dynamically_sized_with_its_action_buttons`
  and visually in the re-rendered gallery snapshot (title bar, wrapped body text, Cancel/Run
  Backtest buttons, correctly centred and sized).
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
- **`extensions/pyside_mvc/kit/raw_primitive_guard.py`** — `find_raw_primitives()`, scoped
  to `Button`/`CheckBox` only (the two controls with a direct kit replacement today).
  `Rectangle` is deliberately not covered: it has too many legitimate non-widget uses
  (dividers, spacers, the corner-squaring trick `BaseCard`-derived components already use)
  to flag lexically without a real QML parser — the same precision-over-completeness call
  `qml_literal_guard.py` made shipping colour-only. No exemption marker exists for this
  guard (unlike the colour one): under the escape-hatch policy, there is no legitimate
  reason to write a bare `Button {`/`CheckBox {` outside the kit at all, so nothing needs
  marking as sanctioned.
- **Ran the new guard against `QmlShared/` itself — found 8 hits, all inside the kit,
  none fixed (recorded honestly, not silently left out):**
  - 2 are the kit's own construction sites (`StatefulButton.qml`, `StyledCheck.qml` —
    exactly where a `Button`/`CheckBox` is *supposed* to be instantiated raw; this is the
    guard correctly not exempting a file just because of what it's named).
  - 6 were real, pre-existing internal inconsistency, predating this epic. **Resolved
    differently per case, not blanket-migrated** — each was actually inspected rather than
    assumed equivalent:
    - **`LogPanel.qml`'s Copy/Clear (2) — migrated to `StatefulButton`.** Genuine 1:1 match:
      icon + text, idle/hover background swap, bordered — exactly the shape `StatefulButton`
      already covers. Only visible change is corner radius (legacy `4px` → `StatefulButton`'s
      real `Theme.radiusMd` default, `6px`) — the old value was never token-backed to begin
      with, so this is a correction, not a regression. Confirmed against the re-rendered
      gallery snapshot; both guards now report zero findings for this file.
    - **`DateTimePicker.qml`'s 4 buttons — deliberately left alone**, after reading each one
      in full rather than assuming they'd migrate like `LogPanel`'s did: the calendar-toggle
      button has a bespoke merged-corner shape to fuse visually with the adjoining text field
      (`StatefulButton` only ever renders a fully-rounded rect); the two month-nav arrows are
      24×24 icon-only glyph buttons (`StatefulButton` is sized/laid out for labelled
      icon+text buttons, `implicitHeight: 32`); the "Apply" button is a solid accent-filled
      primary CTA (`StatefulButton` has no filled variant — only bordered idle/hover/active).
      Forcing any of these through `StatefulButton` would be a real visual regression, not an
      inconsistency fix — left as hand-rolled, correctly still flagged by the guard as a
      reminder, not silently exempted.
  - **Practical scope of the guard right now**: exempting the kit's own directory
    (`exempt_dirs=[QmlShared]`) and running it against a *consuming app's* screens is where
    it earns its keep — there are currently no consuming screens in this repo to run it
    against yet (that's the app-repo migration epic, not started).
- **12 new tests total this session** (`raw_primitive_guard` ×8, `AppModal` ×1 plus 3 shared
  with the wider gallery suite), **`493 passed, 7 skipped` total** (up from 481), `mypy`
  clean (same 26 pre-existing errors as a clean baseline, verified via `git stash`); the
  `LogPanel.qml` fix changed no Python, so no new `ruff`/`mypy` surface there.

**Not delivered — remaining scope for a follow-up pass:**

- The `Rectangle`-as-styled-card gap the raw-primitive guard's scope note names — no
  automated check yet catches a screen re-implementing card/panel visuals from a raw
  `Rectangle` while still using correct tokens.
- `DateTimePicker.qml`'s own calendar `Popup` was not retrofitted onto `AppModal` — it has
  bespoke chrome (no header bar, custom footer with time spinners) that doesn't fit
  `AppModal`'s title/body/actions shape without changes to `AppModal` itself; left as the
  precedent `AppModal` generalizes from, not an immediate consumer of it.
- `StatefulButton` remains the only button primitive — no distinct icon-only/toolbar-button
  variant if one turns out to be needed once a real screen migrates (the 4 buttons found in
  `DateTimePicker.qml`, see above, are exactly the kind of shape such a variant would need to
  cover).
- The gallery does not yet demonstrate hover/pressed states (no synthetic pointer input is
  driven in the offscreen snapshot) — only structurally distinct states (`isActive`,
  `enabled: false`, and now an opened `AppModal`) are visible in the rendered image.
