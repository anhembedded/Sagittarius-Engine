> Applies to Sagittarius Engine v1.x

# Installation

This guide covers installing Sagittarius Engine and verifying your setup.

---

## Requirements

- Python **3.10** or higher
- pip

---

## Install Options

### Option 1: Install from GitHub Repository (Production / Shared)
```bash
pip install git+https://github.com/anhembedded/Sagittarius-Engine.git
```

### Option 2: Local Editable Mode (For Framework Development)
```bash
pip install -e /path/to/Sagittarius_ForkBoy
```

### Option 3: Build & Install Local Wheel (.whl)
```bash
pip install build
python -m build
pip install dist/sagittarius_engine-1.0.0-py3-none-any.whl
```

---

## How to Use in External Projects

### Step 1: Declare Framework Dependency
In your new project's `requirements.txt` or `pyproject.toml`:

```text
# requirements.txt
sagittarius-engine @ git+https://github.com/anhembedded/Sagittarius-Engine.git
```

### Step 2: Scaffold a New Project Structure
Use the built-in Sagittarius CLI / Scaffold tool to generate a production-ready Clean Architecture application skeleton:

```bash
# Generate a new Clean Architecture project:
python -m tools.scaffold my_new_app
```

Or via CLI tool:
```bash
sagittarius new clean my_new_app
```

Generated directory layout:
```
my_new_app/
├── domain/          # Entities, Domain Events, Domain Exceptions (STDLIB only)
├── application/     # Use Cases, Ports (Interfaces), DTOs (Commands/Queries)
├── infrastructure/  # Repositories (SQLite, In-Memory), DB Session Adapters
├── adapters/        # Presentation Interfaces (CLI, Web, PySide6 GUI)
├── modules/         # Packaged Modules (Auto-discovery)
├── config.json      # Environment configuration
└── main.py          # Composition Root & App Kernel startup
```

---

## Quick Verify

After installation, run the following script in your new project to confirm the engine boots and stops cleanly:

```python
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container.std_container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus.memory_event_bus import MemoryEventBus

container = StdLibContainer()
event_bus = MemoryEventBus()

app = App(container, event_bus)
app.boot()
app.stop()

print("Sagittarius Engine OK")
```

Expected output:

```
Sagittarius Engine OK
```

No errors means the engine is installed correctly and ready to host your application logic.

---

## Next Step

→ [Build your first app](first_app.md)

---

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/getting-started/installation.md)
