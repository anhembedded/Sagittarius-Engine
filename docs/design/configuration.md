---
type: design_doc
tags: [sagittarius, configuration]
language: python
---

# Configuration

## Overview
The Configuration components provide a unified way to retrieve settings across the application. It shields application code from needing to know where settings come from (e.g., environment variables, JSON files, `.env` files, or dictionaries).

## Problem Statement
Applications need to read settings for things like database credentials, API keys, or logging levels. Hardcoding these is an anti-pattern. Furthermore, configurations usually come from multiple sources, and higher-priority sources (like Environment variables) need to override lower-priority sources (like default config files).

## Proposed Solution
Sagittarius defines the `IConfig` interface for simple key/value retrieval.
- For testing and simple apps, `DictConfig` provides an in-memory store.
- For complex apps, `ConfigManager` acts as a multi-layer configuration manager. It accepts multiple `ConfigSource` strategies (Dict, Env, Json, Dotenv). Sources are merged in the order they are added, meaning later sources override earlier ones.

## Core API / Interface

### `interface IConfig` (in `src/interfaces/i_config.py`)
- `def get(self, key: str, default: Any=None) -> Any`: Retrieves a config value.
- `def set(self, key: str, value: Any) -> None`: Sets a config value at runtime.

### `class ConfigManager(IConfig)` (in `src/infra/config_manager.py`)
Multi-layer configuration manager.

- `def add_source(self, source: ConfigSource) -> None`: Adds a configuration source strategy to the manager.
- `def get(self, key: str, default: Any = None) -> Any`
- `def set(self, key: str, value: Any) -> None`

### `class ConfigSource` (Abstract Base)
- `def read(self) -> dict[str, Any]`: Reads and returns the config dictionary.
- **Implementations**:
  - `DictSource(data: dict)`
  - `EnvSource(prefix: str)`
  - `JsonSource(filepath: str)`
  - `DotenvSource(filepath: str)` (in `src/infra/config_source/dotenv_source.py`)

### `class DictConfig(IConfig)` (in `src/infra/dict_config.py`)
A simple dictionary-backed configuration for testing.

## Dependencies
- Internal: `IConfig`
- External: `os`, `json`, `python-dotenv` (Optional. `DotenvSource` gracefully falls back to a manual `.env` string parser if missing).

## How to Use / Examples

```python
from sagittarius_engine.infrastructure.config_manager import ConfigManager, JsonSource, EnvSource
from sagittarius_engine.infrastructure.config_source.dotenv_source import DotenvSource
from sagittarius_engine.infrastructure.dict_config import DictConfig

# --- Simple / Test Usage ---
simple_config = DictConfig()
simple_config.set("DB_HOST", "localhost")

# --- Advanced Usage ---
config = ConfigManager()

# 1. Base defaults
config.add_source(JsonSource("default_config.json"))

# 2. Local overrides via .env file
config.add_source(DotenvSource(".env"))

# 3. Environment variables have the highest priority
config.add_source(EnvSource(prefix="APP_"))
# (e.g. if APP_DB_HOST is set, it will be saved as "DB_HOST" overriding previous sources)

db_host = config.get("DB_HOST", "127.0.0.1")
```

## Implementation Notes
- **Lazy Loading**: `ConfigManager` evaluates (`read()`) all registered sources only when `get()` or `set()` is first called (or if a new source is added, resetting the cache).
- **Dotenv fallback**: If `python-dotenv` is missing, `DotenvSource` manually parses the `.env` file and updates `os.environ` to mimic standard behavior, though it might lack advanced feature support (like multiline variables).

## Related Documents
- `container.md` (Config is typically injected via Container)
