---
name: obligatory_mermaid_architecture_documentation
description: Require Mermaid architecture diagrams in documentation updates, including context, component, and runtime flow views.
---

# Obligatory Skill: Mermaid Architecture Documentation

When creating or updating architecture documentation, include Mermaid diagrams that describe structure and flow.

## Minimum Expectations

- Add a high-level system context diagram.
- Add a component/module interaction diagram.
- Add a runtime flow diagram for key user or service paths.
- Keep Mermaid node names aligned with real package/module/service names in the codebase.
- Update diagrams whenever architecture-relevant code changes.

## Recommended Mermaid Types

- `flowchart` for process and request flows
- `sequenceDiagram` for time-ordered service interactions
- `classDiagram` for domain model structures
- `graph TD` / `graph LR` for component dependency overviews
