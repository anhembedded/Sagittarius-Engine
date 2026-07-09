import ast
import glob
import os
import sys
import pytest
from sagittarius_engine.kernel.app import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus


def get_imports_in_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return []

    imported_modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_modules.append(node.module)
    return imported_modules


def check_forbidden_imports(directory: str, forbidden_prefixes: list[str]) -> list[str]:
    violations = []
    py_files = glob.glob(
        os.path.join(directory, "**", "*.py"), recursive=True
    )
    for filepath in py_files:
        # Ignore tests, temp files
        if "tests" in filepath or "temp" in filepath:
            continue
        # Ignore legacy shim files that are explicitly deprecated and redirect to extensions
        filename = os.path.basename(filepath)
        if filename in ("i_command.py", "i_query.py"):
            continue

        imports = get_imports_in_file(filepath)
        for imp in imports:
            for prefix in forbidden_prefixes:
                if imp == prefix or imp.startswith(prefix + "."):
                    violations.append(f"{filepath} imports forbidden module '{imp}'")
    return violations


def test_architectural_dependency_rules():
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "sagittarius_engine")
    )

    # Rule 1: Kernel must NOT import extensions or sdk
    kernel_dir = os.path.join(base_dir, "kernel")
    violations = check_forbidden_imports(
        kernel_dir,
        ["sagittarius_engine.extensions", "sagittarius_engine.sdk"],
    )
    assert not violations, f"Kernel dependency violations found:\n" + "\n".join(
        violations
    )

    # Rule 2: Interfaces must NOT import extensions or sdk
    interfaces_dir = os.path.join(base_dir, "interfaces")
    violations = check_forbidden_imports(
        interfaces_dir,
        ["sagittarius_engine.extensions", "sagittarius_engine.sdk"],
    )
    assert not violations, (
        f"Interfaces dependency violations found:\n" + "\n".join(violations)
    )

    # Rule 3: Extensions must NOT import sdk
    extensions_dir = os.path.join(base_dir, "extensions")
    violations = check_forbidden_imports(
        extensions_dir, ["sagittarius_engine.sdk"]
    )
    assert (
        not violations
    ), f"Extensions dependency violations found:\n" + "\n".join(violations)

    # Rule 4: SDK must NOT import extensions
    sdk_dir = os.path.join(base_dir, "sdk")
    violations = check_forbidden_imports(
        sdk_dir, ["sagittarius_engine.extensions"]
    )
    assert not violations, f"SDK dependency violations found:\n" + "\n".join(
        violations
    )


def test_public_api_exports():
    import sagittarius_engine

    public_exports = set(sagittarius_engine.__all__)
    expected_exports = {
        "App",
        "EngineContext",
        "IExtension",
        "ExtensionDescriptor",
        "ICommand",
        "IQuery",
        "BaseRepository",
    }
    assert (
        public_exports == expected_exports
    ), f"Expected root exports {expected_exports}, got {public_exports}"


def test_deprecation_warnings():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    # Test deprecated App.execute
    with pytest.warns(DeprecationWarning, match="App.execute is deprecated"):

        class DummyCommand:
            def execute(self, dto):
                return "executed"

        container.bind(DummyCommand, DummyCommand)
        app.execute(DummyCommand, {})

    # Test deprecated App.query
    with pytest.warns(DeprecationWarning, match="App.query is deprecated"):

        class DummyQuery:
            def execute(self, dto):
                return "queried"

        container.bind(DummyQuery, DummyQuery)
        app.query(DummyQuery, {})

    # Clear sys.modules shims to force re-evaluation
    shim_modules = [
        "sagittarius_engine.interfaces.i_command",
        "sagittarius_engine.interfaces.i_query",
        "sagittarius_engine.base.base_repository",
    ]
    for mod in shim_modules:
        if mod in sys.modules:
            del sys.modules[mod]

    # Test deprecated interfaces shims
    with pytest.warns(
        DeprecationWarning, match="Importing ICommand from.*is deprecated"
    ):
        from sagittarius_engine.interfaces.i_command import ICommand  # noqa: F401

    with pytest.warns(
        DeprecationWarning, match="Importing IQuery from.*is deprecated"
    ):
        from sagittarius_engine.interfaces.i_query import IQuery  # noqa: F401

    with pytest.warns(
        DeprecationWarning, match="Importing BaseRepository from.*is deprecated"
    ):
        from sagittarius_engine.base.base_repository import (
            BaseRepository,
        )  # noqa: F401
