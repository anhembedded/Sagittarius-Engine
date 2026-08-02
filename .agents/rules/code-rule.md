---
trigger: always_on
---

# PYTHON CODING STANDARDS & GUIDELINES

## Core Architecture Principles
1. **Strong Typing & Type Safety:**
   - Always use explicit type annotations for all function signatures, parameters, return values, and class attributes.
   - Strictly avoid using `Any`. Use `Union`, `Optional`, `Generics`, or `TypeVar` where flexiblity is needed.
   - Use `dataclasses` (with `frozen=True` where possible) or `Pydantic` models instead of raw dictionaries for complex data structures.

2. **Full Abstraction & Decoupling:**
   - Define explicit abstractions using `abc.ABC` or `typing.Protocol` for repositories, services, and external clients.
   - Adhere strictly to the Dependency Inversion Principle (DIP). High-level business logic must depend on abstractions, not concrete implementations.
   - Prefer Dependency Injection (DI) over hardcoded class instantiations inside domain logic.
   - **NO Multiple Inheritance:** Strictly avoid multiple inheritance. Use composition over inheritance, and flatten interfaces where necessary to avoid complex method resolution orders (MRO).

3. **Readability & Clean Code (Over Brevity):**
   - Follow PEP 8 guidelines. Prioritize explicit and self-documenting code over short one-liners.
   - Do NOT use complex, nested list comprehensions or multi-line `lambda` expressions when a clear `for` loop or helper function is more readable.
   - Keep functions small, focused, and single-purpose (Single Responsibility Principle). Use explicit, descriptive variable names.

4. **Immutability & Pure Functions (No Side Effects):**
   - Strive for pure functions: functions should depend only on passed arguments and produce deterministic return values.
   - Never mutate passed arguments in-place. Return new instances or modified copies instead.
   - Strictly avoid mutable default arguments (e.g., NEVER use `def func(items=[]):`).
   - Isolate side effects (I/O, DB calls, network requests) inside dedicated adapter/boundary classes.