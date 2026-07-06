from unittest.mock import Mock

from src.app_kernel import App, ModuleAutoDiscovery


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
from src.base_module import BaseModule
class FakeModule1(BaseModule):
    pass
""")

    sub_pkg2 = pkg_dir / "mod2"
    sub_pkg2.mkdir()
    (sub_pkg2 / "__init__.py").write_text("""
from src.base_module import BaseModule
class FakeModule2(BaseModule):
    pass
""")

    # Create a single .py module (is_pkg=False)
    mod3 = pkg_dir / "mod3.py"
    mod3.write_text("""
from src.base_module import BaseModule
class FakeModule3(BaseModule):
    pass
""")

    # Add the temporary directory to sys.path
    monkeypatch.syspath_prepend(str(tmp_path))

    app_mock = Mock(spec=App)
    ModuleAutoDiscovery.discover("fake_modules", app_mock)

    # Now it should discover 3 modules (2 packages, 1 single file)
    assert app_mock.use.call_count == 3


def test_module_auto_discovery_invalid_package():
    app_mock = Mock(spec=App)
    ModuleAutoDiscovery.discover("non_existent_package_123", app_mock)

    assert app_mock.use.call_count == 0
