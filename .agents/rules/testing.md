---
name: Testing Rules
description: When and how to add or update tests for changed code.
trigger: model_decision
---

# Rules: Testing

## Test Coverage for Changes
- **New behavior:** If a change adds a new public method, branch of logic, or feature that is reasonably testable, you MUST add a test case covering it.
- **Changed behavior:** If a change alters an existing return value, side effect, or signature, you MUST update the existing test(s) that assert on it. Never leave a test passing for the wrong reason or silently outdated.
- **Bug fixes:** Add a regression test that would have failed before the fix.
- **Skip only when:** the change is a pure refactor with no behavior change and is already covered by pre-existing tests (verify by running them), or the change is not reasonably testable (e.g. log wording, a cosmetic constant).

## Where & Style
- Mirror the existing layout: `tests/sanity/...` for boot/import-time checks (must run in well under a second, no real I/O), `tests/unit/...` for isolated logic, `tests/integration/...` for cross-component flows. Match the path of the module under test (e.g. `src/foo/bar.py` → `tests/unit/foo/test_bar.py`).
- Follow the conventions already used in that test file/directory (fixtures, mock patterns, naming) rather than introducing a new one.

## Qt / PySide6 UI Tests
- **No silent swallowing:** never wrap test assertions or setup in `try/except: pass`. Let failures raise.
- **Strict Qt cleanup:** every `QWidget` constructed in a test MUST be registered via `qtbot.addWidget(widget)` (or explicitly `deleteLater()`-ed) so its C++ object doesn't outlive the test and leak signals/slots into the next one.
- **Explicit assertions on async/signal behavior:** a test that triggers a signal or background thread MUST assert the outcome with `assert_called_with(...)` or `qtbot.waitUntil(...)` / `qtbot.waitSignal(...)` — never assume timing worked because the test didn't crash.
- **No `time.sleep()` in UI tests:** use `qtbot.waitUntil()`/`qtbot.waitSignal()` instead; a fixed sleep is either flaky (too short) or wastes CI time (too long).

## Before Considering a Task Done
- Run at least the affected test file(s); run the full suite via `scripts/ci-local.ps1` before commit (see `rules/commit-rule.md`).
- Never mark a task complete with a known-failing test or a newly added test you have not actually run.
