---
type: design_doc
tags: [sagittarius, scaffold, cli]
language: python
---

# Scaffold

## Overview
The Scaffold tool is a project generator script (`src/scaffold.py`) that quickly bootstraps a new Sagittarius application following Clean Architecture folder structures.

## Problem Statement
Manually creating the heavily nested folder structures typical of Clean Architecture (Domain, Application, Infrastructure, Adapters, Modules) and wiring the initial `main.py` Composition Root is tedious and creates a high barrier to entry for new developers.

## Proposed Solution
A simple command-line script that accepts a project name and generates the standardized directory tree, empty `__init__.py` files, a base `config.json`, and a fully wired `main.py` script that utilizes the `App`, `StdLibContainer`, `MemoryEventBus`, and built-in modules.

## Core API / Interface

### `def create_project(project_name: str, base_path: str = ".") -> None` (in `src/scaffold.py`)
Creates the directory structure and files.

## Dependencies
- Internal: None (standalone script generating boilerplate)
- External: `os`, `json`, `sys`

## How to Use / Examples

From the command line:

```bash
python src/scaffold.py my_awesome_app
cd my_awesome_app
python main.py
```

## Implementation Notes
- It automatically creates `domain/`, `application/`, `infrastructure/`, `adapters/`, and `modules/` directories.

## Related Documents
- `app_kernel.md`
