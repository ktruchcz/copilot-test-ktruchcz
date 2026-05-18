---
name: obligatory_mermaid_architecture_documentation
description: >
  Ensures that all architecture documentation in this repository includes Mermaid diagrams
  to visualise structure and flow. Use this skill when creating or updating any architecture
  document (arc42, ADR, README architecture section, design docs), when architecture-relevant
  code changes are made, or when a new component/service/module is introduced. Apply proactively
  whenever the word "architecture", "diagram", "system design", or "component" appears in a task.
---

# Skill: obligatory_mermaid_architecture_documentation

## Purpose

Every architecture document must contain Mermaid diagrams kept in sync with the actual codebase.
Stale diagrams are treated as documentation defects.

## Minimum Required Diagrams (mandatory for every architecture doc)

| # | Type | What it must show |
|---|------|-------------------|
| 1 | **System Context** | High-level boundary + external actors/systems |
| 2 | **Component / Module Interaction** | Internal building blocks and their dependencies |
| 3 | **Runtime Flow** | Step-by-step execution path for the primary interaction |

## Recommended Mermaid Types

| Mermaid type | When to use |
|---|---|
| `flowchart` / `graph TD` / `graph LR` | Process flows, dependency overviews |
| `sequenceDiagram` | Service-to-service, function-call interactions over time |
| `classDiagram` | Domain model, class hierarchies, record/data relationships |

## Diagram Quality Rules

1. Node names must match real package/class/service names in code.
2. Update diagrams on every architecture-relevant code change.
3. Use `classDef` styling to distinguish system, external, and I/O elements.
4. Add a short heading above each Mermaid block.

## Checklist

- [ ] All three mandatory diagram categories present.
- [ ] All diagram node labels match real class/module/service names.
- [ ] `classDef` styling applied.
- [ ] Diagrams updated whenever architecture-relevant code changes.
- [ ] `classDiagram` present for non-trivial domain models.
- [ ] `sequenceDiagram` present for key runtime flows.
- [ ] No stale/out-of-date diagrams merged.

## Source

Cookbook: `cookbooks/mermaid-architecture-documentation-guideline.md`
