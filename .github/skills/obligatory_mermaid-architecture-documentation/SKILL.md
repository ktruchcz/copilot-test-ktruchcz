---
name: obligatory_mermaid-architecture-documentation
description: Enforces the use of Mermaid diagrams in architecture documentation. Apply whenever creating or updating application architecture documentation, README files, or any architecture-relevant documentation.
---

# Obligatory Mermaid Architecture Documentation

## Rule

When creating or updating application architecture documentation, include Mermaid diagrams to visualize structure and flow.

## Minimum Requirements

- Add a **high-level system context diagram**.
- Add a **component or module interaction diagram**.
- Add a **runtime flow diagram** for key user or service paths.
- Keep diagram nodes aligned with real package/module/service names in code.
- Update Mermaid diagrams whenever architecture-relevant code changes.

## Recommended Diagram Types

- `flowchart` — for process and request flows.
- `sequenceDiagram` — for service interactions over time.
- `classDiagram` — for domain model structure.
- `graph TD` or `graph LR` — for component dependency overviews.

## Example

```mermaid
flowchart TD
    A[User] --> B[HelloWorld Application]
    B --> C[Greeting Record]
    B --> D[TimeOfDay Sealed Interface]
    B --> E[seasonOf Method]
```
