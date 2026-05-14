# Review Checklist


- Verify the chosen mode matches the request: API-backed, no-API, or static mockup.
- Verify only the expected files were produced.
- Verify `@Input()` uses DTO models and route parameter handling is correct when required.
- Verify TypeScript strict mode is satisfied with safe defaults and proper typing.
- Verify static mockups contain no Angular bindings or framework-specific syntax.
- Verify dummy or placeholder data was not left in place for API-backed components.
- Verify imported services, models, and utilities match the target project's package structure.
- Verify all component lifecycle hooks are properly implemented without memory leaks.
