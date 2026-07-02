---
type: design_doc
tags: [sagittarius, dx, tooling]
language: python
---

# HotReloader

## Overview
`HotReloader` is a Developer Experience (DX) tool designed to automatically restart the Python process whenever a file modification is detected.

## Problem Statement
During development, stopping and manually restarting the application to test new code changes slows down the feedback loop. Using standard Python `importlib.reload` is often buggy due to cached module states and lingering singletons.

## Proposed Solution
The `HotReloader` runs a background daemon thread that polls `os.stat()` modification times on all `.py` files within specified watch directories. When a change or deletion is detected, it utilizes `os.execv` to completely replace the current process with a brand new one, ensuring a clean state restart.

## Core API / Interface

### `class HotReloader` (in `src/hot_reloader.py`)
- `def __init__(self, watch_paths: List[str], interval: float = 1.0) -> None`: Initializes with paths to watch and polling interval.
- `def start(self) -> None`: Starts the background polling thread.
- `def stop(self) -> None`: Stops the background thread.

## Dependencies
- Internal: None
- External: `os`, `sys`, `time`, `threading`

## How to Use / Examples

```python
import sys
from src.hot_reloader import HotReloader

def main():
    print("Application running...")
    # App logic here

if __name__ == "__main__":
    if "--watch" in sys.argv:
        # Watch the src and modules folders
        reloader = HotReloader(["src", "modules", "main.py"])
        reloader.start()
    main()
```

## Implementation Notes
- **Process Replacement**: Because `os.execv` replaces the current process, any code running after it will not execute. The OS re-runs the script from the beginning.
- **Flushing**: Standard output and error buffers are explicitly flushed (`sys.stdout.flush()`) right before restart to ensure no logs are lost.

## Related Documents
- `scaffold.md`
