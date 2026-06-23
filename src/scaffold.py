import os
import json

def create_project(project_name: str, base_path: str = ".") -> None:
    project_dir = os.path.join(base_path, project_name)

    # Create directories
    os.makedirs(os.path.join(project_dir, "modules"), exist_ok=True)

    # Create config.json
    config_path = os.path.join(project_dir, "config.json")
    with open(config_path, "w") as f:
        json.dump({"app_name": project_name, "version": "1.0.0"}, f, indent=4)

    # Create __init__.py for modules package
    with open(os.path.join(project_dir, "modules", "__init__.py"), "w") as f:
        pass

    # Create main.py
    main_py_content = """from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.core import App, IContainer, IEventBus

def main():
    container = StdLibContainer()
    event_bus = MemoryEventBus()
    app = App(container, event_bus)

    container.singleton(IContainer, container)
    container.singleton(IEventBus, event_bus)

    # Auto-discover modules in the 'modules' package
    # Make sure your PYTHONPATH is set correctly or 'modules' is importable
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
