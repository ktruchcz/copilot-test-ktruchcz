---
name: obligatory_mermaid_architecture_documentation_guideline
description: Enforce Mermaid diagrams in architecture documentation updates.
---

# Skill: Mermaid Architecture Documentation Guideline

When creating or updating architecture documentation, include Mermaid diagrams.

Minimum required diagrams:
- High-level system context diagram.
- Component or module interaction diagram.
- Runtime flow diagram for a key user or service path.

Additional rules:
- Keep diagram nodes aligned with real package/module/service names in code.
- Update Mermaid diagrams whenever architecture-relevant code changes.

Recommended Mermaid diagram types:
- `flowchart`
- `sequenceDiagram`
- `classDiagram`
- `graph TD` or `graph LR`
