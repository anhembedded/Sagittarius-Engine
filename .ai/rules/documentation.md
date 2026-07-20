# Rules: Documentation

> Context: Universal constraints for structuring, writing, and updating project documentation.

## 1. Structure & Formatting

* **Strict Markdown:** Use standard, clean Markdown syntax.
* **Clear Hierarchy:** Use `#`, `##`, `###` logically to create a scannable outline. Never skip heading levels.
* **Code Blocks:** ALWAYS specify the language for syntax highlighting (e.g., ````typescript`).

## 2. Writing Style

* **Active & Direct:** Use active voice. Be concise and instructional (e.g., "Run the server," not "The server should be run").
* **Value-Driven:** Focus on "Why" and "How-to". Avoid dumping internal implementation details into public-facing guides.
* **Consistent Terminology:** Strictly use official project terms. Do not use synonyms for core concepts.

## 3. Diagrams & Visuals

* **Mermaid Only:** Use Mermaid.js for all diagrams (architecture, sequence, relationships, decision flow). Do not use external image files.
* **NO Screenshots:** Never use screenshots for UI or code (they become outdated quickly and cannot be searched).

## 4. Maintenance & Updates

* **Atomic Updates:** Documentation must be updated alongside the code changes in the same context/commit.
* **NO Zombie Docs:** If a feature is deprecated or removed, delete or update its documentation immediately. Never leave stale or misleading information.

## 5. Project-Specific Rules

* *[TBD - Project-specific documentation constraints and structures will be added here]*
