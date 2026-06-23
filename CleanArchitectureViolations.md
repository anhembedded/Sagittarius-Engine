# Clean Architecture Violations

This document explains a previous Clean Architecture violation found in the `ConfigManager` module and how it was resolved.

## The Violation

In Clean Architecture, the Dependency Rule states that source code dependencies can only point inwards. The **Domain Layer** (the innermost circle) should not know anything about the **Adapters Layer** or the **Infrastructure Layer** (the outer circles).

The `ConfigManager` (located in `src/domain/configuration/Configuration_api.py`) violated this rule. Its `load_config` method was written like this:

```python
class ConfigManager:
    # ...
    def load_config(self, config_path: str) -> AppConfig:
        """Load configuration using the adapter."""
        if hasattr(self.__file_manager, "_filepath"):
            self.__file_manager._filepath = config_path
        return self.__file_manager.load()
```

### Why is this a violation?
1. **Implementation Detail Leakage**: The Domain layer (`ConfigManager`) assumed that the adapter (`__file_manager`) was a file-based adapter that had a specific private attribute named `_filepath`.
2. **Coupling**: The domain was tightly coupled to the internal state management of the `LocalConfigAdapter`. If we had used a database or environment variable adapter that didn't have a `_filepath` attribute, this logic would be fragile or irrelevant.
3. **Encapsulation Breakage**: Setting a private attribute (`_filepath`) of another object directly is an anti-pattern. The interface (`ConfigPort`) should define the contract.

## The Fix

To adhere to Clean Architecture, we updated the **Port** (the interface) to explicitly define what the domain needs to provide when loading or saving a configuration.

### 1. Update the Port (`ConfigPort`)
We updated the `ConfigPort` interface in the domain layer to accept `filepath` explicitly as a parameter, so the domain passes the necessary context through the contract.

```python
class ConfigPort(ABC):
    @abstractmethod
    def load(self, filepath: str) -> AppConfig:
        raise NotImplementedError()

    @abstractmethod
    def save(self, config: AppConfig, filepath: str) -> None:
        raise NotImplementedError()
```

### 2. Update the Domain (`ConfigManager`)
The domain now simply relies on the contract defined by the `ConfigPort` and passes the required argument, without manipulating any private adapter state.

```python
class ConfigManager:
    # ...
    def load_config(self, config_path: str) -> AppConfig:
        """Load configuration using the adapter."""
        return self.__file_manager.load(config_path)
```

### 3. Update the Adapter (`LocalConfigAdapter`)
The adapter implements the interface exactly as defined, accepting `filepath` in its methods instead of storing it as a state during initialization.

```python
class LocalConfigAdapter(ConfigPort):
    def __init__(self, json_infra: JsonFileInfra) -> None:
        self._json_infra = json_infra

    def load(self, filepath: str) -> AppConfig:
        # ... logic to load from filepath ...
        pass

    def save(self, config: AppConfig, filepath: str) -> None:
        # ... logic to save to filepath ...
        pass
```

### Conclusion
By refactoring this code, the Domain layer is completely decoupled from the Adapter implementation details. The domain defines *what* is needed (via the Port), and the adapter handles *how* it's done, adhering strictly to the Dependency Rule.
