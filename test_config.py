import sys
import os

sys.path.insert(0, os.path.abspath("."))
from sagittarius_engine.infrastructure.config.config_manager import ConfigManager
from sagittarius_engine.utils.path_utils import PathUtils

config_manager = ConfigManager()
app_json = PathUtils.get_relative_path(
    "Sagittarius_Elite_Warrior/src/main.py", "config", "app_config.json"
)
user_json = PathUtils.get_relative_path(
    "Sagittarius_Elite_Warrior/src/main.py", "config", "user_config.json"
)
ui_matrix_json = PathUtils.get_relative_path(
    "Sagittarius_Elite_Warrior/src/main.py", "config", "ui_matrix.json"
)

config_manager.load_json(app_json)
config_manager.load_json(user_json)
config_manager.load_json(ui_matrix_json)

all_cfg = config_manager.get_all()
print("KEYS:", all_cfg.keys())
print("MAIN:", all_cfg.get("main"))
