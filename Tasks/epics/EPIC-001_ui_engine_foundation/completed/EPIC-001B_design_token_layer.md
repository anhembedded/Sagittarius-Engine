# EPIC-001B — Design Token Layer

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** ✅ **Completed (2026-08-22)**
**Category:** UI Engine / Design System
**Priority:** P1 — first implementation layer of the UI Engine
**Depends on:** EPIC-001A (ownership boundary must be codified first) ✅

---

## 🎯 Summary & Objectives

Establish the token layer as the **single source of every visual value** in the UI Engine,
and make that exclusivity mechanically enforced rather than merely documented.

Today `get_theme_bridge()` exposes whatever palette dict the app supplies, with the engine
holding no opinion on the vocabulary. That was the right call while the engine was
UI-agnostic; it is insufficient for an opinionated UI Engine, because an engine that cannot
name its own tokens cannot validate that a consumer filled them, and cannot ship a widget
kit that depends on them.

### Objectives

1. Define the engine's semantic token vocabulary — colour, spacing, radius, typography,
   motion — as an explicit contract, not an open dict.
2. Validate at bootstrap that a consuming app supplies a complete palette, failing loudly
   and specifically rather than rendering with silent fallbacks.
3. Keep the existing `Theme.<name>` QML access shape so no consumer QML must change.
4. Ship the static test that makes the boundary real: **no literal visual value outside the
   token layer**.

---

## 📐 Scope Notes

- Extends the vocabulary beyond colour. Spacing, radius, typography and motion are
  currently expressed as literals scattered through QML; they are tokens and belong here.
- Backwards compatibility matters: `state_tokens.with_state_token_defaults()` already
  provides defaults for a partially-migrated app. The completeness check must not break
  that transitional path — it should distinguish "not migrated yet" from "wrong".
- The enforcement test lives in the engine but must be runnable against a consuming app's
  QML tree, since that is where violations actually accumulate.

## 🧪 Verification & Test Coverage

- [x] Bootstrap with an incomplete palette raises a specific, actionable error naming the
      missing tokens. — `test_configure_app_qml_raises_on_incomplete_palette`,
      `test_configure_app_qml_error_message_names_every_missing_token`.
- [x] Bootstrap with a complete palette exposes every token to QML under its documented
      name. — `test_with_token_defaults_exposes_every_default_backed_category` (tested at
      the merge-function level; the actual `QQmlPropertyMap` singleton is exercised
      end-to-end by the existing `test_overlay_host.py` suite).
- [x] Static test flags any literal colour value authored outside the token layer — **scope
      note**: only colour is implemented (see Implementation Notes for why spacing/radius
      were deliberately deferred rather than shipped as a noisy, false-positive-prone check).
- [x] Existing `Theme.*` consumers in the app continue to resolve unchanged — the required
      colour vocabulary (10 tokens) was set to exactly match the reference consumer's
      existing `Palette.as_ui_dict()` output, so its current palette already satisfies
      bootstrap validation with zero changes required on the app side.
- [x] Full engine test suite: 481 passed, 7 skipped (pre-existing skips, unchanged) — up
      from 462 passed before this task (19 new tests, zero regressions).
- [x] `ruff check` / `ruff format --check` clean on every file touched, except one
      pre-existing, unrelated `F401` in `pyside_mvc/__init__.py` (a deliberate
      `try: import PySide6 / except ImportError` dependency guard ruff can't distinguish
      from a real dead import — pre-dates this task, left as-is per the project's own
      "don't drive-by fix unrelated findings" convention).
- [x] `mypy` (`pyproject.toml`'s `files = ["sagittarius_engine", "tests"]` gate): zero new
      errors — the 26 errors present are byte-for-byte the same 26 present on a clean stash
      of this change (verified directly via `git stash`/`git stash pop`), none in a file
      this task touched.

## 📝 Implementation Notes

**New package**: `sagittarius_engine/extensions/pyside_mvc/tokens/` (the target location
recorded by `EPIC-001A`), additive only — nothing moved out of `QmlShared/`, no import path
consumers rely on today was broken.

- `tokens/vocabulary.py` — `REQUIRED_COLOUR_TOKENS` (10 `TokenSpec`s: `bg`, `bgSidebar`,
  `bgCard`, `bgCardHeader`, `border`, `textPrimary`, `accent`, `success`, `danger`, `muted`),
  `missing_required_tokens()`, `MissingRequiredTokensError`.
- `tokens/defaults.py` — `DEFAULT_SPACING_TOKENS` / `DEFAULT_RADIUS_TOKENS` /
  `DEFAULT_TYPOGRAPHY_TOKENS` / `DEFAULT_MOTION_TOKENS`, and `with_token_defaults()`, which
  composes those with the existing `state_tokens.with_state_token_defaults()` — app values
  win across every category, verified by
  `test_with_token_defaults_lets_app_values_win_across_every_category`.
- `tokens/qml_literal_guard.py` — `find_literal_colors()` / `format_findings()`, importable
  by any consuming app's own test suite (not only runnable inside this repo).

**Design decision — only colour is required, spacing/radius/typography/motion are
default-backed and optional:** the four new categories are genuinely new vocabulary with
zero existing real-world adoption. Making them required would have hard-failed the
reference consumer's bootstrap immediately (`configure_app_qml()` is unconditional, no
opt-out flag by design — see `ui-architecture.md`'s "fail loud, not configurable to be
silent" stance elsewhere in this codebase), which both breaks a currently-working consumer
and gives no one time to adopt the new categories deliberately. Colour is the one category
that could be made required *for free*: the reference consumer's `Palette.as_ui_dict()`
already supplies exactly and only those 10 keys, confirmed by direct comparison before
writing `REQUIRED_COLOUR_TOKENS` — so turning on strict validation costs that consumer
nothing while still fixing the actually-measured problem (colour drift, not spacing drift).

**Bootstrap validation lives in `configure_app_qml()`**, not in `get_theme_bridge()`. This
is the one place a consuming app declares its palette during startup — failing there means
a broken app fails at boot with a clear message, rather than at whatever point in the
render tree first binds an undefined `Theme.<name>`.

**Scope cut, recorded rather than silently dropped:** the anti-literal static test only
checks colour (`#rrggbb`/`#rgb`/`#aarrggbb` patterns) — precise, near-zero false-positive
rate. Spacing/radius literal detection was evaluated and deliberately not attempted: a bare
integer is too common a token in QML (array indices, non-visual constants, `anchors.margins:
0`, etc.) to regex-match without a real QML parser, and there is no adopted spacing/radius
vocabulary yet to test compliance against in the first place. Revisit once `EPIC-001C`
(Widget Kit) gives spacing/radius tokens real consumers to check.

**One existing test fixture updated**: `tests/extensions/pyside_mvc/test_overlay_host.py`
called `configure_app_qml({}, ...)` — the only call site in the repo besides the new tests.
Updated to a placeholder palette built from `REQUIRED_COLOUR_TOKEN_NAMES` (the suite doesn't
exercise theming; this only satisfies the new validation contract).

**Public API**: all new names re-exported from `pyside_mvc`'s package root (`__init__.py`),
per `EPIC-001A`'s "no flag-day change" commitment — existing imports (`with_state_token_defaults`,
`DEFAULT_STATE_TOKENS`, `get_theme_bridge`, `register_theme`, `configure_app_qml`) are
untouched in shape; only their internal behaviour gained validation/a richer default merge.

**19 new tests** across `test_token_vocabulary.py` (11) and `test_qml_literal_guard.py` (8).
