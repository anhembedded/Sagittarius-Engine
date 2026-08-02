# Configuration Module (Config)

The `Config` module in Sagittarius Engine is a centralized, flexible configuration management system designed according to Clean Architecture principles (providing Interfaces for decoupling). This module allows the application to read configuration parameters from multiple sources (JSON, environment variables, Dictionaries) and makes it easy to mock or replace them in testing environments.

---

## 1. How it works

The Config system revolves around the core Interface **`IConfig`**. All services, use cases, or components that require configuration parameters depend on `IConfig` (via Dependency Injection) rather than directly depending on a configuration file.

There are 2 main implementations of `IConfig`:

1. **`DictConfig`**: Stores configuration in temporary memory as a Dictionary. Primarily used for **Unit Tests** or very simple applications that don't need external configuration loading.
2. **`ConfigManager`**: A multi-layer configuration system. It supports loading configurations from multiple sources (via `ConfigSource`) and automatically merges them.

### Merge and Override Mechanism of ConfigManager

`ConfigManager` stores a list of sources (`ConfigSource`). When initialized, it reads sequentially from the first source to the last. **Sources added later will override the configurations of previously added sources.**
This is extremely useful: You can load a `default.json` file first, and then load an `EnvSource` so that Environment Variables overwrite the default values without requiring code changes.

---

## 2. API and Interfaces

### `IConfig` Interface

Located at `sagittarius_engine.interfaces.i_config`

```python
class IConfig(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None, cast: type[T] | None = None) -> Any:
        """
        Gets a configuration value.
        - key: The configuration key (e.g., 'db_host')
        - default: Returns this value if the key does not exist.
        - cast: Safely casts the data type.
        """
        ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Stores a configuration variable into memory."""
        ...
```

### Sources for ConfigManager

- **`JsonSource`**: Reads configuration from a JSON file (e.g., `config.add_source(JsonSource('appsettings.json'))`).
- **`EnvSource`**: Loads environment variables (supports prefixing).
- **`DictSource`**: Loads configuration from an existing Python dictionary.

---

## 3. Usage Guide

### Initializing ConfigManager (For Production Applications)

You typically set up the configuration before loading it into the DI Container during the Kernel's boot phase:

```python
from sagittarius_engine.infrastructure.config.config_manager import ConfigManager

# Create a new ConfigManager
config = ConfigManager()

# Method 1: Add sources manually
# Add JSON file (lowest priority)
config.load_json("default_config.json")
# Add environment variables (higher priority, overrides JSON)
config.load_env(prefix="MYAPP_") 

# Method 2: Use Factory Chain
config = (ConfigManager()
          .load_json("config.json")
          .load_env())

# Get value with type casting (cast)
port = config.get("PORT", default=8080, cast=int)
db_host = config.get("DB_HOST", default="localhost")
```

### Initializing DictConfig (For Testing)

```python
from sagittarius_engine.infrastructure.config.dict_config import DictConfig

# "Mock" configuration for unit tests
test_config = DictConfig({
    "database": "sqlite:///:memory:",
    "debug": True
})

# Register into the DI Container
container.singleton(IConfig, test_config)
```

---

## 4. Common Misconceptions

### ❌ Misconception 1: Every time `config.get(...)` is called, the system re-reads the JSON file or re-parses Environment Variables

✅ **Truth**: `ConfigManager` uses **Lazy Evaluation** and **Caching**. When you initialize the `Sources`, it doesn't read them immediately. However, on the very first `config.get(...)` call, it reads all sources, merges them, and saves them into an internal `_cache` dictionary. Subsequent calls to `get()` simply read from the `_cache`, which is extremely lightweight and fast.

### ❌ Misconception 2: You cannot cast data types from environment variables

✅ **Truth**: Environment variables are strings by default. You can easily run into logical errors if you use `"123"` for math calculations. However, the `IConfig` API includes a `cast` parameter. If you call `config.get("PORT", cast=int)`, the system will automatically safely cast the value to `int` without crashing the application.

### ❌ Misconception 3: You cannot modify configuration values at Runtime

✅ **Truth**: You can still use the `config.set(key, value)` function. The set function will overwrite that value directly into the RAM `_cache` of the `ConfigManager`. However, note that this action does **not persist** (write back) to the `config.json` file or System Environment.

### ❌ Misconception 4: The framework forces you to use `ConfigManager`

✅ **Truth**: No. The application's Container only requires 1 class that satisfies the `IConfig` Interface. If your project is more complex and uses `pydantic-settings` or `dynaconf`, you can absolutely write an adapter that implements `IConfig` and bind it to the Container without breaking any legacy Engine modules.
