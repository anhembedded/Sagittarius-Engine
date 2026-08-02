# Skill: Generate Architecture Diagrams

Never generate every diagram.
Choose the one that explains the topic best.

## Principles

Diagrams should explain concepts.

NOT implementation.

Avoid:

- private classes
- internal methods
- helper functions
- hidden infrastructure

## Complexity Rules

- Maximum: 10 nodes
- Maximum: 15 arrows
- If larger: Split into multiple diagrams

## Mermaid Style Rules

Always produce valid Mermaid.

## Output Format

Return:

1. Short explanation
2. Mermaid diagram
3. Key takeaways

- Never explain implementation details.
- Focus on understanding the architecture.
