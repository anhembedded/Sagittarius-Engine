# Sagittarius Engine Documentation Roadmap v1

## 🎯 Vision

Documentation không chỉ mô tả API.

Documentation là **specification**, **learning path** và **developer experience** của Sagittarius Engine.

Mục tiêu đạt chất lượng tương đương:

* Microsoft .NET Documentation
* ASP.NET Core
* Rust Book
* FastAPI
* Kubernetes

Documentation phải luôn phản ánh **public API**, **runtime capabilities**, và **best practices** của Sagittarius Engine.

---

# Documentation Philosophy

Documentation ưu tiên dạy **Concept trước API**.

Learning Path:

```text
Getting Started
        │
        ▼
Core Concepts
        │
        ▼
Runtime
        │
        ▼
Advanced Topics
        │
        ▼
Tutorials
        │
        ▼
API Reference
        │
        ▼
Migration
```

Documentation không giải thích implementation.

Documentation giải thích cách **sử dụng Engine**.

---

# Documentation Principles

Mỗi tài liệu phải trả lời được:

```text
What?

Why?

When?

When NOT?

How?

Example

Diagram (if needed)

Best Practices

Common Mistakes

Related APIs
```

---

# Documentation Standards

Mọi code example:

```python
from sagittarius_engine import ...
```

Không:

* import internal packages
* dùng deprecated APIs
* giải thích private implementation
* sử dụng screenshots

Ưu tiên:

* Mermaid Flowcharts
* Mermaid Sequence Diagrams
* Mermaid Class Diagrams

---

# Documentation Source of Truth

Documentation must always follow the following priority:

1. Public API
2. Project Knowledge Base
3. Examples
4. Runtime Behavior
5. Internal Source Code (only if necessary)

AI must never infer undocumented behavior.

If behavior cannot be confirmed by the Project Knowledge Base or Public API, it should be marked as unknown rather than guessed.

---

# Examples Code Rules

Examples are normative.

Whenever possible, documentation should reference the corresponding example application instead of duplicating large code snippets.

Large examples belong in `examples/`.

Documentation should explain them rather than copy them.

---

# Project Knowledge Base

To keep documentation consistent and avoid repeatedly scanning the source tree, AI should use the maintained knowledge base under `.ai/`.

```text
.ai/

project_knowledge.md
public_api.md
runtime_overview.md
architecture.md
terminology.md
examples_index.md
roadmap.md
benchmark_results.md
current_status.md
doc_status.md
doc_plan.md
```

## project_knowledge.md

High-level overview of Sagittarius Engine:

* Vision
* Philosophy
* Runtime capabilities
* Extension system
* SDK
* Roadmap

## public_api.md

Frozen public API.

Contains only officially supported types.

Example:

```text
App
EngineContext
Dispatcher
IExtension
ExtensionDescriptor
IHostedService
TaskManager
Scheduler
CancellationToken
dispatch()
```

## runtime_overview.md

Runtime architecture.

Boot sequence.

Shutdown sequence.

Hosted services.

Scheduler.

Task manager.

Async runtime.

Cancellation.

## architecture.md

Architecture overview.

Kernel responsibilities.

Runtime responsibilities.

Extension lifecycle.

Dependency graph.

## terminology.md

Official vocabulary.

Ensures documentation never mixes terms like:

* Module vs Extension
* Engine vs Application
* Runtime vs Kernel

AI must always consult these files before generating new documentation.

## examples_index.md

Lists all reference applications, their purpose, and the public APIs they illustrate.

## roadmap.md

Summarizes phase status of the engine to keep documentation aligned with the development roadmap.

## benchmark_results.md

Stores core benchmark results (boot time, scheduler latency, hosted services) as a unified reference for performance documentation.

---

# Documentation Status

## ✅ Phase D1 — Documentation Foundation

**Status:** Completed

### Deliverables

```text
docs/

index.md
STYLE_GUIDE.md
DOC_REVIEW_CHECKLIST.md

getting-started/

installation.md
first_app.md
first_extension.md
project_templates.md

concepts/
README.md

tutorials/
README.md

advanced/
extension_dependencies.md
```

### Acceptance

* Landing page completed
* Style guide completed
* Getting Started completed

---

## ✅ Phase D1.5 — Documentation Infrastructure

**Status:** Completed

### Deliverables

```text
mkdocs.yml
requirements-docs.txt

docs/assets/
logo.svg
favicon.png

docs.bat
docs.sh
Makefile
```

### Features

* Material Theme
* Search
* Dark Mode
* Mermaid
* Mike Versioning
* Strict Build
* Reproducible dependency versions

### Acceptance

```bash
docs.bat build
docs.bat serve
```

Both execute successfully.

---

## ✅ Phase D1.6 — Documentation Quality

**Status:** Completed

### Goal

Treat documentation as production code.

### Deliverables

```text
tests/
    test_docs.py

.github/workflows/
    docs.yml
```

### Validation

Verify:

* Markdown links
* MkDocs build
* Python snippets
* Public imports
* Deprecated APIs
* Mermaid rendering
* Broken links

### Acceptance

```bash
pytest
mkdocs build --strict
```

Both pass successfully.

### Future

Prepare pre-commit hooks:

* markdownlint
* ruff
* black

---

## ✅ Phase D1.7 — API Reference

**Status:** Completed

### Goal

Automatically generate API documentation.

### Deliverables

```text
docs/api/

index.md
app.md
engine_context.md
dispatcher.md
event_bus.md
scheduler.md
task_manager.md
hosted_service.md
extension.md
cancellation_token.md
```

Using:

* mkdocstrings
* Docstrings
* Auto-generation

### Public APIs

* App
* EngineContext
* Dispatcher
* EventBus
* IExtension
* IHostedService
* Scheduler
* TaskManager
* CancellationToken

---

## ✅ Phase D2 — Core Concepts

**Status:** Completed

### Goal

Explain the design philosophy of Sagittarius Engine.

### Deliverables

```text
docs/concepts/

engine.md
runtime.md
dispatcher.md
dependency_injection.md
event_bus.md
middleware.md
extensions.md
lifecycle.md
```

Focus:

* WHY
* DESIGN
* RELATIONSHIPS

`runtime.md` should only explain what the Runtime is, what it contains, and the Runtime lifecycle. It must not include API details (to avoid duplication with the API Reference and to keep file sizes manageable).

No API reference.

Acceptance:

Developers understand how Sagittarius Engine works.

---

## ✅ Phase D3 — Runtime Guides

### Goal

Explain how to use the Sagittarius Runtime Infrastructure in real applications.
The goal is to teach developers how the runtime components cooperate and when to use them, going from concept → usage → best practices.

### Deliverables

```text
docs/runtime/

application_lifecycle.md
hosted_services.md
scheduler.md
task_manager.md
async_runtime.md
cancellation_token.md
```

### Clarification: Lifecycle (D2 vs D3)

* **D2 – `concepts/lifecycle.md`**: Explains the architectural lifecycle (Application → Kernel → Runtime → Shutdown). No deep component details.
* **D3 – `runtime/application_lifecycle.md`**: Explains the actual runtime execution, including Boot sequence, Startup order, Rollback, Shutdown order, Thread cleanup, Async runtime shutdown, Scheduler stop, Hosted service stop, and Task cleanup.
  * *Do NOT explain architecture philosophy, kernel responsibilities, or extension concepts here.*

### Document Structure

Every document MUST begin with a "Runtime Component Relationships" section (e.g. Scheduler -> TaskManager -> AsyncRuntime).
Structure:
# Title -> Runtime Component Relationships -> Overview -> Why -> When to Use -> When NOT to Use -> Runtime Responsibilities -> Lifecycle -> Architecture (Mermaid) -> Basic Example -> Advanced Example -> Best Practices -> Common Mistakes -> Related Concepts -> Related Runtime Guides -> Related Tutorials -> Related API Reference.

### Topics:

* application_lifecycle.md: Actual runtime execution, startup ordering, shutdown ordering, runtime resource ownership, rollback guarantees, cleanup guarantees, runtime state transitions.
* hosted_services.md: Hosted Service Lifetime Ownership (Application -> HostedServiceManager -> HostedService), managed lifecycle, rollback, cancellation.
* scheduler.md: Interval scheduling, Cron scheduling (if supported by current public API), isolation.
* task_manager.md: Background execution, Thread Pool, CPU/IO work, Async work, Task Metadata, Task Cleanup.
* async_runtime.md: The asynchronous execution environment managed by the Runtime. Explain why it exists, when developers benefit from it, and how synchronous and asynchronous execution cooperate. (Do NOT use the word "internal").
* cancellation_token.md: Cancellation hierarchy (Application Stop -> CancellationToken -> Hosted Services -> Scheduler -> Background Tasks). Cooperative cancellation.

### Runnable Examples
Examples MUST be:
- <= 50 lines
- executable and terminate cleanly
- use only `from sagittarius_engine import ...`
- no internal imports, no private classes, no deprecated APIs.

### Scope Guard
This phase documents runtime usage.
It must NOT:
- duplicate Core Concepts
- duplicate API Reference
- expose implementation details
- expose internal packages
- explain private classes
If a topic already exists in docs/api/, link to it instead of repeating it.
If a topic belongs to docs/concepts/, summarize it and link to it.

---

## ✅ Phase D4 — Advanced Guides

### Goal

Advanced Guides explain how Sagittarius Engine should be used in large, maintainable applications. Focus on architectural decisions, scalability, maintainability, performance considerations, extension composition, and troubleshooting.
This phase targets experienced developers and architects.

### Deliverables

```text
docs/advanced/

extension_dependencies.md (Review, Expand, Complete existing file)
architecture.md
performance.md
best_practices.md
troubleshooting.md
```

### Document Structure

Every document MUST follow this structure:
# Title -> Overview -> Why -> When to Use -> When NOT to Use -> Architecture -> How it Works -> Examples -> Design Trade-offs -> Best Practices -> Anti-Patterns -> Common Mistakes -> Related Guides -> Related API Reference -> See Also.

Every document should contain at least one Mermaid diagram (flowchart TB, sequenceDiagram, or classDiagram) when appropriate.

### Topics / Scope:

* **extension_dependencies.md**: Review, expand, and complete existing file. Add dependency graph, priority, optional dependency, cycle detection, topological sorting, deterministic ordering, best practices, and common mistakes.
* **architecture.md**: Complete engine architecture with clear separation (Application -> App Host -> Kernel -> Runtime -> EngineContext -> Extensions -> Infrastructure Services). Avoid mixing responsibilities. Include one high-level Mermaid diagram. Do NOT document APIs.
* **performance.md**: Startup optimization, extension loading cost, scheduler overhead, task batching, avoiding unnecessary threads, avoiding blocking the Async Runtime, memory ownership, long-running services. Explain design trade-offs.
* **best_practices.md**: Organized by topic: Application Structure, Extensions, Dependency Injection, Dispatcher, Events, Hosted Services, Scheduler, TaskManager, Async Runtime, Shutdown, Testing. Use DO/DON'T tables.
* **troubleshooting.md**: Common developer issues. Use template for each: Symptoms, Possible Causes, Diagnosis, Resolution, Prevention, Related Guides.

### Scope Guard
This phase documents architecture and advanced usage.
It must NOT:
- duplicate API Reference
- duplicate Runtime Guides
- duplicate Core Concepts
- expose implementation details, private classes, or internal packages.
If a topic is already covered elsewhere, summarize it briefly and link to the existing document.

---

## ✅ Phase D5 — Tutorials

**Status:** Completed

### Goal

Tutorials bridge the gap between Concepts, Runtime/Advanced Guides, and Real Applications. 
The primary goal is to teach developers how to build complete applications using Sagittarius Engine by following real, runnable examples from start to finish.

### Deliverables

```text
docs/tutorials/

desktop_app.md
worker_service.md
trading_bot.md
websocket_client.md
plugin_system.md
```

### Critical Rules

1. **Tutorial <-> Example Mapping (1:1)**: Every tutorial MUST correspond to one reference application in `examples/` (e.g. `examples/desktop` -> `desktop_app.md`). Documentation explains the examples; it does not duplicate them. Do NOT invent APIs or behaviors.
2. **Placeholder**: If an example does not exist, create a "Coming Soon" placeholder tutorial. Do NOT invent or hallucinate the implementation.
3. **Synchronize `examples_index.md`**: The `.ai/examples_index.md` must be updated alongside tutorials to remain the single source of truth for all examples.
4. **Snippets Policy**: Do NOT duplicate large source files. Use small snippets (<50 lines) to highlight and explain code. For large code blocks, reference the file in the `examples/` directory.

### Document Structure

Every tutorial MUST follow this exact structure:
# Title -> Overview -> Why -> What You Will Build -> Prerequisites -> Architecture (Mermaid) -> Project Structure -> Step 1 (Explain -> Show -> Why -> Reference) ... -> Running the Application -> How It Works -> Best Practices -> Common Mistakes -> Next Steps -> Related Guides -> Related API Reference.

---

## ✅ Phase D6 — Documentation Review

### Goal

Review and standardize all documentation.

### Deliverables

Review every page using:

```text
DOC_REVIEW_CHECKLIST.md
STYLE_GUIDE.md
```

### Constraints

* Every example referenced in documentation must exist under `examples/` (do not write separate isolated snippets).

### Review:

* Grammar
* Consistency
* Cross-links
* Mermaid
* Terminology
* Examples
* **Tutorial Checks (Added post-D5):**
  * Every tutorial references its source example under `examples/`.
  * Learning Outcomes are present and accurate.
  * Estimated Time and Difficulty are included where appropriate.
  * All code snippets remain synchronized with the corresponding example projects.
  * Every tutorial links to the relevant Concepts, Runtime Guides, and API Reference pages.

Acceptance:

Every page passes documentation review.

---

## ✅ Phase D7 — Migration Guides

### Goal

Help users migrate from older versions.

### Deliverables

```text
docs/migration/

from_clean_architecture.md
deprecated_apis.md
upgrading.md
```

Topics:

* API changes
* Migration examples
* Compatibility notes
* Deprecated APIs

---

## 🚧 Phase D8 — Documentation Polish & Release

### Goal

Finalize documentation for v1.0.

### Checklist

* Validate all links
* Validate Mermaid diagrams
* Execute all code examples
* Grammar review
* Terminology review
* Synchronize docs with code
* Public API verification
* Navigation review
* Search validation

---

# Definition of Done

A documentation phase is considered **Completed** only if:

* All planned documents are completed.
* All code examples execute successfully.
* `pytest` passes.
* `mkdocs build --strict` passes.
* No broken links.
* No deprecated APIs are used.
* All Mermaid diagrams render correctly.
* Documentation follows `STYLE_GUIDE.md`.
* Documentation passes `DOC_REVIEW_CHECKLIST.md`.
* Documentation is consistent with the Project Knowledge Base.
* Examples remain synchronized with `examples/`.
* Public API matches `public_api.md`.

---

# Official Terminology

Always use these terms consistently.

| Preferred      | Meaning                               |
| -------------- | ------------------------------------- |
| Application    | User's project                        |
| Engine         | Sagittarius Engine                    |
| Kernel         | Minimal orchestration layer           |
| Runtime        | Long-running execution infrastructure |
| Extension      | Pluggable runtime capability          |
| EngineContext  | Shared runtime service registry       |
| Dispatcher     | Unified execution entry point         |
| Hosted Service | Managed long-running service          |
| Task           | Unit of background execution          |
| Scheduler      | Time-based execution component        |
| SDK            | Project generation tooling            |
| Host           | The application host coordinating the engine lifecycle |
| Facade         | The stable public API exposed by Sagittarius Engine |

Never use these outdated terms except in migration documentation:

* Module
* Application Framework
* Clean Architecture Framework
* Business Layer
* UseCase Layer
* Repository Layer
