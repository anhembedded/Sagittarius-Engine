import os
import sys
import time
import threading
from typing import List, Dict, Optional

class HotReloader:
    """
    @brief Developer Experience tool to automatically restart the application when code changes.

    @details Uses a background thread to poll `os.stat` on all python files in the watched directories.
    When a modification is detected, it uses `os.execv` to restart the entire process.
    This provides a clean state restart, avoiding module caching issues.

    @par Tutorial / Usage Example:
    @code
    from src.hot_reloader import HotReloader

    if __name__ == "__main__":
        if "--watch" in sys.argv:
            reloader = HotReloader(["src", "modules", "main.py"])
            reloader.start()
        main()
    @endcode
    """
    def __init__(self, watch_paths: List[str], interval: float = 1.0) -> None:
        """
        @brief Constructor.

        @param watch_paths A list of directories or files to watch.
        @param interval The polling interval in seconds.
        """
        self.watch_paths = watch_paths
        self.interval = interval
        self._mtimes: Dict[str, float] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _get_mtime(self, path: str) -> float:
        return os.stat(path).st_mtime

    def _scan_files(self) -> dict:
        mtimes = {}
        for path in self.watch_paths:
            if not os.path.exists(path):
                continue
            if os.path.isfile(path):
                if path.endswith('.py'):
                    mtimes[path] = self._get_mtime(path)
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith('.py'):
                            full_path = os.path.join(root, file)
                            mtimes[full_path] = self._get_mtime(full_path)
        return mtimes

    def _poll(self) -> None:
        self._mtimes = self._scan_files()
        while self._running:
            time.sleep(self.interval)
            current_mtimes = self._scan_files()
            for path, mtime in current_mtimes.items():
                if path not in self._mtimes or self._mtimes[path] != mtime:
                    print(f"\n[HotReloader] Detected change in '{path}'. Restarting...\n")
                    self._restart()

            # Check for deleted files
            for path in self._mtimes:
                if path not in current_mtimes:
                    print(f"\n[HotReloader] Detected deleted file '{path}'. Restarting...\n")
                    self._restart()

            self._mtimes = current_mtimes

    def _restart(self) -> None:
        """@brief Restarts the current process."""
        sys.stdout.flush()
        sys.stderr.flush()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def start(self) -> None:
        """@brief Starts the hot reloader background thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._poll, daemon=True)
        self._thread.start()
        print(f"[HotReloader] Watching directories: {', '.join(self.watch_paths)} for changes...")

    def stop(self) -> None:
        """@brief Stops the hot reloader."""
        self._running = False
        if self._thread:
            self._thread.join()
