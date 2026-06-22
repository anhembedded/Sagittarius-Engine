import asyncio
import os
from src.infrastructure.logger.Loguru_Logger_infra import LoguruLogger
from src.adapters.logger.Loguru_Logger_adapter import LoguruLoggerAdapter
from src.adapters.logger.Silent_Logger_adapter import SilentLoggerAdapter
from src.infrastructure.configuration.Json_File_Infra import JsonFileInfra
from src.adapters.configuration.Local_Config_Adapter import LocalConfigAdapter
from src.domain.configuration.Configuration_api import AppConfig


async def main() -> None:
    # 1. Initialize Configuration Infra & Adapter
    config_path = "config.json"
    json_infra = JsonFileInfra()
    config_adapter = LocalConfigAdapter(json_infra, config_path)

    # 2. Load or Initialize Config
    if not os.path.exists(config_path):
        config = AppConfig() # Default
        config_adapter.save(config)
    else:
        config = config_adapter.load()

    # 3. Init Logger based on config mode
    if config.mode == "debug":
        infra_logger = LoguruLogger()
        logger = LoguruLoggerAdapter(infra_logger)
    else:
        logger = SilentLoggerAdapter()

    logger.info(f"Application started in {config.mode} mode (loaded from {config_path})")

    # 4. Future steps: Other Adapters, Use Cases, etc.
    # ...

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
