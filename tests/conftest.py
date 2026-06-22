import sys
from pathlib import Path

# Ensure project's root and src directories are on sys.path so tests and internal imports resolve correctly
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

