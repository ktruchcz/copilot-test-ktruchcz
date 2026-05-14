---
name: adf-to-angular-components-code-generator
description: Generate Angular components from legacy UI framework views, including API-backed components, components with route-input-only use, and static HTML mockups. Use this when converting old UI markup (from any legacy framework) into modern Angular with or without service integration.
---

# Legacy UI to Angular Components Code Generator

This skill covers three closely related output modes. Pick the one that matches your use case instead of mixing them.

## Modes

- API-backed Angular component (fetches and displays data from backend services)
- Route-input-only Angular component (receives all data via `@Input()` or route state, no service calls)
- Static HTML mockup (pure HTML for layout prototyping, no Angular bindings)

## Required inputs

- Source UI markup, component layout description, or wireframe
- Data model names and service contracts (for API-backed mode)
- Target file names if specific component names are expected
- CSS framework preference (Bootstrap, Tailwind, Material, etc.) for the target

## Workflow

1. Read [references/api-component.md](references/api-component.md) when the component needs to call backend services.
2. Read [references/no-api-component.md](references/no-api-component.md) when all data arrives through routing or `@Input()` props.
3. Read [references/static-mockup.md](references/static-mockup.md) when you only need a static HTML layout mockup.
4. If reviewing or fixing existing component code, also read [references/review.md](references/review.md).
5. Keep the chosen mode focused. Do not mix static mockups with service calls or add API logic to input-only components unless explicitly requested.

## Output contract

- For Angular modes, generate `{component}.component.ts` and `{component}.component.html` only (unless asked for more).
- For static mockups, output pure HTML5 with the requested CSS framework and no JavaScript bindings.
- Preserve data model names and component naming conventions from the target project.
- Keep styling and template structure minimal and focused.

## Reference files

- [references/api-component.md](references/api-component.md): Angular component generation with backend service calls.
- [references/no-api-component.md](references/no-api-component.md): Angular component generation without services.
- [references/static-mockup.md](references/static-mockup.md): static HTML mockup generation.
- [references/review.md](references/review.md): validation checklist for generated component output.
