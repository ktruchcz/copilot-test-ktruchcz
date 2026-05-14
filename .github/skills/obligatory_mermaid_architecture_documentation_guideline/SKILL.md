---
name: obligatory_mermaid_architecture_documentation_guideline
description: Enforce mandatory Mermaid architecture documentation updates for architecture-relevant code changes. Use this whenever creating or updating architecture docs.
---

# Obligatory Mermaid Architecture Documentation Guideline

When creating or updating architecture documentation, include Mermaid diagrams.

## Minimum required diagrams

- High-level system context diagram
- Component/module interaction diagram
- Runtime flow diagram for key user or service paths

## Rules

- Keep diagram node names aligned with real package/module/service names.
- Update diagrams whenever architecture-relevant code changes.

## Recommended Mermaid types

- `flowchart` for process and request flows
- `sequenceDiagram` for interaction timelines
- `classDiagram` for domain model structure
- `graph TD` / `graph LR` for dependency overviews
