import pytest
import os
import sys
from unittest.mock import Mock
from src.core import App, ModuleAutoDiscovery, BaseModule

def test_module_auto_discovery_discover(tmp_path, monkeypatch):
    # Create a temporary directory structure for our fake modules package
    pkg_dir = tmp_path / "fake_modules"
    pkg_dir.mkdir()

    # Create __init__.py
    (pkg_dir / "__init__.py").write_text("")

    # Create sub-packages (directories with __init__.py) since the discovery expects is_pkg=True
    sub_pkg1 = pkg_dir / "mod1"
    sub_pkg1.mkdir()
    (sub_pkg1 / "__init__.py").write_text("""
from src.core import BaseModule
class FakeModule1(BaseModule):
    pass
""")

    sub_pkg2 = pkg_dir / "mod2"
    sub_pkg2.mkdir()
    (sub_pkg2 / "__init__.py").write_text("""
from src.core import BaseModule
class FakeModule2(BaseModule):
    pass
""")

    # Add the temporary directory to sys.path
    monkeypatch.syspath_prepend(str(tmp_path))

    app_mock = Mock(spec=App)
    ModuleAutoDiscovery.discover("fake_modules", app_mock)

    assert app_mock.use.call_count == 2

def test_module_auto_discovery_invalid_package():
    app_mock = Mock(spec=App)
    ModuleAutoDiscovery.discover("non_existent_package_123", app_mock)

    assert app_mock.use.call_count == 0
