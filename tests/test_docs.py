import os
import re
import ast
import sys
import subprocess
import pytest

# Disable this test file entirely
pytestmark = pytest.mark.skip(reason="Disabled by user request")


DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs"))

# Supported diagram types for Mermaid
SUPPORTED_MERMAID_TYPES = ("flowchart", "sequenceDiagram", "classDiagram")

# Public classes exported at the root sagittarius_engine package
ROOT_EXPORTS = {
    "App",
    "EngineContext",
    "IExtension",
    "ExtensionDescriptor",
    "ICommand",
    "IQuery",
    "BaseRepository",
}

# Snippet execution alias prefix to support legacy infra imports
LEGACY_ALIAS_PREFIX = """import sys
import sagittarius_engine
import sagittarius_engine.infrastructure as infrastructure
sys.modules['sagittarius_engine.infra'] = infrastructure
import sagittarius_engine.infrastructure.container.std_container as std_container
sys.modules['sagittarius_engine.infra.std_container'] = std_container
import sagittarius_engine.infrastructure.event_bus.memory_event_bus as memory_event_bus
sys.modules['sagittarius_engine.infra.memory_event_bus'] = memory_event_bus
"""


def get_markdown_files():
    """Helper to collect all Markdown files under docs/ recursively."""
    md_files = []
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files


@pytest.mark.parametrize("file_path", get_markdown_files())
def test_markdown_file_structure(file_path):
    """Verify that every page starts with the correct header and ends with the GitHub edit footer."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Header Validation
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert lines, f"File {file_path} is empty"
    assert lines[0] == "> Applies to Sagittarius Engine v1.x", (
        f"File {os.path.basename(file_path)} does not start with standard header line"
    )

    # 2. Footer Validation
    assert "Found an issue? Edit this page on GitHub." in content, (
        f"File {os.path.basename(file_path)} is missing the GitHub edit footer"
    )


@pytest.mark.parametrize("file_path", get_markdown_files())
def test_markdown_links(file_path):
    """Extract and validate all relative internal Markdown links and image references."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find patterns like [text](link) and ![alt](link)
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    links = link_pattern.findall(content)

    for link in links:
        link = link.strip()
        # Ignore external, template, or special links
        if (
            link.startswith("http://")
            or link.startswith("https://")
            or link.startswith("mailto:")
            or link.startswith("#")
            or link == "link"
        ):
            continue

        # Strip anchor suffix if present
        clean_link = link.split("#")[0]
        if not clean_link:
            continue

        # Resolve path relative to current markdown file
        file_dir = os.path.dirname(file_path)
        target_path = os.path.normpath(os.path.join(file_dir, clean_link))

        assert os.path.exists(target_path), (
            f"Broken internal link '{link}' found in {os.path.basename(file_path)}"
        )


@pytest.mark.parametrize("file_path", get_markdown_files())
def test_mermaid_blocks(file_path):
    """Verify that every Mermaid block declares a supported diagram type."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all mermaid blocks
    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", content, re.DOTALL)

    for block in mermaid_blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        assert lines, f"Empty Mermaid block found in {os.path.basename(file_path)}"

        first_line = lines[0]
        assert any(first_line.startswith(t) for t in SUPPORTED_MERMAID_TYPES), (
            f"Mermaid block in {os.path.basename(file_path)} declares unsupported diagram type: '{first_line}'"
        )


@pytest.mark.parametrize("file_path", get_markdown_files())
def test_python_code_blocks(file_path):
    """Parse, compile, validate imports, and execute runnable Python code blocks in markdown documents."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all python code blocks
    code_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)

    for code in code_blocks:
        # Check if the block is explicitly a negative example or non-runnable
        is_negative_or_no_run = any(
            tag in code
            for tag in (
                "# non-runnable",
                "# click-only",
                "# no-run",
                "# Never do this",
                "# ❌ Never do this",
                "❌",
                "Never import",
            )
        )

        # 1. Compilation Check (Syntax validation)
        try:
            tree = ast.parse(code)
            compile(code, file_path, "exec")
        except SyntaxError as e:
            pytest.fail(
                f"Syntax error in Python block of {os.path.basename(file_path)}: {e}"
            )

        # If it is a negative example or explicitly skipped, we don't perform import/API/execution checks
        if is_negative_or_no_run:
            continue

        # 2. Import Validation
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Check for direct sagittarius_engine.* imports
                    if alias.name.startswith("sagittarius_engine."):
                        parts = alias.name.split(".")
                        # Reject direct imports of private/internal modules
                        if parts[1] in (
                            "kernel",
                            "interfaces",
                            "runtime",
                            "extensions",
                        ):
                            pytest.fail(
                                f"Non-public direct module import '{alias.name}' in {os.path.basename(file_path)}"
                            )
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("sagittarius_engine"):
                    parts = node.module.split(".")
                    if len(parts) > 1:
                        # Reject sub-module imports of classes exported at the root package
                        if parts[1] in (
                            "kernel",
                            "interfaces",
                            "runtime",
                            "extensions",
                            "adapters",
                            "base",
                            "domain",
                        ):
                            for alias in node.names:
                                if alias.name in ROOT_EXPORTS:
                                    pytest.fail(
                                        f"Public class '{alias.name}' should be imported from root 'sagittarius_engine', "
                                        f"not '{node.module}' in {os.path.basename(file_path)}"
                                    )

        # 3. Deprecated API validation (checking actual method calls to execute() or query())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ("execute", "query"):
                        pytest.fail(
                            f"Use of deprecated API call .{node.func.attr}() found in {os.path.basename(file_path)}"
                        )

        # 4. Snippet Execution (if runnable)
        is_runnable = "sagittarius_engine" in code and "app.boot()" in code

        if is_runnable:
            # Prepend legacy imports mapping to support compat layer execution
            executable_code = LEGACY_ALIAS_PREFIX + code
            try:
                res = subprocess.run(
                    [sys.executable, "-c", executable_code],
                    capture_output=True,
                    text=True,
                    timeout=8,
                    cwd=os.getcwd(),
                )
                assert res.returncode == 0, (
                    f"Code execution failed in {os.path.basename(file_path)} with exit code {res.returncode}.\n"
                    f"STDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
                )
            except subprocess.TimeoutExpired:
                pytest.fail(
                    f"Code block in {os.path.basename(file_path)} timed out (leaked threads/async loop)"
                )
