

from domain.configuration.Configuration_api import CONFIG_KEY
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra


class FileConfigManager:
    """
    This class is responsible for managing the configuration of the application.
    It will read the configuration from a file and provide it to the rest of the application.
    """
    def __init__(self):
        self.__json_file_infra = JsonFileInfra()

    def load_config_from_file(self, file_path: str) -> list[dict[CONFIG_KEY, str]]:
        config_list_of_strings = self.__json_file_infra.load_json(file_path)

        # Convert list of dicts with string values to list of dicts with CONFIG_KEY enum keys
        config_list: list[dict[CONFIG_KEY, str]] = []
        for item in config_list_of_strings:
            config_list.append({CONFIG_KEY[item["key"]]: item["value"]})

        return config_list
    