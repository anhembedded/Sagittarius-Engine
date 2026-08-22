"""Tests for the anti-literal-colour QML static guard (EPIC-001B) — the
enforcement mechanism behind ui-architecture.md §2.2."""

from __future__ import annotations

from pathlib import Path

from sagittarius_engine.extensions.pyside_mvc.tokens import find_literal_colors
from sagittarius_engine.extensions.pyside_mvc.tokens.qml_literal_guard import (
    format_findings,
)


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_finds_a_six_digit_hex_literal(tmp_path: Path):
    _write(tmp_path / "Card.qml", 'Rectangle {\n    color: "#2a2d3e"\n}\n')

    findings = find_literal_colors(tmp_path)

    assert len(findings) == 1
    assert findings[0].matched == "#2a2d3e"
    assert findings[0].line_number == 2


def test_finds_three_and_eight_digit_hex_forms(tmp_path: Path):
    _write(
        tmp_path / "Mixed.qml",
        'Rectangle {\n    color: "#abc"\n    border.color: "#1FF3BA2F"\n}\n',
    )

    findings = find_literal_colors(tmp_path)

    matched = {f.matched for f in findings}
    assert matched == {"#abc", "#1FF3BA2F"}


def test_finds_literals_across_multiple_files(tmp_path: Path):
    _write(tmp_path / "A.qml", 'color: "#111111"\n')
    _write(tmp_path / "sub" / "B.qml", 'color: "#222222"\n')

    findings = find_literal_colors(tmp_path)

    assert {f.matched for f in findings} == {"#111111", "#222222"}


def test_clean_file_reports_no_findings(tmp_path: Path):
    _write(tmp_path / "Clean.qml", "Rectangle {\n    color: Theme.accent\n}\n")

    assert find_literal_colors(tmp_path) == []


def test_ignores_comment_only_lines(tmp_path: Path):
    _write(
        tmp_path / "Commented.qml",
        '// example: color: "#2a2d3e" is not allowed\n'
        "Rectangle {\n"
        "    color: Theme.accent\n"
        "}\n",
    )

    assert find_literal_colors(tmp_path) == []


def test_inline_token_exempt_marker_suppresses_a_finding(tmp_path: Path):
    _write(
        tmp_path / "Fallback.qml",
        'color: parentTheme ? parentTheme.accent : "#181a24"  // token-exempt: '
        "compatibility fallback while legacy screen migrates\n",
    )

    assert find_literal_colors(tmp_path) == []


def test_exempt_dirs_are_skipped_entirely(tmp_path: Path):
    legacy = _write(tmp_path / "legacy" / "Old.qml", 'color: "#333333"\n').parent
    _write(tmp_path / "New.qml", 'color: "#444444"\n')

    findings = find_literal_colors(tmp_path, exempt_dirs=[legacy])

    assert [f.matched for f in findings] == ["#444444"]


def test_does_not_match_a_hash_inside_a_longer_identifier_like_string(tmp_path: Path):
    """A bare `#` followed by fewer than 3 valid hex digits, or embedded in a
    non-colour token, must not false-positive."""
    _write(tmp_path / "NotAColor.qml", 'property string routeId: "#zz"\n')

    assert find_literal_colors(tmp_path) == []


def test_format_findings_includes_file_line_and_literal(tmp_path: Path):
    qml = _write(tmp_path / "Card.qml", 'color: "#2a2d3e"\n')

    findings = find_literal_colors(tmp_path)
    rendered = format_findings(findings)

    assert str(qml) in rendered
    assert "#2a2d3e" in rendered
    assert "1 hardcoded colour literal" in rendered
