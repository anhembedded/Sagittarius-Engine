import os
import glob

# 1. Create directories
base = "sagittarius_engine/extensions"
os.makedirs(f"{base}/health", exist_ok=True)
os.makedirs(f"{base}/logger", exist_ok=True)
os.makedirs(f"{base}/thread_manager", exist_ok=True)

# 2. Move files
moves = [
    ("health_module.py", "health/health_module.py"),
    ("health_check_query.py", "health/health_check_query.py"),
    ("logger_module.py", "logger/logger_module.py"),
    ("thread_manager_module.py", "thread_manager/thread_manager_module.py"),
]

for src, dst in moves:
    src_path = f"{base}/{src}"
    dst_path = f"{base}/{dst}"
    if os.path.exists(src_path):
        os.rename(src_path, dst_path)
        folder = dst.split("/")[0]
        with open(f"{base}/{folder}/__init__.py", "w") as f:
            f.write("")  # create empty __init__

# 3. Search and replace imports globally
replacements = {
    "sagittarius_engine.extensions.health.health_module": "sagittarius_engine.extensions.health.health_module",
    "sagittarius_engine.extensions.health.health_check_query": "sagittarius_engine.extensions.health.health_check_query",
    "sagittarius_engine.extensions.logger.logger_module": "sagittarius_engine.extensions.logger.logger_module",
    "sagittarius_engine.extensions.thread_manager.thread_manager_module": "sagittarius_engine.extensions.thread_manager.thread_manager_module",
}

for ext in ["**/*.py", "**/*.md"]:
    for filepath in glob.glob(ext, recursive=True):
        if "site-packages" in filepath or ".venv" in filepath or ".git" in filepath:
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content
            for old, new in replacements.items():
                new_content = new_content.replace(old, new)

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated imports in {filepath}")
        except Exception:
            pass
