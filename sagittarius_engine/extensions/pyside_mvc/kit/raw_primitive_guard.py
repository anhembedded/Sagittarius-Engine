"""
@brief Static guard against raw Qt Quick Controls primitives authored
outside the Widget Kit — the enforcement mechanism behind
ui-architecture.md §1 ("Never author a raw visual primitive... except
through the escape hatch"). The counterpart to
`tokens.qml_literal_guard`, one layer up: that guard checks *values*
(no literal colours); this one checks *authorship* (no raw controls).

@details
Scope: only `Button` and `CheckBox` — the two controls the kit already
ships a direct replacement for (`StatefulButton`, `StyledCheck`).
`Rectangle` is deliberately NOT flagged here: it has too many legitimate
non-widget uses (backgrounds, dividers, layout spacers, the corner-
squaring trick every `BaseCard`-derived component already uses) to flag
lexically without a real QML parser — flagging it would drown genuine
violations in false positives, the exact failure mode this guard exists to
avoid for itself. Extend coverage control-by-control as the kit grows a
direct replacement, the same incremental approach `qml_literal_guard.py`
took by shipping colour-only first rather than guessing at spacing/radius.

No exemption marker, unlike the colour guard. Under the escape-hatch
policy (`ui-architecture.md` §1.1), a screen without a matching kit
component may derive from a kit *base primitive* — never instantiate the
underlying Qt Quick Controls type directly. There is no legitimate reason
to write a bare `Button {`/`CheckBox {` outside the kit, so there is
nothing to mark as a sanctioned exception.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

#: Matches a raw control declared as the root of a QML block — i.e. at the
#: start of a line (after indentation only), the same shape every real
#: component/delegate root takes in this codebase's QML style. A `Button`
#: appearing mid-expression (e.g. as part of a longer identifier like
#: `StatefulButton`) can't match: `\s*` only consumes whitespace, so the
#: captured name must be the exact token, not a substring.
_RAW_PRIMITIVE_RE = re.compile(r"^\s*(Button|CheckBox)\s*\{")


@dataclass(frozen=True)
class RawPrimitiveFinding:
    """One raw control declaration found outside the widget kit."""

    file: Path
    line_number: int
    line_text: str
    control: str


def find_raw_primitives(
    root: Path, exempt_dirs: Iterable[Path] = ()
) -> list[RawPrimitiveFinding]:
    """
    @brief Scans every `.qml` file under `root` for a bare `Button {` or
    `CheckBox {` declared as a block root, returning one finding per
    occurrence.

    @param root Directory to scan recursively — typically a consuming app's
    screens directory, not the kit itself (the kit is where these controls
    are legitimately built from).
    @param exempt_dirs Directories excluded entirely — pass the kit's own
    location (`QmlShared/`) when scanning a tree that contains it, since
    the kit's job is exactly to construct these controls once.
    @return Findings sorted by file path then line number.
    """
    exempt_dirs = [Path(d).resolve() for d in exempt_dirs]
    findings: list[RawPrimitiveFinding] = []

    for qml_file in sorted(root.rglob("*.qml")):
        resolved = qml_file.resolve()
        if any(_is_within(resolved, exempt) for exempt in exempt_dirs):
            continue

        for line_number, line_text in enumerate(
            qml_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line_text.strip()
            if stripped.startswith(("//", "*")):
                continue
            match = _RAW_PRIMITIVE_RE.match(line_text)
            if match is not None:
                findings.append(
                    RawPrimitiveFinding(
                        file=qml_file,
                        line_number=line_number,
                        line_text=stripped,
                        control=match.group(1),
                    )
                )

    return findings


def _is_within(path: Path, directory: Path) -> bool:
    return directory in path.parents or path == directory


def format_findings(findings: list[RawPrimitiveFinding]) -> str:
    """Renders findings as a human-readable block for an assertion failure
    message — file:line, the control, and the offending line text."""
    lines = [
        f"{len(findings)} raw Qt Quick Controls primitive(s) found outside the widget kit:"
    ]
    for finding in findings:
        lines.append(
            f"  {finding.file}:{finding.line_number}: {finding.control}"
            f"    | {finding.line_text}"
        )
    return "\n".join(lines)
