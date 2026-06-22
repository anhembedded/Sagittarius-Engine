from src.domain.configuration.Configuration_api import AppConfig

class APP_DEFINITIONS:
    CONFIG_PATH = "config.json"

class App_Statup:

    def __init__(self, config: AppConfig):
        self.config = config

    def __load_config(self) -> AppConfig:
        """
        Load configuration from a file or use default values.
        """
        # Placeholder for actual loading logic
        return self.config