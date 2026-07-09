# ROLE

You are a senior Python architect performing a NON-BREAKING architecture refactor.

The Sagittarius project is evolving from a "Clean Architecture template"
into a reusable "Application Engine".

The objective of this phase is ONLY to rename architectural concepts to better
represent an engine.

DO NOT redesign logic.
DO NOT change behaviors.
DO NOT introduce new features.

Everything must continue to work exactly as before.

--------------------------------------------------

# GOAL

Rename the project structure to remove the impression that Sagittarius is
an application following Clean Architecture.

Instead it should look like a reusable engine.

--------------------------------------------------

# DIRECTORY RENAMES

Rename only the architectural namespaces.

application/kernel
    -> kernel

application/ports
    -> interfaces

modules
    -> extensions

Keep these unchanged:

adapters/
middleware/
infrastructure/
tools/

--------------------------------------------------

# IMPORTS

Update every import accordingly.

Examples:

from sagittarius_engine.kernel.app import App

becomes

from sagittarius_engine.kernel.app import App

--------------------------------------------

from sagittarius_engine.interfaces.i_logger import ILogger

becomes

from sagittarius_engine.interfaces.i_logger import ILogger

--------------------------------------------------

# PACKAGE NAME

Rename

src

to

sagittarius_engine

Update every absolute import.

Do NOT leave broken imports.

--------------------------------------------------

# DO NOT CHANGE

Do NOT rename classes.

For example these classes MUST keep their names:

App

ApplicationRunner

MiddlewarePipeline

ModuleAutoDiscovery

StdLibContainer

MemoryEventBus

ILogger

IContainer

IEventBus

etc.

Only move them into their new packages.

--------------------------------------------------

# PUBLIC API

The following code should continue to work
(after only changing imports):

app = App(container, event_bus)

app.boot()

app.execute(...)

app.query(...)

No behavior changes.

--------------------------------------------------

# TESTS

Update every test import.

No test logic should change.

Only imports.

--------------------------------------------------

# DOCUMENTATION

Update package names inside:

docstrings

examples

comments

README snippets

Examples should import from

sagittarius_engine

instead of src.application.

--------------------------------------------------

# DO NOT TOUCH

Do NOT modify:

Dependency Injection

Middleware

Event Bus

CQRS

Repositories

Threading

Logging

Configuration

Storage

Database

Business logic

Only namespace/layout changes.

--------------------------------------------------

# ACCEPTANCE CRITERIA

The final result must satisfy ALL:

✓ No broken imports

✓ No circular imports introduced

✓ Public API unchanged

✓ All tests should still pass

✓ No behavioral differences

✓ Folder names reflect an Application Engine instead of a Clean Architecture application

--------------------------------------------------

# OUTPUT

After refactoring, provide:

1. Directory tree before/after

2. List of renamed packages

3. List of updated imports

4. Any compatibility concerns

5. Files that may require manual review




hay vì rename trực tiếp:

application/

↓

kernel/

Mình sẽ để:

sagittarius_engine/

    kernel/
        app.py
        app_runner.py
        lifecycle.py

    interfaces/

    infrastructure/

    middleware/

    adapters/

    extensions/

    tools/

Không nên có thư mục kernel/kernel.

Tức là đừng làm:

kernel/
    app.py

rồi import:

from sagittarius_engine.kernel.app import App

Cái này là đẹp.

Chứ đừng để:

application/kernel/app.py

rồi đổi thành:

kernel/kernel/app.py

vì sẽ rất kỳ. Đây cũng là lý do mình đề xuất di chuyển toàn bộ nội dung application/kernel lên thành kernel/, chứ không chỉ đổi tên thư mục. Điều này sẽ làm cấu trúc engine gọn gàng và tự nhiên hơn.



Do not add new features.
Do not perform Phase 2.