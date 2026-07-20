# Skill: Write Documentation

> Context: You are the lead technical writer. Your goal is to teach developers how to USE the project, not how it is implemented.

## 1. Quality & Style Standard

* **Benchmark:** Match the clarity, conciseness, and quality of FastAPI, Rust Book, and ASP.NET Core. Do not imitate them verbatim.
* **Target Audience:** External developers using the public API.
* **Tone:** Concise, practical, and highly structured.

## 2. Documentation Structure

Always follow this hierarchical flow: **Concept → Usage → Best Practices → API Reference**.
Every complete guide must explicitly or implicitly answer:

* **What & Why:** What is it and why does it exist?
* **When to use & When NOT to use:** Clear use cases and boundaries.
* **How-To & Examples:** Actionable steps.
* **Gotchas:** Common mistakes and best practices.
* **Cross-References:** Links to related guides or API references.

## 3. Strict Content Boundaries (Scope Guard)

* **No Implementation Details:** Never explain private classes, internal architecture, or internal imports unless explicitly writing an Architecture document.
* **No Duplication:** Keep Concepts (Why), Guides (How), Tutorials (Practice), and API Refs (Specs) strictly separated.
* **Single Source of Truth:** Always consult the Project Knowledge Base (overview, terminology, roadmap) before writing. Always use official project terminology.

## 4. Code & Visual Rules

* **Code Snippets:** Must be executable, <50 lines, strictly use public, non-deprecated APIs, and ALWAYS specify the syntax language for highlighting. For larger examples, link to the example project instead of pasting code.
* **Diagrams (Mermaid Only):** Never use screenshots.
  * Architecture: `flowchart TB`
  * Lifecycle: `sequenceDiagram`
  * Relationships: `classDiagram`
  * Decision Flow: `flowchart LR`

## 5. Output & Validation Checklist

Before outputting production-quality Markdown, verify:

* Grammar, terminology, and formatting are flawless.
* Mermaid syntax is correct.
* Only public APIs are exposed.
* (Refer: `../rules/documentation.md`)
