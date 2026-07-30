> Applies to Sagittarius Engine v1.x

# Documentation Style Guide

This guide defines the standards every contributor must follow.
Documentation in this project is treated as source code — it is reviewed, tested, and must pass automated checks.

---

## Documentation as Code

Documentation must:

- Be kept in version control alongside the source code.
- Pass `mkdocs build` before merging.
- Have all code examples verified by `pytest tests/test_docs.py`.
- Have no broken internal links.

Any pull request that breaks documentation quality checks will not be merged.

---

## Terminology

| Correct Term | Incorrect Term | Notes |
|---|---|---|
| **Extension** | ~~Module~~ | Always use "Extension". Never "Module". |
| **boot()** | — | Internal lifecycle step. Do not teach in Getting Started. |
| **dispatch()** | ~~execute()~~ / ~~query()~~ | The deprecated APIs must not appear in new documentation. |
| **EngineContext** | ~~container~~ / ~~context~~ | Use the full class name in documentation. |
| **Hosted Service** | ~~background service~~ | Use the engine's own naming. |

---

## Mermaid Diagram Standards

Use the correct diagram type for each situation:

| Situation | Diagram Type | Example |
|---|---|---|
| Architecture overview | `flowchart TB` | Layer relationships |
| Execution sequences | `sequenceDiagram` | Boot / shutdown order |
| Class hierarchies | `classDiagram` | Interfaces and implementations |
| Decision flows | `flowchart LR` | If/then routing |
| State machines | `stateDiagram-v2` | Only when documenting actual state |

**Rules:**
- Never use `graph TD` without a defined purpose.
- Never place more than one top-level diagram per section.
- Every diagram must have a caption (title or surrounding explanation).

---

## Images Policy

- **Never use screenshots.**
- **Always use Mermaid** for architecture, lifecycle, and flow diagrams.
- Use SVG files only when an external tool (e.g., draw.io) produces a meaningfully better result than Mermaid. SVG must be committed to the repository — no remote image URLs.

---

## Code Example Rules

Every code example in documentation must satisfy all of the following:

| Requirement | Description |
|---|---|
| **Runnable** | Must execute without errors using `python example.py` |
| **≤ 50 lines** | Each snippet is single-purpose and focused |
| **Single purpose** | One concept per example |
| **Public API only** | Only `from sagittarius_engine import ...` |
| **No omitted code** | No `# ...` or `pass` placeholders hiding required logic |
| **No deprecated APIs** | Do not use `execute()` or `query()` |
| **Clean termination** | No dangling threads, no open async loops after exit |
| **No warnings** | Must run without `DeprecationWarning` or `RuntimeWarning` |

**Correct import:**
```python
from sagittarius_engine import App, IExtension
```

**Incorrect imports:**
```python
# ❌ Never import internal packages
from sagittarius_engine.kernel.app import App
from sagittarius_engine.kernel.bootstrap import Bootstrap
```

---

## Document Structure

Every document should answer, in order:

1. **What** — What is this component?
2. **Why** — Why does it exist?
3. **When** — When should I use it?
4. **When NOT** — When should I not use it?
5. **How** — How do I use it?
6. **Example** — Runnable code example
7. **Diagram** — Mermaid diagram (if useful)
8. **Best Practices** — Dos and don'ts
9. **Common Mistakes** — Frequent errors and their fixes

---

## Page Header

Every page must start with:

```markdown
> Applies to Sagittarius Engine v1.x
```

---

## Page Footer

Every page must end with:

```markdown
> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/STYLE_GUIDE.md)
```

---

## Admonitions

Use MkDocs Material admonitions for callouts:

```markdown
!!! note
    Use for supplemental context.

!!! warning
    Use for common pitfalls or incorrect patterns.

!!! tip
    Use for performance hints or best practices.
```

Do not use consecutive admonitions. Separate them with prose.

---

> [Found an issue? Edit this page on GitHub.](https://github.com/anhembedded/Sagittarius-Engine/edit/main/docs/STYLE_GUIDE.md)
