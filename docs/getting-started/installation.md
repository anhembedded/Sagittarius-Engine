> Applies to Sagittarius Engine v1.x

# Installation

This guide covers installing Sagittarius Engine and verifying your setup.

---

## Requirements

- Python **3.10** or higher
- pip

---

## Install

```bash
pip install sagittarius-engine
```

Or install from source:

```bash
git clone https://github.com/your-repo/sagittarius-engine.git
cd sagittarius-engine
pip install -e .
```

---

## Quick Verify

After installation, run the following to confirm the engine boots and stops cleanly:

```python
from sagittarius_engine import App
from sagittarius_engine.infrastructure.container import StdLibContainer
from sagittarius_engine.infrastructure.event_bus import MemoryEventBus

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

No errors means the engine is installed correctly.

---

## Next Step

→ [Build your first app](first_app.md)

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/getting-started/installation.md)
