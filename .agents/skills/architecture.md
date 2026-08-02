# Skill: Architecture Design

> Context: You are a Principal Architect designing or evaluating a system's structure.
> Architecture decisions are high-leverage, high-cost-to-reverse. Treat them with proportional caution.

## 1. AI Blind Spots to Actively Address

* **Drawing Diagrams ≠ Architecture:** AI agents often produce diagrams that look architectural but don't answer the hard questions: How does the system fail? How does it scale? How does it evolve? Architecture must answer operational reality, not just happy-path structure.
* **Missing Failure Mode Analysis:** Every design decision must explicitly document how it behaves under failure: network partition, service crash, database unavailability, memory exhaustion. AI agents skip this entirely.
* **Ignoring Operational Complexity:** A system that is theoretically elegant but operationally unmanageable is a bad architecture. Consider: How is it deployed? How is it monitored? How is it debugged in production? How is it upgraded with zero downtime?
* **Premature Abstraction:** AI agents add layers and abstractions speculatively. Every layer must have a concrete, current justification — not a future hypothetical.
* **Data Flow is the Real Architecture:** Logic can always be refactored. Data structure and data flow are much harder to change. Define: where data lives, how it moves, how it transforms, and who owns it.
* **Boundary Erosion Over Time:** Architectures degrade because boundaries are violated incrementally. Define explicit forbidden dependencies (what Layer A must NEVER import from Layer B) as enforced rules, not informal agreements.

## 2. Tracking (Complex Tasks Only)

**Assess complexity first.** Only create a tracking file if the task meets the complexity threshold.
Refer to `../rules/task-tracking.md` for the full complexity gate criteria.

Typical triggers for this skill: multi-session design, cross-cutting boundary changes, user approval required for ADRs, 3+ subsystems affected.

If tracking is needed:
```
.ai/tracking/architecture_<YYYYMMDD_HHMM>.md
```
Update phase status at the START and END of each phase.

## 3. Design Workflow

* **Phase 1 — Understand Forces:** Identify functional requirements, NFRs (scale, latency, availability), team size, deployment constraints, and existing constraints. → *Update tracking: 🔄 → ✅*
* **Phase 2 — Define Boundaries:** Name components, define responsibilities, draw dependency graph. Enforce unidirectional dependencies. → *Update tracking*
* **Phase 3 — Define Contracts:** Define public interfaces between components: communication style (call/event/HTTP/queue) and data crossing each boundary. → *Update tracking*
* **Phase 4 — Failure Mode Analysis:** For each component and integration point: failure behavior, graceful degradation strategy, recovery path. → *Update tracking*
* **Phase 5 — Diagram:** Produce Mermaid diagrams — system overview (`flowchart TB`), data flow (`sequenceDiagram`), relationships (`classDiagram`). → *Update tracking*
* **Phase 6 — Document Decisions (ADR):** Write one ADR per significant decision: Context → Decision → Consequences. → *Update tracking: mark task DONE*

## 4. Architectural Quality Checklist

Before finalizing a design:

* [ ] Each component has exactly ONE clear responsibility
* [ ] Dependencies flow in one direction only (no cycles)
* [ ] No component leaks infrastructure details to layers above it
* [ ] Each integration point has a defined failure mode and degradation behavior
* [ ] Deployment strategy is defined and feasible
* [ ] Observability is built in (not bolted on)
* [ ] The design can evolve without a full rewrite (extension points are explicit)
* [ ] Data ownership is unambiguous — no two components own the same data

## 5. Layer Violation Rules (Strictly Forbidden)

* Presentation layer must NEVER access the database directly.
* Domain / Business layer must NEVER import infrastructure packages.
* Infrastructure layer must NEVER contain business logic.
* Shared utilities must NEVER depend on any application layer.

## 6. Architecture Decision Record (ADR) Template

```markdown
## ADR-[N]: [Decision Title]

**Status:** Proposed | Accepted | Superseded

**Context:** Why does this decision need to be made?

**Decision:** What was decided?

**Consequences:**
- Positive: ...
- Negative / Trade-offs: ...
- Risks: ...
```

## 7. Deliverables

* **Component Map:** Named components with responsibilities and boundaries.
* **Dependency Graph:** Directional, cycle-free.
* **Contract Definitions:** Interfaces between components.
* **Failure Mode Analysis:** Per integration point.
* **Mermaid Diagrams:** System overview + sequence diagram for primary flows.
* **ADRs:** One per significant decision.

## 8. Golden Rule

If a design cannot be explained to a new team member in 15 minutes using only diagrams and ADRs, it is too complex. Simplify before finalizing.

Refer:
  - [Architecture Rules](../rules/architecture.md)
  - [Documentation Rules](../rules/documentation.md)
  - [Architecture Context](../context/architecture.md)
  - [Modules Context](../context/modules.md)
