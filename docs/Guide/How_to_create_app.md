---
type: HOW TO CREATE APP FROM THIS FRAMEWORK - HOW TO CREATE APP FROM THIS FRAMEWORK
tags: [First start, core]
language: python
---

# [HOW TO CREATE APP FROM THIS FRAMEWORK - HOW TO CREATE APP FROM THIS FRAMEWORK]

## Overview
Guide for commond use case of HOW TO CREATE APP FROM THIS FRAMEWORK - HOW TO CREATE APP FROM THIS FRAMEWORK

## Core API / Interface
Refer to `src/app_kernel.py` file

## Dependencies
What other modules or external libraries does this depend on?

## How to Use / Examples

```python
from src.infra.std_container import StdLibContainer
from src.infra.memory_event_bus import MemoryEventBus
from src.app_kernel import App
from src.interfaces import IContainer, IEventBus

# Able to use nother infrstructue in src/infra
container = StdLibContainer()
event_bus = MemoryEventBus()
app = App(container, event_bus)

# The container must know about itself
container.singleton(IContainer, container)
container.singleton(IEventBus, event_bus)

# Boot (and auto‑load modules from 'modules' package if you have one)
app.boot(auto_discover="modules")

```

## Implementation Notes
Todo

## Related Documents
Link to other design docs, API specs, or tickets.

- [Todo](todo.md)
