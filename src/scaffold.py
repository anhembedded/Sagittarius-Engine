import os
import json

def create_project(project_name: str, base_path: str = ".") -> None:
    """
    @brief Scaffolds a new project structure.

    @details Creates the basic directory structure and files for a new project using this framework.
    It generates a directory containing `main.py` as the entry point (Composition Root), a
    `modules` directory for business logic, and a `config.json` file.

    @par Tutorial / Usage Example:
    @code
    # 1. From the terminal, run the command:
    python src/scaffold.py my_awesome_app

    # 2. Navigate into the project directory and run it:
    cd my_awesome_app
    python main.py
    @endcode

    @param project_name The name of the project to create.
    @param base_path The path where the project should be created. Defaults to the current directory.
    """
    project_dir = os.path.join(base_path, project_name)

    # Initialize directory
    os.makedirs(os.path.join(project_dir, "modules"), exist_ok=True)

    # Initialize basic config file
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump({"app_name": project_name, "version": "1.0.0"}, f, indent=4)

    # Mark the modules directory as a Python package
    with open(os.path.join(project_dir, "modules", "__init__.py"), "w") as f:
        pass

    # Create the sample Composition Root (main.py)
    main_py_content = """from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.core import App, IContainer, IEventBus

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    # Automatically scan and load IModules present in the 'modules' package
    try:
        app.boot(auto_discover="modules")
        print("Application booted successfully.")
    except Exception as e:
        print(f"Error booting application: {e}")

if __name__ == "__main__":
    main()
"""
    main_path = os.path.join(project_dir, "main.py")
    with open(main_path, "w") as f:
        f.write(main_py_content)

    print(f"Project '{project_name}' scaffolded successfully at '{project_dir}'.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        create_project(sys.argv[1])
    else:
        print("Usage: python scaffold.py <project_name>")
