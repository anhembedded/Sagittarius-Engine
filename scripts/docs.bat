@echo off
if "%1"=="serve" (
    .venv\Scripts\python.exe -m mkdocs serve
) else if "%1"=="build" (
    .venv\Scripts\python.exe -m mkdocs build --strict
) else (
    echo Usage: scripts\docs.bat [serve^|build]
)
