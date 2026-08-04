# TASK-016: Formalize `name` Method on Extension and Middleware Interfaces

## Description
Currently, when logging extensions or middlewares during boot or registration, the framework uses a workaround (e.g., `getattr(obj, "name", lambda: obj.__class__.__name__)`) to safely get their names. To improve type safety and object-oriented design, we need to formalize a `name` method (or `@property`) on the core interfaces.

*Note: This task should be completed **after** [TASK-015](TASK-015_framework_logging_null_object.md).*

## Requirements
1. **Update Interfaces:** Add a `name` method (or property) to the `IExtension` and `IMiddleware` interfaces (and `IModule` if applicable). It could look like this:
   ```python
   def name(self) -> str:
       return self.__class__.__name__
   ```
2. **Refactor Usage (`app.py`):** Remove the `getattr` hacks in `app.py`'s `use` and `use_middleware` methods. Since the interfaces now guarantee a `name` method, you can directly call `extension_or_module.name()` or access `extension_or_module.name` for logging.
3. **Verify Implementations:** Make sure existing extensions and middlewares properly inherit or implement this `name` method without breaking backward compatibility.
