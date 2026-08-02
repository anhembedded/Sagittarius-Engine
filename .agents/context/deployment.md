# Deployment Guide

Sagittarius Engine is distributed via PyPI or installed from source.

## Distributing the Engine
1. Update version in `pyproject.toml`.
2. Build wheel: `python -m build`
3. Publish: `twine upload dist/*`

## Deploying Applications
Since applications own the architecture, deploy them however you prefer:
- **Docker**: Containerize the app and run it as an entrypoint.
- **Systemd**: Run long-lived bots or API servers as daemon processes.
- **Executables**: Use `PyInstaller` (especially for UI tools like `audit_dashboard`).
