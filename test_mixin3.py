import sys
from unittest.mock import MagicMock
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtWidgets'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()

import os
sys.path.insert(0, os.path.abspath("."))
from sagittarius_engine.infrastructure.config.config_manager import ConfigManager
from sagittarius_engine.utils.path_utils import PathUtils
from sagittarius_engine.extensions.pyside_mvc.ui_matrix_mixin import UIMatrixMixin
from Binace_Bot.src.presentation.ui.constants import UIMode

config_manager = ConfigManager()
config_manager.load_json(PathUtils.get_relative_path("Binace_Bot/src/main.py", "config", "ui_matrix.json"))

class MockView(UIMatrixMixin):
    pass

view = MockView()
view.set_ui_matrix(config_manager.get_all())
print("MATRIX:", view._ui_matrix)
view.apply_ui_mode(UIMode.IDLE)
