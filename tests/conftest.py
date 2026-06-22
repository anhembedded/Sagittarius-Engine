import sys
from pathlib import Path

# Ensure project's `src` directory is on sys.path so tests can import top-level packages
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
