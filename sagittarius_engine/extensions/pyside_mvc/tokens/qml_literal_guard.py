"""
@brief Static guard against hardcoded colour literals in QML — the
enforcement mechanism behind `ui-architecture.md` §2.2 ("no literal visual
value outside the token layer").

@details
A rule that says "must use Theme tokens" with nothing automated behind it is
exactly what already happened in the reference consumer: 342 hardcoded
colour literals across 97 distinct values, against 14 official tokens,
including two different "gold" hex values six characters apart that nobody
intended to create. This module is the check that keeps that from
recurring — importable by any consuming app's own test suite, not only
runnable inside this engine's tests.

Scope note: only colour literals are checked here. Spacing/radius/
typography/motion literal detection is deferred — those categories have no
real consumer adoption yet to write a meaningful, low-false-positive check
against (a bare integer is far too common a token to regex-match safely;
see `EPIC-001B`). Colour literals have a precise, low-noise pattern (`#` +
hex digits) that spacing/radius do not.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

#: 3, 6 or 8 hex digits after `#` — QML's supported colour literal lengths
#: (`#rgb`, `#rrggbb`, `#aarrggbb`). Matched via word boundary so it does not
#: false-positive on a longer alphanumeric token that merely contains a `#`.
_HEX_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")

#: A line carrying this marker is a deliberate, reviewed exception — see
#: `ui-architecture.md` §2.2's "sanctioned compatibility fallbacks" carve-out
#: for the kit's own base primitives during migration. The marker must be on
#: the same line as the literal so the exemption is visible at the exact
#: point of use, not hidden in a file-level comment far away.
_EXEMPT_MARKER = "token-exempt"


@dataclass(frozen=True)
class LiteralColorFinding:
    """One hardcoded colour literal found outside the token layer."""

    file: Path
    line_number: int
    line_text: str
    matched: str


def find_literal_colors(
    root: Path, exempt_dirs: Iterable[Path] = ()
) -> list[LiteralColorFinding]:
    """
    @brief Scans every `.qml` file under `root` for hardcoded colour
    literals, returning one finding per occurrence.

    @param root Directory to scan recursively.
    @param exempt_dirs Directories (e.g. the kit's own primitives, while
    they carry documented, reviewed compatibility fallbacks) excluded from
    scanning entirely. Prefer the inline `token-exempt` marker for a single
    justified literal instead of exempting a whole directory where possible
    — a directory exemption hides drift from this check just as easily as
    it hides a legitimate fallback.
    @return Findings sorted by file path then line number, so output is
    stable across runs and diff-able in CI logs.
    """
    exempt_dirs = [Path(d).resolve() for d in exempt_dirs]
    findings: list[LiteralColorFinding] = []

    for qml_file in sorted(root.rglob("*.qml")):
        resolved = qml_file.resolve()
        if any(_is_within(resolved, exempt) for exempt in exempt_dirs):
            continue

        for line_number, line_text in enumerate(
            qml_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if _EXEMPT_MARKER in line_text:
                continue
            stripped = line_text.strip()
            if stripped.startswith(("//", "*")):
                continue
            match = _HEX_COLOR_RE.search(line_text)
            if match is not None:
                findings.append(
                    LiteralColorFinding(
                        file=qml_file,
                        line_number=line_number,
                        line_text=line_text.strip(),
                        matched=match.group(0),
                    )
                )

    return findings


def _is_within(path: Path, directory: Path) -> bool:
    return directory in path.parents or path == directory


def format_findings(findings: list[LiteralColorFinding]) -> str:
    """
    @brief Renders findings as a human-readable block for an assertion
    failure message — file:line, the literal, and the offending line text.
    """
    lines = [
        f"{len(findings)} hardcoded colour literal(s) found outside the token layer:"
    ]
    for finding in findings:
        lines.append(
            f"  {finding.file}:{finding.line_number}: {finding.matched}"
            f"    | {finding.line_text}"
        )
    return "\n".join(lines)
