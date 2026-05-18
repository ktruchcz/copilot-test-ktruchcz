---
name: adf-to-angular-component-improver
description: Improve an existing Angular component by implementing missing business logic, state handling, and conditional rendering or input-enablement rules without changing unrelated files. Use this when the user has an existing Angular component that was generated from a migration but is incomplete, especially if they mention missing logic, disabled fields, incomplete event handlers, or other unfinished behavior.
---

# UI Framework to Angular Component Improver

Enhance existing component code by adding missing business logic instead of regenerating the whole feature.

## Required inputs

- Existing Angular component files (`{component}.component.ts`, template, styles)
- Original source view, business rules, or requirements documentation
- Service and data model contracts already available in the target application
- Descriptions of missing functionality or incomplete behavior

## Workflow

1. Read [references/implementation.md](references/implementation.md).
2. Preserve the existing component structure, naming conventions, and file organization.
3. Study the original business requirements to identify missing or incomplete logic.
4. Implement missing field state handling, conditional rendering, input enablement/disablement.
5. Keep changes scoped to the component; avoid redesigning module wiring or routing.

## Output contract

- Improve and complete existing component logic only.
- Do not rename files, move logic to other components, or introduce unrelated modules.
- Maintain type safety and alignment with the project's existing services and data models.
- Preserve the component's current styling and template structure unless specifically asked to change them.

## Reference files

- [references/implementation.md](references/implementation.md): component-improvement rules and patterns.
