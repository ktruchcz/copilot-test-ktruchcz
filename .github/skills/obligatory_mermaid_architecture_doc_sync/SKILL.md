---
name: obligatory_mermaid_architecture_doc_sync
description: Keep architecture documentation synchronised with code using Mermaid diagrams. Always apply when architecture-relevant code changes, new classes/modules are added, runtime flows change, or any section of arc42-documentation.md is modified. Diagrams must reflect the real current class structure and flows.
---

# Obligatory Mermaid Architecture Documentation Sync

## When to apply
Apply this skill whenever:
- New classes, records, interfaces, or modules are added
- Existing class hierarchies or call flows are modified
- Build tooling, CI, or deployment topology changes
- `arc42-documentation.md` or any other architecture document is created or updated

## Required diagram set

Every architecture document must contain **at minimum** these diagram types:

| Diagram Type | Purpose | Mermaid Syntax |
|-------------|---------|----------------|
| System context | High-level system boundary and external actors | `graph LR` |
| Component / module interaction | Which classes call which | `graph TB` or `classDiagram` |
| Runtime sequence | Key execution flows step-by-step | `sequenceDiagram` |
| Deployment topology | Build + runtime infrastructure | `flowchart LR` |

## Alignment rules

1. **Node names must match real code names** — class `HelloWorld`, record `Greeting`, sealed interface `TimeOfDay`, inner records `Morning`, `Afternoon`, `Evening`
2. **Update diagrams whenever the code changes** — adding a new record or method requires a corresponding diagram update
3. **Reflect the actual build toolchain** — diagrams must show Maven (`pom.xml`) and GitHub Actions CI, not manual `javac`
4. **Class diagram must include all public/package-visible types**:
   - `HelloWorld` (entry point class)
   - `Greeting` (record — fields: `recipient: String`, `message: String`)
   - `TimeOfDay` (sealed interface — permits `Morning`, `Afternoon`, `Evening`)
   - `TimeOfDay.Morning`, `TimeOfDay.Afternoon`, `TimeOfDay.Evening` (records implementing `TimeOfDay`)

## Current project — required `classDiagram` (minimum)

```mermaid
classDiagram
    direction TB

    class HelloWorld {
        <<entry point>>
        +main(args: String[])$ void
        +seasonOf(month: Month)$ String
    }

    class Greeting {
        <<record>>
        +recipient: String
        +message: String
        +formatted() String
    }

    class TimeOfDay {
        <<sealed interface>>
        +of(hour: int)$ TimeOfDay
    }

    class Morning {
        <<record>>
    }

    class Afternoon {
        <<record>>
    }

    class Evening {
        <<record>>
    }

    HelloWorld +-- Greeting : inner type
    HelloWorld +-- TimeOfDay : inner type
    TimeOfDay <|.. Morning : implements
    TimeOfDay <|.. Afternoon : implements
    TimeOfDay <|.. Evening : implements
```

## Recommended Mermaid diagram types
- `flowchart` — process and request flows
- `sequenceDiagram` — service/method interactions over time
- `classDiagram` — domain model and class structure
- `graph TD` / `graph LR` — component dependency overviews
- `stateDiagram-v2` — application lifecycle states
- `mindmap` — quality goal trees
- `quadrantChart` — risk matrices
- `gantt` — roadmaps and timelines

## Outdated content to remove or update in `arc42-documentation.md`
When the architecture documentation still describes the **old simple HelloWorld** (5 lines, single class, no build tool, no tests), update:
- Section 2 (Architecture Constraints) — remove "no build tool", "no external deps", "JDK ≥ 1.0"; add Maven, JUnit 5, Java 25
- Section 4 (Solution Strategy) — update decomposition description to reflect records, sealed interfaces
- Section 5 (Building Block View) — update class diagram to include `Greeting`, `TimeOfDay` hierarchy
- Section 6 (Runtime View) — update sequence diagrams to reflect actual `main()` logic
- Section 9 (Architecture Decisions) — supersede ADR-002 and ADR-004 with updated decisions
- Section 10 (Quality Requirements / Code Metrics) — update LOC, class count, method count
- Section 11 (Risks & Technical Debt) — remove resolved risks and closed debt items
