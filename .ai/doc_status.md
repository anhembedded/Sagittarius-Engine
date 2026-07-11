==================================================
Documentation Status
==================================================

Phase D1 — Documentation Foundation
Status: COMPLETED

Deliverables:

docs/
  index.md                          ✅ Done
  STYLE_GUIDE.md                    ✅ Done
  DOC_REVIEW_CHECKLIST.md           ✅ Done
  getting-started/
    installation.md                 ✅ Done
    first_app.md                    ✅ Done
    first_extension.md              ✅ Done
    project_templates.md            ✅ Done
  concepts/
    README.md                       ✅ Done (Placeholder)
  tutorials/
    README.md                       ✅ Done (Placeholder)
  advanced/
    extension_dependencies.md       ✅ Done

--------------------------------------------------

Phase D1.5 — Documentation Infrastructure
Status: COMPLETED
Deliverables: mkdocs.yml

Phase D1.6 — Documentation Quality
Status: COMPLETED
Deliverables: tests/test_docs.py, .github/workflows/docs.yml

Phase D1.7 — API Reference
Status: COMPLETED
Deliverables: mkdocstrings integration, docs/api/index.md, app.md, engine_context.md, dispatcher.md, event_bus.md, scheduler.md, task_manager.md, hosted_service.md, extension.md, cancellation_token.md

Phase D2 — Core Concepts
Status: COMPLETED
Deliverables: docs/concepts/engine.md, docs/concepts/runtime.md, docs/concepts/dispatcher.md, docs/concepts/dependency_injection.md, docs/concepts/event_bus.md, docs/concepts/middleware.md, docs/concepts/extensions.md, docs/concepts/lifecycle.md

Phase D3 — Runtime Guides
Status: COMPLETED
Deliverables: docs/runtime/application_lifecycle.md, docs/runtime/hosted_services.md, docs/runtime/scheduler.md, docs/runtime/task_manager.md, docs/runtime/async_runtime.md, docs/runtime/cancellation_token.md

Phase D4 — Advanced Guides
Status: NOT STARTED

Phase D5 — Tutorials
Status: NOT STARTED

Phase D6 — Documentation Review
Status: NOT STARTED

Phase D7 — Migration Guides
Status: NOT STARTED

Phase D8 — Documentation Polish & Release
Status: NOT STARTED

==================================================
Documentation Rules
==================================================

Every page MUST:

- Start with: > Applies to Sagittarius Engine v1.x
- End with: > [Found an issue? Edit this page on GitHub.](link)

Code examples MUST:

- Use only: from sagittarius_engine import ...
- Be <= 50 lines
- Be runnable and terminate cleanly
- Use no deprecated APIs (execute(), query())

Diagrams MUST:

- Architecture: flowchart TB
- Lifecycle/Sequence: sequenceDiagram
- Abstractions: classDiagram
- Decision: flowchart LR
- No screenshots. Mermaid only.

Terminology:

- Always: "Extension"
- Never: "Module"
- Always: "dispatch()"
- Never: "execute()" or "query()" in new docs

==================================================
