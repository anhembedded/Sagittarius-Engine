> Applies to Sagittarius Engine v1.x

# Documentation Review Checklist

Use this checklist before marking any documentation phase as complete.

---

## Content Quality

- [ ] Every page answers: What / Why / When / When NOT / How
- [ ] No internal implementation details exposed
- [ ] No private class names referenced
- [ ] No kernel internals mentioned
- [ ] Terminology follows `STYLE_GUIDE.md`
- [ ] No use of the word "Module" (always "Extension")
- [ ] No deprecated APIs (`execute()`, `query()`) documented as current
- [ ] Each page has a "Applies to Sagittarius Engine v1.x" header
- [ ] Each page has a "Found an issue? Edit this page on GitHub." footer

---

## Code Examples

- [ ] All code examples use only `from sagittarius_engine import ...`
- [ ] All code examples are ≤ 50 lines
- [ ] All code examples are single-purpose
- [ ] No omitted code (`# ...` or hidden logic)
- [ ] All examples compile without errors
- [ ] All examples run without warnings
- [ ] All examples terminate cleanly (no dangling threads or async loops)

---

## Diagrams

- [ ] Architecture diagrams use `flowchart TB`
- [ ] Lifecycle diagrams use `sequenceDiagram`
- [ ] Abstraction diagrams use `classDiagram`
- [ ] No screenshots in any documentation page
- [ ] All Mermaid diagrams render correctly

---

## Automation

- [ ] `mkdocs build` passes with zero errors
- [ ] `pytest tests/test_docs.py` passes with zero failures
- [ ] No broken internal links
- [ ] Markdown linting passes

---

> [Found an issue? Edit this page on GitHub.](https://github.com/your-repo/edit/main/docs/DOC_REVIEW_CHECKLIST.md)
