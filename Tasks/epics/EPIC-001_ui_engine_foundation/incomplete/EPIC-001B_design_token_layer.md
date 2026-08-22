# EPIC-001B — Design Token Layer

**Epic:** [EPIC-001 — UI Engine Foundation](../README.md)
**Status:** 🔵 Backlog
**Category:** UI Engine / Design System
**Priority:** P1 — first implementation layer of the UI Engine
**Depends on:** EPIC-001A (ownership boundary must be codified first)

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

- Bootstrap with an incomplete palette raises a specific, actionable error naming the
  missing tokens.
- Bootstrap with a complete palette exposes every token to QML under its documented name.
- Static test flags any literal colour/spacing/radius value authored outside the token
  layer and the kit's compatibility primitives.
- Existing `Theme.*` consumers in the app continue to resolve unchanged.
